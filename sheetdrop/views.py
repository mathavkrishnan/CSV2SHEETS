from django.shortcuts import render,redirect
import random
import json
import pandas as pd
import csv
import os
import gspread
from django.conf import settings
from django.conf.urls.static import static
from .models import CSV_FILES
from sklearn.impute import SimpleImputer
# Create your views here.
def random_num():
  return str(random.randint(1000000000, 9999999999))

def process_csv_file(file):
    with open(file, 'r') as f:
     ds = pd.read_csv(f, encoding='ISO-8859-1')
     return ds.columns.values

def remove_cols(file,columns):
    df = pd.read_csv(file, encoding='ISO-8859-1')
    for i in columns:
     df = df.drop(i, axis=1)
    df.to_csv(file, index=False)

def clean_csv(file):
    ds = pd.read_csv(file, encoding='ISO-8859-1')
    imputer = SimpleImputer(strategy='most_frequent')
    imputer.fit(ds)
    ds = imputer.transform(ds)

def feature_scale(file):
    ds = pd.read_csv(file, encoding='ISO-8859-1')
    imputer = SimpleImputer(strategy='most_frequent')
    imputer.fit(ds)
    ds = imputer.transform(ds)

def home(request):
    if request.method == 'POST':
        fil = request.FILES.getlist('file')
        x = random_num()
        for i in fil:
           p = CSV_FILES.objects.create()
           p.name = x
           p.file = i
           p.save()
        return redirect(filtersheet,pk = x)
        
    else:
     return render(request,'sheetdrop/home.html')
    
def filtersheet(request,pk):
   x = CSV_FILES.objects.filter(name = pk)


   if request.method == 'POST':
      b = []
      for i in range(1,len(x)+1):
       a = request.POST.getlist(str(i))
       b.append(a)
      ###filter out these columns from csv
      t = 0
      for j in x:
        remove_cols(os.path.join(settings.MEDIA_ROOT,str(j.file)),b[t])
        t = t+1
        checklist_values = []
        for i in range(1, len(x) + 1):
         a = request.POST.getlist(str(i)+str(i)+'[]')
         checklist_values.append(a)
        if checklist_values[0] == 'on':
          clean_csv(os.path.join(settings.MEDIA_ROOT,str(j.file)))
      return redirect(newcsv,pk = pk)
   

   else:
    arr = []
    for i in x:
      arr.append([process_csv_file(os.path.join(settings.MEDIA_ROOT,str(i.file)))])
    return render(request,'sheetdrop/filtersheet.html',{'pk':pk,'users':arr})

def newcsv(request,pk):
    if request.method == 'POST':
     x = CSV_FILES.objects.filter(name = pk)
     gc = gspread.oauth(credentials_filename="C:\\Users\\Mathav Krishnan\\Desktop\\csvtosheet\\credentials.json")
     url = []
     for i in x:
       sh = gc.create(str(i.name))
       spreadsheet = gc.open(str(i.name))
       p = os.path.join(settings.MEDIA_ROOT,str(i.file))
       with open(p, 'r') as file_obj:
        content = file_obj.read()
        gc.import_csv(spreadsheet.id, data=content)
        spreadsheet.share(request.POST['email'], perm_type='user', role='writer', notify=False)
       url.append(sh.url)
     return render(request,'sheetdrop/newcsv.html',{'url':url})
    else:
      return render(request,'sheetdrop/newcsv.html')