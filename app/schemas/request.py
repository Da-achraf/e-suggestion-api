from pydantic import BaseModel
from typing import List


class PatchDeleteReq(BaseModel):
    ids: List[int]