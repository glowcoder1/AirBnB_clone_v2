#!/usr/bin/env python3

"""
   fabric script that generates a .tgz archive
   from the contents of the web_static
"""

import os
from datetime import datetime
from fabric.api import local, runs_once

@runs_once
def do_pack():
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
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
        print("Packing web_static to {}".format(curr_version))
        local("tar -cvzf {} web_static".format(curr_version))
        size = os.stat(curr_version).st_size
        print("web_static packed: {} -> {} Bytes".format(curr_version, size))
    except Exception:
        curr_version = None
    return curr_version
