import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle


#Load the trained Model

model= tf.keras.models.load_model('model.h5')

#Load the scaler and encoders

with open('Label_encoder_gender.pkl','rb') as file:
    Label_encoder_gender=pickle.load(file)
with open('onehot_encoder_geo.pkl','rb') as file:
    onehot_encoder_geo=pickle.load(file)
with open('scaler.pkl','rb') as file:
    scaler=pickle.load(file)    


## Streamlit App

st.title('Customer Churn Prediction')

## User Input
geography=st.selectbox('Geography',onehot_encoder_geo.categories_[0])
gender=st.selectbox('Gender', Label_encoder_gender.classes_)
age=st.slider('Age',18,92)
balance=st.slider('Balance',10000,100000)
credit_score=st.slider('Credit Score',600,900)
estimated_salary=st.slider('Estimate Salary',15000,110000)
tenure=st.slider('Tenure',0,30)
num_of_products=st.slider('Number of Product',1,4)
has_cr_card=st.selectbox('Has Credit Card',[0,1])
is_active_member=st.selectbox('Is Active Member',[0,1])

##Prepare the input data

input_data=pd.DataFrame({
    'CreditScore':[credit_score],
    'Gender':[Label_encoder_gender.transform([gender])[0]],
    'Age':[age],
    'Tenure':[tenure],
    'Balance': [balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_member],
    'EstimatedSalary':[estimated_salary]
})

## One-hot Encoded 'Geography'

geo_encoded=onehot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df=pd.DataFrame(geo_encoded,columns=onehot_encoder_geo.get_feature_names_out(['Geography']))



## Combiner one hot encoded columns with input data
input_data=pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)

## Scaled the input data
input_data_scaled=scaler.transform(input_data)

##Predict the Churn

prediction= model.predict(input_data_scaled)
predict_prob=prediction[0][0]

st.write(f'Churn Probability : {predict_prob:2f}')

if predict_prob >0.5:
    st.write("The customer is likely to churn")
else:
    st.write("The customer is not likely to churn")    
