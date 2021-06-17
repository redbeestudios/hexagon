from os import chdir
from e2e import run_hexagon

def test_install_cli():
  chdir('../install_cli')
  run_hexagon()