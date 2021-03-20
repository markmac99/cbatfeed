#!/bin/bash

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
 
cd $here
# curl http://www.cbat.eps.harvard.edu/unconf/tocp.xml > newtocp.xml

python cbatFeed.py

cp cbattocp.html ~/data