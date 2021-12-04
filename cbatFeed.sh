#!/bin/bash

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
source ~/venvs/CBATfeed/bin/activate
source $here/config.ini

cd $here
# curl http://www.cbat.eps.harvard.edu/unconf/tocp.xml > newtocp.xml
python $here/cbatFeed.py

scp -i $SSHKEY ./cbattocp.html $USERNAME@$HOSTNAME:$DESTDIR
