#!/bin/bash

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

source ~/venvs/CBATfeed/bin/activate

cd $here
# curl http://www.cbat.eps.harvard.edu/unconf/tocp.xml > newtocp.xml

python cbatFeed.py

#cp cbattocp.html ~/data
scp -i $SSHKEY ./cbattocp.html $USERNAME@$HOSTNAME:$DESTDIR
