SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 || exit ; pwd -P )"
cd "$SCRIPTPATH" || exit
if ! [[ $PYTHONPATH =~ $SCRIPTPATH ]]
then
  export PYTHONPATH=$PYTHONPATH:$SCRIPTPATH/src
fi
apt-get install -y docker.io x11-xserver-utils  # ensure docker and xhost commands are available
systemctl start docker  # ensure docker daemon is running
service docker start  # ensure docker service is running
docker build -t temporal_model_gui .  # build the docker container
xhost +  # let the docker container use the host display
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix temporal_model_gui  # run the docker container
