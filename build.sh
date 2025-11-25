#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Seed initial data (runs during deploy so you don't need shell access on Render)
# These commands are idempotent for subsequent deploys (they delete/recreate predictable demo data).
echo "Running data seeding management commands..."
python manage.py cargar_datos || echo "cargar_datos failed (continuing)"

# Asignar imágenes a bandas, países y estilos (si los archivos están en media/)
python manage.py asignar_imagenes || echo "asignar_imagenes failed (continuing)"
python manage.py asignar_imagenes_paises || echo "asignar_imagenes_paises failed (continuing)"
python manage.py asignar_imagenes_estilos || echo "asignar_imagenes_estilos failed (continuing)"

# Finalmente crear las canciones
python manage.py cargar_canciones || echo "cargar_canciones failed (continuing)"