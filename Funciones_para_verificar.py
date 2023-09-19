import requests
import re
from bs4 import BeautifulSoup
from tkinter import messagebox

def url_pagina_extraccion(url):
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
                        mensaje = f"La página está disponible '{url_verificada}' y lista para la extracción de datos."
                        messagebox.showinfo("Información", mensaje)
                        return url_verificada  # Devuelve la URL verificada para su uso posterior
                    elif estado_de_url.status_code == 404:
                        messagebox.showerror("Error", "La página no se encontró (Error 404).")
                    elif estado_de_url.status_code == 403:
                        messagebox.showerror("Error", "Acceso prohibido a la página (Error 403).")
                    elif estado_de_url.status_code == 500:
                        messagebox.showerror("Error", "Error interno del servidor (Error 500).")
                    else:
                        mensaje = f"El estado de la página es {estado_de_url.status_code}."
                        messagebox.showwarning("Advertencia", mensaje)   
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"Error al hacer la solicitud a la página: {e}")                     
            else:
                messagebox.showerror("Error", "Por favor, verifique la URL ingresada. Debe comenzar con 'http', 'https' o 'ftp'.")
                
        
def elementos_html(Elemento_Html):
    try:
        # Intenta analizar el valor como HTML
        comprobacion_html = BeautifulSoup(Elemento_Html, 'html.parser')
        
        # Buscar cualquier etiqueta que tenga la clase y obtener la clase
        etiqueta_con_clase = comprobacion_html.find(class_=True)
        
        if etiqueta_con_clase:                
            clase_obtenida = etiqueta_con_clase.get('class', [])
            clase_obtenida = ' '.join(clase_obtenida)
            
            mensaje = f"Clase encontrada en el HTML: {clase_obtenida}\nNombre de la clase: {clase_obtenida}\nElemento HTML verificado con éxito."
            messagebox.showinfo("Información", mensaje)
            
        else:
            messagebox.showwarning("Advertencia", "Clase no encontrada en HTML")
        
    except:
        messagebox.showerror("Error", "Fallo: No es un elemento HTML válido. Verifique e ingrese de nuevo.")           


def imagenes_elementos_html(Elemento_html_img):
    try:
        # Intenta analizar el valor como HTML
        comprobacion_html_img = BeautifulSoup(Elemento_html_img, 'html.parser')
        
        # Buscar cualquier etiqueta que tenga la clase y obtener la clase
        etiqueta_con_clase = comprobacion_html_img.find(class_=True)
        
        if etiqueta_con_clase:                
            clase_obtenida = etiqueta_con_clase.get('class', [])
            clase_obtenida = ' '.join(clase_obtenida)
            
            mensaje = f"Clase encontrada en el HTML: {clase_obtenida}\nNombre de la clase: {clase_obtenida}\nElemento HTML verificado y guardado con éxito."
            messagebox.showinfo("Información", mensaje)
            
        else:
            messagebox.showwarning("Advertencia", "Clase no encontrada en HTML")
        
    except:
        messagebox.showerror("Error", "Fallo: No es un elemento HTML válido. Verifique e ingrese de nuevo.")
    
    
        
def elemento_boton_siguiente(Elemento_boton):
    if Elemento_boton:
        try:
            # Intenta analizar el valor como HTML
            comprobacion_html_boton = BeautifulSoup(Elemento_boton, 'html.parser')
            
            # Buscar cualquier etiqueta que tenga la clase y obtener la clase
            etiqueta_con_clase = comprobacion_html_boton.find(class_=True)
            
            if etiqueta_con_clase:                
                clase_obtenida = etiqueta_con_clase.get('class', [])
                clase_obtenida = ' '.join(clase_obtenida)
                
                mensaje = f"Clase encontrada en el HTML: {clase_obtenida}\nNombre de la clase: {clase_obtenida}\nElemento HTML verificado y guardado con éxito."
                messagebox.showinfo("Información", mensaje)
                
            else:
                messagebox.showwarning("Advertencia", "Clase no encontrada en HTML")
            
        except:
            messagebox.showerror("Error", "Fallo: No es un elemento HTML válido. Verifique e ingrese de nuevo.")
    else:
        messagebox.showwarning("Advertencia", "El elemento no contiene HTML válido.")
                
            