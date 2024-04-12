#!/usr/bin/python3

"""
   fabric script that generates a .tgz archive
   from the contents of the web_static
"""

import os
from datetime import datetime
from fabric.api import local, run, put, env


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
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        uncompressed = "/data/web_static/releases/{}".format(archive_path[:-4])
        archived_file = "/tmp/{}".format(archived_file)

        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(uncompressed))
        run("sudo tar -xzf {} -C {}/".format(archived_file, uncompressed))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(uncompressed,
                                                uncompressed))
        run("sudo rm -rf {}/web_static".format(uncompressed))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(uncompressed))

        print("New version deployed!")
        return True

    else:
        return False
