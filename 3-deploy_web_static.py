#!/usr/bin/python3
from fabric.api import put, run, local, env
from os import path
from datetime import datetime

env.hosts = ["54.208.140.192", "18.210.10.70"]
env.user = 'ubuntu'


def do_pack():
    """generates a .tgz archive from web_static folder"""
    version = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    try:
        local("mkdir -p versions")
        local(f"tar -czvf versions/web_static_{version}.tgz web_static/")

        return f"versions/web_static_{version}.tgz"

    except Exception as error:
        return None


def do_deploy(archive_path):
    """distributes an archive to web servers"""
    if not path.exists(archive_path):
        return None

    try:
        tgzfile = archive_path.split("/")[-1]
        print(tgzfile)
        filename = tgzfile.split(".")[0]
        print(filename)
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


def deploy():
    """runs the 2 functions"""
    path = do_pack()
    if not path:
        return False

    return do_deploy(path)
