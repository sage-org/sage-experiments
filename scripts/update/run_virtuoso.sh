#!/usr/bin/env bash
#!/bin/bash
# Run execution time experiment for virtuoso

QUERIES=$1 # i.e. a folder that contains SPARQL queries to execute
OUTPUT=$2

if [ "$#" -ne 2 ]; then
  echo "Illegal number of parameters."
  echo "Usage: ./run_virtuoso.sh <queries-directory> <output-folder>"
  exit
fi

SERVER="http://localhost:8000/sparql"

mkdir -p $OUTPUT/results/
mkdir -p $OUTPUT/errors/

RESFILE="${OUTPUT}/execution_times_virtuoso.csv"

# init results file with headers
echo "query,time,httpCalls,nbResults,errors" > $RESFILE

for qfile in $QUERIES/*; do
  # save query name
  x=`basename $qfile`
  qname="${x%.*}"
  echo -n "${qname}," >> $RESFILE
  # execute query
  ./bin/virtuoso.js $SERVER -f $qfile -m $RESFILE > $OUTPUT/results/$qname.log 2> $OUTPUT/errors/$qname.err
  echo -n "," >> $RESFILE
  # nb results
  echo -n `wc -l ${OUTPUT}/results/${qname}.log | awk '{print $1}'` >> $RESFILE
  echo -n "," >> $RESFILE
  # nb errors during query processing
  echo `wc -l ${OUTPUT}/errors/${qname}.err | awk '{print $1}'` >> $RESFILE
done

# remove tmp folders
rm -rf $OUTPUT/errors/
