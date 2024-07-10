#!/usr/bin/env bash
# exit on error
set -o errexit

# poetry install
pip install --upgrade pip
#pip install poetry
#poetry install

# python manage.py collectstatic --no-input
python manage.py migrate