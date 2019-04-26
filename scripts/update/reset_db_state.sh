#!/usr/bin/env bash
# Reset a running PostgreSQL Docker container
# Author: Thomas Minier

BIGBOSS_USERNAME='ladda'
BIGBOSS_IP='172.16.8.50'
START_DB_SCRIPT='./postgre_backup/run_postgre.sh'
START_SAGE_SCRIPT='./postgre_backup/start_sage_server.sh'
SAGE_CONTAINER_NAME='sage-postgres'
POSTGRES_CONTAINER_NAME='some-postgres'

POSTGRES_PASSWORD='sage'
POSTGRES_USER='minier-t'
POSTGRES_DB='minier-t'

# stop SaGe server
# we need to completely remove the container as the link with the postgre container
# will be broken when re-building it.
SAGE_PID=`ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker ps -aqf "name=${SAGE_CONTAINER_NAME}"`
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker kill ${SAGE_PID}
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker rm ${SAGE_PID}

# restart PostgreSQL DB
# we need to kill, delete and recreate the whole container
# to ensure that the DB goes back in its initial state
POSTGRES_PID=`ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker ps -aqf "name=${POSTGRES_CONTAINER_NAME}"`

ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker kill ${POSTGRES_PID}
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker rm ${POSTGRES_PID}
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} ${START_DB_SCRIPT}

# block until the PostgreSQL DB server has finished to load the backup
# and is ready to receive SQL queries
until ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker run --rm --link ${POSTGRES_CONTAINER_NAME}:pg postgres pg_isready -U $POSTGRES_USER -h pg; do sleep 10; done

# restart SaGe server
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} ${START_SAGE_SCRIPT}

# sleep another 10 seconds, for the sake of safety (I do not trust this script at 100% )
sleep 10
