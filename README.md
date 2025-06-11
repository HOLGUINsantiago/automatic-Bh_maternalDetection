# Maternal behaviours automatic classification - With [DeepEthogram](https://github.com/jbohnslav/deepethogram)

- Written by Santiago Holguin 
- [holguinsanty@gmail.com](mailto:holguinsanty@gmail.com)

## DeepEthogram installation - For NVIDIA GPU - CUDA 11.8
Make sure to have cuda and conda installed on your PC
1. Create environment : 
    
    `conda create --name deg python=3.7`
    
2. Connect to env : 
    
     `conda activate deg`
    
3. Installer pyside2 : 
    
    `conda install -c conda-forge pyside2=5.15.6`
    
4. Install torch versions (for cuda 11.3 even if you have cuda 11.8) : 
    
    `pip install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio==0.10.2 -f https://download.pytorch.org/whl/cu113/torch_stable.html`
    
5. Resolve issues by installing tensorboard : 
    
    `pip install tensorboard==2.11.2`
    
6. Change version of pytorch-lighting :
    
    `pip install pytorch-lightning==1.5.10`
    
7. Install it 
    
    `pip install deepethogram`
    
8. Try it !!
    
    `deepethogram`

## DeepEthogram training
We trained the open source package DeepEtogram using different labeled videos. 
The DeepEthogram project [Maternal_auto_classification_train_deepethogram](Maternal_auto_classification_train_deepethogram) can be use for training different models. In it, complex training files can used for training with different model configurations.

Each resulted model can be used on [Maternal_auto_classification_TS7_deepethogram](Maternal_auto_classification_TS7_deepethogram) for new video processing : 

1.  Copy and pase the last trained models for flow generation, feature extraction and sequence on [models dir](Maternal_auto_classification_TS7_deepethogram/models/)

2. Change configurations off infer files by giving the exact path of each new added model
3.  If the number of videos is elevated, use the python script for infering. On the contrary, you can use directly the DeepEthogram GUI
   
## Data processing
### Trained models validation
You can process training results with [read metrics script](utils\validation\readMetrics.py).

### Results processing 
- You can follow the [LaunchDeg pipeline](LaunchDEG.ipynb) part "3." for transforming all the outputs on .csv files. T
- You can use [analyseResultats pipeline](analyseResultats.ipynb) for merging results on a single df containing temporal data transformation, and all the maternal behaviours
- You can also create a summary df where the results of a single video are resumed on a single line eliminating "frame dimension"

### Results analysis
Different analysis for maternal and pup's data are available on [AnalyseR file](AnalyseR.Rmd)

## Data availability
Pretrained models, and annotated videos are available on demand by contacting our [Neuropsi team](https://neuropsi.cnrs.fr/departements/cnn/equipe-sylvie-granon/)

### Good maternal video processing !!!!!