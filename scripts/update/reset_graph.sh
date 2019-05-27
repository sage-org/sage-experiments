#!/usr/bin/env bash
# reset the WatDiv additions graph in the PostgreSQL database

home/ladda/thomas/local/bin/psql -U ladda -d ladda -c 'TRUNCATE additionsgraph'
