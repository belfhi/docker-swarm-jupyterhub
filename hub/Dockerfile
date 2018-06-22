ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

RUN apt-get update && apt-get install -y libnfs11 libnfs-dev \
    git swig gcc
RUN git clone https://github.com/jupyterhub/dockerspawner.git 
RUN cd dockerspawner && /opt/conda/bin/pip install -e .
RUN /opt/conda/bin/pip install jupyterhub-ldapauthenticator==1.1 psycopg2

RUN git clone https://github.com/jiaqianjing/libnfs-python.git && \
    cd libnfs-python && /opt/conda/bin/python3.6 setup.py install

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

COPY adminlist /srv/jupyterhub/adminlist
