from typing import Optional

from pydantic import BaseModel, DirectoryPath


class Cli(BaseModel):
    name: str
    command: str
    custom_tools_dir: Optional[DirectoryPath]
