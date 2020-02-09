SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 || exit ; pwd -P )"
cd "$SCRIPTPATH" || exit
if ! [[ $PYTHONPATH =~ $SCRIPTPATH ]]
then
  export PYTHONPATH=$PYTHONPATH:$SCRIPTPATH/src
fi
python -m unittest discover -s "$SCRIPTPATH"/test -t "$SCRIPTPATH"
