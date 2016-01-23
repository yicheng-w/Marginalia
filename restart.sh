#!/bin/sh

rm db/infos.db
python init.py
gunicorn -w 4 -b 10 api-gunicorn:app
