import subprocess

def runHexagon(args):
  return subprocess.run(args=['python', '-m', 'hexagon', *args], encoding='UTF-8')