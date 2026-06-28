import json
import random
from trace import Trace
import gymnasium as gym
import minigrid

ENVIRONMENTS = [
    "MiniGrid-Empty-5x5-v0",
    "MiniGrid-Empty-8x8-v0",
    "MiniGrid-DoorKey-5x5-v0",
    "MiniGrid-FourRooms-v0",
    "MiniGrid-LavaGapS5-v0",
]

ACTION_NAMES = {
    0: "turn_left",
    1: "turn_right",
    2: "move_forward",
    3: "pickup",
    4: "drop",
    5: "toggle",
    6: "done"
}

def run_tasks(num_traces=50):
    all_traces = []
    task_count = 0

    while task_count < num_traces:
        env_name = random.choice(ENVIRONMENTS)
        env = gym.make(env_name)
        obs, info = env.reset()

        trace = Trace(
            task_id=f"task_{task_count + 1}",
            task_description=f"Complete {env_name}"
        )

        print(f"\nTask {task_count + 1}: {env_name}")

        done = False
        steps = 0
        total_reward = 0

        while not done and steps < 20:
            action = env.action_space.sample()
            action_name = ACTION_NAMES.get(action, f"action_{action}")
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            total_reward += reward
            success = reward > 0
            trace.add_step(
                action=action_name,
                observation=f"reward={reward:.2f} done={done}",
                success=success
            )
            steps += 1

        trace.completed = total_reward > 0
        trace.final_result = "success" if total_reward > 0 else "failed"
        all_traces.append(trace)
        task_count += 1
        print(f"  Steps: {steps}, Result: {trace.final_result}")
        env.close()

    return all_traces

def save_traces(traces):
    output = []
    for trace in traces:
        output.append({
            "task_id": trace.task_id,
            "task_description": trace.task_description,
            "completed": trace.completed,
            "final_result": trace.final_result,
            "timestamp": trace.timestamp,
            "steps": [
                {"action": s.action, "observation": s.observation, "success": s.success}
                for s in trace.steps
            ]
        })

    with open("minigrid_traces.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved {len(traces)} traces to minigrid_traces.json")

if __name__ == "__main__":
    traces = run_tasks(num_traces=50)
    save_traces(traces)
    successful = sum(1 for t in traces if t.completed)
    print(f"Success rate: {successful}/{len(traces)} ({100*successful//len(traces)}%)")