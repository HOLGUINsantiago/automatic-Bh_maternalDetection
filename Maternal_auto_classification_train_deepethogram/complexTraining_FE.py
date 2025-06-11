import os
from deepethogram.feature_extractor.train import feature_extractor_train
from deepethogram.configuration import make_config
from deepethogram.flow_generator.train import flow_generator_train
import os


if __name__ == '__main__':
    project_path = r"D:\LBN\Maternal_auto_classification_train_deepethogram"

    data_path = os.path.join(project_path, "DATA")
    all_records = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]

    dirs_to_infer = []
    for record in all_records:
        output_file = os.path.join(data_path, record, "output.h5")
        if not os.path.isfile(output_file):
            dirs_to_infer.append(os.path.join(data_path, record))

    data_path = os.path.join(project_path, "DATA")
    feature_weights = r"D:\LBN\Maternal_auto_classification_train_deepethogram\models\250610_122625_feature_extractor_train\lightning_checkpoints\epoch=0-step=999.ckpt"
    flow_weights = r"D:\LBN\Maternal_auto_classification_train_deepethogram\models\250606_152347_flow_generator_train\lightning_checkpoints\epoch=1-step=1999.ckpt"

    cfg = make_config(
        project_path=project_path,
        config_list=['config', 'augs', 'model/feature_extractor', 'model/flow_generator', 'train', 'postprocessor', 'inference'],
        run_type='train',
        model='feature_extractor',
        use_command_line=False,
        preset="deg_s"
    )

    # Pongo los pesos directamente en la config
    cfg.feature_extractor.weights = feature_weights
    cfg.flow_generator.weights = flow_weights

    # Lista de carpetas a inferir
    cfg.inference.directory_list = dirs_to_infer
    cfg.inference.overwrite = True

    feature_extractor_train(cfg)
