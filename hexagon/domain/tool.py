from typing import Optional, Dict, Any

from pydantic import BaseModel


class Tool(BaseModel):
    action: str
    type: str = "misc"
    alias: Optional[str] = None
    long_name: Optional[str] = None
    description: Optional[str] = ""
    envs: Optional[Dict[str, Any]] = None
