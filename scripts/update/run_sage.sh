#!/usr/bin/env bash
#!/bin/bash
# Run experiments for Sage

QUERIES=$1 # i.e. a folder that contains SPARQL queries to execute
OUTPUT=$2

if [ "$#" -ne 2 ]; then
  echo "Illegal number of parameters."
  echo "Usage: ./run_sage.sh <queries-directory> <output-folder>"
  exit
fi

SERVER="http://172.16.8.50:8000/sparql/watdiv"

mkdir -p $OUTPUT
mkdir -p $OUTPUT/results/
mkdir -p $OUTPUT/errors/

RESFILE="${OUTPUT}/execution_times_sage.csv"

# init results file with headers
echo "query,time,httpCallsRead,httpCallsWrite,serverTimeRead,serverTimeWrite,resumeTimeRead,resumeTimeWrite,suspendTimeRead,suspendTimeWrite,errors" > $RESFILE

# execute inserts first
for qfile in $QUERIES/inserts/*; do
  x=`basename $qfile`
  qname="${x%.*}"
  # save query name
  echo -n "${qname}," >> $RESFILE
  # execute query
  timeout 30m ./bin/sage-jena-1.1/bin/sage-jena $SERVER --update -f $qfile -m $RESFILE > /dev/null 2> ${OUTPUT}/errors/${qname}.err
  echo -n "," >> $RESFILE
  # save nb errors during query processing
  echo `wc -l ${OUTPUT}/errors/${qname}.err | awk '{print $1}'` >> $RESFILE
done

# execute delete last
for qfile in $QUERIES/deletes/*; do
  x=`basename $qfile`
  qname="${x%.*}"
  # save query name
  echo -n "${qname}," >> $RESFILE
  # execute query
  timeout 30m ./bin/sage-jena-1.1/bin/sage-jena $SERVER --update -f $qfile -m $RESFILE > /dev/null 2> ${OUTPUT}/errors/${qname}.err
  echo -n "," >> $RESFILE
  # save nb errors during query processing
  echo `wc -l ${OUTPUT}/errors/${qname}.err | awk '{print $1}'` >> $RESFILE
done

# remove tmp folders
rm -rf $OUTPUT/errors/ $OUTPUT/results/
