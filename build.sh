echo "Creating superuser admin/admin..."
#!/usr/bin/env bash
# Salir en caso de error
set -o errexit

# Instalar gettext para compilar los mensajes de traducción
apt-get update && apt-get install -y gettext

# Instalar dependencias Python
pip install -r requirements.txt

# Compilar los mensajes de traducción (necesario para i18n en producción)
python manage.py compilemessages

# Copiar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones pendientes de la base de datos
python manage.py migrate

# Crear superusuario admin/admin si no existe
echo "Creando superusuario admin/admin..."
python - <<'PY'
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jukeBox.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@example.com'
password = 'admin'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✓ Superusuario "{username}" creado correctamente')
else:
    print(f'✓ El superusuario "{username}" ya existe')
PY

# Cargar datos iniciales (se ejecuta durante el despliegue para evitar entrada manual)
echo "Ejecutando comandos de carga de datos..."
python manage.py cargar_datos || echo "cargar_datos falló (continuando)"

# Asignar imágenes a bandas, países y estilos (si los archivos están en media/)
python manage.py asignar_imagenes || echo "asignar_imagenes falló (continuando)"
python manage.py asignar_imagenes_paises || echo "asignar_imagenes_paises falló (continuando)"
python manage.py asignar_imagenes_estilos || echo "asignar_imagenes_estilos falló (continuando)"

# Finalmente crear las canciones
python manage.py cargar_canciones || echo "cargar_canciones falló (continuando)"