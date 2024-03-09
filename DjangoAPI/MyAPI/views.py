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

# Create your views here.
class ApprovalsView(viewsets.ModelViewSet):
	queryset = approvals.objects.all()
	serializer_class = approvalsSerializers
	

@api_view(['POST'])
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
            
	