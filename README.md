
---

# Video demostracion

[![Alt text](https://github.com/user-attachments/assets/ba6fe74e-4529-447c-803b-e01692153038)](https://youtu.be/Sy-Kcgu5nG0)


La función `extracion_de_datos_entry` es una herramienta robusta para la extracción automatizada de datos desde páginas web. Utiliza solicitudes HTTP y procesa contenido HTML con `BeautifulSoup`, almacenando los datos extraídos en un archivo Excel y registrando el proceso en un log.

## Descripción

### 1. Configuración Inicial

- **Inicialización de Listas**: Para almacenar tiempos y tamaños de respuesta.
- **Configuración de Logs**: Registro detallado del proceso de extracción.
- **Creación de Archivo Excel**: Plantilla preparada para almacenar los datos extraídos.

### 2. Extracción de Datos

- **Obtención de URLs y HTML**: Recibe URLs y cadenas HTML del usuario.
- **Solicitudes HTTP**: Realiza solicitudes a las URLs y registra tiempos/tamaños de respuesta.
- **Análisis y Extracción**: Usa `BeautifulSoup` para analizar y extraer datos específicos del HTML.
- **Almacenamiento de Datos**: Guarda los datos en el archivo Excel y la base de datos.

### 3. Manejo de Errores y Finalización

- **Gestión de Errores**: Captura y maneja errores durante el proceso.
- **Exportación de Datos**: Permite al usuario guardar el archivo Excel en la ubicación deseada.
- **Finalización**: Detiene la barra de carga y cierra el archivo de logs.

## Requisitos

Para utilizar esta función, asegúrate de tener las siguientes librerías instaladas:

```bash
pip install requests beautifulsoup4 openpyxl logging re tkinter
```

## Uso

### 1. Preparación

- **Datos Requeridos**: Asegúrate de tener disponibles las URLs y cadenas HTML necesarias.
- **Configuración**: Define las cadenas HTML para los elementos que deseas buscar.

### 2. Ejecución

- **Invocación**: Ejecuta la función como método de una clase que contenga las propiedades necesarias (`confirmar_url_pagina`, `elementos_pagina_html_N1`, etc.).
- **Barra de Carga**: La barra se iniciará automáticamente al comenzar la extracción y se detendrá al finalizar.

### 3. Exportación

- **Guardar Archivo**: Al concluir, el sistema abrirá un diálogo para guardar el archivo Excel en la ubicación preferida por el usuario.

## Ejemplo de Código

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

## Notas Adicionales

- **Instalación**: Verifica que todas las librerías requeridas estén instaladas y configuradas correctamente.
- **Entradas Específicas**: La función depende de configuraciones de entrada como cadenas HTML y URLs proporcionadas por el usuario.
- **Personalización**: Ajusta el código según la estructura de tu proyecto y las necesidades específicas.

## Capturas de Pantalla

| Screenshot | Screenshot |
|-----------|-----------|
| ![Screenshot 1](https://github.com/user-attachments/assets/3f8a4272-de68-47ff-9851-28e921369dc4) | ![Screenshot 2](https://github.com/user-attachments/assets/68b0ce51-fa96-4562-8d8e-b6c373da7845) |
| ![Screenshot 3](https://github.com/user-attachments/assets/87ea04f2-e7f8-4558-a09d-00f1fe97ac5d) | ![Screenshot 4](https://github.com/user-attachments/assets/02fa4548-eb04-445e-b72f-ae9c87165e16) |


![Screenshot 2024-09-02 010927](https://github.com/user-attachments/assets/baf882aa-eaad-4d5d-b42e-8478578f2c18)
![Screenshot 2024-09-02 010940](https://github.com/user-attachments/assets/fb90903e-9d1d-4bcd-b377-6f42ecca9248)



| Exporte Excel | Gui main | Visualizacion de los datos | Metricas |
|-----------|-----------|-----------|-----------|
| ![Screenshot 1](https://github.com/user-attachments/assets/3f8a4272-de68-47ff-9851-28e921369dc4) | ![Screenshot 2](https://github.com/user-attachments/assets/68b0ce51-fa96-4562-8d8e-b6c373da7845) | ![Screenshot 3](https://github.com/user-attachments/assets/baf882aa-eaad-4d5d-b42e-8478578f2c18) | ![Screenshot 4](https://github.com/user-attachments/assets/fb90903e-9d1d-4bcd-b377-6f42ecca9248) |

Esta tabla ahora muestra todos los screenshots juntos para facilitar la visualización.


---
