import json
import random
import yaml
import alfworld.agents.environment as environment
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional

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

    def add_step(self, action, observation, success):
        self.steps.append(Step(action=action, observation=observation, success=success))

config = yaml.safe_load(open('/root/.alfworld/data/base_config.yaml'))
env = environment.get_environment('AlfredTWEnv')(config, train_eval='train')
env = env.init_env(batch_size=1)

all_traces = []

for i in range(50):
    obs, info = env.reset()
    task_desc = obs[0].split('\n\n')[-1].strip()[:100]
    trace = Trace(task_id=f"task_{i+1}", task_description=task_desc)
    print(f"\nTask {i+1}: {task_desc[:60]}")

    done = False
    steps = 0
    while not done and steps < 15:
        admissible = list(info['admissible_commands'][0])
        action = random.choice(admissible)
        obs, scores, dones, infos = env.step([action])
        success = scores[0] > 0
        trace.add_step(action=action, observation=obs[0].strip()[:150], success=success)
        done = dones[0]
        steps += 1
        info = infos

    trace.completed = done
    trace.final_result = "success" if done else "failed"
    all_traces.append(trace)
    print(f"  Result: {trace.final_result}")

output = []
for trace in all_traces:
    output.append({
        "task_id": trace.task_id,
        "task_description": trace.task_description,
        "completed": trace.completed,
        "final_result": trace.final_result,
        "timestamp": trace.timestamp,
        "steps": [{"action": s.action, "observation": s.observation, "success": s.success} for s in trace.steps]
    })

with open('/root/alfworld_traces.json', 'w') as f:
    json.dump(output, f, indent=2)

successful = sum(1 for t in all_traces if t.completed)
print(f"\nSaved 50 traces to alfworld_traces.json")
print(f"Success rate: {successful}/50")
