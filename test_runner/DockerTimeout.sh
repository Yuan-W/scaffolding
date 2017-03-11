#!/bin/bash
set -e

to=$1
shift

if [[ "$OSTYPE" == "linux-gnu" ]]; then
      TIMEPUT_TOOL="timeout"
elif [[ "$OSTYPE" == "darwin"* ]]; then
      TIMEPUT_TOOL="gtimeout"
fi

cont=$(docker run -d "$@")
code=$("$TIMEPUT_TOOL" "$to" docker wait "$cont" || true)
docker kill $cont &> /dev/null
echo -n 'status: '
if [ -z "$code" ]; then
    echo timeout
else
    echo exited: $code
fi

echo output:

docker logs $cont | sed 's/^/\t/'

docker rm $cont &> /dev/null