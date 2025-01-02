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
  
### Methodology
The project employs the Clue And Reasoning Prompting (CARP) method, which involves:
- **Clue Identification**: Extracting important clues from the input text.
- **Reasoning**: Using these clues to identify the most appropriate category.
- **Fine-Tuning**: Fine-tuning LLMs for improved classification performance on industry-specific datasets.

### Industries Covered
The model is designed to be flexible and adaptable across multiple industries, including:
- Finance
- Healthcare
- New Energy
- And more...

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/industry-data-classification.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Download any necessary pretrained models (if applicable).

## Usage

1. Input the unstructured industry data text into the model.
2. Provide the industry classification guidelines as part of the input.
3. Run the model to get the output:
   - **Category Level**: The predicted industry category.
   - **Matching Criteria**: The specific criteria from the guidelines that match the input text.

Example:
```python
from model import classify_text

text = "Sample unstructured data about new energy car market trends."
classification_criteria = ["finance", "new energy", "automotive"]

category, matching_criteria = classify_text(text, classification_criteria)
print(f"Predicted Category: {category}")
print(f"Matching Criteria: {matching_criteria}")
