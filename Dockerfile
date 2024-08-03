FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos y el script de inicialización de la base de datos
COPY requirements.txt requirements.txt
COPY init_db.sql init_db.sql

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Comando para iniciar la aplicación
cMD ["python", "app.py"]
