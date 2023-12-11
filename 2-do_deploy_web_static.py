#!/usr/bin/python3
from fabric.api import put, run, local, env
from os import path

env.hosts = ["54.208.140.192", "18.210.10.70"]


def do_deploy(archive_path):
    """distributes an archive to web servers"""
    if not path.exists(archive_path):
        return None

    try:
        put(archive_path, '/tmp/')

        filename = archive_path.split('/')[-1]
        release_path = f"/data/web_static/releases/{filename.split('.')[0]}"

        run(f'mkdir -p {release_path}')
        run(f"tar -xzf /tmp/{filename} -C {release_path}")

        run(f"rm /tmp/{filename}")

        current = '/data/web_static/current'
        run(f"rm -f {current}")

        run(f"ln -s {release_path} {current}")

        return True

    except Exception as error:
        return False
