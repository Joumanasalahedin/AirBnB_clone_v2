#!/usr/bin/python3
"""Fabric script generates a .tgz archive"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """generates a .tgz archive from web_static folder"""
    version = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    try:
        local("mkdir -p versions")
        local(f"tar -czvf versions/web_static_{version}.tgz web_static/")

        return f"versions/web_static_{version}.tgz"

    except Exception as error:
        return None
