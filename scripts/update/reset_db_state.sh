#!/usr/bin/env bash
# Reset a running PostgreSQL database + SaGe server from a backup
# Author: Thomas Minier

BIGBOSS_USERNAME='ladda'
BIGBOSS_IP='172.16.8.50'

RESET_ADDITIONS_GRAPH_SCRIPT='./thomas/reset_graph.sh'
START_SAGE_SCRIPT='./thomas/start_sage.sh'
STOP_SAGE_SCRIPT='./thomas/stop_sage.sh'

# stop SaGe server
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} ${START_SAGE_SCRIPT}

# reset additions graph back to an empty state
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} ${RESET_ADDITIONS_GRAPH_SCRIPT}

# restart SaGe
ssh ${BIGBOSS_USERNAME}@${BIGBOSS_IP} ${STOP_SAGE_SCRIPT}
