import matplotlib.pyplot as plt
import customtkinter
import threading
import requests
import logging
import shutil
import re
import os
from tkinter import ttk
from ctk_tooltip import *
from ctk_rangeslider import *
from datetime import datetime
from openpyxl import Workbook
from bs4 import BeautifulSoup
from tkinter import filedialog
from urllib.parse import urljoin
from urllib.parse import urlparse
from screeninfo import get_monitors
from matplotlib.figure import Figure
from CTkMessagebox import CTkMessagebox
from BaseDeDatosExtracion import Data_Extraida, session, func
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Obtén la lista de monitores
        monitors = get_monitors()

        if len(monitors) >= 2:
            # Si hay al menos dos monitores, utiliza el segundo monitor
            second_monitor = monitors[1]
            self.geometry(f"{second_monitor.width}x{second_monitor.height}+{second_monitor.x}+{second_monitor.y}")
        else:
            pantalla_principal = monitors[0]
            self.geometry(f"{pantalla_principal.width}x{pantalla_principal.height}")
            
        # Configuramos la ventana principal self
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        self.title("Scrap")
        
        # Frame base para todos los demás frames    
        self.frame_base = customtkinter.CTkScrollableFrame(master=self, fg_color="#242424")
        self.frame_base.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")

        # Configuración de las columnas de frame_base para que ocupen todo el ancho
        self.frame_base.grid_columnconfigure(0, weight=1)
        self.frame_base.grid_columnconfigure(1, weight=1)

        # Creación de los frames principales
        self.frame_titulo_arriba = customtkinter.CTkFrame(self.frame_base, height=100)
        self.frame_titulo_arriba.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.frame_medio_izquierda = customtkinter.CTkFrame(self.frame_base)
        self.frame_medio_izquierda.grid(row=1, column=0, padx=5, pady=20, sticky="nsew")

        self.frame_medio_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_medio_derecha.grid(row=1, column=1, padx=5, pady=20, sticky="nsew")

        self.frame_intermedio_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_intermedio_derecha.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        self.frame_medio_bajo_izquierda = customtkinter.CTkFrame(self.frame_base)
        self.frame_medio_bajo_izquierda.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_medio_bajo_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_medio_bajo_derecha.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        self.frame_medio_bajo_titulo = customtkinter.CTkFrame(self.frame_base)
        self.frame_medio_bajo_titulo.grid(row=4, column=0, columnspan=2, padx=5, pady=20, sticky="nsew")

        self.frame_bajo_izquierda = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_izquierda.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_bajo_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_derecha.grid(row=5, column=1, padx=5, pady=5, sticky="nsew") 
        
        self.frame_bajo_izquierda_N2 = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_izquierda_N2.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_bajo_derecha_N2 = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_derecha_N2.grid(row=6, column=1, padx=5, pady=5, sticky="nsew") 
        
        self.frame_bajo_derecha_NP = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_derecha_NP.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_bajo_derecha_NP_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_derecha_NP_derecha.grid(row=7, column=1, padx=5, pady=5, sticky="nsew") 
        
        self.frame_medio_bajo_titulo_numero2 = customtkinter.CTkFrame(self.frame_base)
        self.frame_medio_bajo_titulo_numero2.grid(row=8, column=0, columnspan=2, padx=5, pady=20, sticky="nsew")
        
        self.frame_bajo_izquierda_N3 = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_izquierda_N3.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_bajo_derecha_N3 = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_derecha_N3.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")
        
        self.frame_medio_bajo_titulo_numero3 = customtkinter.CTkFrame(self.frame_base)
        self.frame_medio_bajo_titulo_numero3.grid(row=10, column=0, columnspan=2, padx=5, pady=20, sticky="nsew")
        
        self.frame_bajo_izquierda_N4 = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_izquierda_N4.grid(row=11, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_bajo_derecha_N4 = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_derecha_N4.grid(row=11, column=1, padx=5, pady=5, sticky="nsew")
        
        self.frame_bajo_izquierda_N5 = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_izquierda_N5.grid(row=12, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_bajo_derecha_N5 = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_derecha_N5.grid(row=12, column=1, padx=5, pady=5, sticky="nsew")
        
        self.frame_semi_bajo = customtkinter.CTkFrame(self.frame_base)
        self.frame_semi_bajo.grid(row=13, column=0, columnspan=2,padx=5, pady=20, sticky="nsew")
        
        self.frame_bajo = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo.grid(row=14, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_bajo_N1_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_N1_derecha.grid(row=14, column=1, padx=5, pady=5, sticky="nsew")   
        
        self.frame_bajo_N2 = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_N2.grid(row=15, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_bajo_N2_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_bajo_N2_derecha.grid(row=15, column=1, padx=5, pady=5, sticky="nsew")          
        
        self.frame_funciones_bajo = customtkinter.CTkFrame(self.frame_base)
        self.frame_funciones_bajo.grid(row=16, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_funciones_bajo_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_funciones_bajo_derecha.grid(row=16, column=1, padx=5, pady=5, sticky="nsew")
        
        self.frame_funciones_bajo_N2 = customtkinter.CTkFrame(self.frame_base)
        self.frame_funciones_bajo_N2.grid(row=17, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_funciones_bajo_N2_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_funciones_bajo_N2_derecha.grid(row=17, column=1, padx=5, pady=5, sticky="nsew")
        
        self.frame_resumen = customtkinter.CTkFrame(self.frame_base)
        self.frame_resumen.grid(row=18, column=0, padx=5, pady=5, sticky="nsew") 
        
        self.frame_resumen_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_resumen_derecha.grid(row=18, column=1, padx=5, pady=5, sticky="nsew") 
        
        self.frame_imagenes = customtkinter.CTkFrame(self.frame_base)
        self.frame_imagenes.grid(row=19, column=0, padx=5, pady=5, sticky="nsew") 
        
        self.frame_imagenes_derecha = customtkinter.CTkFrame(self.frame_base)
        self.frame_imagenes_derecha.grid(row=19, column=1, padx=5, pady=5, sticky="nsew") 
    
    
       # Labels dentro de los frames principales      
        self.app_title = customtkinter.CTkLabel(self.frame_titulo_arriba, text="Data Extraction Focused on CSS Classes and HTML Elements",
                                                font=customtkinter.CTkFont(size=23, weight="bold"))
        self.app_title.pack(padx=10, pady=10)

        self.extraction_title = customtkinter.CTkLabel(self.frame_intermedio_derecha, text="Please complete the following details to start the extraction process",
                                                        font=customtkinter.CTkFont(size=20, weight="bold"))
        self.extraction_title.pack(padx=10, pady=10)

        self.description_title = customtkinter.CTkLabel(self.frame_medio_izquierda,
                                                        text="Description",
                                                        font=customtkinter.CTkFont(size=18, weight="bold"))
        self.description_title.pack(side="top", padx=(5, 5), pady=(5, 5))

        self.description = customtkinter.CTkLabel(self.frame_medio_izquierda,
                                                text="This application has been developed to extract data from various websites that use CSS classes.\nThis allows us to obtain the desired information through the corresponding HTML elements.",
                                                font=customtkinter.CTkFont(size=13, weight="normal"))
        self.description.pack(padx=(10, 15), pady=(10, 10))

        self.warning_title = customtkinter.CTkLabel(self.frame_medio_derecha,
                                                    text="Warning",
                                                    font=customtkinter.CTkFont(size=18, weight="bold"))
        self.warning_title.pack(side="top", padx=(5, 5), pady=(5, 5))

        self.warning = customtkinter.CTkLabel(self.frame_medio_derecha,
                                            text="The extraction of data and any resulting processing is your own responsibility,\nas we do not have the necessary permissions from the respective websites.",
                                            font=customtkinter.CTkFont(size=13, weight="normal"))
        self.warning.pack(padx=(10, 15), pady=(10, 10))

        self.info_label = customtkinter.CTkLabel(self.frame_medio_bajo_titulo,
                                                text="Once you have verified your page, complete the fields with your HTML elements")
        self.info_label.pack(side="left", padx=10, pady=10)

        self.url_label = customtkinter.CTkLabel(self.frame_medio_bajo_izquierda,
                                                text="Please provide a web address so we can check its functionality:")
        self.url_label.pack(side="left", padx=10, pady=10)

        self.first_html_element_label = customtkinter.CTkLabel(self.frame_bajo_izquierda,
                                                            text="Please enter the first HTML element you want to extract:")
        self.first_html_element_label.pack(side="left", padx=10, pady=10)

        self.second_html_element_label = customtkinter.CTkLabel(self.frame_bajo_izquierda_N2,
                                                                text="Please enter the second HTML element you want to extract:")
        self.second_html_element_label.pack(side="left", padx=10, pady=10)

        self.href_element_label = customtkinter.CTkLabel(self.frame_bajo_derecha_NP,
                                                        text="Please enter the href element you want to extract:")
        self.href_element_label.pack(side="left", padx=10, pady=10)

        self.image_extraction_info_label = customtkinter.CTkLabel(self.frame_medio_bajo_titulo_numero2,
                                                                text="To extract images, provide the HTML element of an image (Only the 'src' will be retrieved)")
        self.image_extraction_info_label.pack(side="left", padx=10, pady=10)

        self.image_element_label = customtkinter.CTkLabel(self.frame_bajo_izquierda_N3,
                                                        text="Please enter the HTML element of the image you want to extract:")
        self.image_element_label.pack(side="left", padx=10, pady=10)

        self.next_button_label = customtkinter.CTkLabel(self.frame_bajo_izquierda_N4,
                                                        text="Please enter the HTML element of the 'next' button for extraction:")
        self.next_button_label.pack(side="left", padx=10, pady=10)

        self.full_extraction_info_label = customtkinter.CTkLabel(self.frame_medio_bajo_titulo_numero3,
                                                                text="To perform the full extraction, you need to provide the HTML element of the next button")
        self.full_extraction_info_label.pack(side="left", padx=10, pady=10)

        self.page_range_label = customtkinter.CTkLabel(self.frame_bajo_izquierda_N5,
                                                    text="Please specify from which page to which page you want to perform the extraction:")
        self.page_range_label.pack(side="left", padx=10, pady=10)

        self.functions_label = customtkinter.CTkLabel(self.frame_semi_bajo,
                                                    text="Now, you can proceed with the extraction and have various functions at your disposal:")
        self.functions_label.pack(side="left", padx=10, pady=10)

        self.data_proceed_label = customtkinter.CTkLabel(self.frame_bajo,
                                                        text="If you have completed all fields and verified the information, you can proceed with the extraction")
        self.data_proceed_label.pack(side="left", padx=10, pady=10)

        self.export_txt_label = customtkinter.CTkLabel(self.frame_bajo_N2,
                                                    text="You have the option to export the log of the last extraction as a text file (.txt)")
        self.export_txt_label.pack(side="left", padx=10, pady=10)

        self.export_db_label = customtkinter.CTkLabel(self.frame_funciones_bajo,
                                                    text="If you have already performed the extraction, you have the option to export a copy of the database")
        self.export_db_label.pack(side="left", padx=10, pady=10)

        self.clear_data_label = customtkinter.CTkLabel(self.frame_funciones_bajo_N2,
                                                    text="If you want to perform a new extraction, we recommend clearing the data beforehand:")
        self.clear_data_label.pack(side="left", padx=10, pady=10)

        self.summary_label = customtkinter.CTkLabel(self.frame_resumen,
                                                    text="If you want, you can view a summary of the entire process, including data and graphics:")
        self.summary_label.pack(side="left", padx=10, pady=10)

        self.download_images_label = customtkinter.CTkLabel(self.frame_imagenes,
                                                            text="If you want, you can download the images from your last extraction:")
        self.download_images_label.pack(side="left", padx=10, pady=10)

        
        
           
        #Entry y botones Y demas widgets dentro de los frames principales    
        self.confirmar_url_pagina = customtkinter.CTkEntry(self.frame_medio_bajo_derecha,
                                                   width=900, placeholder_text="Web Page")
        self.confirmar_url_pagina.grid(row=0, column=0, padx=10, pady=10)

        self.obtener_url_usuario = customtkinter.CTkButton(self.frame_medio_bajo_derecha, text="Verify", width=90,
                                                        command=lambda: self.url_pagina_extraccion())
        self.obtener_url_usuario.grid(row=0, column=1, padx=10, pady=10)

        self.verificasion_switch_url = customtkinter.CTkSwitch(self.frame_medio_bajo_derecha, width=90, text="Not Verified",
                                                                onvalue="on", offvalue="off", progress_color="#1f6aa5", state="disabled")
        self.verificasion_switch_url.grid(row=0, column=2, padx=10, pady=10)

        self.elementos_pagina_html_N1 = customtkinter.CTkEntry(self.frame_bajo_derecha,
                                                            width=900, placeholder_text="First <HTML> Element")
        self.elementos_pagina_html_N1.grid(row=0, column=0, padx=10, pady=10)

        self.Verificar_N1 = customtkinter.CTkButton(self.frame_bajo_derecha, text="Verify", width=90,
                                                    command=lambda: self.elementos_html_N1())
        self.Verificar_N1.grid(row=0, column=1, padx=10, pady=10)

        self.verificasion_switch_N1 = customtkinter.CTkSwitch(self.frame_bajo_derecha, width=90, text="Not Verified",
                                                            onvalue="on", offvalue="off", progress_color="#1f6aa5", state="disabled")
        self.verificasion_switch_N1.grid(row=0, column=2, padx=10, pady=10)

        self.elementos_pagina_html_N2 = customtkinter.CTkEntry(self.frame_bajo_derecha_N2,
                                                            width=900, placeholder_text="Second <HTML> Element")
        self.elementos_pagina_html_N2.grid(row=0, column=0, padx=10, pady=10)

        self.Verificar_N2 = customtkinter.CTkButton(self.frame_bajo_derecha_N2, text="Verify", width=90,
                                                    command=lambda: self.elementos_html_N2())
        self.Verificar_N2.grid(row=0, column=1, padx=10, pady=10)

        self.verificasion_switch_N2 = customtkinter.CTkSwitch(self.frame_bajo_derecha_N2, width=90, text="Not Verified",
                                                            onvalue="on", offvalue="off", progress_color="#1f6aa5", state="disabled")
        self.verificasion_switch_N2.grid(row=0, column=2, padx=10, pady=10)

        self.Url_pagina_producto = customtkinter.CTkEntry(self.frame_bajo_derecha_NP_derecha,
                                                        width=900, placeholder_text="Third <HREF> Element for Products")
        self.Url_pagina_producto.grid(row=0, column=0, padx=10, pady=10)

        self.Verificar_url_producto = customtkinter.CTkButton(self.frame_bajo_derecha_NP_derecha, text="Verify", width=90,
                                                            command=lambda: self.elementos_html_N2())
        self.Verificar_url_producto.grid(row=0, column=1, padx=10, pady=10)

        self.Verificar_url_producto_switch = customtkinter.CTkSwitch(self.frame_bajo_derecha_NP_derecha, width=90, text="Not Verified",
                                                                    onvalue="on", offvalue="off", progress_color="#1f6aa5", state="disabled")
        self.Verificar_url_producto_switch.grid(row=0, column=2, padx=10, pady=10)

        self.elementos_pagina_html_N3 = customtkinter.CTkEntry(self.frame_bajo_derecha_N3,
                                                            width=900, placeholder_text="<HTML> Element for Images")
        self.elementos_pagina_html_N3.grid(row=0, column=0, padx=10, pady=10)

        self.Verificar_N3 = customtkinter.CTkButton(self.frame_bajo_derecha_N3, text="Verify", width=90,
                                                    command=lambda: self.imagenes_elementos_html())
        self.Verificar_N3.grid(row=0, column=1, padx=10, pady=10)

        self.verificasion_switch_N3 = customtkinter.CTkSwitch(self.frame_bajo_derecha_N3, width=90, text="Not Verified",
                                                            onvalue="on", offvalue="off", progress_color="#1f6aa5", state="disabled")
        self.verificasion_switch_N3.grid(row=0, column=2, padx=10, pady=10)

        self.elementos_pagina_html_N4 = customtkinter.CTkEntry(self.frame_bajo_derecha_N4,
                                                            width=900, placeholder_text="<HTML> Element for 'Next' Button")
        self.elementos_pagina_html_N4.grid(row=0, column=0, padx=10, pady=10)

        self.Verificar_N4 = customtkinter.CTkButton(self.frame_bajo_derecha_N4, text="Verify", width=90,
                                                    command=lambda: self.elemento_boton_siguiente())
        self.Verificar_N4.grid(row=0, column=1, padx=10, pady=10)

        self.verificasion_switch_N4 = customtkinter.CTkSwitch(self.frame_bajo_derecha_N4, width=90, text="Not Verified",
                                                            onvalue="on", offvalue="off", progress_color="#1f6aa5", state="disabled")
        self.verificasion_switch_N4.grid(row=0, column=2, padx=10, pady=10)

        def show_value(value):
            valor_1 = int(value[0])
            valor_2 = int(value[1])
            self.tooltip_1.configure(message=f"From: {valor_1}, To: {valor_2}")

        self.Rango_slider_paginas = CTkRangeSlider(self.frame_bajo_derecha_N5, from_=1, to=200, command=show_value)
        self.Rango_slider_paginas.pack(fill="both", padx=15, pady=(15, 10))

        self.tooltip_1 = CTkToolTip(self.Rango_slider_paginas, message="From: 1, To: 200")

        self.Boton_extraer_Data = customtkinter.CTkButton(self.frame_bajo_N1_derecha, text="Start Extraction",
                                                        command=lambda: self.Hilo_extraccion_de_data(), width=135)
        self.Boton_extraer_Data.pack(side="right", padx=(10, 30), pady=10)

        self.Barrra_de_carga = customtkinter.CTkProgressBar(self.frame_bajo_N1_derecha, width=1000, orientation="horizontal", mode="indeterminate")
        self.Barrra_de_carga.pack(side="left", padx=(30, 10), pady=10)

        self.Boton_exportar_data = customtkinter.CTkButton(self.frame_bajo_N2_derecha, text="Export Log",
                                                        command=lambda: self.exportar_registro(), width=135)
        self.Boton_exportar_data.pack(side="right", padx=(10, 30), pady=10)

        self.Barrra_de_carga_exportacion = customtkinter.CTkProgressBar(self.frame_bajo_N2_derecha, width=1000, orientation="horizontal", mode="indeterminate")
        self.Barrra_de_carga_exportacion.pack(side="left", padx=(30, 10), pady=10)

        self.Boton_exportar_dataBase = customtkinter.CTkButton(self.frame_funciones_bajo_derecha, text="Export Database",
                                                            command=lambda: self.exportar_data_base(), width=135)
        self.Boton_exportar_dataBase.pack(side="right", padx=(10, 30), pady=10)

        self.Barrra_de_carga_exportacion_data_base = customtkinter.CTkProgressBar(self.frame_funciones_bajo_derecha, width=1000, orientation="horizontal", mode="indeterminate")
        self.Barrra_de_carga_exportacion_data_base.pack(side="left", padx=(30, 10), pady=10)

        self.Boton_limpiar_data = customtkinter.CTkButton(self.frame_funciones_bajo_N2_derecha, text="Clear Logs",
                                                        command=lambda: self.limpiar_data_todo(), width=135)
        self.Boton_limpiar_data.pack(side="right", padx=(10, 30), pady=10)

        self.Barrra_de_carga_limpiar_data = customtkinter.CTkProgressBar(self.frame_funciones_bajo_N2_derecha, width=1000, orientation="horizontal", mode="indeterminate")
        self.Barrra_de_carga_limpiar_data.pack(side="left", padx=(30, 10), pady=10)

        self.Boton_descargar_resumen = customtkinter.CTkButton(self.frame_resumen_derecha, text="Show Summary",
                                                            command=lambda: self.resumen_extracion(), width=135)
        self.Boton_descargar_resumen.pack(side="right", padx=(10, 30), pady=10)

        self.Barrra_de_carga_resumen = customtkinter.CTkProgressBar(self.frame_resumen_derecha, width=1000, orientation="horizontal", mode="indeterminate")
        self.Barrra_de_carga_resumen.pack(side="left", padx=(30, 10), pady=10)

        self.Boton_descargar_imagenes = customtkinter.CTkButton(self.frame_imagenes_derecha, text="Download Images",
                                                                command=lambda: self.Hilo_descarga_de_imagenes(), width=135)
        self.Boton_descargar_imagenes.pack(side="right", padx=(10, 30), pady=10)

        self.Barrra_de_carga_funciones = customtkinter.CTkProgressBar(self.frame_imagenes_derecha, width=1000, orientation="horizontal", mode="indeterminate")
        self.Barrra_de_carga_funciones.pack(side="left", padx=(30, 10), pady=10)
        
    def extracion_de_datos_entry(self):            
        # Listas para almacenar el tiempo y el tamaño de respuesta de cada solicitud de red
        self.tiempos_respuesta = []
        self.tamanos_respuesta = []
        
        #Iniciamos un log para guardar toda la data que sera extraida
        logging.basicConfig(filename='data_extraida.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Guardar los datos en un archivo Excel
        libro_excel = Workbook()
        hoja_excel = libro_excel.active

        # Escribir el encabezado en la primera fila
        hoja_excel.append(['Texto N1', 'Texto N2','Src Imagenes','URL del producto'])
        
        #Obtenemos La URL
        url = self.confirmar_url_pagina.get()
        #Obtnemos los elementos <HTML>
        cadena_htmlN1 = self.elementos_pagina_html_N1.get()
        cadena_htmlN2 = self.elementos_pagina_html_N2.get()
        cadena_html_productos= self.Url_pagina_producto.get()
        #Obtenemos el elemento <HTML> de las imagenes
        cadena_imagen = self.elementos_pagina_html_N3.get()
        #Obtenemos el elemento <HTML del boton siguiente>
        boton_siguiente = self.elementos_pagina_html_N4.get()
     
        
        valor = self.Rango_slider_paginas.get()
        valor_1_slider= int(valor[0])
        valor_2_slider= int(valor[1])
        
        #Proporsionamos informacion de la solicitud HTTP para reducir los fallos
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":
                    "gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":
                    "close", "Upgrade-Insecure-Requests":"1"
                    }
        
        #La primer URl para la extracion es la que nos da el usuario:
        url_siguiente = url 
        
        # Registra la fecha y hora de inicio
        self.inicio = datetime.now()   
        
        try:
            #Iniciamos la proggressbar antes del ciclo
            self.Barrra_de_carga.start()
            #Empezamos la extracion para la cantidad de paginas requeridas por el usuario
            for i in range (valor_1_slider, valor_2_slider+1):
                if url_siguiente:
                    try:
                        #Iniciamos con el primer logging del .log
                        logging.info("Pagina numero: %s URL: %s", i, url_siguiente)
                       
                        # Realizar una solicitud GET a la URL
                        response = requests.get(url_siguiente, headers= headers)
                        
                        # Registrar el tiempo de respuesta y el tamaño de la respuesta
                        self.tiempo_respuesta = response.elapsed.total_seconds()  # Tiempo en segundos
                        self.tamaño_respuesta = len(response.content) / 1024  # Tamaño en kilobytes
                        self.tiempos_respuesta.append(self.tiempo_respuesta)
                        self.tamanos_respuesta.append(self.tamaño_respuesta)
                        
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
                            soup_href_productos = BeautifulSoup(cadena_html_productos, 'html.parser')
                            soup_img_src = BeautifulSoup(cadena_imagen, 'html.parser')

                            # Buscar cualquier etiqueta que tenga la clase y obtener la clase
                            etiqueta_con_clase_N1 = soup_N1.find(class_=True)
                            etiqueta_con_clase_N2 = soup_N2.find(class_=True)
                            etiqueta_con_clase_url_href = soup_boton_siguiente.find(class_=True)
                            etiqueta_con_clase_productos_href = soup_href_productos.find(class_=True)
                            etiqueta_con_clase_img_src = soup_img_src.find(class_=True)

                            # registrar las clases encontradas
                            if etiqueta_con_clase_N1:
                                self.claseN1 =etiqueta_con_clase_N1['class']
                                logging.info("Clase encontrada en HTML 1: %s", etiqueta_con_clase_N1['class'])
                            else:
                                self.claseN1 = "Clase no encontrada"
                                logging.info("Clase no encontrada en HTML 1")

                            if etiqueta_con_clase_N2:
                                self.claseN2 =etiqueta_con_clase_N2['class']
                                logging.info("Clase encontrada en HTML 2: %s", etiqueta_con_clase_N2['class'])
                            else:
                                self.claseN2 = "Clase no encontrada"
                                logging.info("Clase no encontrada en HTML 2")

                            if etiqueta_con_clase_img_src:
                                self.claseN3 = etiqueta_con_clase_img_src['class']
                                logging.info("Clase encontrada en la imagen: %s", etiqueta_con_clase_img_src['class'])
                            else:
                                self.claseN3 = "Clase no encontrada"
                                logging.info("Clase no encontrada en la imagen")

                            if etiqueta_con_clase_url_href:
                                self.claseN4 = etiqueta_con_clase_url_href['class']
                                logging.info("Clase encontrada en el botón 'Siguiente': %s", etiqueta_con_clase_url_href['class'])
                            else:
                                self.claseN4 ="Clase no encontrada"
                                logging.info("Clase no encontrada en el botón 'Siguiente'")
                            if etiqueta_con_clase_productos_href:
                                self.claseN5 = etiqueta_con_clase_productos_href['class']
                                logging.info("Clase encontrada en el botón 'Siguiente': %s", etiqueta_con_clase_productos_href['class'])
                            else:
                                self.claseN5 ="Clase no encontrada"
                                logging.info("Clase no encontrada en el botón 'Siguiente'")
 
                            if etiqueta_con_clase_N1 and etiqueta_con_clase_N2 and etiqueta_con_clase_url_href and etiqueta_con_clase_img_src and etiqueta_con_clase_productos_href:
                                # Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento HTML N1
                                clase_obtenida_N1 = etiqueta_con_clase_N1.get('class', [])
                                clase_obtenida_N1 = ' '.join(clase_obtenida_N1)
                                logging.info("Clase obtenida N1: %s", clase_obtenida_N1)

                                # Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento HTML N2
                                clase_obtenida_N2 = etiqueta_con_clase_N2.get('class', [])
                                clase_obtenida_N2 = ' '.join(clase_obtenida_N2)
                                logging.info("Clase obtenida N2: %s", clase_obtenida_N2)

                                # Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento del botón 'Siguiente' (URLS)
                                clase_obtenida_url = etiqueta_con_clase_url_href.get('class', [])
                                clase_obtenida_url = ' '.join(clase_obtenida_url)
                                logging.info("Clase obtenida Botón 'Siguiente': %s", clase_obtenida_url)

                                # Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento que contiene las imágenes 'src'
                                clase_obtenida_src = etiqueta_con_clase_img_src.get('class', [])
                                clase_obtenida_src = ' '.join(clase_obtenida_src)
                                logging.info("Clase obtenida 'Imagenes': %s", clase_obtenida_src)
                                
                                # Obtenemos la string de la clase en el fragmento de codigo HTML para el Elemento que contiene las Url de los productos <href>'
                                clase_obtenida_href = etiqueta_con_clase_productos_href.get('class', [])
                                clase_obtenida_href = ' '.join(clase_obtenida_href)
                                logging.info("Clase obtenida 'Imagenes': %s", clase_obtenida_href)
                                
                                
                            else:
                                logging.error("Hubo un fallo obteniendo las clases")
                                #En caso no encontrarse las clases se rompera el ciclo
                                break

                                
                            if clase_obtenida_N1 and clase_obtenida_N2 and clase_obtenida_url and clase_obtenida_src and clase_obtenida_href:
                                # Encontrar todas las instancias de las clases obtenidas
                                # Clase elemento HTML N1
                                elementos_con_clase_N1 = soup.find_all(class_=clase_obtenida_N1)
                                # Clase elemento HTML N2
                                elementos_con_clase_N2 = soup.find_all(class_=clase_obtenida_N2)
                                # Clase elemento HTML URLS "Boton siguiente (URLS)"
                                elementos_con_clase_url = soup.find_all(class_=clase_obtenida_url)
                                # Clase elemento HTML URLS "Boton siguiente (URLS)"
                                elementos_con_clase_href = soup.find_all(class_=clase_obtenida_href)
                                # Clase elemento HTML de las imágenes
                                elementos_con_clase_src = soup.find_all(class_=clase_obtenida_src.split())

                                # Registrar el número de elementos encontrados
                                logging.info("Elementos con clase N1 encontrados: %d", len(elementos_con_clase_N1))
                                logging.info("Elementos con clase N2 encontrados: %d", len(elementos_con_clase_N2))
                                logging.info("Elementos con clase URL encontrados: %d", len(elementos_con_clase_url))
                                logging.info("Elementos con clase SRC encontrados: %d", len(elementos_con_clase_src))
                                logging.info("Elementos con clase SRC encontrados: %d", len(elementos_con_clase_href))
                            else:
                                logging.error("Hubo un fallo encontrando las clases")
    
                            # Lista donde almacenamos la data extraida
                            data = []   
                            # Lista para almacenar los valores 'src' de la imagenes
                            src_values = []
                            #Lista para las Url de los productos
                            href_values= []
                                
                            # Hallamos todas las imagenes (Los 'src')
                            if elementos_con_clase_src:
                                for elemento in elementos_con_clase_src:
                                    # Obtener el valor del atributo 'src'
                                    src = elemento.get('src')
                                    if src:
                                        src_values.append(src)
                                        # Registrar el valor del atributo src
                                        logging.info("Valor del atributo src: %s SRC Numero: %s", src, elemento)
                                    else:
                                        src_values.append('null')
                            else:
                                logging.info("No se encontró el 'src' en las instancias de las clases.")
                                                            
                            
                            #Hallamos la siguiente pagina (URL) a la cual se le extraeran los datos
                            if elementos_con_clase_url:
                                # Hallamos la última instancia de la clase que contiene el URL de la siguiente página
                                ultimo_elemento = elementos_con_clase_url[-1]
                                # Una vez tomado el último elemento, extraemos el 'href' que contiene la URL necesaria
                                etiqueta_con_clase_boton_siguiente = ultimo_elemento.get('href')

                                if etiqueta_con_clase_boton_siguiente:
                                    patron_url = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
                                    if re.match(patron_url, etiqueta_con_clase_boton_siguiente):
                                        logging.info("Siguiente página encontrada: %s", etiqueta_con_clase_boton_siguiente)

                                        # Reasignación de URL
                                        url_siguiente = etiqueta_con_clase_boton_siguiente
                                    else:
                                        base_url = "https://www.amazon.com"
                                        url_siguiente = urljoin(base_url, etiqueta_con_clase_boton_siguiente)
                            else:
                                logging.info("No se encontraron más páginas")
                                #Rompemos el ciclo en caso de no tener mas URL
                                break
                            
                            # Hallamos las url de los productos
                            if elementos_con_clase_href:
                                for elemento in elementos_con_clase_href:
                                    # Hallamos el href
                                    href_producto = elemento.get('href')

                                    if href_producto:
                                        if urlparse(href_producto).scheme in ('http', 'https'):
                                            href_values.append(href_producto)
                                            logging.info("URL de producto encontrada: %s", href_producto)
                                        else:
                                            base_url = "https://www.amazon.com"
                                            href_producto_amazon = urljoin(base_url, href_producto)
                                            href_values.append(href_producto_amazon)
                            else:
                                logging.info("No se encontraron más páginas")
                            

                            # Usar zip para combinar las listas 
                            for elemento, elemento2, src, href  in zip(elementos_con_clase_N1, elementos_con_clase_N2, src_values, href_values):
                                print("Guardando data")
                                #Extraemos el texto que se encuentre dentro de las instancias del elemento HTML N1
                                textoN1 = elemento.get_text()
                                #Extraemos el texto que se encuentre dentro de las instancias del elemento HTML N2
                                textoN2 = elemento2.get_text()
                                
                                #Anadimos la data a una nueva fila de la base de datos
                                nueva_fila_db = Data_Extraida(Texto_N1=textoN1,Texto_N2=textoN2, Src_imagenes=src, href_productos= href)
                                print(nueva_fila_db)
                                session.add(nueva_fila_db)
                                session.commit()
                                
                                #Agregamos los datos a lista de data 
                                data.append([textoN1, textoN2, src, href])

                            # Escribir los datos en las filas
                            for fila in data:
                                hoja_excel.append(fila)  
                                
                        else:
                            CTkMessagebox(master=self, title="Fallo", message="Hubo un fallo al contactar con la pagina", icon="warning")
                            self.Barrra_de_carga.stop()
                            return
                    except Exception as e:
                        self.Barrra_de_carga.stop()
                        CTkMessagebox(master=self,title="Advertencia", message=f"Fallo en el proceso de extraccion:\n\n{e}", icon="warning", option_1="Cancelar", option_2="Reintentar")          
                else:
                    self.Barrra_de_carga.stop()
                    CTkMessagebox(master=self,title="Advertencia", message="Fallo en el proceso de extraccion", icon="warning", option_1="Cancelar", option_2="Reintentar")
                    return

            if data is not None:
                #Detenemos la progrress bar
                self.Barrra_de_carga.stop()
                # Registra la fecha y hora de finalización
                self.fin = datetime.now()
                #Exportamos la el archivo de excel a una direccion dada por el usuario        
                Ruta_archivo_excel = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])

                if Ruta_archivo_excel:
                    # Guardar el archivo Excel en la ubicación elegida por el usuario
                    libro_excel.save(Ruta_archivo_excel)
                    CTkMessagebox(master=self, title="Informacion", message="Se ha exportado el documento de excel correctamente")
                else:
                    CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error al exportar el documento de excel", icon="cancel")  
                    
                #Cerramos el registro de los log        
                logging.shutdown()
            else:
                self.Barrra_de_carga.stop()
                return    
            
            
        except:
            CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error", icon="cancel") 
            #Detenemos la progressbar en caso de una excepsion 
            self.Barrra_de_carga.stop()
            #Cerramos el log, para liberar data
            logging.shutdown()
            
    def mostar_graficos(self):
        try:
            # Tamaño de la figura en píxeles
            fig_width_pixels = 1600
            fig_height_pixels = 400
                              
            self.frame_grafico_N1 = customtkinter.CTkFrame(self.frame_base, fg_color="#ffffff")
            self.frame_grafico_N1.grid(row=25, column=0, columnspan=2,padx=5, pady=5, sticky="nsew")
            
            self.frame_grafico_N2 = customtkinter.CTkFrame(self.frame_base, fg_color="#ffffff")
            self.frame_grafico_N2.grid(row=26, column=0, columnspan=2,padx=5, pady=(5,25), sticky="nsew")
            
            if self.tiempos_respuesta and self.tamanos_respuesta is not None:
            # Crear un gráfico que muestre el tiempo de respuesta de cada solicitud de red
                #plt.style.use('Selenium_app\graficos_mtlip.mplstyle')
                plt.style.use('bmh')
                
                fig = Figure(figsize=(fig_width_pixels / 80, fig_height_pixels / 80), dpi=80)
                ax1 = fig.add_subplot(1, 1, 1)
                ax1.plot(range(1, len(self.tiempos_respuesta) + 1), self.tiempos_respuesta, marker='o')
                #ax1.set_xlabel("Páginas")
                ax1.set_ylabel("Tiempo de Respuesta (segundos)")
                ax1.set_title("Tiempo de Respuesta de las Solicitudes de Red")
                
                # Crear un lienzo para la figura
                canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico_N1)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack()
                    
                # Crear un gráfico que muestre el tamaño de respuesta de cada solicitud de red
                fig_2 = Figure(figsize=(fig_width_pixels / 80, fig_height_pixels / 80), dpi=80)
                ax2 = fig_2.add_subplot(1, 1, 1)
                ax2.plot(range(1, len(self.tamanos_respuesta) + 1), self.tamanos_respuesta, marker='o')
                #ax2.set_xlabel("Páginas")
                ax2.set_ylabel("Tamaño de Respuesta (KB)")
                ax2.set_title("Tamaño de Respuesta de las Solicitudes de Red")

                # Crear un lienzo para la figura
                canvas_2 = FigureCanvasTkAgg(fig_2, master=self.frame_grafico_N2)
                canvas_widget_2 = canvas_2.get_tk_widget()
                canvas_widget_2.pack()        
            else:
                return
        except Exception as e:
            CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error: {e}", icon="cancel")

    def exportar_data_base(self):
        self.Barrra_de_carga_exportacion_data_base.start()
        try:
            # Ruta de la base de datos original
            ruta_base_de_datos_original = 'Base_De_Datos_Data.db'

            # Abre un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo de copia de seguridad
            ruta_copia_de_seguridad = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])

            if ruta_copia_de_seguridad:
                # Realiza una copia de seguridad de la base de datos en la ubicación seleccionada
                shutil.copyfile(ruta_base_de_datos_original, ruta_copia_de_seguridad)
                CTkMessagebox(master=self, title="Informacion", message="Copia de seguridad creada exitosamente")
            else:
                CTkMessagebox(master=self, title="Informacion", message="Exportación cancelada por el usuario")
        except Exception as e:
            CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error: {e}", icon="cancel") 
        #Se detiene la barra de carga al final del try    
        self.Barrra_de_carga_exportacion_data_base.stop()        

    def exportar_registro(self):
        self.Barrra_de_carga_exportacion.start()
        try:
            #Preguntamos al usuario donde guardar el archivo
            Ruta_archivo_log_txt = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            
            # Abre el archivo de registro
            with open('data_extraida.log', 'r') as log_file:
                log_data = log_file.read()
                
            if Ruta_archivo_log_txt:
                # Guarda el contenido en el archivo seleccionado por el usuario
                with open(Ruta_archivo_log_txt, 'w') as export_file:
                    export_file.write(log_data)
                    CTkMessagebox(master=self, title="Informacion", message="Se ha exportado el log correctamente")
            else:
                CTkMessagebox(master=self, title="Informacion", message="Se ha cancelado la exportacion")
        except Exception as e:
            CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error: {e}", icon="cancel") 
        #Detenemos la barra de carga
        self.Barrra_de_carga_exportacion.stop()
    
    def limpiar_data_todo(self):
        self.Barrra_de_carga_limpiar_data.start()
        try:
            #Borramos todo lo que haya dentro de los entrys
            self.confirmar_url_pagina.delete(0, customtkinter.END)
            self.elementos_pagina_html_N1.delete(0, customtkinter.END)
            self.elementos_pagina_html_N2.delete(0, customtkinter.END)
            self.elementos_pagina_html_N3.delete(0, customtkinter.END)
            self.elementos_pagina_html_N4.delete(0, customtkinter.END)
            
            #Configuramos los valores del slider:
            self.Rango_slider_paginas.set([1,200])
            
            #Restauramos la confioguraciond de los swhichets
            self.verificasion_switch_url.configure(state="normal")
            self.verificasion_switch_url.deselect()
            self.verificasion_switch_url.configure(text="No verificado")
            self.verificasion_switch_url.configure(state="disabled")
            #
            self.verificasion_switch_N1.configure(state="normal")
            self.verificasion_switch_N1.configure(text="No verificado")
            self.verificasion_switch_N1.deselect()
            self.verificasion_switch_N1.configure(state="disabled")
            #
            self.verificasion_switch_N2.configure(state="normal")
            self.verificasion_switch_N2.configure(text="No verificado")
            self.verificasion_switch_N2.deselect()
            self.verificasion_switch_N2.configure(state="disabled")
            #
            self.verificasion_switch_N3.configure(state="normal")
            self.verificasion_switch_N3.configure(text="No verificado")
            self.verificasion_switch_N3.deselect()
            self.verificasion_switch_N3.configure(state="disabled")
            #
            self.verificasion_switch_N4.configure(state="normal")
            self.verificasion_switch_N4.configure(text="No verificado")
            self.verificasion_switch_N4.deselect()
            self.verificasion_switch_N4.configure(state="disabled")
            
            #Elinamos el registro de extracion .log
            try:
                ruta_archivo = 'data_extraida.log'
                # Verifica si el archivo existe antes de intentar eliminarlo
                if os.path.exists(ruta_archivo):
                    os.remove(ruta_archivo)
                    print(f"Archivo '{ruta_archivo}' eliminado correctamente.")
                else:
                    print(f"El archivo '{ruta_archivo}' no existe.")
            except:
                self.Barrra_de_carga_limpiar_data.stop() 
               
                
            #Eliminamos todos los registros que haya en la base de datos:
            try:
                # Elimina todos los registros de la tabla 'Data_Extraida'
                session.query(Data_Extraida).delete()

                # Confirma la transacción
                session.commit()
                   
            except:
                # En caso de error, realiza un rollback de la transacción
                session.rollback()
                self.Barrra_de_carga_limpiar_data.stop() 
                
                
            #Detenemos la barra de carga
            
            try:
               self.frame_resumen_datos_N1.forget()
               self.frame_resumen_datos_N1_derecha.forget()
               self.frame_resumen_datos_N2.forget()
               self.frame_resumen_datos_N2_derecha.forget()
               self.frame_resumen_datos_N3.forget()
               self.frame_resumen_datos_N3_derecha.forget()
               self.frame_resumen_datos_N4.forget()
               self.frame_resumen_datos_N4_derecha.forget()
               #
               self.frame_resumen_tabla.forget()
               #
               self.frame_grafico_N1.forget()
               self.frame_grafico_N2.forget()
               
            except:
                self.Barrra_de_carga_limpiar_data.stop() 
                
            
            self.Barrra_de_carga_limpiar_data.stop()            
        except Exception as e:
            CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error: {e}", icon="cancel") 
        #Detenmos la barra de carga
        CTkMessagebox(master=self,title="info", message="Todos los campos y registros se han limpiado correctamen")
        self.Barrra_de_carga_limpiar_data.stop()     
    
    def resumen_extracion(self):
        if session.query(func.count(Data_Extraida.Id)).scalar() > 0:
            try: 
                #Calcula el total de filas
                total_filas = session.query(func.count(Data_Extraida.Id)).scalar()  
                session.commit()
                
                #Calcular el total de elementos (celdas)
                total_celdas = total_filas * 3
                
                # Calcula el tiempo transcurrido
                tiempo_transcurrido = self.fin - self.inicio
        
                fecha_actual= datetime.now()
                       
                self.frame_resumen_datos_N1 = customtkinter.CTkFrame(self.frame_base)
                self.frame_resumen_datos_N1.grid(row=20, column=0, padx=5, pady=5, sticky="nsew") 
                
                self.frame_resumen_datos_N1_derecha = customtkinter.CTkFrame(self.frame_base)
                self.frame_resumen_datos_N1_derecha.grid(row=20,column=1, padx=5, pady=5, sticky="nsew")
                
                self.frame_resumen_datos_N2 = customtkinter.CTkFrame(self.frame_base)
                self.frame_resumen_datos_N2.grid(row=21, column=0, padx=5, pady=5, sticky="nsew") 
                
                self.frame_resumen_datos_N2_derecha = customtkinter.CTkFrame(self.frame_base)
                self.frame_resumen_datos_N2_derecha.grid(row=21, column=1,padx=5, pady=5, sticky="nsew")
                
                self.frame_resumen_datos_N3 = customtkinter.CTkFrame(self.frame_base)
                self.frame_resumen_datos_N3.grid(row=22, column=0, padx=5, pady=5, sticky="nsew") 
                
                self.frame_resumen_datos_N3_derecha = customtkinter.CTkFrame(self.frame_base)
                self.frame_resumen_datos_N3_derecha.grid(row=22, column=1,padx=5, pady=5, sticky="nsew")
                
                self.frame_resumen_datos_N4 = customtkinter.CTkFrame(self.frame_base)
                self.frame_resumen_datos_N4.grid(row=23, column=0, padx=5, pady=5, sticky="nsew") 
                
                self.frame_resumen_datos_N4_derecha = customtkinter.CTkFrame(self.frame_base)
                self.frame_resumen_datos_N4_derecha.grid(row=23, column=1,padx=5, pady=5, sticky="nsew")
            
                self.label_resumen_tiempo = customtkinter.CTkLabel(self.frame_resumen_datos_N1, 
                                                    text="Duraccion: ")
                self.label_resumen_tiempo.pack(side="left", padx=10, pady=10)
                
                self.label_resumen_numero_filas = customtkinter.CTkLabel(self.frame_resumen_datos_N2, 
                                                        text="Total filas: ")
                self.label_resumen_numero_filas.pack(side="left", padx=10, pady=10)
                
                self.label_resumen_numero_celdas = customtkinter.CTkLabel(self.frame_resumen_datos_N3, 
                                                            text="Total de datos: ")
                self.label_resumen_numero_celdas.pack(side="left", padx=10, pady=10)
                
                self.label_resumen_fecha = customtkinter.CTkLabel(self.frame_resumen_datos_N4, 
                                                            text="Fecha de creacion: ")
                self.label_resumen_fecha.pack(side="left", padx=10, pady=10)
                
                self.label_resumen_fecha_valor = customtkinter.CTkLabel(self.frame_resumen_datos_N4_derecha, 
                                                            text=fecha_actual)
                self.label_resumen_fecha_valor.pack(side="left", padx=10, pady=10)
                
                self.label_resumen_tiempo_valor = customtkinter.CTkLabel(self.frame_resumen_datos_N1_derecha, 
                                                            text=tiempo_transcurrido)
                self.label_resumen_tiempo_valor.pack(side="left", padx=10, pady=10)
                
                self.label_resumen_numero_filas_valor = customtkinter.CTkLabel(self.frame_resumen_datos_N2_derecha, 
                                                        text=total_filas)
                self.label_resumen_numero_filas_valor.pack(side="left", padx=10, pady=10)
                
                self.label_resumen_numero_celdas_valor = customtkinter.CTkLabel(self.frame_resumen_datos_N3_derecha, 
                                                            text=total_celdas)
                self.label_resumen_numero_celdas_valor.pack(side="left", padx=10, pady=10)
                            
            except Exception as e:
                CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error. Verifica que hayas seguido los pasos correctamente\n\nFallo: {e}", icon="cancel") 
        else:
            return
        
        if session.query(func.count(Data_Extraida.Id)).scalar() > 0:
            try:
                self.frame_resumen_tabla = customtkinter.CTkFrame(self.frame_base, fg_color="#ffffff")
                self.frame_resumen_tabla.grid(row=24, column=0, columnspan=2, padx=5, pady=5, sticky="nsew") 

                # Obtener los datos de la base de datos SQLAlchemy
                datos = session.query(Data_Extraida).all()

                # Crear un Treeview para mostrar los datos en forma de tabla
                treeview = ttk.Treeview(self.frame_resumen_tabla, columns=("Id", "Texto_N1", "Texto_N2", "Src_imagenes", "href_productos"), show="headings")

                # Configurar los encabezados de las columnas
                treeview.heading("Id", text="ID")
                treeview.heading("Texto_N1", text="Texto N1")
                treeview.heading("Texto_N2", text="Texto N2")
                treeview.heading("Src_imagenes", text="URL imágenes")
                treeview.heading("href_productos", text="URL producto")

                # Configurar el ancho de las columnas
                treeview.column("Id", width=50, anchor="center")
                treeview.column("Texto_N1", width=150, anchor="w")
                treeview.column("Texto_N2", width=150, anchor="w")
                treeview.column("Src_imagenes", width=200, anchor="w")
                treeview.column("href_productos", width=200, anchor="w")

                # Empacar el Treeview y ajustar su tamaño
                treeview.pack(fill="both", expand=True, padx=10, pady=20)

                
                # Limpiar cualquier dato previo en el Treeview
                for fila in treeview.get_children():
                    treeview.delete(fila)

                # Insertar los datos en el Treeview
                for dato in datos:
                    treeview.insert("", "end", values=(dato.Id, dato.Texto_N1, dato.Texto_N2, dato.Src_imagenes, dato.href_productos))
                                                    
            except Exception as e:
                CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error: {e}", icon="cancel") 
        else:
            return
        #Mostramos los graficos
        self.mostar_graficos()
    
    def Hilo_extraccion_de_data(self):
        # Iniciar un hilo para ejecutar la extracción de datos
        extraccion_thread = threading.Thread(target=self.extracion_de_datos_entry)
        extraccion_thread.start()    
    
    def Hilo_descarga_de_imagenes(self):
        # Iniciar un hilo para ejecutar la extracción de datos
        descarga_thread = threading.Thread(target=self.descargar_imagenes)
        descarga_thread.start()       
        
    def descargar_imagenes(self):
        self.Barrra_de_carga_funciones.start()
        #Verificamos que la base de datos con imagenes no este vacia
        if session.query(func.count(Data_Extraida.Id)).scalar() > 0:
            #procedemos a extraer todas las imagnees
            imagenes = session.query(Data_Extraida.Src_imagenes).all()
            #Creamos la carpeta para las imagenes 
            carpeta_imagenes = filedialog.askdirectory(title="Selecciona donde guardar las imagenes")
            if not carpeta_imagenes:
                CTkMessagebox(master=self, title="Informacion", message="Se ha cancelado la exportacion")
                return
            else:
                    try:
                        for imagen in imagenes:
                            # Obtener el nombre de archivo de la URL
                            nombre_archivo = os.path.basename(imagen[0])
                            # Crear la ruta completa de destino
                            ruta_destino = os.path.join(carpeta_imagenes, nombre_archivo)
                            
                            # Descargar la imagen desde la URL 'imagen[0]' y guardarla en 'ruta_destino'
                            response = requests.get(imagen[0])
                            if response.status_code == 200:
                                with open(ruta_destino, 'wb') as file:
                                    file.write(response.content)
                            else:
                                CTkMessagebox(master=self, title="Error", message="Ha ocurrido un fallo al contactar con la pagina", icon="cancel")
                                return
                                        
                    except Exception as e:
                        CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error: {e}", icon="cancel") 
                        
            CTkMessagebox(master=self, title="Informacion", message="proceso de descargas completado")   
            self.Barrra_de_carga_funciones.stop()           
        else:
            self.Barrra_de_carga_funciones.stop() 
            return                
                            
    def url_pagina_extraccion(self):
        url_sin_revisar = self.confirmar_url_pagina.get()
        if url_sin_revisar != "":
            # Patrón de expresión regular para verificar si es una URL válida
            patron_url = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
            #Se compara la ulr del usuario con una expresion regular de URLS       
            if re.match(patron_url, url_sin_revisar):
                url_verificada = url_sin_revisar
                try: 
                    # Verificación de la página
                    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":
                    "gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":
                    "close", "Upgrade-Insecure-Requests":"1"
                    }
                    #Realizamos una peticion a la pagina
                    estado_de_url = requests.get(url_verificada, headers=headers)
                    
                    # Verifica el código de estado de la respuesta
                    if estado_de_url.status_code == 200:
                        mensaje = f"La página está disponible '{url_verificada}' y lista para la extracción de datos."
                        self.verificasion_switch_url.configure(text="Verificado")
                        self.verificasion_switch_url.configure(state="normal")
                        self.verificasion_switch_url.select()
                        self.verificasion_switch_url.configure(state="disabled")
                        
                        #Mostramos el estado de la pagina
                        CTkMessagebox(master=self,title="Error", message=f"{mensaje}") 
                    elif estado_de_url.status_code == 404:
                        CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error (404)", icon="cancel")   
                    elif estado_de_url.status_code == 403:
                        CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error (403)", icon="cancel")   
                    elif estado_de_url.status_code == 500:
                        CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error (500)", icon="cancel")   
                    else:
                        #En caso de cualquier otro estado:
                        mensaje = f"El estado de la página es: {estado_de_url.status_code}."
                        CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error:\n\n{mensaje}", icon="cancel")    
                except requests.exceptions.RequestException as e:
                    #En caso de cualquier otro estado especificamos el tipo de error:
                    CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error: {e}", icon="cancel")                      
            else:
                CTkMessagebox(master=self,title="Error", message="Por favor, verifique la URL ingresada. Debe comenzar con 'http', 'https' o 'ftp'", icon="cancel")  
        else:
             CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error", icon="cancel")     
        
    def elementos_html_N1(self):
        Elemento_Html= self.elementos_pagina_html_N1.get()
        Elemento_Html_verificado = Elemento_Html
            
        try:
            # Intenta analizar el valor como HTML
            comprobacion_html = BeautifulSoup(Elemento_Html_verificado, 'html.parser')
            
            # Buscar cualquier etiqueta que tenga la clase y obtener la clase
            etiqueta_con_clase = comprobacion_html.find(class_=True)
            
            if etiqueta_con_clase:                
                clase_obtenida = etiqueta_con_clase.get('class', [])
                clase_obtenida = ' '.join(clase_obtenida)
                
                mensaje = f"Clase encontrada en el HTML:\nNombre de la clase(s): {clase_obtenida}\nElemento HTML verificado con éxito."
                self.verificasion_switch_N1.configure(text="Verificado")
                self.verificasion_switch_N1.configure(state="normal")
                self.verificasion_switch_N1.select()
                self.verificasion_switch_N1.configure(state="disabled")
                
                CTkMessagebox(master=self,title="info", message=f"{mensaje}") 
            else:
                CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error", icon="cancel") 
        except Exception as e:
            CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error:\n\n{e}", icon="cancel") 
            
    def elementos_html_N2(self):
        Elemento_Html= self.elementos_pagina_html_N2.get()
        Elemento_Html_verificado = Elemento_Html
            
        try:
            # Intenta analizar el valor como HTML
            comprobacion_html = BeautifulSoup(Elemento_Html_verificado, 'html.parser')
            
            # Buscar cualquier etiqueta que tenga la clase y obtener la clase
            etiqueta_con_clase = comprobacion_html.find(class_=True)
            
            if etiqueta_con_clase:                
                clase_obtenida = etiqueta_con_clase.get('class', [])
                clase_obtenida = ' '.join(clase_obtenida)
                
                mensaje = f"Clase encontrada en el HTML:\nNombre de la clase(s): \nNombre de la clase: {clase_obtenida}\nElemento HTML verificado con éxito."
                self.verificasion_switch_N2.configure(text="Verificado")
                self.verificasion_switch_N2.configure(state="normal")
                self.verificasion_switch_N2.select()
                self.verificasion_switch_N2.configure(state="disabled")
                CTkMessagebox(master=self,title="info", message=f"{mensaje}") 
                
            else:
                CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error", icon="cancel") 
        except Exception as e:
            CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error:\n\n{e}", icon="cancel")                   
    
    def imagenes_elementos_html(self):
        Elemento_html_img = self.elementos_pagina_html_N3.get()
        if Elemento_html_img !="" :
            try:
                # Intenta analizar el valor como HTML
                comprobacion_html_img = BeautifulSoup(Elemento_html_img, 'html.parser')
                
                # Buscar cualquier etiqueta que tenga la clase y obtener la clase
                etiqueta_con_clase = comprobacion_html_img.find(class_=True)
                
                if etiqueta_con_clase:                
                    clase_obtenida = etiqueta_con_clase.get('class', [])
                    clase_obtenida = ' '.join(clase_obtenida)
                    
                    mensaje = f"Clase encontrada en el HTML:\nNombre de la clase(s):  {clase_obtenida}\nElemento HTML verificado y guardado con éxito."
                    self.verificasion_switch_N3.configure(text="Verificado")
                    self.verificasion_switch_N3.configure(state="normal")
                    self.verificasion_switch_N3.select()
                    self.verificasion_switch_N3.configure(state="disabled")
                    CTkMessagebox(master=self,title="info", message=f"{mensaje}")
                    
                else:
                    CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error", icon="cancel") 
            except Exception as e:
                CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error:\n\n{e}", icon="cancel")
        else:
            CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error", icon="cancel") 
        
    def elemento_boton_siguiente(self):
        Elemento_boton = self.elementos_pagina_html_N4.get()
        if Elemento_boton:
            try:
                # Intenta analizar el valor como HTML
                comprobacion_html_boton = BeautifulSoup(Elemento_boton, 'html.parser')
                
                # Buscar cualquier etiqueta que tenga la clase y obtener la clase
                etiqueta_con_clase = comprobacion_html_boton.find(class_=True)
                
                if etiqueta_con_clase:                
                    clase_obtenida = etiqueta_con_clase.get('class', [])
                    clase_obtenida = ' '.join(clase_obtenida)
                    
                    mensaje = f"Clase encontrada en el HTML:\nNombre de la clase(s):  {clase_obtenida}\nElemento HTML verificado y guardado con éxito."
                    self.verificasion_switch_N4.configure(text="Verificado")
                    self.verificasion_switch_N4.configure(state="normal")
                    self.verificasion_switch_N4.select()
                    self.verificasion_switch_N4.configure(state="disabled")
                    CTkMessagebox(master=self,title="info", message=f"{mensaje}")
                    
                else:
                    CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error", icon="cancel")
            except Exception as e:
                CTkMessagebox(master=self,title="Error", message=f"Ha ocurrido un error:\n\n{e}", icon="cancel")
        else:
            CTkMessagebox(master=self,title="Error", message="Ha ocurrido un error", icon="cancel")  
         
                 
if __name__ == "__main__":
    app = App()
    app.mainloop()



