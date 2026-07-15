# test_connection.py (en la raíz, temporal, se borra después)
import os
from dotenv import load_dotenv
from supabase import create_client

# abre el archivo .env y carga las variables de entorno
load_dotenv()
# variable de entorno extraídas del archivo .env
url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_ANON_KEY"]
# Cleinte de supabase, se conecta a la base de datos(tiene las credenciales de la base de datos)
client = create_client(url, key)
# peticion a la base de datos, selecciona todos los registros de la tabla quizzes y ejecuta la consulta
# .execute() es el metodo que ejecuta la consulta y devuelve la respuesta de la base de datos
response = client.table("quizzes").select("*").execute()
# .data es el atributo que contiene los datos de la respuesta de la base de datos.
# Existen otros atributos como .status_code, .error, .count, etc.
# print(response.data)
