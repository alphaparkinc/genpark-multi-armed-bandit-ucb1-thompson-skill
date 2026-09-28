import sys
import json
from client import MultiArmedBanditEngine

bandit = MultiArmedBanditEngine(k_arms=5)

def handle_rpc(line):
    global bandit
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-multi-armed-bandit-ucb1-thompson-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "select_arm",
                    "description": "Select the next arm to pull using UCB1 exploration-exploitation strategy",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "update_reward",
                    "description": "Report observed reward for an arm to update belief distributions",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "arm": {"type": "integer"},
                            "reward": {"type": "number"}
                        },
                        "required": ["arm", "reward"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "select_arm":
            arm = bandit.select_ucb1()
            res = {"content": [{"type": "text", "text": json.dumps({"selected_arm": arm, "current_stats": bandit.get_stats()})}]}
        elif tool_name == "update_reward":
            arm = args.get("arm", 0)
            rew = args.get("reward", 0.0)
            bandit.update(arm, rew)
            res = {"content": [{"type": "text", "text": json.dumps(bandit.get_stats())}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
