#!/usr/bin/python3
from fabric.api import put, run, local, env
from os import path

env.hosts = ["54.208.140.192", "18.210.10.70"]


def do_deploy(archive_path):
    """distributes an archive to web servers"""
    if not path.exists(archive_path):
        return None

    try:
        tgzfile = archive_path.split("/")[-1]
        filename = tgzfile.split(".")[0]
        pathname = "/data/web_static/releases/" + filename

        put(archive_path, '/tmp/')
        run(f"mkdir -p /data/web_static/releases/{filename}/")
        run(f"""tar -zxvf /tmp/{tgzfile} -C
            /data/web_static/releases/{filename}/""")
        run(f"rm /tmp/{tgzfile}")
        run(f"mv /data/web_static/releases/{filename}/web_static/*\
            /data/web_static/releases/{filename}/")
        run(f"rm -rf /data/web_static/releases/{filename}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"""ln -s /data/web_static/releases/{filename}/
            /data/web_static/current""")

        return True

    except Exception as error:
        return False
