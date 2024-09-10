import requests
import json
import time
import pandas as pd

# Configuración de autenticación API y URL
api_key_id = 'ADD API ID KEY HERE'
api_secret_key = 'ADD SECRET API KEY HERE'
url = 'https://portal.immuniweb.com/API/discovery/json/'
discovery_id = 'ADD DISCOVERY PROJECT ID  HERE'

# Lista de pestañas que queremos solicitar
tabs = ['domains', 'webapps', 'network', 'mobileapps', 'incidents', 'cloud', 'repositories']

# Función para hacer la solicitud de una pestaña y esperar hasta obtener datos
def request_tab(tab_name):
    print(f"Solicitando datos de la pestaña: {tab_name}")
    payload = {
        'discovery_id': discovery_id,
        f'tabs[]': [tab_name]
    }

    while True:
        response = requests.post(url, auth=(api_key_id, api_secret_key), data=payload)

        # Si la respuesta indica que la consulta está en cola, esperamos y reintentamos
        if response.status_code == 200:
            data = response.json()
            if data.get("res") == 1:
                print(f"La consulta está en cola para la pestaña {tab_name}. Esperando 1 minuto antes de reintentar...")
                time.sleep(60)  # Esperamos 2 minutos
            else:
                # Si tenemos una respuesta válida, la guardamos en un archivo JSON
                with open(f'{tab_name}.json', 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                print(f"Datos de {tab_name} guardados en {tab_name}.json")
                break
        else:
            print(f"Error al solicitar la pestaña {tab_name}: {response.status_code}")
            break

# Iterar sobre las pestañas con un delay de 2 minutos entre cada una
for tab in tabs:
    request_tab(tab)
    print(f"Esperando 1 minuto antes de solicitar la siguiente pestaña...")
    time.sleep(60)  # Delay de 2 minutos entre solicitudes de pestañas

# Consolidar los archivos JSON en un archivo Excel
def json_to_excel():
    all_data = []

    for tab in tabs:
        file_name = f'{tab}.json'
        try:
            with open(file_name, 'r') as json_file:
                data = json.load(json_file)

                # Si el JSON contiene datos para la pestaña
                if tab in data and isinstance(data[tab], list):
                    for entry in data[tab]:
                        entry['Tab'] = tab  # Añadir una columna para identificar la pestaña
                        all_data.append(entry)

        except FileNotFoundError:
            print(f"No se encontró el archivo {file_name}, saltando...")
    
    # Convertir a DataFrame de pandas
    df = pd.DataFrame(all_data)
    
    # Guardar en un archivo Excel
    df.to_excel('immuniweb_CTI_report.xlsx', index=False)
    print("Reporte consolidado generado como 'immuniweb_CTI_report.xlsx'.")

# Llamar a la función para consolidar los archivos JSON en Excel
json_to_excel()
