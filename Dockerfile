FROM ubuntu:16.04

RUN apt-get clean all && apt-get update && apt-get upgrade -y && apt-get install -y  git  wget \  
python3 python3-pip samtools 

RUN pip3 install wget pyftpdlib numpy tensorflow-gpu

WORKDIR /dir_docker/

RUN git clone https://github.com/bioinformagic/monica

RUN git clone https://github.com/rrwick/Porechop.git && cd Porechop && python3 setup.py install

RUN wget ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/ncbi-magicblast-1.4.0-x64-linux.tar.gz && \ tar xvfz ncbi-magicblast-1.4.0-x64-linux.tar.gz && cd ncbi-magicblast-1.4.0/bin && \ ln -s ./magicblast /usr/local/bin/magicblast && ln -s ./makeblastdb /usr/local/bin/makeblastdb




# please add here what you think you may need 
# if you have troubles with conda you can use this as environment
# docker build -t monica_image .
# docker run -it monica_image






