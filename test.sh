SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 || exit ; pwd -P )"
cd "$SCRIPTPATH" || exit
if ! [[ $PYTHONPATH =~ $SCRIPTPATH ]]
then
  export PYTHONPATH=$PYTHONPATH:$SCRIPTPATH/src
fi
python3 -m unittest discover -s "$SCRIPTPATH"/src/test -t "$SCRIPTPATH"/src
