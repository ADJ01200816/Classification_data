# Industry Data Classification using Large Language Models (LLMs)

This repository contains the implementation for classifying unstructured industry data based on large language models (LLMs). The project focuses on improving the accuracy and efficiency of classifying industry-specific data into predefined categories, using state-of-the-art machine learning techniques. The goal is to take an input text along with industry classification guidelines and output the corresponding category and specific matching criteria.

## Project Overview

The main objective of this project is to develop a classification model that can automatically categorize unstructured industry data into predefined classes based on a set of industry-specific classification criteria. It leverages large language models (LLMs) for improved fine-grained classification and interpretability, reducing the need for large datasets and offering a more transferable and efficient classification framework.

### Key Features
- **Input**: Unstructured text (industry data) and classification guidelines.
- **Output**: Classified category and specific matching criteria based on industry standards.
- **Focus Areas**:
  - Reducing reliance on large datasets for training.
  - Improving the classification granularity and interpretability.
  - Handling few-sample and zero-sample conditions.
  - Transferability of the model across different industries (e.g., finance, healthcare, etc.).

 ## File Descriptions

- **classify_model.py**: Machine learning model for classification, constructing inverted index or trie tree models.
- **classify.py**: Uses the above models to generate classification results and extracts named entities from text using LLM.
- **identify.py**: Verifies the classification and pre-classification results. The other two functions are for testing purposes and are unrelated to the main functionality.
- **new_data.py**: Generates a test dataset using LLM.
- **outdependence.py**: Contains all imports.
- **pre_classify.py**: Used for the pre-classification process, including word frequency statistics and keyword extraction.
- **read_information.py**: Extracts file information.
- **setting.py**: Configuration of relevant parameters.
- **tools.py**: Utility functions, including word vector conversion and LLM usage.


  
### Methodology
The project employs method which involves:
- **Feature extraction**: Extracting important feature from the input text.
- **Design Question Template**: Ask questions to your LLM using question templates.
- **Pre-classification**: Use the pre-classification method to select the rules that the text may meet, and then perform feature matching.


### Industries Covered
The model is designed to be flexible and adaptable across multiple industries, including:
- Finance
- Healthcare
- New Energy

## Dependencies

This project requires the following Python libraries and tools:

### Basic Libraries

- `re`: Regular expression operations
- `os`: Interacting with the operating system
- `time`: Time-related functionality
- `shutil`: High-level file operations
- `numpy`: Numerical computation library
- `pandas`: Data processing and analysis library
- `collections`: Provides special data structures like `Counter`
- `jieba`: Chinese text segmentation tool

### Machine Learning Libraries

- `sklearn`:
  - `metrics.pairwise`: For calculating similarities (e.g., cosine similarity)
  - `feature_extraction.text`: Provides `TfidfVectorizer` and `CountVectorizer`
  - `model_selection`: Provides `train_test_split`
  - `metrics`: Includes classification reports and accuracy evaluation
  - `neighbors`: k-nearest neighbors classifier
  - `tree`: Decision tree classifier
  - `svm`: Support vector machine classifier
  - `linear_model`: Logistic regression classifier
  - `ensemble`: Random forest and gradient boosting classifiers
  - `naive_bayes`: Multinomial Naive Bayes classifier

### Deep Learning and Natural Language Processing

- `torch`: PyTorch, deep learning framework
- `transformers`: For handling pre-trained BERT models (including `BertModel`, `BertTokenizer`, `Trainer`, and `TrainingArguments`)

### Other Dependencies

- `datasets`: For loading and processing datasets
- `zhipuai`: Interface to the Zhipu AI service for model inference
## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/industry-data-classification.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r outdependence.txt
    ```

3. Download any necessary pretrained models (if applicable).

## Usage

1. Input the unstructured industry data text into the model.
2. Provide the industry classification guidelines as part of the input.
3. Run the model to get the output:
   - **Category Level**: The predicted industry category.
   - **Matching Criteria**: The specific criteria from the guidelines that match the input text.

Example:

text: Xiao Zhang has handled business through online banking and mobile banking apps, and has also made an appointment for counter services, which are received by his account manager Xiao Li. He occasionally uses remote banking services and receives notifications via email and text messages. Social networks have become an auxiliary channel for him to interact with financial institutions. Recently, he compared the products and services of several institutions and plans to make a choice during his visit time next Wednesday. He usually logs in at night and visits mostly at home. In addition, his web browsing history and APP browsing history show inquiries about personal driving habits.

output:
['Personal public-private relationship information', 'Unit public-private relationship information'] [2]


### Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. Make sure to follow the project's coding standards and write appropriate tests for your changes.

### License

This project is licensed under the MIT License - see the LICENSE file for details.



