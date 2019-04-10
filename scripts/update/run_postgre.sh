#!/usr/bin/env bash
# Run the special postgres image with automatic pg_restore
# Author: Thomas Minier

POSTGRES_PASSWORD='sage'
POSTGRES_USER='minier-t'
POSTGRES_DB='minier-t'

docker run --name some-postgres -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_DB=$POSTGRES_DB -d postgres-restore
