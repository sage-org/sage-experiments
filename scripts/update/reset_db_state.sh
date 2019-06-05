#!/usr/bin/env bash
# Reset a running PostgreSQL database + SaGe server from a backup
# Author: Thomas Minier

BIGBOSS_USERNAME='ladda'
BIGBOSS_IP='172.16.8.50'
START_DB_SCRIPT='./postgre_backup/run_postgre.sh'
START_SAGE_SCRIPT='./postgre_backup/start_sage_server.sh'

# stop SaGe server
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} ./thomas/stop_sage.sh

# restart PostgreSQL DB

ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} /home/ladda/thomas/local/bin/pg_ctl -D /home/ladda/thomas/postgres_data -l logfile stop
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} rm -rf /home/ladda/thomas/postgres_data
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} cp -r /home/ladda/thomas/postgres_backup /home/ladda/thomas/postgres_data
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} /home/ladda/thomas/local/bin/pg_ctl -D /home/ladda/thomas/postgres_data -l logfile start

# restart SaGe
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} ./thomas/start_sage.sh
