FROM ubuntu:16.04

WORKDIR /usr/local/bin/

# Dependencies
RUN apt update && apt install -y \
    build-essential \
    curl \
    git samtools bedtools parallel \
    wget python3 python3-pip \
    bc build-essential libjpeg-dev \
    openjdk-8-jdk \
    g++ gfortran git \
		libffi-dev \
		libfreetype6-dev \
		libhdf5-dev \
		libjpeg-dev \
		liblcms2-dev \
		libopenblas-dev \
		liblapack-dev \
		libpng12-dev \
		libssl-dev \
		libtiff5-dev \
		libwebp-dev \
		libzmq3-dev \
		nano \
		pkg-config \
		python-dev \
		software-properties-common \
		unzip \
		vim \
		wget \
		zlib1g-dev \
		qt5-default \
		libvtk6-dev \
		zlib1g-dev \
		libjpeg-dev \
		libwebp-dev \
		libpng-dev \
		libtiff5-dev \
		libjasper-dev \
		libopenexr-dev \
		libgdal-dev \
		libdc1394-22-dev \
		libavcodec-dev \
		libavformat-dev \
		libswscale-dev \
		libtheora-dev \
		libvorbis-dev \
		libxvidcore-dev \
		libx264-dev \
		yasm \
		libopencore-amrnb-dev \
		libopencore-amrwb-dev \
		libv4l-dev \
		libxine2-dev \
		libtbb-dev \
		libeigen3-dev \
		python3-dev \
		python3-tk \
		python3-numpy \
		ant \
		default-jdk \
		doxygen \
		&& \
	rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
		python3-numpy \
		python3-scipy \
		python3-nose \
		python3-h5py \
		python3-skimage \
		python3-matplotlib \
		python3-pandas \
		python3-sklearn \
		python3-sympy \
		&& \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

RUN pip3 install pyftpdlib flask flask_socketio requests \
pandas subprocess.run \
# solve dependencies conflicts
# libs.dbees libs.bammer multiprocessing pickle
# glob subprocess os xml.etree.ElementTree src.piper_pan

RUN git clone https://github.com/bioinformagic/monica

RUN git clone https://github.com/rrwick/Porechop.git && cd Porechop && python3 setup.py install

RUN git clone https://github.com/nanoporetech/flappie &&  cd flappie && make flappie

RUN git clone --depth 1 https://github.com/nanoporetech/scrappie.git && \
        cd scappie && mkdir build && cd build && cmake .. && make && make test

RUN wget ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/ncbi-magicblast-1.4.0-x64-linux.tar.gz && \
tar xvfz ncbi-magicblast-1.4.0-x64-linux.tar.gz && cd ncbi-magicblast-1.4.0/bin && \
ln -s ./magicblast /usr/local/bin/magicblast && ln -s ./makeblastdb /usr/local/bin/makeblastdb

COPY build.sh /build.sh

COPY setup_cuda.sh /setup_cuda.sh

CMD bash build.sh
