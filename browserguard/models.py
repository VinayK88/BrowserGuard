from dataclasses import dataclass, asdict
from enum import Enum

class Decision(str, Enum):
    NORMAL='NORMAL'; REVIEW='REVIEW'; HIGH_RISK='HIGH_RISK'; CRITICAL='CRITICAL'

@dataclass(frozen=True)
class Extension:
    ext_id:str; name:str; publisher_verified:bool; permissions:tuple[str,...]
    permission_delta:int; update_channel:str; age_days:int; active_users:int
    session_access:bool; cookie_access:bool; ai_assistant:bool; external_posting:bool
    oauth_bridge:bool; observed_events:int; baseline_events:int; expected:Decision

@dataclass(frozen=True)
class Assessment:
    ext_id:str; name:str; decision:Decision; risk_score:int; api_ratio:float
    users_exposed:int; reasons:list[str]; actions:list[str]
    def to_dict(self):
        d=asdict(self); d['decision']=self.decision.value; return d
