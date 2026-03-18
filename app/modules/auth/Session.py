from dataclasses import dataclass
@dataclass
class Session:
    token:str
    last_accessed_at:str
    user_id:int