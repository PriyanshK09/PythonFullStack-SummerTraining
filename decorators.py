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

def parse_log(add_log):
    def wrapper(log):
        arr=log.split(" ", 3)
        timestamp = arr[0].strip("[]")
        level = arr[1]
        user_part = arr[2].split(":")
        message =  arr[3]
        log_dict={
            "timestamp": timestamp,
            "level": level,
            "user": user_part[0],
            "message": message.strip()
        }
        result= add_log(log_dict)
        print("Converted string ")
    return wrapper

User_Dict = defaultdict(list)
level_Dict  = defaultdict(int)
recent_logs = deque(maxlen=5)
logs_dict = {}

@parse_log
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


