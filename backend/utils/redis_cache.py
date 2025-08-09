import os
import redis
import json

# Get the Redis host from environment variable or default to "localhost"
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = 6379  # Default Redis port

# Create a Redis client connection
try:
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        db=0,                   # Redis has numbered databases; we use the default (0)
        decode_responses=True   # Automatically decode bytes to strings
    )
    # Test the connection
    r.ping()
    REDIS_AVAILABLE = True
except (redis.ConnectionError, ConnectionRefusedError):
    print("⚠️ Redis not available, caching disabled")
    REDIS_AVAILABLE = False
    r = None

def get_from_cache(key: str):
    """
    Try to retrieve a value from Redis using the given key.
    If found, deserialize it from JSON and return the Python object.
    If not found, return None.
    """
    if not REDIS_AVAILABLE:
        return None
    try:
        value = r.get(key)
        if value:
            return json.loads(value)
    except:
        pass
    return None

def set_in_cache(key: str, value, ttl: int = 300):
    """
    Store a value in Redis under the given key, with an optional time-to-live (TTL).
    The value is serialized to JSON before storing.
    
    Args:
        key (str): The cache key.
        value (Any): The Python object to cache.
        ttl (int): Time to live in seconds (default is 300 seconds = 5 minutes).
    """
    if not REDIS_AVAILABLE:
        return
    try:
        r.setex(key, ttl, json.dumps(value))
    except:
        pass

def delete_from_cache(key: str):
    """
    Delete a value from Redis using the given key.
    
    Args:
        key (str): The cache key to delete.
    """
    if not REDIS_AVAILABLE:
        return
    try:
        r.delete(key)
    except:
        pass