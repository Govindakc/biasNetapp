FROM informaticsmatters/rdkit-python3-debian:Release_2019_03_1

MAINTAINER Govinda KC<gbkc@miners.utep.edu>

USER ${UID}:${GID}
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --allow-releaseinfo-change && apt-get install -y libpango1.0-0 \
    python3-distutils \
#    python3-pip \
    libcairo2 \
    libpq-dev \
    perl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY model ./model
COPY templates ./templates
COPY requirements.txt app.py features.py run_biasnet.py ./
RUN apt update
RUN apt install -y git
#RUN apt-get install libblas-dev liblapack-dev gfortran
RUN apt-get install -y python3-scipy
RUN git clone https://github.com/Govindakc/hypopt.git
RUN cd hypopt
RUN pip install -e ./hypopt
RUN cd ../

RUN pip3 install -r requirements.txt

#ENTRYPOINT ["python3", "run_biasnet.py"]
#---------For web application --------#
ENTRYPOINT ["python3", "app.py"]
#CMD ["python3", "app.py"]
EXPOSE 5000
