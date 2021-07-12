from e2e.tests.utils.hexagon_spec import as_a_user


def test_show_errors_when_invalid_yaml():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "There were 3 error(s) in your YAML",
                "",
                "cli.command -> field required",
                "",
                "envs -> field required",
                "",
                "tools.0.action -> field required",
            ]
        )
        .exit(status=1)
    )
