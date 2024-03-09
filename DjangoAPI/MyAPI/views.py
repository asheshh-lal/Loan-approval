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
from  MyAPI.serializers import approvalsSerializers
from .forms import ApprovalForm
# Create your views here.
class ApprovalsView(viewsets.ModelViewSet):
	queryset = approvals.objects.all()
	serializer_class = approvalsSerializers
	

# @api_view(['POST'])
def approvereject(request):
        try:
            mdl = joblib.load("/Users/asheshlalshrestha/Desktop/Datanal/Project/Loan-approval/DjangoAPI/MyAPI/loan_model.pkl")
            scalers = joblib.load("/Users/asheshlalshrestha/Desktop/Datanal/Project/Loan-approval/DjangoAPI/MyAPI/scalers.pkl")
            mydata = request.data
            unit = np.array(list(mydata.values()))
            unit = unit.reshape(1,-1)
            X = scalers.transform(unit)
            y_pred = mdl.predict(X)
            y_pred = (y_pred>0.58)
            new_df = pd.DataFrame(y_pred,columns=['Status'])
            new_df = new_df.replace({True:'Approved',False:'Rejected'})
            return JsonResponse("Your status is {}",new_df,safe=False)

        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
        
def cxcontact(request):
	if request.method=='POST':
		form=ApprovalForm(request.POST)
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
				print(Firstname,Lastname,Dependents,Married,Property_Area)
					
	form=ApprovalForm()
				
	return render(request, 'myform/cxform.html', {'form':form})
     



            
	