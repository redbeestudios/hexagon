import os

from .configuration import Configuration
from .options import get_hexagon_options

CONFIG_FILE_ENV_VARIABLE_NAME = "HEXAGON_CONFIG_FILE"


configuration = Configuration()
cli, tools, envs = configuration.init_config(
    os.getenv(CONFIG_FILE_ENV_VARIABLE_NAME, "app.yaml")
)
get_options = get_hexagon_options
