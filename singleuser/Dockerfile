ARG DOCKER_NOTEBOOK_IMAGE
FROM $DOCKER_NOTEBOOK_IMAGE
ARG JUPYTERHUB_VERSION
RUN /opt/conda/bin/pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION
#ENTRYPOINT ['start-singleuser.sh']
