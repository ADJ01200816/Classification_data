# Financial Industry Data Classification Standard

Welcome to the warehouse of industry classification datasets! This dataset is designed for research and analysis of industry data classification. The dataset contains three main sets of data: financial industry classification criteria, medical industry classification criteria, and new energy vehicle industry classification criteria.

## Description

The data in this dataset is constructed according to the classification criteria to ensure its applicability and ability to replace real situations. By using this data, we can verify whether our method is suitable for classifying unstructured data.

## Usage

You are free to utilize this dataset for academic, research, or commercial purposes. If you find this dataset valuable for your work, please consider citing our paper and providing a link back to this repository.

## Dataset Details
| Dataset Name   | Data Format | 
|----------------|-------------|
| NewEnergyVehicles   | txt         | 
| Finance     | txt         | 
| Medical      | txt         | 

The structure of each folder is the same, so we will only show one of them here.

## Folder Structure

### `cn/en`(chinese and english version)
- **-rules**:Includes three files:feature_data、level_data、category_data .
- **-Text_files**: This folder contains sample data, and a Data_label.txt file that marks the classification and security level of each text file．
- **-Data_labels.txt**: This file contains the category corresponding to each Text_files.

### feature_data
One line represents the content of one guideline 

### level_data
Each number corresponds to the level of each row of rules in feature_data

### category_data
Each name corresponds to the category of each row of rules in feature_data

## Citation

If you utilize this dataset in your research or project, we kindly request you to cite the following:
```
[Insert the citation details of the paper where this dataset is introduced or published]
```

## Contact Information

If you have any inquiries or require further assistance regarding the dataset, please feel free to contact us.
