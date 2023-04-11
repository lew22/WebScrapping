#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from .models import project
from django.shortcuts import render
from .forms import NewForm
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from .wscrapping import webscrappingMain

# Create your views here.

def index(request):
    title = "django cool"
    return render(request,"index.html",{
        "title": title
    })

def hello(request):
    return HttpResponse("<h2> hola </h2>")

def projects(request):
    projects = list(project.objects.all())
    return render(request, 'projects.html',{
        "projects": projects
    })

#@csrf_protect
@csrf_exempt
def form(request):
    if request.method == 'GET':
        return render(request, 'form.html',{
        "form" : NewForm
        })
    else:
        user=request.POST['user']
        password=request.POST['password']
        webscrappingMain(user,password)
        return HttpResponse("<h2> Se realizo con exito</h2>")
