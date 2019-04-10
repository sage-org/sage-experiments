#!/usr/bin/env bash
# Reset a running PostgreSQL Docker container
# Author: Thomas Minier

BIGBOSS_USERNAME='ladda'
BIGBOSS_IP='172.16.8.50'
START_DB_SCRIPT='./postgre_backup/run_postgre.sh'
DOCKER_CONTAINER_NAME='some-postgres'

POSTGRES_PASSWORD='sage'
POSTGRES_USER='minier-t'
POSTGRES_DB='minier-t'

DOCKER_PID=`ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker ps -aqf "name=${DOCKER_CONTAINER_NAME}"`

ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker kill ${DOCKER_PID}
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker rm ${DOCKER_PID}
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} ${START_DB_SCRIPT}

# block until the PostgreSQL DB server has finished to load the backup
# and is ready to receive SQL queries
until ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker run --rm --link ${DOCKER_CONTAINER_NAME}:pg postgres pg_isready -U $POSTGRES_USER -h pg; do sleep 10; done

# sleep another 30 seconds, for the sake of safety (I do not trust this script at 100% )
sleep 30
