import datetime
from pydantic.main import BaseModel


class UpdateOptions(BaseModel):
    time_between_checks: datetime.timedelta


update_options_keys = ["time_between_checks"]
default_update_options = UpdateOptions(time_between_checks=datetime.timedelta(days=1))
