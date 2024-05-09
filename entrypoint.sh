#!/bin/bash

# Wait for the database service to become available
sleep 20


# Once the database service is available, run Django migrations

python manage.py makemigrations vendor
python manage.py makemigrations purchase
python manage.py makemigrations

python manage.py migrate

# Finally, start the Django application
exec "$@"
