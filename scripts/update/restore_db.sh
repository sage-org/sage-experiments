#!/bin/bash
# Restores a PostgreSQL DB from a backup using pg_restore
# This script must be run inside a special docker container (see Dockerfile)
# Author: Thomas Minier

INPUT='/opt/backup/watdiv10M/'
HOST=''
PORT=''
USERNAME=''

set -e

# restore database from a dump
# --host=$HOST --port=$PORT --username=$USERNAME
pg_restore -j 10 -d $POSTGRES_DB --username=$POSTGRES_USER $INPUT
