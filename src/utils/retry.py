import time
import functools
import requests

def retry_request(max_attempts=3, delay=2):
    """
    Decorator: Retries a function if it crashes.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.RequestException, ConnectionError) as e:
                    print(f"⚠️ Network Error (Attempt {attempt + 1}/{max_attempts}): {e}")
                    if attempt < max_attempts - 1:
                        print(f"   ⏳ Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("❌ Max retries reached. Giving up.")
                        raise e # Re-raise the error so the main program knows
            return None
        return wrapper
    return decorator