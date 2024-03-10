from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import approvals
from django.core import serializers
from rest_framework.decorators import api_view
import joblib
import numpy as np
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
import pandas as pd
from keras import backend as K  # Import K from keras.backend
from  MyAPI.serializers import approvalsSerializers
from .forms import ApprovalForm
from django.contrib import messages

# Create your views here.
class ApprovalsView(viewsets.ModelViewSet):
	queryset = approvals.objects.all()
	serializer_class = approvalsSerializers
	

import joblib
import pandas as pd

def ohevalue(df):
    # Load the expected one-hot encoded columns
    ohe_col = joblib.load("/Users/asheshlalshrestha/Desktop/Datanal/Project/Loan-approval/DjangoAPI/MyAPI/allcol.pkl")
     #    Index(['Loan_ID', 'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
    #    'Loan_Amount_Term', 'Credit_History', 'Property_Area', 'Loan_Status'],
    #   dtype='object')
    
    # Define categorical columns
    cat_columns = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    
    # Perform one-hot encoding
    df_processed = pd.get_dummies(df, columns=cat_columns)
    
    # Initialize a dictionary to hold the one-hot encoded values
    newdict = {}
    
    # Iterate through each expected one-hot encoded column
    for i in ohe_col:
        if i in df_processed.columns:
            newdict[i] = df_processed[i].values
        else:
            newdict[i] = 0  # If the column is missing, add it as zeros
    
    # Create a DataFrame from the dictionary
    newdf = pd.DataFrame(newdict)
    
    return newdf



def approvereject(unit):
    try:
        mdl = joblib.load("/Users/asheshlalshrestha/Desktop/Datanal/Project/Loan-approval/DjangoAPI/MyAPI/loan_model.pkl")
        scalers = joblib.load("/Users/asheshlalshrestha/Desktop/Datanal/Project/Loan-approval/DjangoAPI/MyAPI/scalers.pkl")
        X = scalers.transform(unit)
        y_pred = mdl.predict(X)
        y_pred = (y_pred > 0.58)
        newdf = pd.DataFrame(y_pred, columns=['Status'])
        newdf = newdf.replace({True: 'Approved', False: 'Rejected'})
        return (newdf.values[0][0])
    except ValueError as e:
        return (e.args[0])

			
def cxcontact(request):
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            Firstname = form.cleaned_data['firstname']
            Lastname = form.cleaned_data['lastname']
            Dependents = form.cleaned_data['Dependents']
            ApplicantIncome = form.cleaned_data['ApplicantIncome']
            CoapplicantIncome = form.cleaned_data['CoapplicantIncome']
            LoanAmount = form.cleaned_data['LoanAmount']
            Loan_Amount_Term = form.cleaned_data['Loan_Amount_Term']
            Credit_History = form.cleaned_data['Credit_History']
            Gender = form.cleaned_data['Gender']
            Married = form.cleaned_data['Married']
            Education = form.cleaned_data['Education']
            Self_Employed = form.cleaned_data['Self_Employed']
            Property_Area = form.cleaned_data['Property_Area']
            myDict = (request.POST).dict()
            df = pd.DataFrame(myDict, index=[0])
            print(approvereject(ohevalue(df)))
            answer = approvereject(ohevalue(df))
            messages.success(request,'Application Status: {}'.format(answer))
					
    form=ApprovalForm()

    return render(request, 'myform/cxform.html', {'form':form})
     
		
	