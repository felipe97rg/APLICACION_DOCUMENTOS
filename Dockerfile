# Imagen base oficial de Python
FROM python:3.11-slim

# Variables de entorno para evitar .pyc y forzar stdout/stderr sin buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear directorio de la app
WORKDIR /app

# Instalar dependencias del sistema necesarias para PostgreSQL y Pillow
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && apt-get install -y libjpeg-dev zlib1g-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt /app/

# Instalar dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el proyecto
COPY . /app
WORKDIR /app


# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto (se sobreescribirá en docker-compose)
CMD ["gunicorn", "aplicacion_documentos.wsgi:application", "--bind", "0.0.0.0:8000"]
