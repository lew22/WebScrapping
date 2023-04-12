

#importamos las librerías necesarias
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_experimental_option("detach", True)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def webscrappingMain(user,password):
    driver = webdriver.Chrome(chrome_options=options)
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
    sleep(5)
    return courses,courses_id
    #driver.implicitly_wait(5)
    # for i in course_titles:
    #     values = i.text
    #     print("Este es el valor: ",values)

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
    driver.get(linkCourses[1])
    wait = WebDriverWait(driver,10)
    #wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath("//iframe[@class='iframe_class']")))
    wait.until(EC.frame_to_be_available_and_switch_to_it("classic-learn-iframe"))
    # print(WAS)
    puller = driver.find_element(By.XPATH, "//a[@class='clickpuller']")
    print(puller)
    
    # if (puller.get_attribute('aria-expanded') == "false"):
    #     puller.click()
    # courses_content = driver.find_elements(By.XPATH, "//a[@target='self']")
    # print(courses_content)
    # for i in courses_content:
    #     print("Contenidos encontrados : ", i)

# def webscrappingFiles():
#     print (os.getcwd())