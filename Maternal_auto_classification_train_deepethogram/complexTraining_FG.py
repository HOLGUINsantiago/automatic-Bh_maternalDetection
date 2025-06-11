import os
from deepethogram.configuration import make_config
from deepethogram.flow_generator.train import flow_generator_train
import os


if __name__ == '__main__':
    project_path = r"D:\LBN\Maternal_auto_classification_train_deepethogram"

    flow_weights = r"D:\LBN\Maternal_auto_classification_train_deepethogram\models\pretrained_models\200313_125331_TinyMotionNet3D_kinetics\checkpoint.pt"

    cfg = make_config(
        project_path=project_path,
        config_list=['config', 'augs', 'model/flow_generator', 'train'],
        run_type='train',
        model='flow_generator',
        use_command_line=False,
        preset="deg_s"
    )

    cfg.flow_generator.weights = flow_weights

    flow_generator_train(cfg)
