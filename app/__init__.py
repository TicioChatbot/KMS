from flask import Flask

# Inicializa la app
app = Flask(__name__)

# Cargar la configuración
app.config.from_object('config')

# Cargar el secret key para manejar sesiones
app.secret_key = 'your_secret_key'

# Importar rutas después de inicializar la app
from app import routes
