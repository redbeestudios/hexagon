import os
import sys
from typing import Dict

from pydantic import BaseModel, ValidationError
from ruamel.yaml import YAML

from hexagon.domain.cli import Cli
from hexagon.domain.env import Env
from hexagon.domain.tool import Tool
from hexagon.support.printer import log


class ConfigFile(BaseModel):
    cli: Cli
    envs: Dict[str, Env]
    tools: Dict[str, Tool]


class Configuration:
    def __init__(self, path: str = None):
        self.project_path = path
        self.project_yaml = None
        self.custom_tools_path = None
        self.__config_yaml = None
        self.__config = None

    def init_config(self, path: str):
        self.project_yaml = path
        self.project_path = os.path.dirname(self.project_yaml)

        __defaults = {
            "save-alias": Tool(
                long_name="Save Last Command as Linux Alias",
                type="hexagon",
                action="hexagon.tools.internal.save_new_alias",
            ),
            "create-tool": Tool(
                long_name="Create A New Tool",
                type="hexagon",
                action="hexagon.tools.internal.create_new_tool",
            ),
        }
        try:
            with open(path, "r") as f:
                self.__config_yaml = YAML().load(f)
                self.__config = ConfigFile(**self.__config_yaml)

                if self.__config.cli.custom_tools_dir:
                    self.__register_custom_tools_path()

        except FileNotFoundError:
            return self.__initial_setup_config()
        except ValidationError as errors:
            log.error("There was an error validating your YAML", errors)
            sys.exit(1)

        return (
            self.__config.cli,
            {**self.__config.tools, **__defaults},
            {**self.__config.envs},
        )

    def refresh(self):
        return self.init_config(self.project_yaml)

    def save(self):
        with open(self.project_yaml, "w") as f:
            YAML().dump(self.__config_yaml, f)
        return (
            self.__config_yaml["cli"],
            self.__config_yaml["tools"],
            self.__config_yaml["envs"],
        )

    def add_tool(self, command, config):
        self.__config_yaml["tools"].insert(
            len(self.__config_yaml["tools"]), command, config
        )
        self.__config_yaml["tools"].yaml_set_comment_before_after_key(
            command, before="\n"
        )

    def update_custom_tools_path(self, value, comment=None, position=0):
        self.__config_yaml["cli"].insert(position, "custom_tools_dir", value, comment)
        self.__register_custom_tools_path()

    def __register_custom_tools_path(self):
        self.custom_tools_path = os.path.abspath(
            os.path.join(
                self.project_path, self.__config_yaml["cli"]["custom_tools_dir"]
            )
        )
        sys.path.append(self.custom_tools_path)

    @staticmethod
    def __initial_setup_config():
        return (
            Cli(name="Hexagon", command="hexagon"),
            {
                "install": Tool(
                    long_name="Install CLI",
                    description="Install a custom project CLI from a YAML file.",
                    type="hexagon",
                    action="hexagon.tools.internal.install_cli",
                )
            },
            {},
        )
