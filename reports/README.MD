Reports 
- Notebooks in the report section are designed to be stand alone notebooks which generate information for the user. 
- You MUST have followed all steps in the notebooks folder to be able to use these files. Given the size of the YT8M dataset we cannot store 
the data for you to easily use, and intermediate files will need to be generated. Please see the main repository page for information on the data access.

- ClassifierComparison.ipynb: builds the SVM, CNN, Fully Connected, and LSTM models and shows various metrics. (Runs in Great Lakes)
- Descriptive.ipynb: runs descriptive analysis by merging in translated titles/descriptives, video details dataset, and 'hunting' label from topic modeling results.
- pyCaret_classification.ipynb: runs the automated comparison of a bunch of models for determining which models were worth pursuing. (Runs in Colab)
- videoSVM.ipynb: creates an SVC classifier and performs GridSearchCV on it to determine the best performing hyperparameters (Runs in Great Lakes)
- video_Classifier_CNN.ipynb: creates the CNN neural network classifier and does an initial run using both the imbalanced dataset and then with an artificially balanced dataset.
- video_Classifier_NN.ipynb: builds the Fully Connected neural network classifiers and does an initial run using both the imbalanced dataset and then with an artificially balanced dataset.
