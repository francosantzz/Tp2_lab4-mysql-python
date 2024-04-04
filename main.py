import requests
import mysql.connector

# Conexión a la base de datos
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lab4apirest"
)
cursor = db_connection.cursor()

# Iterar sobre los códigos de país (desde 1 hasta 300)
for calling_code in range(1, 301):
    url = f"https://restcountries.com/v2/callingcode/{calling_code}"
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()

        # Iterar sobre los datos recibidos
        for country_data in data:
            # Construir el diccionario con los datos del país
            pais = {
                'numericCode': country_data.get('numericCode', 0),
                'nombrePais': country_data.get('name', ''),
                'capitalPais': country_data.get('capital', ''),
                'region': country_data.get('region', ''),
                'poblacion': country_data.get('population', 0),
                'latitud': country_data.get('latlng', [0, 0])[0],
                'longitud': country_data.get('latlng', [0, 0])[1]
            }

            # Insertar los datos en la tabla Pais
            insert_query = """INSERT INTO pais (codigoPais, nombrePais, capitalPais, region, poblacion, latitud, longitud)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)
                              ON DUPLICATE KEY UPDATE
                              nombrePais = VALUES(nombrePais),
                              capitalPais = VALUES(capitalPais),
                              region = VALUES(region),
                              poblacion = VALUES(poblacion),
                              latitud = VALUES(latitud),
                              longitud = VALUES(longitud)"""
            insert_values = (pais['numericCode'], pais['nombrePais'], pais['capitalPais'], pais['region'], pais['poblacion'], pais['latitud'], pais['longitud'])
            cursor.execute(insert_query, insert_values)
            db_connection.commit()

            print(f"Datos migrados para el país con código de llamada {calling_code}")
    else:
        print(f"No se pudo obtener datos para el país con código de llamada {calling_code}")

# Cerrar la conexión a la base de datos
cursor.close()
db_connection.close()