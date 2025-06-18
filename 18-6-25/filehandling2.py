import json
import os
from collections import defaultdict, deque
from datetime import datetime

MAX_LOGS = 5
recent_logs = deque(maxlen=MAX_LOGS)
user_logs = defaultdict(list)
level_counts = defaultdict(int)
all_logs = []

TEXT_FILE = "18-6-25/textfiles/logs.txt"
JSON_FILE = "18-6-25/textfiles/logs.json"

def parse_log_line(line):
    end = line.find(']')
    timestamp = line[1:end]
    rest = line[end + 2:]
    level, rest = rest.split(' ', 1)
    user, message = rest.split(':', 1)
    return {
        "timestamp": timestamp,
        "level": level,
        "user": user,
        "message": message.strip(),
        "raw": line.strip()
    }

def save_log_to_text(log):
    with open(TEXT_FILE, "a") as f:
        f.write(f"[{log['timestamp']}] {log['level']} {log['user']}: {log['message']}\n")

def save_all_logs_to_json():
    data = {
        "total_logs": len(all_logs),
        "last_updated": datetime.now().isoformat(),
        "logs": all_logs
    }
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_log(line):
    log = parse_log_line(line)
    recent_logs.append(log)
    user_logs[log["user"]].append(log)
    level_counts[log["level"]] += 1
    all_logs.append(log)
    save_log_to_text(log)
    save_all_logs_to_json()

def clear_files():
    if os.path.exists(TEXT_FILE):
        os.remove(TEXT_FILE)
    if os.path.exists(JSON_FILE):
        os.remove(JSON_FILE)

def show_file_info():
    if os.path.exists(TEXT_FILE):
        print(f"{TEXT_FILE}: {os.path.getsize(TEXT_FILE)} bytes")
    if os.path.exists(JSON_FILE):
        print(f"{JSON_FILE}: {os.path.getsize(JSON_FILE)} bytes")

if __name__ == "__main__":
    clear_files()

    logs = [
        "[2025-06-16T10:00:00] INFO user1: Started process",
        "[2025-06-16T10:00:01] ERROR user1: Failed to connect",
        "[2025-06-16T10:00:02] INFO user2: Login successful",
        "[2025-06-16T10:00:03] WARN user3: Low memory",
        "[2025-06-16T10:00:04] ERROR user2: Timeout occurred",
        "[2025-06-16T10:00:05] INFO user1: Retrying connection"
    ]

    for log in logs:
        add_log(log)

    show_file_info()
    print("Recent logs:")
    for log in recent_logs:
        print(log)