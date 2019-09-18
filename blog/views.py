from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

def home_page(request):
    context ={
        "title":"Hello World"
    }
    return render(request,"index.html",context)