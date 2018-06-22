# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Use this file to set default values for environment variables specified in
# docker-compose configuration file.  docker-compose will substitute these
# values for environment variables in the configuration file IF the variables
# are not set in the shell environment.

# To override these values, set the shell environment variables.
export JUPYTERHUB_VERSION=0.9.0

# Name of Docker machine
export DOCKER_MACHINE_NAME=jupyterhub

# Name of Docker network
export DOCKER_NETWORK_NAME=jupyterhub-network

# Single-user Jupyter Notebook server container image
export DOCKER_NOTEBOOK_IMAGE=jupyter/scipy-notebook:03b897d05f16
#export DOCKER_NOTEBOOK_IMAGE=eosc-docker-hub.desy.de:443/reppinjo/jupyter-fix-nfs:0.25

# Image of the JupyterHub on DESY registry
#export DOCKER_HUB_IMAGE=eosc-docker-hub.desy.de:443/jupyterhub:0.1
export DOCKER_HUB_IMAGE=eosc-docker-hub.desy.de:443/reppinjo/jupyterhub-ubuntu-nfs:0.18

# the local image we use, after pinning jupyterhub version
export LOCAL_NOTEBOOK_IMAGE=eosc-docker-hub.desy.de:443/reppinjo/jupyterhub-user:0.27
#LOCAL_NOTEBOOK_IMAGE=eosc-docker-hub.desy.de:443/jupyter-fix-nfs
# Notebook directory in the container.
# This will be /home/jovyan/work if the default
# This directory is stored as a docker volume for each user
export DOCKER_NOTEBOOK_DIR=/home/jovyan/nfs

# Docker run command to use when spawning single-user containers
export DOCKER_SPAWN_CMD=start-singleuser.sh

# Name of JupyterHub container data volume
export DATA_VOLUME_HOST=jupyterhub-data

# Data volume container mount point
export DATA_VOLUME_CONTAINER=/data

# Name of JupyterHub postgres database data volume
export DB_VOLUME_HOST=jupyterhub-db-data

# Postgres volume container mount point
export DB_VOLUME_CONTAINER=/var/lib/postgresql/data

# NFS SHARE NAME
export NFS_SHARE=jupyterhub-nfs

# NFS SHARE DIR
export NFS_SHARE_DIR=/home/jovyan/nfs

# The name of the postgres database containing JupyterHub state
export POSTGRES_DB=jupyterhub

# The image of the nginx proxy
export DOCKER_NGINX_IMAGE=eosc-docker-hub.desy.de:443/reppinjo/nginx-belle:0.1
