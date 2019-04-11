#!/usr/bin/env bash
# Start a SaGe server connected to a PostgreSQL server
# Author: Thomas Minier

SAGE_DOCKER_IMAGE='sage-postgre'
SAGE_CONTAINER_NAME='sage-postgres'
POSTGRES_CONTAINER_NAME='some-postgres'
NB_WORKERS='1'

docker run -p 8000:8000 -v /home/ladda/datasets:/opt/data/ --name ${SAGE_CONTAINER_NAME} --link ${POSTGRES_CONTAINER_NAME}:pg -d ${SAGE_DOCKER_IMAGE} sage /opt/data/postgre.yaml -w ${NB_WORKERS}
