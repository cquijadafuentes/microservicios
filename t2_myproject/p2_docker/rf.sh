#!/bin/sh
echo 'Exportando ...'
export FLASK_APP=run.py
echo 'Lanzando app ...' 
flask run
echo 'fin!'