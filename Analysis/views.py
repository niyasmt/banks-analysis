from django.http import HttpResponse
from django.shortcuts import redirect, render
from Analysis.forms import DetailForm
from Analysis.models import Details
from django.conf import settings
import pandas as pd
import pdfplumber
from pathlib import Path
import pickle
from django.contrib import messages
from django.views.generic import ListView

# Create your views here.

def Home(request):
    form = DetailForm()
    # print(settings.MEDIA_ROOT)

    if request.method == 'POST':
        form = DetailForm(request.POST,request.FILES)
        if form.is_valid():
            pdf = form.cleaned_data['document']
            document = form.save(commit=False)
            document.save()
            # root = f'{settings.MEDIA_ROOT}\{pdf.name}'
            # root = str(settings.MEDIA_ROOT) +"\" + str(pdf.name)
            file_name = document.document.name.split('/')[-1]
            value = Predict(settings.MEDIA_ROOT,file_name)
            document.predicted_balance = value
            document.save()
            messages.success(request, ' predicted balance is' + "    " + str(document.predicted_balance))
            return redirect('Home')

    context = {
        'form': form,
    }

    return render(request,'home.html',context)


def Predict(doc_root,filename):
    root = Path(doc_root+'/files/'+filename)
    print(root,'*'*100)
    pdf = pdfplumber.open(root)
    df = pd.DataFrame()
    table_settings={"vertical_strategy": "text", 
        "horizontal_strategy": "lines","intersection_y_tolerance": 8}
    df = pd.DataFrame(pdf.pages[3].extract_table(table_settings))

    df.loc[:, 4] = df.loc[:, 4].astype('str')
    df.iloc[:, 5] = df.iloc[:, 5].astype('str')
    debit = []
    credit = []
    c = 0
    c2 = 0
    for i in df.loc[:, 4]:
        if i == '-':
            debit.append(0.0)
            c = c + 1
        else:
            debit.append(float(i))
            
    df.loc[:, 4] = debit
    su = df.loc[:, 4].sum()
    le = 130 - c
    avg = su / le

    for i in df.iloc[:, 5]:
        if i == '-':
            credit.append(0.0)
            c2 = c2 + 1
        else:
            credit.append(float(i))
            
    df.iloc[:, 5] = credit
    su2 = df.iloc[:, 5].sum()
    le2 = 130 - c2
    avg2 = su2 / le2


    
    load = pickle.load(open(r'C:\Users\HP\Desktop\Brocamp\Account_Analysis\Bank_Analysis\media\files\model', 'rb'))
    amount = load.predict([[avg,avg2]])
    return amount[0]


class AllPrediction(ListView):
    model = Details
    template_name = 'details.html'
    context_object_name = 'details'
