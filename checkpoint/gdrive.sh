#!/bin/bash

SOURCE="$1"
if [ "${SOURCE}" == "" ]; then
    echo "Must specify a source url"
    exit 1
fi

DEST="$2"
if [ "${DEST}" == "" ]; then
    echo "Must specify a destination filename"
    exit 1
fi

FILEID=$(echo $SOURCE | rev | cut -d= -f1 | rev)
COOKIES=$(mktemp)

CODE=$(wget --save-cookies $COOKIES --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=${FILEID}" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/Code: \1\n/p')

# cleanup the code, format is 'Code: XXXX'
CODE=$(echo $CODE | rev | cut -d: -f1 | rev | xargs)

wget --load-cookies $COOKIES "https://docs.google.com/uc?export=download&confirm=${CODE}&id=${FILEID}" -O $DEST

rm -f $COOKIES
