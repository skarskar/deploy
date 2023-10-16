import pandas as pd
import numpy as np
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import chi2
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display
import category_encoders as ce
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_extraction import DictVectorizer
from scipy.stats.mstats import winsorize
from feature_engine.outliers import Winsorizer
from sklearn.preprocessing import TargetEncoder 
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, log_loss, classification_report, accuracy_score,  roc_auc_score, roc_curve, auc
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

# prepare input data
def prepare_inputs(X_train):
  #https://towardsdatascience.com/dealing-with-categorical-variables-by-using-target-encoder-a0f1733a4c69
 #oe = ce.CountEncoder()
 #oe.fit(X_train)
  encoder = TargetEncoder(smooth='auto', target_type='binary')
  X_train_enc = encoder.fit_transform(X_train.drop(columns='loan_default_status'), X_train['loan_default_status']) 
  return X_train_enc

 # prepare target
def prepare_targets(y_train, y_test):
  le = LabelEncoder()
  le.fit(y_train)
  y_train_enc = le.transform(y_train)
  y_test_enc = le.transform(y_test)
  return y_train_enc, y_test_enc

 # feature selection based on chi2
def select_features(X_train, y_train, X_test):
  fs = SelectKBest(score_func=chi2, k=1)
  fs.fit(X_train, y_train)
  X_train_fs = fs.transform(X_train)
  X_test_fs = fs.transform(X_test)
  return X_train_fs, X_test_fs, fs

 # feature selection based on Mutual Importance
def select_features_mutual_info(X_train, y_train, X_test):
  fs = SelectKBest(score_func=mutual_info_classif, k=1)
  fs.fit(X_train, y_train)
  X_train_fs = fs.transform(X_train)
  X_test_fs = fs.transform(X_test)
  return X_train_fs, X_test_fs, fs

st.title("Loan Default model will predict if a person would default on their loan or not")
st.text('Dataset')
df= read_csv('https://raw.githubusercontent.com/skarskar/MLWorkshop/main/dataset/Loan%20Default%20prediction%20dataset%20Train.csv')

df.rename(columns={'Loan Status': 'Loan Default Status', 'Employment Duration': 'Home Ownership','Home Ownership':'Annual Income'}, inplace=True)

#drop columns as these only have 1 unique value
df.drop(columns=['Payment Plan','Accounts Delinquent'], inplace=True)
df.drop(columns=['ID'], inplace=True)

# change columns & categorical column values to lower case and replace space with hyphen
df.columns = df.columns.str.lower().str.replace(' ', '_')
string_columns = list(df.dtypes[df.dtypes == 'object'].index)

for col in string_columns:
    df[col] = df[col].str.lower().str.replace(' ', '_')

#check for duplicates
df.drop_duplicates(inplace=True)

#outliers
capper = Winsorizer(capping_method='iqr',
                    tail='both',
                    fold=3,
                    variables=['funded_amount_investor', 'interest_rate',
                               'annual_income', 'open_account', 'total_accounts',
                               'revolving_balance','total_received_interest','total_current_balance',
                               'total_revolving_credit_limit'])
capper.fit(df)
print(capper.right_tail_caps_)
print(capper.left_tail_caps_)
# transform the data
df = capper.transform(df)

#Feature Selection
df.drop(columns=['initial_list_status','application_type','verification_status'], axis=1, inplace=True)

st.table(df.head(5).T)

st.subheader('Features Coorelation with Target')
df.drop("loan_default_status", axis=1).apply(lambda x: x.corr(df.loan_default_status,method='spearman')).sort_values(ascending=False).plot(kind='barh', figsize=(14,8))
st.pyplot()
st.divider()
st.subheader('Outliers')
for col in df.drop(columns='loan_default_status').select_dtypes(exclude=['object']).columns:
  plt.figure(figsize=(3,3))
  sns.boxplot(x='loan_default_status', y=col, data=df)
  st.pyplot()
st.divider()
# split into train and test sets
df_X_train_test = df.drop(columns='loan_default_status', axis=1).to_dict(orient='records')

#DictVectorizer can be used in Neural Networks
#dv = DictVectorizer(sparse=False)
#dv.fit(df_X_train_test)
#dv.get_feature_names_out()
#X = dv.transform(df_X_train_test)

#TargetEncode
X_train_enc = prepare_inputs(df)
#y_train_enc, y_test_enc = prepare_targets(df.loan_default_status, df.loan_default_status)
X_train, X_test, y_train, y_test = train_test_split(X_train_enc, df.loan_default_status, test_size=0.20, random_state=10)

#Accuracy Score
model =  LogisticRegression(solver='liblinear', random_state=12)
model.fit(X_train, y_train)
# evaluate the model
yhat = model.predict(X_test)

st.subheader('Features Co-efficients')
coeffs = model.coef_.reshape(-1)
# visualizing coefficients
index = pd.DataFrame(X_train, columns = df.drop(columns='loan_default_status', axis=1).columns.tolist()).columns.tolist()
#(pd.DataFrame(coeffs, index = index, columns = ['coeff']).sort_values(by = 'coeff')
 #.plot(kind='barh', figsize=(8,24)))
# summarize feature importance
#for i,v in enumerate(coeffs):
 #st.text('Feature: %0d, Score: %.5f' % (i,v))
# plot feature importance
plt.bar([x for x in range(len(coeffs))], coeffs)
st.pyplot()
st.divider()
st.subheader('Confusion Matrix')
cm = confusion_matrix(y_test, yhat)
# Plot confusion matrix using ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
st.pyplot()
st.divider()
#Roc Curve
fpr, tpr, thresholds = roc_curve(y_test, yhat)
roc_auc = auc(fpr, tpr)
roc_auc_score = roc_auc_score(y_test, yhat)

plt.figure(figsize=(5, 5))
plt.plot(fpr, tpr, color='lightblue', lw=2, label='ROC curve (AUC = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='dashed', alpha=0.5)

plt.xlim([-0.02, 1.02])
plt.ylim([-0.02, 1.02])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')

plt.title('ROC curve')
plt.legend(loc="lower right")
st.pyplot()
st.divider()
st.subheader('Model Accuracy')
accuracy = accuracy_score(y_test, yhat)
st.text('Accuracy: %.2f' % (accuracy*100))