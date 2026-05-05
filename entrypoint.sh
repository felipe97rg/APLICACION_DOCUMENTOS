#!/bin/sh
set -e

# Espera a que la base de datos esté lista (opcional usar wait-for-it)
echo "Esperando a la base de datos..."
sleep 5

# Ejecuta migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Colecta archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Arranca el servidor Gunicorn
echo "Levantando Gunicorn..."
exec gunicorn APLICACION_DOCUMENTOS.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --log-level info
