import os
import yaml
import time
import random
from deepethogram.feature_extractor.train import feature_extractor_train
from deepethogram.configuration import make_config

def get_video_names(data_path):
    valid_dirs = []
    for folder in os.listdir(data_path):
        folder_path = os.path.join(data_path, folder)
        if not os.path.isdir(folder_path):
            continue
        # Buscar cualquier archivo que termine en 'labels.csv'
        for file in os.listdir(folder_path):
            if file.endswith('labels.csv'):
                valid_dirs.append(folder)
                break  # Ya encontramos uno, no hace falta seguir
    random.shuffle(valid_dirs)
    return valid_dirs


def make_split_yaml(split_path, train_names, val_names):
    split_dict = {
        'metadata': {'split': [0.9, 0.1, 0.0]},
        'train': train_names,
        'val': val_names,
        'test': []
    }
    with open(split_path, 'w') as f:
        yaml.dump(split_dict, f)

def create_incremental_splits(data_path, splits_dir, total_splits=7, initial_frac=0.4, increment_frac=0.1):
    video_names = get_video_names(data_path)
    random.shuffle(video_names)
    n = len(video_names)

    val_size = int(n * 0.1)
    val_names = video_names[-val_size:]
    available_for_train = video_names[:-val_size]

    total_train_max = len(available_for_train)

    # Tamaño inicial y tamaño de incremento
    initial = int(total_train_max * initial_frac)
    increment = int(total_train_max * increment_frac)

    for i in range(total_splits):
        num_train = min(initial + i * increment, total_train_max)
        train_names = available_for_train[:num_train]

        split_path = os.path.join(splits_dir, f'split_{i+1}.yaml')
        make_split_yaml(split_path, train_names, val_names)

        print(f'[+] Split {i+1} creado con {len(train_names)} train y {len(val_names)} val')

# def create_splits_for_behaviour() :



def find_latest_model_dir(models_dir):
    all_dirs = [d for d in os.listdir(models_dir)
                if os.path.isdir(os.path.join(models_dir, d)) and 'feature_extractor_train' in d]
    if not all_dirs:
        return None
    return os.path.join(models_dir, sorted(all_dirs)[-1])

def find_best_ckpt(checkpoints_dir):
    ckpts = [f for f in os.listdir(checkpoints_dir)
             if f.endswith('.ckpt') and f != 'last.ckpt']
    if not ckpts:
        return None
    return os.path.join(checkpoints_dir, sorted(ckpts)[0])

def run_incremental_training(
    project_path,
    total_splits=7,
    initial_ratio=0.4,
    increment_ratio=0.1,
    preset="deg_m",
    feature_weights=None,
    flow_weights=None
):
    data_path = os.path.join(project_path, "DATA")
    splits_path = os.path.join(project_path, "SPLITS")
    models_dir = os.path.join(project_path, "models")
    os.makedirs(splits_path, exist_ok=True)

    create_incremental_splits(data_path, splits_path, total_splits, initial_ratio, increment_ratio)

    for i in range(total_splits):
        print(f'\n[***] Entrenando split {i+1}...\n')

        split_file = os.path.join(splits_path, f'split_{i+1}.yaml')

        cfg = make_config(
            project_path=project_path,
            config_list=['config', 'augs', 'model/feature_extractor', 'model/flow_generator', 'train', 'postprocessor', 'inference'],
            run_type='train',
            model='feature_extractor',
            use_command_line=False,
            preset=preset
        )

        cfg.feature_extractor.weights = feature_weights
        cfg.flow_generator.weights = flow_weights
        cfg.split.file = split_file
        cfg.split.train_val_test = [0.9, 0.1, 0.0]
        cfg.split.reload=False
        cfg.validSplitsOnly= False
        cfg.own_split = True
        feature_extractor_train(cfg)

        print('[+] Entrenamiento terminado. Buscando mejores pesos...')
        latest_model_dir = find_latest_model_dir(models_dir)
        if not latest_model_dir:
            print('[!] No se encontró el directorio del modelo')
            break

        checkpoints_dir = os.path.join(latest_model_dir, 'lightning_checkpoints')
        best_ckpt = find_best_ckpt(checkpoints_dir)

        if best_ckpt:
            print(f'[✓] Mejores pesos encontrados: {best_ckpt}')
            feature_weights = best_ckpt  # Update for next iteration
        else:
            print('[!] No se encontró .ckpt bueno')
            break

        time.sleep(5)

if __name__ == '__main__':
    run_incremental_training(
        project_path=r"D:\LBN\Maternal_auto_classification_train_deepethogram",
        total_splits=7,
        initial_ratio=0.4,
        increment_ratio=0.1,
        preset="deg_m",
        feature_weights=r"D:\LBN\Maternal_auto_classification_train_deepethogram\models\pretrained_models\200410_142156_hidden_two_stream_kinetics_degm\flow\checkpoint.pt",
        flow_weights=r"D:\LBN\Maternal_auto_classification_train_deepethogram\models\250616_164900_flow_generator_train\lightning_checkpoints\epoch=1-step=1999.ckpt"
    )
