#!/usr/bin/env bash

ROOT="./watdiv_queries"
OUT="./watdiv_tpf_ttf"

SERVER="http://172.16.8.50:5000/watdiv10M"

for qmix in $ROOT/*; do
  y=`basename $qmix`
  mkdir -p $OUT/$y
  mkdir -p $OUT/errors
  RESFILE="${OUT}/${y}/execution_times_tpf.csv"
  echo "query,time,httpCalls,serverTime,errors" > $RESFILE
  for qfile in $qmix/*; do
    x=`basename $qfile`
    qname="${x%.*}"
    echo -n "${qname}," >> $RESFILE
    gtimeout 120s ./bin/reference.js $SERVER -f $qfile -m $RESFILE > /dev/null 2> $OUT/errors/$qname.err
    echo -n "," >> $RESFILE
    # nb errors during query processing
    echo `wc -l ${OUT}/errors/${qname}.err | awk '{print $1}'` >> $RESFILE
  done
  rm -rf $OUT/errors
done
