import subprocess
from e2e.tests.utils.hexagon_spec import as_a_user
from e2e.tests.utils.path import e2e_test_folder_path
import os

test_folder_path = os.path.join(e2e_test_folder_path(__file__))


def test_seed_springboot():
    springboot_folder_path = os.path.join(test_folder_path, "springboot")

    if not os.path.exists(springboot_folder_path):
        os.mkdir(springboot_folder_path)

    (
        as_a_user(__file__)
        .run_hexagon(cwd=springboot_folder_path)
        .enter()
        .enter()
        .arrow_down()
        .carriage_return()
        .arrow_down()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .exit()
    )

    subprocess.check_call(
        "./gradlew build", shell=True, cwd=os.path.join(springboot_folder_path, "demo")
    )
