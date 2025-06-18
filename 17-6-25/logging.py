from collections import defaultdict, deque
from typing import List, Dict

# Data structures
CAPACITY = 5
recent_logs = deque(maxlen=CAPACITY)
user_logs = defaultdict(list)
level_counts = defaultdict(int)

def parse_log(line: str) -> Dict:
    # Example: "[2025-06-16T10:00:00] INFO user1: Started process"
    timestamp_end = line.find(']')
    timestamp = line[1:timestamp_end]
    
    remaining = line[timestamp_end + 2:]  # Skip "] "
    level, user_msg = remaining.split(' ', 1)
    user, message = user_msg.split(':', 1)

    return {
        "timestamp": timestamp,
        "level": level,
        "user": user,
        "message": message.strip()
    }

def add_log(line: str) -> None:
    log = parse_log(line)
    recent_logs.append(log)
    user_logs[log["user"]].append(log)
    level_counts[log["level"]] += 1

def get_user_logs(user_id: str) -> List[Dict]:
    return user_logs[user_id]

def count_levels() -> Dict[str, int]:
    return dict(level_counts)

def filter_logs(keyword: str) -> List[Dict]:
    keyword = keyword.lower()
    return [log for log in recent_logs if keyword in log["message"].lower()]

def get_recent_logs() -> List[Dict]:
    return list(recent_logs)

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
# Example usage

if __name__ == "__main__":
    print("Recent Logs:")
    for log in get_recent_logs():
        print(log)

    print("\nUser Logs for 'user1':")
    for log in get_user_logs("user1"):
        print(log)

    print("\nLevel Counts:")
    print(count_levels())

    print("\nFiltered Logs containing 'connection':")
    for log in filter_logs("connection"):
        print(log)