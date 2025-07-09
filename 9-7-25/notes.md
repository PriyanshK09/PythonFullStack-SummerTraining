# Lazy vs Eager Loading

## Eager Loading
- **Definition:** Loads all related data as soon as the main object is loaded.
- **Use Case:** When you know you'll need related data immediately.
- **Pros:** Fewer database queries (avoids N+1 problem).
- **Cons:** Can load unnecessary data, increasing memory usage.

**Example (SQLAlchemy):**
```python
from sqlalchemy.orm import joinedload
session.query(User).options(joinedload(User.posts)).all()
```

## Lazy Loading
- **Definition:** Loads related data only when it's accessed for the first time.
- **Use Case:** When related data might not always be needed.
- **Pros:** Saves memory and speeds up initial load.
- **Cons:** Can cause multiple database queries (N+1 problem).

**Example (SQLAlchemy):**
```python
user = session.query(User).first()
posts = user.posts  # Triggers a separate query
```

## Summary Table

| Feature        | Eager Loading         | Lazy Loading         |
|----------------|----------------------|----------------------|
| When Loaded    | Immediately          | On Access            |
| Performance    | Fewer queries        | More queries         |
| Memory Usage   | Higher               | Lower                |
| Use Case       | Need all data upfront| Data may not be needed|
