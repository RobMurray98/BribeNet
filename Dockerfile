FROM python:3.7.5-alpine3.10
MAINTAINER Robert Murray

COPY requirements.txt /
RUN mkdir src
COPY src/* src/

# install numpy/matplotlib/scipy
RUN apk --update add --virtual scipy-runtime 
RUN apk add --virtual scipy-build build-base python-dev openblas-dev freetype-dev pkgconfig gfortran 
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h 
RUN pip install --no-cache-dir numpy 
RUN pip install --no-cache-dir matplotlib 
RUN pip install --no-cache-dir scipy 
RUN apk del scipy-build 
RUN apk add --virtual scipy-runtime freetype libgfortran libgcc libpng  libstdc++ musl openblas tcl tk 
RUN rm -rf /var/cache/apk/*

# install other requirements (networkx, networkit...)
RUN apk add cmake gcc g++ make cython python3-tkinter linux-headers libexecinfo-dev
RUN pip install -r /requirements.txt

WORKDIR src

ENTRYPOINT ["python", "main.py"]