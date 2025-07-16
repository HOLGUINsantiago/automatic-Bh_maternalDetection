# Training and validation data
## Folders
Each folder is named as follow : {cageId}-{condition}-{recording_date(YYYY-MM-DD)}_{recording_time(HH-MM-SS)}.

For some folders cage id is misssing : eg. CONT-2024-05-06_20-00-34.

**Folder content** :
- Mp4 video : {folderName}.mp4
- csv annotation : {folderName}_labels.csv
- DeepEthgoram output : {folderName}_outputs.h5
- DeepEthogram metadata : recors.yaml
- DeepEthogram metadata stats : stats.yaml
  
## Training and validation
A "split.yaml" file has the metadata for video repartition between training and validation