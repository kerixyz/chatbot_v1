##import stuff
import pandas as pd
import numpy as np
import ktrain

from ktrain import text
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, f1_score
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split

##tutorial source: https://github.com/ugolbck/construct_tutorial/blob/master/src/train.py

## initializing variables and paths
PATH_DATA = 'data/'
PATH_MODELS = 'models/'
LABELS = [0, 1]
MODEL_NAME = 'bert-base-uncased' #distilbert is 40% smaller than bert and still good enough
MAXLEN = 150 #can finetune parameter later

##data source: https://www.kaggle.com/datasets/mtaboada/c3-constructive-comments-corpus
df = pd.read_csv(PATH_DATA + 'C3.csv')

#we're using stratified train and test splitting
#need to do it multiple times i guess? first round gives us intermediate set, and test set, then second round is train set then validation set

#stratified train/test splitting
ss1 = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, intermediate_index in ss1.split(df, df['constructive_binary']):
    intermediate_set = df.loc[train_index]
    test_set = df.loc[intermediate_index]

#indeces unordered, reset
intermediate_set.reset_index(drop=True, inplace=True)
test_set.reset_index(drop=True, inplace=True)

#stratified train/val splitting
ss2 = StratifiedShuffleSplit(n_splits=1, test_size = 0.1, random_state=42)
for train_index, val_index in ss2.split(intermediate_set, intermediate_set['constructive_binary']):
    train_set = intermediate_set.loc[train_index]
    val_set = intermediate_set.loc[val_index]

#resetting indeces again
train_set.reset_index(drop=True, inplace=True)
val_set.reset_index(drop=True, inplace=True)

#inputs
X_train = np.asarray(train_set.comment_text)
X_val = np.asarray(val_set.comment_text)
X_test = np.asarray(test_set.comment_text)

#outputs
y_train = train_set.constructive_binary.astype('int8').tolist()
y_val = val_set.constructive_binary.astype('int8').tolist()
y_test = test_set.constructive_binary.astype('int8').tolist()

#loading the transformer model from hugging face
t = text.Transformer(MODEL_NAME, maxlen=MAXLEN, class_names=LABELS)

#preprocessing
train_final = t.preprocess_train(X_train, y_train)
val_final = t.preprocess_test(X_val, y_val)

#model generation
model = t.get_classifier()

# learner object generation
learner = ktrain.get_learner(model, train_data=train_final, val_data=val_final, batch_size=32) #another prameter to finetune

#fitting hte training data
learner.fit_onecycle(1e-5, 4)

#validation step
learner.validate(class_names = t.get_classes())

#get predictor object
predictor = ktrain.get_predictor(learner.model, preproc=t)

#test step
y_pred = predictor.predict(X_test)

#results visulaization
print("Accuracy: ", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred, average='weighted'))
print(classification_report(y_test, y_pred, target_names=['nonconstructive','constructive']))
print(confusion_matrix(y_test,y_pred))
report = classification_report(y_test, y_pred, output_dict=True)

#saving
#predictor.save(PATH_MODELS + 'distilbert-construct')