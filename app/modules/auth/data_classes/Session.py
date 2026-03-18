from dataclasses import dataclass
from datetime import datetime
@dataclass
class Session:
    token:str
    last_accessed_at:datetime
    user_id:int