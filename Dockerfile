FROM python:3.8-alpine

ENV PYTHONUNBUFFERED=1
# Crear un directorio para la app
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el resto del código de la app
COPY . ./

# Comando para iniciar la app
CMD ["python3", "app_model_db.py"]