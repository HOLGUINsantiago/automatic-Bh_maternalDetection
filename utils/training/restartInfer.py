import os

# Ruta al directorio raíz
root_dir = r"D:\LBN\Maternal_auto_classification_train_deepethogram\DATA"

# Recorre todos los subdirectorios y archivos
for dirpath, _, filenames in os.walk(root_dir):
    for file in filenames:
        if file.endswith(".h5") or file.endswith("_outputs_labels_predictions.csv") or file.endswith("_outputs_predictions.csv")  :
            file_path = os.path.join(dirpath, file)
            try:
                os.remove(file_path)
                print(f"Eliminado: {file_path}")
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")
