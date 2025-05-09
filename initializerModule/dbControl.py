import subprocess


# Controls the setup for the DB container. Python Podman bindings do exist, however this is much shorter (also there are critical bugs
# in the bindings at the time of writing this)
class DBControl:

    _containerId = 0

    @staticmethod
    def startContainer(pathToMount):
        # Starting the container in detached mode with -d returns the id of said container
        # TODO this somehow changes user/permission for some content of the mounted directory, should avoid that
        idValue = subprocess.check_output(
            f"podman run --rm -d -p 27017:27017 -v '{pathToMount}:/data/db:Z' mongo",
            shell=True,
        )
        DBControl._containerId = str(idValue.decode("utf-8")).strip("\n")

    @staticmethod
    def stopContainer():
        subprocess.check_output(
            f"podman container stop {DBControl._containerId}", shell=True
        )
