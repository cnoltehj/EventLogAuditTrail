from pydantic import BaseModel
from datetime import datetime

from pyparsing import Optional

class EventLogModel(BaseModel):
    CorrelationId: str
    Event: str
    Url: str
    RequestBody: str
    ResponseBody: str
    Duration: int
    UserId: int
    Created: datetime
    TransactionId: Optional[int]