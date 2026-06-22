import json
from trace import Trace
from kitchen import KitchenEnvironment

TASKS = [
    {
        "id": "task_1",
        "description": "Open the fridge",
        "steps": ["open_fridge"]
    },
    {
        "id": "task_2",
        "description": "Get milk from the fridge",
        "steps": ["open_fridge", "grab_milk"]
    },
    {
        "id": "task_3",
        "description": "Make toast",
        "steps": ["grab_bread", "turn_on_toaster"]
    },
    {
        "id": "task_4",
        "description": "Get a plate out",
        "steps": ["get_plate"]
    },
    {
        "id": "task_5",
        "description": "Get buttered toast",
        "steps": ["open_fridge", "grab_butter", "grab_bread", "turn_on_toaster", "get_plate"]
    },
    {
        "id": "task_6",
        "description": "Boil the kettle",
        "steps": ["turn_on_kettle"]
    },
    {
        "id": "task_7",
        "description": "Make tea",
        "steps": ["turn_on_kettle", "get_cup"]
    },
    {
        "id": "task_8",
        "description": "Full breakfast prep",
        "steps": ["open_fridge", "grab_milk", "grab_butter", "grab_bread", "turn_on_toaster", "get_plate", "turn_on_kettle", "get_cup"]
    },
]

def run_all_tasks():
    env = KitchenEnvironment()
    all_traces = []

    for task in TASKS:
        env.reset()
        trace = Trace(task_id=task["id"], task_description=task["description"])

        print(f"\nRunning: {task['description']}")

        for action in task["steps"]:
            observation, success = env.act(action)
            trace.add_step(action=action, observation=observation, success=success)
            print(f"  {action} -> {observation}")

        trace.completed = all(step.success for step in trace.steps)
        trace.final_result = "success" if trace.completed else "failed"
        all_traces.append(trace)

        print(f"  Result: {trace.final_result}")

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

    with open("traces.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nTraces saved to traces.json")

if __name__ == "__main__":
    traces = run_all_tasks()
    save_traces(traces)