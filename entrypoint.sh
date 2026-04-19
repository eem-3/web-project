#!/bin/sh
# entrypoint.sh
set -e  # Si la migración falla, que el contenedor se detenga

echo "Aplicando migraciones..."
uv run python ./manage.py migrate

echo "Iniciando servidor..."
exec uv run python ./manage.py runserver 0.0.0.0:8000