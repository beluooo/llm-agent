from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Step:
    action: str
    observation: str
    success: bool

@dataclass
class Trace:
    task_id: str
    task_description: str
    steps: List[Step] = field(default_factory=list)
    final_result: Optional[str] = None
    completed: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_step(self, action: str, observation: str, success: bool):
        self.steps.append(Step(action=action, observation=observation, success=success))