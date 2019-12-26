#!/bin/sh
source venv/bin/activate
python models.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app
