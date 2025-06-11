from moviepy import VideoFileClip
import pandas as pd
import os
import csv

# Mappage des comportements possibles dans la colonne 'Autres'
excel_behavior_mapping = {
    "Carryingpups": ["Carrying pups"],
    "Selfgrooming": ["Self grooming"],
    "Eat_drink": ["Eat/drink"],
    "Kicking": ["Kicking"],  
    "Groomingpups": ["Grooming pups"],
    "Build": ["Build"]
}

def nettoyer_csv(filepath):
    lignes_nettoyees = []
    entete_trouvee = False

    with open(filepath, 'r', encoding='utf-8') as f:
        lecteur = csv.reader(f, delimiter=";")
        for ligne in lecteur:
            if not ligne or all(cellule.strip() == "" for cellule in ligne):
                if entete_trouvee:
                    break
                continue

            if not entete_trouvee:
                if ligne[0].strip().lower() == 'time':
                    lignes_nettoyees.append(ligne)
                    entete_trouvee = True
                continue

            try:
                float(ligne[0].replace(',', '.'))
                lignes_nettoyees.append(ligne)
            except ValueError:
                continue

    return lignes_nettoyees

def traiter_fichier_csv_unique(filepath, chemin_video, dossier_sortie_csv, csv_frames_global, shift_fraction):
    nom_video = os.path.basename(chemin_video)

    # Lire le nombre de frames
    frames_totales = None
    with open(csv_frames_global, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if nom_video.strip() == row["video"].strip():
                frames_totales = int(row["frames"]) + 1
                break

    if frames_totales is None:
        print(f"❌ Nombre de frames non trouvé pour {nom_video}")
        return

    donnees_nettoyees = nettoyer_csv(filepath)
    df = pd.DataFrame(donnees_nettoyees[1:], columns=donnees_nettoyees[0])

    if 'Time' not in df.columns:
        print(f"⚠️ Colonne 'Time' non trouvée dans {filepath}")
        return None

    df['Time'] = df['Time'].str.replace(',', '.', regex=False)
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
    df = df.dropna(subset=['Time']).sort_values(by='Time').reset_index(drop=True)

    lignes_count = len(df)
    if lignes_count == 0:
        print("❌ Aucune ligne exploitable dans le fichier.")
        return

    base_repeats = frames_totales // lignes_count
    reste = frames_totales % lignes_count

    colonnes_comportements = [
        col for col in df.columns
        if col not in ['Time'] and not col.startswith('Test') and not col.startswith("Unnamed") and col.strip() != ""
    ]

    # Expansion des comportements dans les colonnes
    lignes_expandees = []
    for idx, (_, ligne) in enumerate(df.iterrows()):
        rep = base_repeats + (1 if idx < reste else 0)
        for _ in range(rep):
            nouvelle_ligne = {col: 1 if str(ligne[col]).strip() != "" else 0 for col in colonnes_comportements}
            
            # Gérer la colonne 'Autres' et ajouter les comportements associés
            if 'Autres' in ligne:
                # Convertir la valeur dans 'Autres' en 1 dans la colonne correspondante et 0 pour les autres
                for comportement, valeurs in excel_behavior_mapping.items():
                    if any(valeur.strip() in str(ligne['Autres']) for valeur in valeurs):
                        nouvelle_ligne[comportement] = 1
                    else:
                        nouvelle_ligne[comportement] = 0
            lignes_expandees.append(nouvelle_ligne)

    resultat = pd.DataFrame(lignes_expandees)
    resultat['background'] = (resultat[colonnes_comportements].sum(axis=1) == 0).astype(int)
    colonnes_finales = ['background'] + colonnes_comportements + list(excel_behavior_mapping.keys())
    resultat = resultat[colonnes_finales]

    os.makedirs(dossier_sortie_csv, exist_ok=True)
    nom_fichier = os.path.basename(filepath)
    chemin_sortie = os.path.join(dossier_sortie_csv, nom_fichier)

    print(f"✔ CSV homogène produit ({len(resultat)} frames) → {chemin_sortie}")

    def normaliser_decalage(df_etiquetas):
        total = len(df_etiquetas)
        max_shift = int(total * shift_fraction)
        if max_shift < 1:
            return df_etiquetas
        new_order = list(range(max_shift, total)) + list(range(max_shift))
        return df_etiquetas.iloc[new_order].reset_index(drop=True)

    if shift_fraction != 0:
        resultat = normaliser_decalage(resultat)
    
    resultat = resultat.drop(columns=['Transitions', 'Autres', 'Non visible'], errors='ignore')
    resultat.to_csv(chemin_sortie, index=False)

def trouver_video_recursive(base_nom, dossier_parent):
    for racine, _, fichiers in os.walk(dossier_parent):
        for fichier in fichiers:
            if fichier.startswith(base_nom):
                return os.path.join(racine, fichier)
    return None

def traiter_lot(dossier_csvs, dossier_videos, csv_frames_global, dossier_sortie, shift_fraction=0.0005):
    print("📦 Traitement en lot...")

    df_frames = pd.read_csv(csv_frames_global)
    video_to_frames = {
        row["video"]: int(row["frames"])
        for _, row in df_frames.iterrows()
    }

    fichiers_csv = []
    for racine, _, fichiers in os.walk(dossier_csvs):
        for f in fichiers:
            if f.endswith(".csv"):
                fichiers_csv.append(os.path.join(racine, f))

    for nom_csv in fichiers_csv:
        chemin_csv = nom_csv 
        base_nom = os.path.splitext(os.path.basename(nom_csv))[0]

        # 🔍 Recherche récursive de la vidéo correspondante
        chemin_video = trouver_video_recursive(base_nom, dossier_videos)

        if not chemin_video:
            print(f"❌ Vidéo non trouvée pour {nom_csv}")
            continue

        nom_video = os.path.basename(chemin_video)
        if nom_video not in video_to_frames:
            print(f"❌ Nombre de frames non trouvé pour {nom_video}")
            continue

        try:
            traiter_fichier_csv_unique(
                filepath=chemin_csv,
                chemin_video=chemin_video,
                dossier_sortie_csv=dossier_sortie,
                csv_frames_global=csv_frames_global,
                shift_fraction=shift_fraction
            )
        except Exception as e:
            print(f"⚠️ Erreur sur {nom_csv} → {e}")

    print("✅ Traitement terminé.")

traiter_lot(
    dossier_csvs="1. VEAVE_LBN-CONT",
    dossier_videos=r"Maternal_auto_classification_deepethogram\DATA",
    csv_frames_global=r"training_data_conversion\frames_per_video.csv",
    dossier_sortie="./csv_deg_TN-5/",
    shift_fraction=0
)
