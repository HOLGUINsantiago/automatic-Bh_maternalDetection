import os
import yaml
import time
import random
from deepethogram.feature_extractor.train import feature_extractor_train
from deepethogram.configuration import make_config

cfg = make_config(
    project_path=r"D:\LBN\Maternal_auto_classification_train_deepethogram",
    config_list=['config', 'augs', 'model/feature_extractor', 'model/flow_generator', 'train', 'postprocessor', 'inference'],
    run_type='train',
    model='feature_extractor',
    use_command_line=False,
    preset="deg_m"
    )

cfg.feature_extractor.weights = r"D:\LBN\Maternal_auto_classification_train_deepethogram\models\250627_042102_feature_extractor_train\lightning_checkpoints\epoch=1-step=1999.ckpt"
cfg.flow_generator.weights = r"D:\LBN\Maternal_auto_classification_train_deepethogram\models\250616_164900_flow_generator_train\lightning_checkpoints\epoch=1-step=1999.ckpt"
cfg.split.train_val_test = [0.9, 0.1, 0.0]
cfg.split.reload=False
cfg.validSplitsOnly= False
cfg.own_split = True
cfg.split.file = r"D:\LBN\Maternal_auto_classification_train_deepethogram\SPLITS\split_4.yaml"
feature_extractor_train(cfg)