import h5py
import numpy as np

path = r'D:\LBN\Maternal_auto_classification_train_deepethogram\models\250610_173633_feature_extractor_train\classification_metrics.h5'

with h5py.File(path, 'r') as f:
    print("Raíz:", list(f.keys()))
    
    class_names = ['background', 'Onnest', 'Offnest', 'ABN', 'Carryingpups',
                   'Selfgrooming', 'Eat_drink', "kicking", 'Groomingpups', 'Build']

    for split in ['train', 'val']:
        group = f[split]
        print(f"\n--- Métricas por comportamiento ({split}) última época ---")
        
        f1 = group['f1_by_class'][:]      # shape (epochs, clases)
        accuracy = group['accuracy_by_class'][:]  # shape (epochs, clases)

        f1_last_epoch = f1[-1]  # última fila
        accuracy_last_epoch = accuracy[-1]

        for i, name in enumerate(class_names):
            print(f"{name}: F1 = {f1_last_epoch[i]:.4f}, Accuracy = {accuracy_last_epoch[i]:.4f}")

        print(f"\nF1 medio (incluyendo background) última época: {group['f1_class_mean'][-1]}")
        print(f"F1 medio (sin background) última época: {group['f1_class_mean_nobg'][-1]}")
        print(f"F1 overall última época: {group['f1_overall'][-1]}")
