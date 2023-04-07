#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from .models import project
from django.shortcuts import render
from .forms import NewForm
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

#importamos las librerías necesarias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from time import sleep

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
        webscrapping(user,password)


def webscrapping(user,password):
    #inicializamos el driver de chrome
    driver = webdriver.Chrome()
    #abrimos la página web
    driver.get("https://aulavirtual.upc.edu.pe")

    #wait = WebDriverWait(driver, 10)

    #Busca el div con id "loginFormFields"
    form_div = driver.find_element(By.ID, "loginFormFields")

    #Busca el tag ul con id "loginFormList"
    form_list = form_div.find_element(By.ID, "loginFormList")

    #Busca los li con id user_id y password
    user_id_input = form_list.find_element(By.ID, "user_id")
    password_input = form_list.find_element(By.ID, "password")

    #Ingresa los datos
    user_id_input.send_keys(user)
    password_input.send_keys(password)

    #Busca el input con id entry-login y le das click
    login_btn = driver.find_element(By.ID, "entry-login")
    login_btn.click()

    #wait = WebDriverWait(driver, 10)
    #sleep(5)

    # Cuando cargue la pagina busca un tag section con class show-for-medium-down y dale click
    section_tag = driver.find_element(By.CLASS_NAME, "show-for-medium-down")
    section_tag.click()

    #Luego identifica un tag a con con class "base-navigation-button-content themed-background-primary-alt-fill-only theme-border-left-active" y href "https://aulavirtual.upc.edu.pe/ultra/course"
    a_tag = driver.find_element(By.CSS_SELECTOR, ".base-navigation-button-content.themed-background-primary-alt-fill-only.theme-border-left-active[href='https://aulavirtual.upc.edu.pe/ultra/course']")
    a_tag.click()

    sleep(5)

