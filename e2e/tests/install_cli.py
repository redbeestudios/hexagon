from e2e.tests.utils.path import e2e_test_folder_path
from e2e.tests.utils.assertions import assert_process_output
from e2e.tests.utils.run import discard_output, run_hexagon_e2e_test, write_to_process
import os

aliases_file_path = os.path.realpath(os.path.join(
    __file__, os.path.pardir, os.path.pardir, 'install_cli', 'home-aliases.txt'))


def test_install_cli():
    with open(aliases_file_path, 'w') as file:
        file.write('previous line\n')

    process = run_hexagon_e2e_test(
        __file__,
        env={
            'HEXAGON_TEST_SHELL': 'HEXAGON_TEST_SHELL'
        }
    )
    assert_process_output(process, [
        '╭╼ Hexagon',
        '│',
        '│ This looks like your first time running Hexagon.',
        '│ You should probably run "Install CLI".',
        '│',
        '[?2004h[?1l[?25l[0m[?7l[0m[J[0;38;5;180m?[0m Hi, which tool would you like to use today?[0m',
        '[0;38;5;240m┌──────────────────────────────────────────────────────────────────────────────',
        '',
        '[0;38;5;240m│[0;38;5;176m❯ [0m  [0;38;5;73m1/1[0m',
        '',
        '[0;38;5;240m│[0;38;5;75m❯[0;38;5;180m [0;38;5;75m⬡ Install CLI                                               Install a custom',  # noqa: E501
        '',
        '[0;38;5;240m└──────────────────────────────────────────────────────────────────────────────',
        '',
    ])
    write_to_process(process, '\n')
    assert_process_output(process, [
        '[0m [3A[3C[?7h[0m[?12l[?25h[?25l[?7l[2A[3D[0m[J[0;38;5;180m?[0m Hi, which tool would you like to use today?[0;38;5;75m ⬡ Install CLI',  # noqa: E501
        '',
        '',
        '[J[?7h[0m[?12l[?25h[?2004l[?2004h[?1l[?25l[0m[?7l[0m[J[0;38;5;180m?[0m Where is your project\'s hexagon config file? [0;38;5;108m',  # noqa: E501
        '',
        '[0;38;5;108minstall_cli[0m',
    ])
    discard_output(process, 5)
    write_to_process(process, '/config.yml\n')
    assert_process_output(
        process,
        [
            '│ Added alias to home-aliases.txt',
            '┆',
            '',
            '',
            '# added by hexagon',
            'alias hexagon-test="HEXAGON_CONFIG_FILE=',
            '',
            '',
            '┆',
            '│',
            '╰╼',
        ],
        discard_until_initial=True
    )

    with open(aliases_file_path, 'r') as file:
        assert file.read() == f'previous line\n\n# added by hexagon\nalias hexagon-test="HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config.yml")} hexagon"'  # noqa: E501
