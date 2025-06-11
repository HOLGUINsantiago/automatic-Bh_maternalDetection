import os
from moviepy.editor import VideoFileClip
from concurrent.futures import ThreadPoolExecutor, as_completed

def convertir_video(chemin_avi, chemin_mp4):
    try:
        print(f"🎞️ Convertiendo: {chemin_avi} → {chemin_mp4}")
        clip = VideoFileClip(chemin_avi)
        clip.write_videofile(chemin_mp4, codec="libx264", fps=30)
        clip.close()
        return chemin_mp4
    except Exception as e:
        print(f"❌ Error al convertir {chemin_avi}: {e}")
        return None

def convertir_avi_a_mp4_threaded(dossier_entree, dossier_sortie=None, recursive=True, max_threads=4):
    if dossier_sortie is None:
        dossier_sortie = dossier_entree

    jobs = []

    for racine, _, fichiers in os.walk(dossier_entree):
        for fichier in fichiers:
            if fichier.lower().endswith(".avi"):
                chemin_avi = os.path.join(racine, fichier)
                rel_path = os.path.relpath(racine, dossier_entree)
                dossier_sortie_relatif = os.path.join(dossier_sortie, rel_path)
                os.makedirs(dossier_sortie_relatif, exist_ok=True)
                nom_sans_ext = os.path.splitext(fichier)[0]
                chemin_mp4 = os.path.abspath(os.path.join(dossier_sortie_relatif, f"{nom_sans_ext}.mp4"))
                jobs.append((chemin_avi, chemin_mp4))

        if not recursive:
            break

    print(f"🚀 {len(jobs)} vidéos à convertir avec {max_threads} threads...")

    mp4_paths = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(convertir_video, *args): args for args in jobs}
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                mp4_paths.append(result)

    print("✅ Conversion terminée.")
    return mp4_paths

# 🔧 Utilisation :
# chemins_videos_converties = convertir_avi_a_mp4_threaded(r"D:\Training-5", "Training-5", max_threads=4)

# Affichage des chemins
# print("\n📝 Chemins des vidéos converties :")
# for chemin in chemins_videos_converties:
#     print(chemin)
