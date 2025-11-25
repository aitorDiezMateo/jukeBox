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
python manage.py cargar_canciones || echo "cargar_canciones failed (continuing)"