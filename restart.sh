#!/bin/sh

rm db/infos.db
python init.py
gunicorn -w 4 -b 0.0.0.0:8000 api:app
