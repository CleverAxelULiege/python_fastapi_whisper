from dataclasses import dataclass
@dataclass
class User:
    id:int
    username:str
    password:str
    uploaded_audio:str|None
    has_started_transcription:bool