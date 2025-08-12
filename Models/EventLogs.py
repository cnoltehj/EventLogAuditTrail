from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pyparsing import Optional

class EventLog(BaseModel):
    CorrelationId: Optional[str] = None
    Event: str
    Url: str
    RequestBody: str
    ResponseBody: str
    Duration: int
    UserId: int
    TransactionId: Optional[int] = None