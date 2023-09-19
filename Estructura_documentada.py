import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Guardar los datos en un archivo Excel
libro_excel = Workbook()
hoja_excel = libro_excel.active

# Escribir el encabezado en la primera fila
hoja_excel.append(['Texto N1', 'Texto N2','Src Imagenes'])


# URL de la página web que deseas analizar
url = input("URL de la página: ")

# Cadena de búsqueda para elementos N1
cadena_htmlN1 = input("Por favor, ingrese la cadena HTML 1: ")
# Cadena de búsqueda para elementos N2
cadena_htmlN2 = input("Por favor, ingrese la cadena HTML 2: ")
# Cadena de búsqueda para la imagen
cadena_imagen = input("Por favor, ingrese la cadena HTML de la imagen: ")
# Cadena de búsqueda para el botón "Siguiente"
boton_siguiente = input("Por favor, ingrese la cadena HTML del botón 'Siguiente': ")


#Numero de paginas de la web- inicio
numero_de_paginas_inicial= int(input("Por favor, ingrese el numero desde el cual se iniciara la extracion de datos (Inicio/Desde): "))
#Numero de paginas de la web- Final
numero_de_paginas_final= int(input("Por favor, ingrese el numero hasta el cual se realizara la extracion de datos  (Fin/Hasta): "))

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def Extraer_Datos():
    #La primer URl para la extracion es la que nos da el usuario:
    url_siguiente = url 
    for i in range (numero_de_paginas_inicial, numero_de_paginas_final):
        if url_siguiente:
            
            print("Pagina numero: ", i ,"URL:", url_siguiente )
            
            # Realizar una solicitud GET a la URL
            response = requests.get(url_siguiente, headers= headers)
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                # Obtener el contenido HTML de la página
                html = response.text

                # Parsear el HTML con BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')

                # Parsear las cadenas HTML proporcionadas por los usuarios
                soup_N1 = BeautifulSoup(cadena_htmlN1, 'html.parser')
                soup_N2 = BeautifulSoup(cadena_htmlN2, 'html.parser')
                soup_boton_siguiente = BeautifulSoup(boton_siguiente, 'html.parser')
                soup_img_src = BeautifulSoup(cadena_imagen, 'html.parser')

                # Buscar cualquier etiqueta que tenga la clase y obtener la clase
                etiqueta_con_clase_N1 = soup_N1.find(class_=True)
                etiqueta_con_clase_N2 = soup_N2.find(class_=True)
                etiqueta_con_clase_url_href = soup_boton_siguiente.find(class_=True)
                etiqueta_con_clase_img_src = soup_img_src.find(class_=True)

                # Puedes imprimir las clases encontradas
                if etiqueta_con_clase_N1:
                    print("Clase encontrada en HTML 1:", etiqueta_con_clase_N1['class'])
                else:
                    print("Clase no encontrada en HTML 1")

                if etiqueta_con_clase_N2:
                    print("Clase encontrada en HTML 2:", etiqueta_con_clase_N2['class'])
                else:
                    print("Clase no encontrada en HTML 2")

                if etiqueta_con_clase_img_src:
                    print("Clase encontrada en la imagen:", etiqueta_con_clase_img_src['class'])
                else:
                    print("Clase no encontrada en la imagen")

                if etiqueta_con_clase_url_href:
                    print("Clase encontrada en el botón 'Siguiente':", etiqueta_con_clase_url_href['class'])
                else:
                    print("Clase no encontrada en el botón 'Siguiente'")
                    
                if etiqueta_con_clase_N1 and etiqueta_con_clase_N2 and etiqueta_con_clase_url_href and etiqueta_con_clase_img_src: 
                    #Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento HTML N1
                    clase_obtenida_N1 = etiqueta_con_clase_N1.get('class', [])
                    clase_obtenida_N1 = ' '.join(clase_obtenida_N1)
                    print("clase obtenida N1:", clase_obtenida_N1)

                    #Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento HTML N2
                    clase_obtenida_N2 = etiqueta_con_clase_N2.get('class', [])
                    clase_obtenida_N2 = ' '.join(clase_obtenida_N2)
                    print("clase obtenida N2:", clase_obtenida_N2)

                    #Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento del boton 'Siguiente' (URLS)
                    clase_obtenida_url = etiqueta_con_clase_url_href.get('class', [])
                    clase_obtenida_url = ' '.join(clase_obtenida_url)
                    print("clase obtenida Boton 'Siguiente':", clase_obtenida_url)
                    
                    ##Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento que contiene las imagenes 'src'
                    clase_obtenida_src = etiqueta_con_clase_img_src.get('class', [])
                    clase_obtenida_src = ' '.join(clase_obtenida_src)
                    print("clase obtenida 'Imagenes':", clase_obtenida_src)
                    
                else:
                    print("Hubo un fallo obteniendo las clases")
                    break
                    
                if clase_obtenida_N1 and clase_obtenida_N2 and clase_obtenida_url and clase_obtenida_src:
                    # Encontrar todas las instancias de la clases obtenidas
                    #Clase elemento HTML N1
                    elementos_con_clase_N1 = soup.find_all(class_=clase_obtenida_N1)
                    #Clase elemento HTML N2
                    elementos_con_clase_N2 = soup.find_all(class_=clase_obtenida_N2)
                    #Clase elemento HTML URLS "Boton siguiente (URLS)"
                    elementos_con_clase_url = soup.find_all(class_=clase_obtenida_url)
                    #Clase elemento HTML de las imagenes
                    elementos_con_clase_src = soup.find_all(class_=clase_obtenida_src.split())
                else:
                    print("Hubo un fallo encontrando las clases")
                    
                #Cramos las listas necesarias:    
                #Lista donde almacenamos la data extraida
                data = []   
                #Lista para almacenar los valores 'src' de la imagenes
                src_values = []
                    
                #Hallamos todas las imagenes (Los 'src')
                # Iterar a través de los elementos con la clase
                
                if elementos_con_clase_src:
                    for elemento in elementos_con_clase_src:
                        # Obtener el valor del atributo 'src' y agregarlo a la lista
                        src = elemento.get('src')
                        if src:
                            src_values.append(src) 
                            #Imprime el valor del atributo src
                            print("Valor del atributo src:", src, "SRC Numero: ", elemento)    
                        else:
                            src_values.append('N\A')
                else:
                    print("No se encontró el 'src' en las instancias de las clases.")
                
                
                #Hallamos la siguiente pagina (URL) a la cual se le extraeran los datos
                if elementos_con_clase_url:
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
                

                # Usar zip para combinar las listas 
                for elemento, elemento2, src in zip(elementos_con_clase_N1, elementos_con_clase_N2, src_values):
                    #Extraemos el texto que se encuentre dentro de las instancias del elemento HTML N1
                    textoN1 = elemento.get_text()
                    #Extraemos el texto que se encuentre dentro de las instancias del elemento HTML N2
                    textoN2 = elemento2.get_text()

                    #Agregamos los datos a lista de data 
                    data.append([textoN1, textoN2, src])

                # Escribir los datos en las filas
                for fila in data:
                    hoja_excel.append(fila)  

                
            else:
                print("Error al obtener la página web. Código de estado:", response.status_code)

if __name__ == "__main__":
    print("Iniciando Extracion de datos")
    Extraer_Datos()
    
    
# Guardar el archivo Excel después de que el bucle haya terminado
libro_excel.save('resultados.xlsx')
print("Todos los datos se han guardado en 'resultados.xlsx'")
    
    



