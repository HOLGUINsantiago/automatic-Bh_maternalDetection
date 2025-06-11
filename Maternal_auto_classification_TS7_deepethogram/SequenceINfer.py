import os
from deepethogram.feature_extractor.inference import feature_extractor_inference
from deepethogram.configuration import make_config
from deepethogram.sequence.inference import sequence_inference
import os
import torch

if __name__ == '__main__':
    torch.cuda.empty_cache()
    project_path = r"D:\LBN\Maternal_auto_classification_TS7_deepethogram"
    data_path = os.path.join(project_path, "DATA")

    all_records = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]

    dirs_to_infer = []
    for record in all_records:
        output_file = os.path.join(data_path, record, "output.h5")
        if not os.path.isfile(output_file):
            dirs_to_infer.append(os.path.join(data_path, record))

    print("Registros a inferir (con output.h5):", len(dirs_to_infer))

    cfg = make_config(
        project_path=project_path,
        config_list=['config', 'augs', 'model/sequence', 'inference', 'postprocessor', 'model/feature_extractor'],
        run_type='inference',
        model='sequence',
        use_command_line=False
    )

    cfg.sequence.weights = r"D:\LBN\Maternal_auto_classification_TS7_deepethogram\models\250603_145653_sequence_train\lightning_checkpoints\epoch=28-step=9685.ckpt"

    cfg.inference.directory_list = dirs_to_infer
    cfg.inference.overwrite = True

    cfg.postprocessor.min_bout_length = 10
    cfg.postprocessor.min_bout_per_behavior = [5] * 10

    cfg.compute.num_workers=8
    cfg.compute.batch_size=8

    sequence_inference(cfg)
