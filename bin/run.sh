#!/bin/bash
mongod &
BINDIR=`dirname $0`/../src
python2 $BINDIR/main.py "$@"
