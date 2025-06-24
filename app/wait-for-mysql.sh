#!/bin/sh

echo "⏳ Warten auf MySQL bei $DB_HOST..."

until mysqladmin ping -h "$DB_HOST" -uroot -p"$DB_ROOT_PASSWORD" --silent; do
  sleep 2
done

echo "✅ MySQL ist bereit – starte Gunicorn"
exec "$@"