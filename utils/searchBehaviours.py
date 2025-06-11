import os
import pandas as pd

def chercher_fichiers_comportement(dossier, pattern_fin='_output.csv', comportements_recherches=None):
    if comportements_recherches is None:
        comportements_recherches = []

    dossiers_avec_comportement = []

    for racine, _, fichiers in os.walk(dossier):
        for fichier in fichiers:
            if any(f.endswith('labels.csv') for f in fichiers):
                continue
            if fichier.endswith(pattern_fin):
                chemin_complet = os.path.join(racine, fichier)

                try:
                    df = pd.read_csv(chemin_complet)

                    # Vérifie que les colonnes demandées existent
                    colonnes_valides = [c for c in comportements_recherches if c in df.columns]

                    if not colonnes_valides:
                        continue  # Aucun des comportements n'est présent dans ce fichier

                    # Vérifie s'il y a au moins un "1" dans l'une des colonnes
                    if (df[colonnes_valides] == 1).any().any():
                        dossier_parent = os.path.basename(os.path.dirname(chemin_complet))
                        dossiers_avec_comportement.append((dossier_parent, fichier))

                except Exception as e:
                    print(f"Erreur lors du traitement de {chemin_complet} : {e}")

    return dossiers_avec_comportement

# Exemple d'utilisation :
if __name__ == "__main__":
    dossier = "D:\LBN\Maternal_behaviour_results"  
    pattern = "_outputs_labels_predictions.csv"
    comportements = ["Carryingpups", "Groomingpups"]

    resultats = chercher_fichiers_comportement(dossier, pattern, comportements)

    print("\nFichiers contenant les comportements recherchés :")
    for dossier_parent, fichier in resultats:
        print(f"- {dossier_parent} / {fichier}")
