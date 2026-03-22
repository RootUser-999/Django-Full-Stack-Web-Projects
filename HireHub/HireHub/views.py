from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect    
def home(request):
    return render(request,'home.html')

def features(request):
    return render(request, 'features.html')

def about(request):
    return render(request, 'about.html')