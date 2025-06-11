from datetime import datetime
import pandas as pd
import json
import numpy as np



class LbnSessions:
    behavioural_annotation = r"behavioural_annotation.csv"
    behavioursTot = ["Onnest","Offnest","ABN","Carryingpups","Selfgrooming","Eat_drink","Kicking","Groomingpups","Build","Nest_entry","Nest_exits"]
    def __init__(self, cage=None, pup=None,
                 startDate=datetime(2010, 7, 5),
                 endDate=datetime(2025, 7, 5),
                 projectConfig=r"Maternal_auto_classification_deepethogram\project_config.yaml",
                 data=behavioural_annotation,
                 interestedBehaviours=behavioursTot):
        
        self.cage = [str(c) for c in cage] if isinstance(cage, list) else ([str(cage)] if cage is not None else None)
        self.pup = pup
        self.start = startDate
        self.end = endDate
        self.projectConfigPath = projectConfig
        self.dataPath = data
        self.behaviuors = interestedBehaviours

        df = pd.read_csv(data, dtype={
        "Recording_duration": str,
        "ID blind": str,
        "PupID": str,
        "Sexe": str,
        "Cage" : str,
        },
        low_memory=False
        )

        df["Start_time"] = pd.to_datetime(df["Start_time"])
        
        df["Recording_duration"] = pd.to_numeric(df["Recording_duration"], errors="coerce")

        if self.pup is None and self.cage is None:
            raise ValueError("Au moins un des deux paramètres `cage` ou `pup` doit être fourni.")

        # Filter by cage list if provided
        if self.cage is not None:
            df = df[df["Cage"].isin(self.cage)]

        # Filter by pup if provided
        if self.pup is not None:
            df = df[df["PupID"] == self.pup]
            # Infer cage if not provided
            if not self.cage:
                cages = df["Cage"].unique().tolist()
                if len(cages) == 1:
                    self.cage = cages
                else:
                    raise ValueError(f"df mal définie : le pup {self.pup} a plusieurs cages de provenance: {cages}")
                

        # Filter by time window
        df = df[(df["Start_time"] >= self.start) & (df["Start_time"] <= self.end)]

        # Add time
        df["Start_time"] = pd.to_datetime(df["Start_time"])

        df["Time"] = None  # Inicializar
        for cage_id, group in df.groupby("Cage"):
            start_0 = group["Start_time"].min()
            total_frames = group["frame"].max()

            mask = df["Cage"] == cage_id
            df.loc[mask, "Time"] = (
                (df.loc[mask, "Start_time"] - start_0).dt.total_seconds() +
                df.loc[mask, "frame"] * df.loc[mask, "Recording_duration"] / total_frames
            )

        self.data_cage = df.copy()

        # For pup-specific data
        if self.pup is not None:
            self.data_pup = df.copy()
        else:
            first_pup = df["PupID"].unique()[0]
            self.data_pup = df[df["PupID"] == first_pup].copy()


    def getPups(self):
        return sorted([
            str(p) for p in self.data_cage["PupID"].unique()
            if isinstance(p, str) and p.strip() != ""
        ])


    def getBehaviours(self):
        df = self.data_pup[self.behaviuors + ["Recording_duration"]].copy()
        resumen = {}
        total_duration = self.getTotalDuration()
        total_frames = self.getTotalFrames()

        for behaviour in self.behaviuors:
            serie = df[behaviour].fillna(0).astype(int)
            transiciones = (serie.shift(1, fill_value=0) == 0) & (serie == 1)
            ocurrencias = transiciones.sum()
            frames_activos = (serie == 1).sum()
            resumen[behaviour] = {
                "bouts": int(ocurrencias),
                "frames": int(frames_activos),
                "duration": float(frames_activos * total_duration / total_frames)
            }
        return resumen

    def getTotalFrames(self):
        return len(self.data_cage) / len(self.getPups())

    def getTotalDuration(self):
        return float(self.data_pup.groupby("Start_time")["Recording_duration"].first().sum())

    def getBehavioursPups(self):
        return {
            pup: LbnSessions(
                cage=self.cage,
                pup=pup,
                startDate=self.start,
                endDate=self.end,
                projectConfig=self.projectConfigPath,
                data=self.dataPath,
                interestedBehaviours=self.behaviuors
            ).getBehaviours()
            for pup in self.getPups()
        }

    def getBehavioursByPup(self, pupId):
        return self.getBehavioursPups().get(pupId)

    def exportResults(self, output_path="resultados.json"):
        results = {
            "cages": self.cage,
            "total_duration": self.getTotalDuration(),
            "total_frames": self.getTotalFrames(),
            "first_pup_behaviours": self.getBehaviours(),
            "all_pups_behaviours": self.getBehavioursPups(),
            "videos": self.getVideosList()
        }

        def convert_types(d):
            for key, value in d.items():
                if isinstance(value, dict):
                    d[key] = convert_types(value)
                elif isinstance(value, np.integer):
                    d[key] = int(value)
                elif isinstance(value, np.floating):
                    d[key] = float(value)
                elif isinstance(value, np.ndarray):
                    d[key] = value.tolist()
                elif isinstance(value, list):
                    d[key] = [convert_types(item) if isinstance(item, dict) else item for item in value]
            return d

        results = convert_types(results)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Resultados exportados a '{output_path}'")

        return output_path

    def getVideosList(self):
        return self.data_pup["Start_time"].dt.strftime('%Y-%m-%d %H:%M:%S').unique().tolist()

    def getResumedDf(self, getCsv=False):
        meta_cols = ["Recording_duration","Project","Cohort","Group","Cage ID","ID blind","PupID","Sexe", "Time"]
        rows = []
        pups = self.getPups()
        for pup in pups:
            pup_data = LbnSessions(
                cage=self.cage,
                pup=pup,
                startDate=self.start,
                endDate=self.end,
                projectConfig=self.projectConfigPath,
                data=self.dataPath,
                interestedBehaviours=self.behaviuors
            ).data_pup

            grouped = pup_data.groupby("Start_time")[meta_cols].first().reset_index()
            for _, base_row in grouped.iterrows():
                video_frames = pup_data[pup_data["Start_time"] == base_row["Start_time"]]["frame"].max()
                recording_duration = base_row["Recording_duration"]
                row = base_row.to_dict()
                row["PupID"] = pup
                for behaviour in self.behaviuors:
                    serie = pup_data[pup_data["Start_time"] == base_row["Start_time"]][behaviour].fillna(0).astype(int)
                    transiciones = (serie.shift(1, fill_value=0) == 0) & (serie == 1)
                    ocurrencias = transiciones.sum()
                    frames_activos = (serie == 1).sum()
                    row[f"{behaviour}_bouts"] = int(ocurrencias)
                    row[f"{behaviour}_duration"] = float(frames_activos * recording_duration / video_frames)
                rows.append(row)

        result_df = pd.DataFrame(rows)
        if getCsv:
            if self.cage is None:
                cages_str = "All"
            else:
                cages_str = ",".join(map(str, self.cage))
                pups_str = ",".join(map(str, self.getPups()))
            result_df.to_csv(f"Resume_df.csv", index=False)
            print(f"Resume_df.csv")
        return result_df

    def getSessionDataForCagePups(self):
        return self.data_cage

    def getSessionDataForPup(self):
        return self.data_pup
    


# Exemple d'utilisation avec plusieurs cages
# session = LbnSessions(cage=["A","C"], startDate=datetime(2024,7,5), endDate=datetime(2025,7,6))
# session.getResumedDf(getCsv=True)
