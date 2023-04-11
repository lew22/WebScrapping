

#importamos las librerías necesarias
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

def webscrappingMain(user,password):
    # Recolectamos los cursos
    courses = webscrappingCour(user,password)
    print(courses)

    #Busqueda de carpetas por curso

def webscrappingCour(user,password):
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

    #esperamos que la pagina termine de cargar porque sino no obtiene la data 
    sleep(5)
    
    #saber que toggle esta seleccionado
    toggleA = driver.find_element(By.ID, 'square-toggle-option-one-id_2')
    toggleB = driver.find_element(By.ID, 'square-toggle-option-two-id_3')  
    
    if (toggleA.is_selected()):
        course_titles = driver.find_elements(By.XPATH, "//h4[@class='js-course-title-element ellipsis']")
    elif (toggleB.is_selected()):
        course_titles = driver.find_elements(By.XPATH, "//h4[@class='js-course-title-element']")
    
    courses = []
    #Localizamos el atributo h4 con clase ... que contienen los cursos
    for i in course_titles:
        print("El elemento encontrado es: ",i.text)
        courses.append(i.text)
    sleep(5)
    
    driver.quit()
    return courses
    #driver.implicitly_wait(5)
    # for i in course_titles:
    #     values = i.text
    #     print("Este es el valor: ",values)

