#!/usr/bin/python3

"""
   fabric script that generates a .tgz archive
   from the contents of the web_static
"""

import os
from datetime import datetime
from fabric.api import local, run, put, env


env.hosts = ["100.26.244.115", "52.206.162.79"]
env.user = "ubuntu"


def do_pack():
    """Archives the static files and returns path if successful."""
    local("mkdir -p versions")
    d_time = datetime.now()
    curr_version = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        d_time.year,
        d_time.month,
        d_time.day,
        d_time.hour,
        d_time.minute,
        d_time.second
    )
    try:
        local("tar -cvzf {} web_static".format(curr_version))
    except Exception:
        curr_version = None
    return curr_version


def do_deploy(archive_path):
    """distributes an archive to web servers"""
    if os.path.isfile(archive_path) is False:
        return False
    try:
        archived_file = archive_path.split("/")[-1]
        no_ext = archived_file.split(".")[0]
        uncompressed = "/data/web_static/releases/{}".format(no_ext)
        archived_file = "/tmp/{}".format(archived_file)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(uncompressed))
        run("tar -xzf {} -C {}/".format(archived_file, uncompressed))
        run("rm {}".format(archived_file))
        run("mv {}/web_static/* {}/".format(uncompressed, uncompressed))
        run("rm -rf {}/web_static".format(uncompressed))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(uncompressed))

        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
