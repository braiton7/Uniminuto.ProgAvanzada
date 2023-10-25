import requests

# Define la URL de la ruta /productos
url = 'http://127.0.0.1:4000/productos'

# Define el token que obtuviste durante el inicio de sesión
token = 'f00633b24e8d033ef41810db1532f3cdcd0cf43bd1f816836c052e9bc0c8487f'  # Reemplaza 'tu_token_aqui' con el token real

# Configura los encabezados de autorización con el token
headers = {'Authorization': f'Bearer {token}'}

# Realiza una solicitud GET a la ruta /productos con el token
response = requests.get(url, headers=headers)

# Verifica la respuesta
if response.status_code == 200:
    # La solicitud fue exitosa, y los datos de productos están en response.json()
    data = response.json()
    print(data)
else:
    # La solicitud no fue exitosa, imprime el mensaje de error
    print(f"Error: {response.status_code} - {response.json()}")
