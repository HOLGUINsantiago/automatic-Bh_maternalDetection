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

If you use DeepEthogram within Jupyter Notebook or install any packages beyond DeepEthogram's dependencies, you may experience a loss of functionality in DeepEthogram.
We recommend creating two separate conda environments: one for Jupyter Notebook and another exclusively for DeepEthogram.

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
Different analysis for maternal and pup's data are available on [AnalyseR file](results_analysis.Rmd)

## Data availability
Pretrained models, and annotated videos are available on demand by contacting Dr. Marion Rivalan ([marion.rivalan@cnrs.fr](mailto:marion.rivalan@cnrs.fr)) from [NeuroPSI Sylvie Granon team](https://neuropsi.cnrs.fr/departements/cnn/equipe-sylvie-granon/)


## Typical errors
- Assert error on Bout Lengths :
  - Change the asserts block on process function, defining a predeterminated bout_length
    ```{python}
    def __init__(self, thresholds: np.ndarray, bout_lengths: list, **kwargs):
            super().__init__(thresholds, **kwargs)

            if bout_lengths is None or len(thresholds) != len(bout_lengths):
                print(f"[WARNING] Ajustando bout_lengths automáticamente: thresholds={len(thresholds)}, bout_lengths={len(bout_lengths) if bout_lengths else 'None'}")
                bout_lengths = [10] * len(thresholds)
                self.bout_lengths = bout_lengths

        def process(self, probabilities: np.ndarray) -> np.ndarray:
            T, K = probabilities.shape
            if (not hasattr(self, 'bout_lengths') or self.bout_lengths is None or K != len(self.bout_lengths)):
                print(f"[WARNING] Ajustando bout_lengths automáticamente")
                bout_lengths = [10] * K
                self.bout_lengths = bout_lengths
    ```
### Good maternal video processing !!!!!