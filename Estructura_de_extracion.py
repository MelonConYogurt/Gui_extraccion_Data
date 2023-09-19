import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

 # Guardar los datos en un archivo Excel
libro_excel = Workbook()
hoja_excel = libro_excel.active

# Escribir el encabezado en la primera fila
hoja_excel.append(['Texto N1', 'Texto N2','Texto N3'])

# URL de la página web que deseas analizar
url = input("URL de la página: ")

# Cadena de búsqueda para elementos N1
cadena_html = input("Por favor, ingrese la cadena HTML 1: ")
# Cadena de búsqueda para elementos N2
cadena_html2 = input("Por favor, ingrese la cadena HTML 2: ")
# Cadena de búsqueda para la imagen
cadena_imagen = input("Por favor, ingrese la cadena HTML de la imagen: ")
# Cadena de búsqueda para el botón "Siguiente"
boton_siguiente = input("Por favor, ingrese la cadena HTML del botón 'Siguiente': ")


#Numero de paginas de la web
numero_de_paginas_inicial= int(input("Por favor, ingrese el numero desde el cual se iniciara la extracion de datos (Inicio/Desde): "))
numero_de_paginas_final= int(input("Por favor, ingrese el numero hasta el cual se realizara la extracion de datos  (Fin/Hasta): "))

#presentacion del bot a la pagina
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
        
       
def Extracion_de_datos():
    url_siguiente = url 
    for i in range (numero_de_paginas_inicial, numero_de_paginas_final):
            if url_siguiente:
                print("Procensando",i)
                
                # Realizar una solicitud GET a la URL
                response = requests.get(url_siguiente, headers=headers)

                # Verificar si la solicitud fue exitosa
                if response.status_code == 200:
                    # Obtener el contenido HTML de la página
                    html = response.text

                    # Parsear el HTML con BeautifulSoup
                    soup = BeautifulSoup(html, 'html.parser')
                    soup2 = BeautifulSoup(cadena_html, 'html.parser')
                    soup3 = BeautifulSoup(cadena_html2, 'html.parser')
                    soup4 = BeautifulSoup(boton_siguiente, 'html.parser')
                    soup5 = BeautifulSoup(cadena_imagen, 'html.parser')

                    # Buscar cualquier etiqueta que tenga la clase y obtener la clase
                    etiqueta_con_clase = soup2.find(class_=True)
                    etiqueta_con_clase2 = soup3.find(class_=True)
                    etiqueta_con_clase3 = soup4.find(class_=True)
                    etiqueta_con_clase4 = soup5.find(class_=True)
                    
                    
                    if etiqueta_con_clase and etiqueta_con_clase2:
                        
                        clase_obtenida = etiqueta_con_clase.get('class', [])
                        clase_obtenida = ' '.join(clase_obtenida)

                        clase_obtenida2 = etiqueta_con_clase2.get('class', [])
                        clase_obtenida2 = ' '.join(clase_obtenida2)

                        clase_obtenida3 = etiqueta_con_clase3.get('class', [])
                        clase_obtenida3 = ' '.join(clase_obtenida3)
                        
                        clase_obtenida4 = etiqueta_con_clase4.get('class', [])
                        clase_obtenida4 = ' '.join(clase_obtenida4)
                        
                    else:
                        print("Hubo un fallo con las clases 1 y 2")
                        break
                                            
                    # Encontrar todas las instancias de la clase "mi-clase"
                    elementos_con_clase = soup.find_all(class_=clase_obtenida)
                    elementos_con_clase2 = soup.find_all(class_=clase_obtenida2)
                    elementos_con_clase3 = soup.find_all(class_=clase_obtenida3)
                    elementos_con_clase4 = soup.find_all(class_=clase_obtenida4.split())
                    
                
                    # Crear una lista para almacenar los valores 'src'
                    src_values = []

                    # Iterar a través de los elementos con la clase
                    for elemento in elementos_con_clase4:
                        # Obtener el valor del atributo 'src' y agregarlo a la lista
                        src = elemento.get('src')
                        if src:
                            src_values.append(src)       
                            
                    if elementos_con_clase3:
                        ultimo_elemento= elementos_con_clase3[-1]
                        etiqueta_con_clase_boton_siguiente = ultimo_elemento.get('href')

                    else:
                        print("No se encontraron mas paginas")
                        break


                    #Lista donde almacenamos la data extraida
                    data = []
                    
                    
                    # Usar zip para combinar las listas en pares
                    for elemento, elemento2, src in zip(elementos_con_clase, elementos_con_clase2, src_values):
                        texto = elemento.get_text()
                        texto2 = elemento2.get_text()

                        data.append([texto, texto2,src])
                    
                    # Escribir los datos en las filas
                    for fila in data:
                        hoja_excel.append(fila)        

                    
                #Reasignación de url
                url_siguiente = etiqueta_con_clase_boton_siguiente       
            else:
                print("Error al cargar la página:", response.status_code)    
                
        


if __name__ == "__main__":
    print("Este script se está ejecutando directamente.")
    Extracion_de_datos()

    
# Guardar el archivo Excel después de que el bucle haya terminado
libro_excel.save('resultados.xlsx')
print("Todos los datos se han guardado en 'resultados.xlsx'")