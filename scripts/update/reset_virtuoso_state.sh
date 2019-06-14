#!/usr/bin/env bash
# Reset a running Virtuoso database
# Author: Thomas Minier

BIGBOSS_USERNAME='ladda'
BIGBOSS_IP='172.16.8.50'
START_VIRTUSO_SCRIPT='./ladda/run-virtuso.sh'
VIRTUOSO_DOCKER_ID_FILE='/home/ladda/virtuoso-docker-id'

VIRTUOSO_DATA='/home/ladda/docker-containers/data'
VIRTUOSO_BACKUP='/home/ladda/docker-containers/backup'

# stop Virtuoso server
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker kill `cat /home/ladda/virtuoso-docker-id`
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} docker rm `cat /home/ladda/virtuoso-docker-id`

# restart Virtuoso state
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} rm -rf ${VIRTUOSO_DATA}
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} cp -r ${VIRTUOSO_BACKUP} ${VIRTUOSO_DATA}

# restart Virtuoso
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} ${START_VIRTUSO_SCRIPT}
