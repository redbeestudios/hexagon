import sys
from hexagon.cli.args import fill_args


def main(env_values):
    _, _tool = fill_args(sys.argv, 2)
    print(f"executed {_tool} with env args:")
    for env_value in env_values:
        print(env_value)
