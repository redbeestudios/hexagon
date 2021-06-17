import os

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from rich import print


def main(_):
    with open('last_command', 'r') as f:
        last_command = f.read()

    alias_name = inquirer.text(
        message=f"Ultimo comando: {last_command} ¿Qué alias querés crear?",
        validate=EmptyInputValidator("Es necesario ingresar un alias")
    ).execute()

    save_new_alias(alias_name, last_command)


def save_new_alias(alias_name, command):
    shell_ = os.environ['SHELL']

    shell_aliases = {
        '/usr/bin/zsh': f'{os.environ["HOME"]}/.oh-my-zsh/custom/aliases.zsh',
        '/usr/bin/bash': f'{os.environ["HOME"]}/.bash_aliases'
    }

    with open(shell_aliases[shell_], 'r+') as aliases_file:
        aliases_file.read()
        aliases_file.write(
            '\n'
            '# added by hexagon\n'
            f'alias {alias_name}="{command}"'
        )
        aliases_file.seek(0)
        __pretty_print_created_alias(aliases_file, shell_aliases[shell_], lines_to_show=-3)
        aliases_file.close()


def __pretty_print_created_alias(aliases_file, file, lines_to_show=-10):
    print('│')
    print(f'│ Added alias to {file}')
    print('┆\n')
    print("\n".join(aliases_file.read().splitlines()[lines_to_show:]))
    print('\n┆')