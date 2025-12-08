echo "Creating superuser admin/admin..."
#!/usr/bin/env bash
# Salir en caso de error
set -o errexit

# Instalar gettext para compilar los mensajes de traducción
apt-get update && apt-get install -y gettext

# Instalar dependencias Python
pip install -r requirements.txt

# Compilar los mensajes de traducción (necesario para i18n en producción)
# Evitar que compilemessages recorra la virtualenv (.venv) y los paquetes del sistema,
# ya que eso puede causar errores en deploys donde la virtualenv está dentro del repo.
# En su lugar compilamos únicamente los .po del proyecto y de las apps dentro del repo.
echo "Compilando archivos .po del proyecto (excluyendo .venv)..."
PO_FILES=$(find . -path './.venv' -prune -o -name "django.po" -print)
if [ -z "$PO_FILES" ]; then
    echo "No se han encontrado archivos .po en el proyecto. Saltando compilación.";
else
    set -o errexit
    for po in $PO_FILES; do
        mo_dir=$(dirname "$po")
        mo_file="$mo_dir/django.mo"
        echo "Compilando $po -> $mo_file"
        msgfmt -o "$mo_file" "$po" || {
            echo "Error compilando $po";
            exit 1;
        }
    done
    echo "Compilación de .po completada.";
fi

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