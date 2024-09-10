# ImmuniWeb API Data Extraction Script

## Descripción

Este script en Python automatiza la extracción de datos de diferentes pestañas de un proyecto de **ImmuniWeb** utilizando su API. Está diseñado para realizar solicitudes consecutivas a la API para las pestañas **domains**, **webapps**, **network**, **mobileapps**, **incidents**, **cloud**, y **repositories**, manejando las respuestas en cola de forma eficiente y guardando los resultados en archivos `.json`. Finalmente, el script consolida los datos de todas las pestañas y los exporta a un único archivo Excel para su análisis.

## Características principales

- **Solicitudes a la API de ImmuniWeb**: El script realiza solicitudes para cada una de las pestañas del proyecto.
- **Manejo de respuestas en cola**: Si la API devuelve el mensaje que indica que la solicitud está en cola (`"This query has been added to queue..."`), el script espera 2 minutos antes de volver a intentarlo, garantizando que no se avance hasta obtener una respuesta completa.
- **Almacenamiento en archivos JSON**: Los datos de cada pestaña se guardan en archivos `.json` individuales, nombrados según la pestaña solicitada (por ejemplo, `domains.json`, `webapps.json`, etc.).
- **Consolidación de datos**: Una vez que se han solicitado y guardado todas las pestañas, el script toma los archivos `.json` y los convierte en un archivo Excel consolidado (`immuniweb_all_tabs_report.xlsx`) para facilitar su análisis.
- **Configuración de delays**: El script aplica un retraso de 2 minutos entre las solicitudes para evitar sobrecargar la API y respetar las políticas de espera de la misma.

## Requisitos

- **Python 3.x**
- **Librerías**:
  - `requests`: para realizar las solicitudes HTTP.
  - `pandas`: para la consolidación y exportación de los datos en Excel.
  - `json`: para manejar los datos en formato JSON.

### Instalación de dependencias

Instala las dependencias necesarias ejecutando:

```bash
pip install requests pandas
