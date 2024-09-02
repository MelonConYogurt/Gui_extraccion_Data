

# Extracción de Datos Entry

La función `extracion_de_datos_entry` está diseñada para extraer datos de páginas web mediante solicitudes HTTP y procesar el contenido HTML utilizando `BeautifulSoup`. Los datos extraídos se almacenan en un archivo Excel y se registran en un archivo de log.

## Descripción

Esta función realiza las siguientes tareas:

1. **Configuración Inicial**:
   - Inicializa listas para almacenar tiempos de respuesta y tamaños de respuesta.
   - Configura un archivo de log para registrar el proceso de extracción.
   - Prepara un archivo Excel para almacenar los datos extraídos.

2. **Extracción de Datos**:
   - Obtiene URLs y cadenas HTML proporcionadas por el usuario.
   - Realiza solicitudes HTTP a las URLs y registra tiempos y tamaños de respuesta.
   - Utiliza `BeautifulSoup` para analizar el HTML y extraer clases y datos específicos.
   - Almacena los datos extraídos en el archivo Excel y en la base de datos.

3. **Manejo de Errores y Finalización**:
   - Maneja errores durante el proceso de extracción.
   - Exporta el archivo Excel a una ubicación elegida por el usuario.
   - Detiene la barra de carga y cierra el registro de logs.

## Requisitos

- **Librerías**:
  - `requests`
  - `beautifulsoup4`
  - `openpyxl`
  - `logging`
  - `re`
  - `tkinter`

## Uso

1. **Preparación**:
   - Asegúrate de que los datos requeridos (URLs, cadenas HTML) estén disponibles.
   - Configura las cadenas HTML de los elementos que se deben buscar.

2. **Ejecutar la Función**:
   - La función se debe invocar como un método de una clase que tenga las propiedades necesarias (`confirmar_url_pagina`, `elementos_pagina_html_N1`, etc.).
   - La barra de carga se iniciará antes del ciclo de extracción y se detendrá al finalizar el proceso.

3. **Exportación de Datos**:
   - Al finalizar, se abrirá un diálogo para guardar el archivo Excel en la ubicación deseada.

## Ejemplo de Código

```python
def extracion_de_datos_entry(self):
    # Lista para almacenar tiempos y tamaños de respuesta
    self.tiempos_respuesta = []
    self.tamanos_respuesta = []
    
    # Configuración de logging
    logging.basicConfig(filename='Selenium_app/data_extraida.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Crear archivo Excel
    libro_excel = Workbook()
    hoja_excel = libro_excel.active
    hoja_excel.append(['Texto N1', 'Texto N2', 'Src Imagenes', 'URL del producto'])
    
    # Obtener datos de entrada
    url = self.confirmar_url_pagina.get()
    cadena_htmlN1 = self.elementos_pagina_html_N1.get()
    cadena_htmlN2 = self.elementos_pagina_html_N2.get()
    cadena_html_productos = self.Url_pagina_producto.get()
    cadena_imagen = self.elementos_pagina_html_N3.get()
    boton_siguiente = self.elementos_pagina_html_N4.get()
    
    # Configuración de solicitudes HTTP
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }
    
    url_siguiente = url
    self.inicio = datetime.now()
    
    try:
        self.Barrra_de_carga.start()
        for i in range(int(self.Rango_slider_paginas.get()[0]), int(self.Rango_slider_paginas.get()[1]) + 1):
            if url_siguiente:
                try:
                    logging.info("Pagina numero: %s URL: %s", i, url_siguiente)
                    response = requests.get(url_siguiente, headers=headers)
                    self.tiempo_respuesta = response.elapsed.total_seconds()
                    self.tamaño_respuesta = len(response.content) / 1024
                    self.tiempos_respuesta.append(self.tiempo_respuesta)
                    self.tamanos_respuesta.append(self.tamaño_respuesta)
                    
                    if response.status_code == 200:
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        # Procesamiento y extracción de datos
                        # ...
                    else:
                        CTkMessagebox(master=self, title="Fallo", message="Hubo un fallo al contactar con la pagina", icon="warning")
                        self.Barrra_de_carga.stop()
                        return
                except Exception as e:
                    self.Barrra_de_carga.stop()
                    CTkMessagebox(master=self, title="Advertencia", message=f"Fallo en el proceso de extraccion:\n\n{e}", icon="warning", option_1="Cancelar", option_2="Reintentar")
            else:
                self.Barrra_de_carga.stop()
                CTkMessagebox(master=self, title="Advertencia", message="Fallo en el proceso de extraccion", icon="warning", option_1="Cancelar", option_2="Reintentar")
                return
        
        if data:
            self.Barrra_de_carga.stop()
            self.fin = datetime.now()
            Ruta_archivo_excel = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
            if Ruta_archivo_excel:
                libro_excel.save(Ruta_archivo_excel)
                CTkMessagebox(master=self, title="Informacion", message="Se ha exportado el documento de excel correctamente")
            else:
                CTkMessagebox(master=self, title="Error", message="Ha ocurrido un error al exportar el documento de excel", icon="cancel")
            logging.shutdown()
        else:
            self.Barrra_de_carga.stop()
            return
    except:
        CTkMessagebox(master=self, title="Error", message="Ha ocurrido un error", icon="cancel")
        self.Barrra_de_carga.stop()
        logging.shutdown()
```

## Notas

- Asegúrate de tener las librerías requeridas instaladas y configuradas.
- La función depende de las configuraciones de entrada específicas, como las cadenas HTML y las URLs proporcionadas por el usuario.

Para más detalles sobre cada parte del código, revisa los comentarios y el código fuente en la función.


Asegúrate de ajustar cualquier detalle según la estructura de tu proyecto y los requisitos específicos de la función.

![Screenshot 2024-09-02 002852](https://github.com/user-attachments/assets/3f8a4272-de68-47ff-9851-28e921369dc4)
![demo scrapp 3](https://github.com/user-attachments/assets/68b0ce51-fa96-4562-8d8e-b6c373da7845)
![Demo scrap 2](https://github.com/user-attachments/assets/87ea04f2-e7f8-4558-a09d-00f1fe97ac5d)
![Screenshot 2024-09-02 003918](https://github.com/user-attachments/assets/02fa4548-eb04-445e-b72f-ae9c87165e16)
![Screenshot 2024-09-02 010927](https://github.com/user-attachments/assets/5ca9d924-0959-415b-8efd-59bb041e3405)
![Screenshot 2024-09-02 010940](https://github.com/user-attachments/assets/ba6fe74e-4529-447c-803b-e01692153038)


