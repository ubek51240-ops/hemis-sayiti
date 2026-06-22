#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Creating default users..."
export SUPERADMIN_PASSWORD="admin_password123!"
export OPERATOR_PASSWORD="operator_password123!"
python create_admin.py

echo "Build finished!"
