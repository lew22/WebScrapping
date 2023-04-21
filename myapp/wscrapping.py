
#importamos las librerías necesarias
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import os
import shutil
import glob
from selenium.webdriver.chrome.options import Options
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : 'C:\\Users\pc\Desktop\Descargas'}
chrome_options.add_experimental_option('prefs',prefs)
chromedriver = "C:\\Users\pc\Documents\djangoproject\chromedriver.exe"
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=chrome_options)

def webscrappingMain(user,password):
    #abrimos la página web
    driver.get("https://aulavirtual.upc.edu.pe")
    
    #Recolectamos los cursos
    courses,courses_id= webscrappingCour(user,password,driver)

    #Probando contenido de cursos
    webscrappingCourCont(courses_id,driver)

def webscrappingCour(user,password,driver):
    #inicializamos el driver de chrome
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

    #esperamos que la pagina termine de cargar porque sino no obtiene la data 
    sleep(5)
    #saber que toggle esta seleccionado
    toggleA = driver.find_element(By.ID, 'square-toggle-option-one-id_2')
    toggleB = driver.find_element(By.ID, 'square-toggle-option-two-id_3')

    #Localizamos el atributo h4 con clase ... que contienen los cursos
    if (toggleA.is_selected()):
        course_titles = driver.find_elements(By.XPATH, "//h4[@class='js-course-title-element ellipsis']")
        course_id = driver.find_elements(By.XPATH, "//a[@class='course-title ellipsis hide-focus-outline large-10 medium-10 small-12']") 
    elif (toggleB.is_selected()):
        course_titles = driver.find_elements(By.XPATH, "//h4[@class='js-course-title-element']")
        course_id = driver.find_elements(By.XPATH, "//a[@class='course-title ellipsis hide-focus-outline large-10 medium-10 small-12']") 

    #Guardamos los cursos encontrados
    courses = []
    for i in course_titles:
        print("Curso encontrado : ",i.text)
        courses.append(i.text)
    
    #Guardamos los id de los cursos
    courses_id = []
    for i in course_id:
        #Limpiando id
        aux = i.get_attribute('id')
        id_clean = aux.replace('course-link-','')
        print("El id del curso es: ",id_clean)
        courses_id.append(id_clean)
    
    return courses,courses_id

def webscrappingCourCont(courses_id,driver):
    lbase = "https://aulavirtual.upc.edu.pe/ultra/courses/"
    lend = "/cl/outline"
    lcourse = ""
    linkCourses = []
    for i in courses_id:
        lcourse = lbase+i+lend
        print("El link del curso: ", lcourse)
        linkCourses.append(lcourse)
    
    #abrimos una pagina de cada curso y realizamos la lectura
    # driver.get(linkCourses[1])
    driver.maximize_window()
    curso = "https://aulavirtual.upc.edu.pe/webapps/blackboard/content/listContent.jsp?course_id=_367607_1&content_id=_39746882_1&mode=reset"
    path =  "C:\\Users\pc\Desktop\Curso"
    depth = 2
    scrape_page(curso,path,depth)

def scrape_page(url, folder_path,depth):
    
    if depth == 0:
        return
    
    driver.get(url)
    # Crear la carpeta para guardar los archivos descargados (si no existe)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    links = driver.find_elements(By.XPATH, "//div[@class='item clearfix']//h3//a")
    titleHeaderPager = driver.find_element(By.XPATH, "//h1[@id='pageTitleHeader']//span[@id='pageTitleText']")

    path_downloads = "C:\\Users\pc\Desktop\Descargas"
    newfolder= folder_path + "\\" + titleHeaderPager.text
    if not os.path.exists(newfolder):
        os.mkdir(newfolder)

    for link in links:
        # print("Href encontrado: ",link.get_attribute('href'))
        # Si onclick no es nulo, es un archivo que se puede descargar
        if link.get_attribute('onclick') is not None:
            href = link.get_attribute('href')
            driver.get(href)
            sleep(1)
            # Busca todos los archivos con extensiones .doc, .exe y .pdf en la carpeta original
            extensiones = ['doc','docx', 'exe', 'pdf','pptx']
            archivos = []
            for extension in extensiones:
                archivos.extend(glob.glob(os.path.join(path_downloads, f"*.{extension}")))

            for archivo in archivos:
                ruta_archivo_destino = os.path.join(newfolder, os.path.basename(archivo))
                if os.path.exists(ruta_archivo_destino):
                    print(f"El archivo {ruta_archivo_destino} ya existe en la carpeta de destino")
                    os.remove(archivo)
                else:
                    shutil.move(archivo, ruta_archivo_destino)
                    #os.remove(archivo)
        # Si el enlace es una página, llamar a la función de scraping nuevamente
        elif link.get_attribute('href').startswith('https://aulavirtual.upc.edu.pe/webapps/'):
            href = link.get_attribute('href')
            # print("Es un enlace que me lleva a otra pagina \n",href)
            # next_folder_path = os.path.join(folder_path, os.path.basename(href))
            # link.click()
            sleep(1)
            scrape_page(href, newfolder ,depth-1)
            sleep(1)
            driver.get(url)