"""Flask application entry point for the Edge Service."""

from flask import Flask

import iam.application.services
from iam.interfaces.services import iam_api
# --- 1. Importar el nuevo blueprint ---
from edge.interfaces.services import greenhouse_api
from shared.infrastructure.database import init_db

app = Flask(__name__)

# --- 2. Registrar los blueprints ---
app.register_blueprint(iam_api)
app.register_blueprint(greenhouse_api) # <--- REGISTRAR NUEVA API

first_request = True

@app.before_request
def setup():
    """Initialize the database and create a test device before the first request."""
    global first_request
    if first_request:
        first_request = False
        init_db()
        # El setup del dispositivo de prueba puede permanecer
        auth_application_service = iam.application.services.AuthApplicationService()
        auth_application_service.get_or_create_test_device()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000) # Usar host='0.0.0.0' para que sea accesible en tu red local