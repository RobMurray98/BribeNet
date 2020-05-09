# BribeNet

BribeNet implements various models and bribing strategies for graphs of customers being influenced by bribing actors under a certain rating method. Please see the Final Report for a full discussion of the project.

4th year group project by:

* Robert Murray ([R.Murray.1@warwick.ac.uk](mailto:R.Murray.1@warwick.ac.uk))
* Finnbar Keating ([F.Keating@warwick.ac.uk](mailto:F.Keating@warwick.ac.uk))
* Callum Marvell ([C.Marvell@warwick.ac.uk](mailto:C.Marvell@warwick.ac.uk))
* Nathan Cox ([N.Cox.2@warwick.ac.uk](mailto:N.Cox.2@warwick.ac.uk))



## Prerequisites

### Operating System
It is strongly recommended to run BribeNet on a Debian-based Linux distribution such as Ubuntu. The implementation has been tested on Ubuntu 16.04 LTS through to Ubuntu 20.04 LTS. NetworKit, a core dependency of our implementation, is not supported for Windows, and is supported for MacOS but this is untested for our implementation. It may be possible to run the BribeNet GUI on Windows 10 using Windows Subsystem for Linux, Docker for Windows (using a host Docker server from within the Windows Subsystem for Linux environment) and an X server for Windows such as Xming, but this is again untested and unsupported.

### Hardware Requirements

The implementation is not especially computationally demanding and is expected to run smoothly on most modern systems. During implementation the implementation was run on a Ubuntu 16.04 LTS virtual machine given 8GB RAM and 4 virtual processing cores, but is anticipated to function well with lower specifications than this.

## Run GUI using Docker
First download the latest release of the `.tar.gz` archive of BribeNet and extract it using:
```bash
tar -xzf BribeNet-x.x.x.tar.gz
```
At the top level of the implementation directory there is the bash script `run.sh`. This script will install Docker and `x11-xserver-utils` (required for the GUI to display on the host machine). It will then enable and start the Docker daemon and service, then build and run the `Dockerfile` defined at the top level of the implementation directory. The Docker image is based off of the `python:3.7.7-slim-buster` image. In case this script does not work, we will describe the steps needed to run the GUI in a Docker container.
* `sudo apt-get install docker.io x11-xserver-utils` - installs Docker and the `xhost` command if not already installed.
* `systemctl start docker' - ensure the Docker daemon is running.
* `service docker start` - ensure the Docker service is running.
* `xhost +` - disable access control for the X window system such that the Docker container can display the GUI on the host machine.
* `docker build -t model\_gui .` - build the Docker container. Ensure you are in the same directory as the `Dockerfile` before running. The container will then be named `model\_gui:latest`.
* `docker run -it --rm -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix model\_gui` - run the Docker container. We talk through what each option does below.
    * `-it` - run in interactive mode and attach to the container.
    * `--rm` - automatically remove the container when it exits.
    * `-e DISPLAY=\$DISPLAY` - set the `DISPLAY` environment variable inside the container to be the value of the `DISPLAY` environment variable on the host machine.
    * `-v /tmp/.X11-unix/:/tmp/.X11-unix` - mount the host machine's X11 server Unix-domain socket in to the same location in the container, allowing the container to access the host's display.


## Run GUI locally
First download the latest release of the `.tar.gz` archive of BribeNet and extract it using:
```bash
tar -xzf BribeNet-x.x.x.tar.gz
```
Prior to installing the dependencies of BribeNet, make sure that the required packages are installed for the dependencies. First run `sudo apt-get update` and then install the required packages:
```bash
sudo apt-get install wget gcc g++ make cmake tk
```
As an optional step, in order to work in a clean Python environment, [install Conda](https://docs.continuum.io/anaconda/install/linux/) and create a new environment for BribeNet and activate it:
```bash
conda create -n bribe_net python=3.7
conda activate bribe_net
```
Then to install the dependencies, at the top level of the implementation directory use `pip} to install the dependencies defined in the `requirements.txt} file:
```bash
pip install -r requirements.txt
```
We can then run the GUI by running:
```bash
python src/main.py
```
If you are having issues where the application does not exit after closing all windows, you can use an alternative runner which is guaranteed to exit:
```bash
python src/docker_main.py
```

## Install as package
Prior to installing BribeNet as a package, make sure that the required packages are installed for the dependencies. First run `sudo apt-get update} and then install the required packages:
```bash
sudo apt-get install wget gcc g++ make cmake tk
```
First download the wheel of the latest release (`.whl` file) archive of BribeNet and install it using:
```bash
pip install BribeNet-x.x.x-py3-none-any.whl
```
This will automatically install the requirements as well as BribeNet. You can now import and use the entire codebase, or you can still run the GUI using:
```bash
python -m BribeNet.gui.main
```