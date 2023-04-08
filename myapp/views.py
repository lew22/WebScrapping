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
from selenium.webdriver.support import expected_conditions as EC


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

    # wait = WebDriverWait(driver, 10)

    #Buscamos el div con id "loginFormFields"
    form_div = driver.find_element(By.ID, "loginFormFields")

    #Buscamos el tag ul con id "loginFormList"
    form_list = form_div.find_element(By.ID, "loginFormList")

    #Buscamos los li con id user_id y password
    user_id_input = form_list.find_element(By.ID, "user_id")
    password_input = form_list.find_element(By.ID, "password")

    #Ingresamos los datos
    user_id_input.send_keys(user)
    password_input.send_keys(password)

    #Buscamos el input con id entry-login y le damos click
    login_btn = driver.find_element(By.ID, "entry-login")
    login_btn.click()

    #ahora ingresamos a los cursos
    driver.get("https://aulavirtual.upc.edu.pe/ultra/course")

    #hacemos que la pagina termine de cargar porque sino no obtiene la data 
    sleep(5)
    #Localizamos el atributo h4 con clase ... que contienen los cursos
    course_titles = driver.find_elements(By.XPATH, "//h4[@class='js-course-title-element ellipsis']")
    for i in course_titles:
        print("El elemento encontrado es: ",i.text)
    sleep(5)
    driver.quit()
    #driver.implicitly_wait(5)
    # for i in course_titles:
    #     values = i.text
    #     print("Este es el valor: ",values)

