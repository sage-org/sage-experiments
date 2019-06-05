#!/bin/bash

NBRUNS=(1 2 3)
NBCLIENTS=(1 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100)

for run in ${NBRUNS[@]}; do
  RESDIR="/home/minier/jsw2019-watdiv-sage-1s/run${run}"
  mkdir -p $RESDIR
  for nb in ${NBCLIENTS[@]}; do
    python3 scripts/run_load.py watdiv_queries/ $RESDIR $nb sage
    # ./scripts/update/reset_db_state.sh > /dev/null
  done
done
