#!/usr/bin/env bash
# Creates a backup of a PostgreSQL DB using pg_dump
# Author: Thomas Minier

DBNAME=''
HOST=''
PORT=''
USERNAME=''
OUTPUT=''

pg_dump -F d -f $OUTPUT -j 10 --host=$HOST --port=$PORT --username=$USERNAME $DBNAME
