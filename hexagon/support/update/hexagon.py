from hexagon.support.storage import HEXAGON_STORAGE_APP
from hexagon.support.update.shared import already_checked_for_updates
import pkg_resources
import json
import os
import subprocess
import sys
from urllib.request import urlopen
from packaging.version import parse as parse_version
from hexagon.support.printer import log
from InquirerPy import inquirer
from halo import Halo

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"
REPO_ORG = "redbeestudios"
REPO_NAME = "hexagon"


def check_for_hexagon_updates():
    if bool(os.getenv("HEXAGON_UPDATE_DISABLED")):
        return
    if already_checked_for_updates(HEXAGON_STORAGE_APP):
        return

    current_version = os.getenv(
        "HEXAGON_TEST_VERSION_OVERRIDE", pkg_resources.require("hexagon")[0].version
    )

    latest_github_release = json.load(
        urlopen(f"https://api.github.com/repos/{REPO_ORG}/{REPO_NAME}/releases/latest")
    )
    latest_github_release_version = latest_github_release["name"].replace("v", "")

    if parse_version(current_version) >= parse_version(latest_github_release_version):
        return

    log.info(
        f"New [cyan]hexagon [white]version available [green]{latest_github_release_version}[white]!"
    )

    if not inquirer.confirm("Would you like to update?", default=True).execute():
        return

    with Halo(text="Updating"):
        subprocess.check_call(
            f"{sys.executable} -m pip --disable-pip-version-check install https://github.com/{REPO_ORG}/{REPO_NAME}/releases/download/v{latest_github_release_version}/hexagon-{latest_github_release_version}.tar.gz",
            shell=True,
            stdout=subprocess.DEVNULL,
        )
    log.info("[green]🗸 [white]Updated to latest version")
    log.finish()
    sys.exit(1)
