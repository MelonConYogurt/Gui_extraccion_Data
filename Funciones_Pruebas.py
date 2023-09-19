import requests
import re
from bs4 import BeautifulSoup


def url_pagina_extraccion(url):
    while True:
        url_sin_revisar = url

        if url_sin_revisar:
            # Patrón de expresión regular para verificar si es una URL válida
            patron_url = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
        
            if re.match(patron_url, url_sin_revisar):
                url_verificada = url_sin_revisar
                try: 
                    # Verificación de la página
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                    }
                    
                    estado_de_url = requests.get(url_verificada, headers=headers)
                    
                    # Verifica el código de estado de la respuesta
                    if estado_de_url.status_code == 200:
                        print(f"La página está disponible '{url_verificada}' y lista para la extracción de datos.")
                        return url_verificada  # Devuelve la URL verificada para su uso posterior
                    elif estado_de_url.status_code == 404:
                        print("La página no se encontró (Error 404).")
                    elif estado_de_url.status_code == 403:
                        print("Acceso prohibido a la página (Error 403).")
                    elif estado_de_url.status_code == 500:
                        print("Error interno del servidor (Error 500).")
                    else:
                        print(f"El estado de la página es {estado_de_url.status_code}.")
                        break
                except requests.exceptions.RequestException as e:
                    print(f"Error al hacer la solicitud a la página: {e}")
                    break                   
            else:
                print("Por favor, verifique la URL ingresada. Debe comenzar con 'http', 'https' o 'ftp'.")
                break
        
def elementos_html():
    elementos = {}
    
    while True:
        clave_diccionario = input("Ingresa el nombre del elemento (HTML). De lo contrario, escribe 'aceptar' para detenerte: ")
        
        if clave_diccionario.lower() == 'aceptar':
            break
        
        valor_diccionario = input("Ingresa el elemento HTML ('Titulos' 'Precios' 'Descripcion'): ")
        
        try:
            # Intenta analizar el valor como HTML
            comprobacion_html = BeautifulSoup(valor_diccionario, 'html.parser')
            
            # Buscar cualquier etiqueta que tenga la clase y obtener la clase
            etiqueta_con_clase = comprobacion_html.find(class_=True)
            
            if etiqueta_con_clase:                
                print("Clase encontrada en el HTML:", etiqueta_con_clase['class'])
                
                #Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento HTML
                clase_obtenida = etiqueta_con_clase.get('class', [])
                clase_obtenida = ' '.join(clase_obtenida)
                print("Nombre de la case:", clase_obtenida) 
                
            else:
                print("Clase no encontrada en HTML")
            
            # Si no se genera una excepción, el valor es un elemento HTML válido
            elementos[clave_diccionario] = clase_obtenida
            print(f"Elemento '{clave_diccionario}', con valor '{clase_obtenida}', guardado con éxito.")
        except:
            # Si se genera una excepción, el valor no es un elemento HTML válido
            print(f"Fallo: '{valor_diccionario}' no es un elemento HTML válido. Verifique e ingrese de nuevo.")            
    return elementos


def imagenes_elementos_html():
    img_elementos = {}
    
    while True:
        print("Unicamente para imágenes")
        
        clave_img_elemento = input("Ingrese el nombre del elemento img. De lo contrario, escriba 'aceptar' para detenerse: ")
        
        if clave_img_elemento.lower() == 'aceptar':
            break
        
        valor_img_elemento = input("Ingrese el elemento HTML de la imagen: ")
        
        try:
            # Intenta analizar el valor como HTML
            comprobacion_html_img = BeautifulSoup(valor_img_elemento, 'html.parser')
            
            # Buscar cualquier etiqueta que tenga la clase y obtener la clase
            etiqueta_con_clase = comprobacion_html_img.find(class_=True)
            
            if etiqueta_con_clase:                
                print("Clase encontrada en el HTML:", etiqueta_con_clase['class'])
                
                #Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento HTML
                clase_obtenida = etiqueta_con_clase.get('class', [])
                clase_obtenida = ' '.join(clase_obtenida)
                print("Nombre de la case:", clase_obtenida) 
            
            # Si no se genera una excepción, el valor es un elemento HTML válido
            img_elementos[clave_img_elemento] = clase_obtenida
            print(f"Elemento '{clave_img_elemento}', con valor '{clase_obtenida}', guardado con éxito.")
            break        
        except:
            # Si se genera una excepción, el valor no es un elemento HTML válido
            print(f"Fallo: '{valor_img_elemento}' no es un elemento HTML válido. Verifique e ingrese de nuevo.")
                
    return img_elementos
    
        
def elemento_boton_siguiente():
    print("Solo si la página contiene un botón 'Siguiente' y deseas extraer datos de varias páginas. (Solo funciona para 'href')")
    
    while True:
        boton_siguiente_sin_verificar = input("Ingrese el elemento HTML del botón 'Siguiente' (ejemplo: <a href='siguiente.html'>Siguiente</a>): ")
        
        
        if boton_siguiente_sin_verificar:
            try:
                # Intenta analizar el valor como HTML
                comprobacion_html_boton = BeautifulSoup(boton_siguiente_sin_verificar, 'html.parser')
                
                # Buscar cualquier etiqueta que tenga la clase y obtener la clase
                etiqueta_con_clase = comprobacion_html_boton.find(class_=True)
                
                if etiqueta_con_clase:                
                    print("Clase encontrada en el HTML:", etiqueta_con_clase['class'])
                    
                    #Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento HTML
                    clase_obtenida = etiqueta_con_clase.get('class', [])
                    clase_obtenida = ' '.join(clase_obtenida)
                    print("Nombre de la case:", clase_obtenida) 
                
                # Si no se genera una excepción, el valor es un elemento HTML válido
                boton_siguiente_verificado = clase_obtenida
                
                if boton_siguiente_verificado:
                    print(f"Elemento '{boton_siguiente_sin_verificar}' se ha verificado como elemento HTML y guardado con éxito.")
                    
                    #inicio
                    numero_de_paginas_inicial= int(input("Ingrese el numero desde el cual se iniciara la extracion de datos ( Inicio / Desde ): "))
                    
                    #Final
                    numero_de_paginas_final= int(input("Ingrese el numero hasta el cual se realizara la extracion de datos ( Fin / Hasta ): "))
                    
                    return boton_siguiente_verificado, numero_de_paginas_inicial, numero_de_paginas_final
                
                else:
                    print("El elemento no es un enlace ('<a>') válido. Verifique e ingrese de nuevo.")
                    break
            except:
                # Si se genera una excepción, el valor no es un elemento HTML válido
                print(f"Fallo: '{boton_siguiente_sin_verificar}' no es un elemento HTML válido. Verifique e ingrese de nuevo.")
                
            
def obtener_clases():
    try:
        # lista para las clases de los elementos HTML
        Clases_obtenidas_elementos =  []
        
        # lista para las clases de los elementos HTML
        Clases_obtenidas_imagenes =  []
        
        # Recolecion de elementos HTML para los elementos:
        diccionario_elementos_html  = elementos_html()
        
        #Recorre el diccionario y agrega los valores a la lista
        if diccionario_elementos_html:
            for clave, valor in diccionario_elementos_html.items():
                Clases_obtenidas_elementos.append(valor)    
        else:
            print("No se ha inicialiado el diccionario de elementos HTML")
        
        
        # Recolecion de elementos HTML para las imagenes:
        diccionario_elementos_html_imagenes = imagenes_elementos_html()
        
        # Recorre el diccionario y agrega los valores a la lista
        if diccionario_elementos_html_imagenes:
            for clave, valor in diccionario_elementos_html_imagenes.items():
                Clases_obtenidas_imagenes.append(valor)       
        else:
            print("No se ha inicialiado el diccionario de las imagenes")
            
            
        return Clases_obtenidas_elementos, Clases_obtenidas_imagenes      
    except:
        print("No se encontraron elementos en los diccionarios")


def extraccion_de_data():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    print("Se ha iniciado la extracion de datos")
        
    #Obtenemos la url y la verificamos
    url_input = input("Ingrese la URL de la página para extraer datos: ")

    if url_input:
        url_inicial = url_pagina_extraccion(url= url_input)
    else:
        print("Error")
    
    # Llamamos la funcion que extrae las clases de los elementos y las imagenes:
    clases = obtener_clases()

    # Desempaquetamos las listas en su variable correspondientes
    etiquetas_elementos , etiquetas_imagenes = clases
    
    # Llamamos a la función elemento_boton_siguiente y almacenamos su resultado en una variable
    resultado = elemento_boton_siguiente()

    # Desempaquetamos los valores de retorno en las variables correspondientes
    clase_obtenida_boton_url, inicio_bucle, final_bucle = resultado

    if url_inicial:
        url_siguiente = url_inicial
    else:
        print("Error")
        
    if resultado:
        for i in range(inicio_bucle, final_bucle):
            if url_siguiente:
                print("Pagina numero: ", i ,"URL:", url_siguiente)
                
                # Realizar una solicitud GET a la URL
                response = requests.get(url_siguiente, headers= headers)
                if response.status_code == 200:
                    html = response.text
                    
                    #Lista para almacenar los valores 'src' de la imagenes
                    src_values = []

                    # Crea un diccionario para almacenar los elementos por clase
                    elementos_por_clase = {}
                    
                    #Lista para almacenar todo
                    data = []
                    
                    # Parsear el HTML con BeautifulSoup
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Búsqueda en las etiquetas de elementos
                    if etiquetas_elementos and etiquetas_imagenes:
                        
                        # Encontrar todas las instancias de la clases obtenidas
                        for clase in etiquetas_elementos:
                            elementos_encontrados = soup.find_all(class_=clase)
                            print(f"Elementos con clase '{clase}':")
                            elementos_por_clase[clase] = elementos_encontrados  # Guarda los elementos en el diccionario

                        # Encontrar todas las instancias de la clases obtenidas en las etiquetas de imágenes
                        for clase in etiquetas_imagenes:
                            imagenes_encontradas = soup.find_all(class_=clase.split())
                            print(f"Imágenes con clase '{clase}':")
                            for elemento in imagenes_encontradas:
                                # Obtener el valor del atributo 'src' y agregarlo a la lista
                                src = elemento.get('src')
                                if src:
                                    src_values.append(src) 
                                    #Imprime el valor del atributo src
                                    print("Valor del atributo src:", src, "SRC Numero: ", elemento)    
                                else:
                                    src_values.append('N\A')             
                    else:
                        print("No se han inicialido las clases que contienen los elementos HTMl (CLASS)")
                                          
                    #Hallamos la siguiente pagina (URL) a la cual se le extraeran los datos
                    if clase_obtenida_boton_url:
                        elementos_con_clase_url = soup.find_all(class_=clase_obtenida_boton_url)
                        #Hallamos la ultima instancia de la clase que contiene el URL de la siguiente pagina
                        ultimo_elemento= elementos_con_clase_url[-1]
                        #Una vez tomado el ultimo elemento, extraemos el 'href' que contiene la URL necesaria
                        etiqueta_con_clase_boton_siguiente = ultimo_elemento.get('href')
                        print("Siguiente pagina encontrada: ", etiqueta_con_clase_boton_siguiente)
                    
                        #Reasignación de url
                        url_siguiente = etiqueta_con_clase_boton_siguiente
                    else:
                        print("No se encontraron mas paginas")
                        break        
                else:
                    print("Error al obtener la página web. Código de estado:", response.status_code)        
            else:
                print("Error")         
    else:
        print("Error")
        
                