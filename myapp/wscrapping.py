
#importamos las librerías necesarias
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import os
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
    path =  "C:\\Users\pc\Desktop\Descargas"
    depth = 3
    scrape_page(curso,path,depth)
    
    # sleep(3)
    #Guardamos la ventana de los items de un curso
    # original_window = driver.current_window_handle

    #verificamos que solo tengamos una ventana abierta
    # assert len(driver.window_handles) == 1

    # wait = WebDriverWait(driver,10)
    # wait.until(EC.frame_to_be_available_and_switch_to_it("classic-learn-iframe"))

    # sleep(5)

    # #verificaremos si el puller esta expandido o contraido
    # menupullercollapse = driver.find_element(By.XPATH, "//a[@aria-expanded='false']")
    # menupullerexpanded = driver.find_element(By.XPATH, "//a[@aria-expanded='true']")

    # if (menupullercollapse is not None):
    #     menupullercollapse.click()
    # if (menupullerexpanded is not None):
    #     print("puller expandido")

    #ahora buscamos un ul que tenga li's y los guardamos
    # menucontent = driver.find_elements(By.XPATH, "//ul[@id='courseMenuPalette_contents']//li[@class='clearfix ']//a")
    
    # for i in menucontent:
    #     span = i.find_element(By.TAG_NAME,'span')
    #     span.get_attribute('title')
    #     i.get_attribute('href')
    #     # i.click()
    # print(data)


def scrape_page(url, folder_path,depth):
    
    if depth == 0:
        return
    
    driver.get(url)
    # Crear la carpeta para guardar los archivos descargados (si no existe)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for link in links:
        href = link.get_attribute('href')
        onclick = link.get_attribute('onclick')

        links = driver.find_elements(By.XPATH, "//h3//a")

        # Si onclick no es nulo, es un archivo que se puede descargar
        if onclick is not None:
            response = requests.get(href)
            filename = os.path.join(folder_path, os.path.basename(href))
            with open(filename, 'wb') as f:
                f.write(response.content)

        # Si el enlace es una página, llamar a la función de scraping nuevamente
        elif href.startswith('/webapps/'):
            next_folder_path = os.path.join(folder_path, os.path.basename(href))
            scrape_page(href, next_folder_path,depth-1)

