# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
#c.JupyterHub.spawner_class = 'dockerspawner.SwarmSpawner'
from dockerspawner import SwarmSpawner
c.JupyterHub.spawner_class = SwarmSpawner
# Spawn containers from this image
notebook_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
c.SwarmSpawner.image = notebook_image
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
## An optional hook function that you can implement to do some bootstrapping work
#  before the spawner starts. For example, create a directory for your user or
#  load initial content.
#  
#  This can be set independent of any concrete spawner implementation.
#  
#  Example::
#  
#from subprocess import check_call
#def my_hook(spawner):
#    username = spawner.user.name
#    check_call(['./examples/bootstrap-script/bootstrap.sh', username])
# in jupyterhub_config.py  
import os
import libnfs
def create_dir_hook(spawner):
    username = spawner.user.name # get the username
    #volume_path = os.path.join('/volumes/jupyterhub', username)
    nfs = libnfs.NFS('nfs://koben-tsvm/nfs4_ostack')
    volume_path = os.path.join('/users/', username)
    if not nfs.isdir(volume_path):
        # create a directory with umask 0755 
        # hub and container user must have the same UID to be writeable
        # still readable by other users on the system
        nfs.mkdir(volume_path) #, 0o755)
        # now do whatever you think your user needs
        # ...
        #pass

c.SwarmSpawner.pre_spawn_hook = create_dir_hook
#c.Spawner.pre_spawn_hook = None
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.SwarmSpawner.cmd = spawn_cmd
#c.SwarmSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.SwarmSpawner.use_internal_ip = True
c.SwarmSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.SwarmSpawner.extra_host_config = { 'network_mode': network_name }
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
#nfs_share_dir = os.environ.get('NFS_SHARE_DIR') or '/home/jovyan/nfs'
#nfs_share_dir = os.environ.get('NFS_SHARE_DIR') or '/home/jovyan/nfs'
#c.SwarmSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
#c.SwarmSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir}#, '/mnt/nfs/{username}': nfs_share_dir}
#c.SwarmSpawnervolumes = { 'jupyterhub-user-{username}': notebook_dir, '/mnt/nfs-share/{username}': nfs_share_dir}
#c.SwarmSpawner.extra_create_kwargs.update({ 'driver_opts': {'type': 'nfs', 'o': 'addr=koben-tsvm,nolock,rw', 'device': ':/nfs4_ostack/users/{username}'}})
#c.SwarmSpawner.extra_create_kwargs.update({ 'volume_driver': 'nfs' , 'o':'addr=koben-tsvm,nolock,rw', 'device':':nfs4_ostack/users/{username}'})

mounts = [{'type': 'volume',
           'source': 'jupyterhub-user-{username}',
           'target': notebook_dir,
        'no_copy' : True,
        'driver_config' : {
          'name' : 'local',
          'options' : {
             'type' : 'nfs4',
             'o' : 'addr=koben-tsvm,rw',
             'device' : ':/nfs4_ostack/users/{username}/'
           }
        },
}]
c.SwarmSpawner.mounts = mounts
#
#c.SwarmSpawner.container_spec = {
#    # The command to run inside the service
#    'args': spawn_cmd, #'/usr/local/bin/start-singleuser.sh'],  # (string or list)
#    'Image': notebook_image, #'jupyter/datascience-notebook:latest',
#    # Replace mounts with [] to disable permanent storage
#    'mounts': mounts
#}
#
#c.SwarmSpawner.resource_spec = {
#    # (int)  CPU limit in units of 10^9 CPU shares.
#    'cpu_limit': int(1 * 1e9),
#    # (int)  Memory limit in Bytes.
#    'mem_limit': int(512 * 1e6),
#    # (int)  CPU reservation in units of 10^9 CPU shares.
#    'cpu_reservation': int(1 * 1e9),
#    # (int)  Memory reservation in bytes
#    'mem_reservation': int(512 * 1e6),
#}
# Remove containers once they are stopped
c.SwarmSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.SwarmSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8080

# redirect to https EDIT: let nginx do that
#c.ConfigurableHTTPProxy.command = ['configurable-http-proxy', '--redirect-port', '80']

# EDIT: let nginx do the SSL 
# TLS config
#import socket
#pub_ip = socket.gethostbyname(socket.gethostname())
#c.JupyterHub.ip = pub_ip.JupyterHub.port = 443
c.JupyterHub.port = 8000
#c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Authenticate users with the LDAP JupyterHub plugin
c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = 'it-ldap-slave.desy.de'
c.LDAPAuthenticator.bind_dn_template = 'uid={username},ou=people,ou=rgy,o=desy,c=de' # from "ldapsearch -x sn=username" result
c.LDAPAuthenticator.lookup_dn = True
c.LDAPAuthenticator.use_ssl = False
c.LDAPAuthenticator.server_port = 1389

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

# Whitlelist admins
c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True
pwd = os.path.dirname(__file__)
with open(os.path.join(pwd, 'adminlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        admin.add(name)
