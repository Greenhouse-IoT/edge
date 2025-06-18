# --- Fase 1: Definir la imagen base ---
# Usar una imagen oficial de Python ligera.
# python:3.9-slim es una buena opción por su tamaño reducido.
FROM python:3.9-slim

# --- Fase 2: Configurar el entorno ---
# Establecer el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Establecer variables de entorno para Python.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- Fase 3: Instalar dependencias ---
# Copiar solo el archivo de requisitos primero para aprovechar el caché de capas de Docker.
# Esta capa solo se reconstruirá si requirements.txt cambia.
COPY requirements.txt .

# Instalar las dependencias de la aplicación.
RUN pip install --no-cache-dir -r requirements.txt

# --- Fase 4: Copiar el código de la aplicación ---
# Copiar el resto del código fuente de la aplicación al directorio de trabajo.
# Los archivos listados en .dockerignore serán excluidos.
COPY . .

# --- Fase 5: Exponer el puerto ---
# Exponer el puerto 3000, que es el puerto en el que la aplicación Flask se ejecuta.
EXPOSE 3000

# --- Fase 6: Comando de ejecución ---
# El comando para iniciar la aplicación cuando se ejecute el contenedor.
# app.py usa host='0.0.0.0' lo cual es correcto para ser accesible desde fuera del contenedor.
CMD ["python", "app.py"]