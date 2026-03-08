from django.shortcuts import render,redirect
from django.http import HttpResponse
import pandas as pd

# Create your views here.


def login(request):

    if request.method == "POST":
        return redirect("upload")

    return render(request,"main/login.html")

def upload(request):
    if request.method == "POST":
        file = request.FILES["excel_file"]
        df = pd.read_excel(file)
        filename = file.name
        
        

        if 'excel_file' not in request.FILES:
            return HttpResponse("No file uploaded.")

        if "Marks" not in df.columns:
            return HttpResponse("file must have a marks column")

        marks = df["Marks"]

        stats= {
            "mean": marks.mean(),
            "median": marks.median(),
            "standard deviation" : marks.std(),
            "max": marks.max(),
            "min": marks.min()
        }
        return render(request, "main/stats.html", {"stats": stats, "filename":filename })
    return render(request,"main/upload.html")

def marksheets(request):
    #return HttpResponse("marksheets page")
    return render(request,"main/marksheets.html")

