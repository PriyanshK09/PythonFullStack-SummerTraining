from collections import defaultdict, deque
import functools

logs = [
    "[2025-06-16T10:00:00] INFO user1: Started process",
    "[2025-06-16T10:00:01] ERROR user1: Failed to connect",
    "[2025-06-16T10:00:02] INFO user2: Login successful",
    "[2025-06-16T10:00:03] WARN user3: Low memory",
    "[2025-06-16T10:00:04] ERROR user2: Timeout occurred",
    "[2025-06-16T10:00:05] INFO user1: Retrying connection"
]

User_Dict = defaultdict(list)
level_Dict  = defaultdict(int)
recent_logs = deque(maxlen=5)
logs_dict = {}

def add_log(log):
    user = log["user"]
    level = log["level"]
    
    recent_logs.append(log)
    User_Dict[user].append(log)
    level_Dict[level] += 1
    
    for i in logs:
        add_log(i)

print(User_Dict)
print(level_Dict)
print(recent_logs)


