from dataclasses import dataclass, field
from functools import update_wrapper, wraps
from typing import Any, Dict
import datetime
import builtins

@dataclass
class TaskResult:
    result: Any = None
    logs: Dict = field(default_factory=dict)
    success: bool = False

def task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrap_func = kwargs.pop('wrap_func', False)

        # If the wrap_func flag is not provided, execute the function and return the result directly
        if not wrap_func:
            return func(*args, **kwargs)

        # Otherwise, perform the decorated logic
        # Create a dictionary to store log messages
        logs = {}  

        def custom_print(*args, **kwargs):
            # Instead of printing, append the message to the log dict
            message = " ".join(map(str, args))
            
            # Get the current datetime and convert it to milliseconds
            now = datetime.datetime.now()
            timestamp = now.timestamp() * 1000
            logs[timestamp] = message

            # Call original print function
            original_print(*args, **kwargs)

        # Save original print
        original_print = builtins.print
        
        # Override print
        builtins.print = custom_print

        try:
            result = func(*args, **kwargs)
            # Mark the task as completed successfully
            return TaskResult(result, logs, True)
        except Exception as e:
            # If there's an error, log it and return a TaskResult indicating failure
            now = datetime.datetime.now()
            timestamp = now.timestamp() * 1000
            logs[timestamp] = f"Error: {e}"
            return TaskResult(None, logs, False)
        finally:
            # Restore original print
            builtins.print = original_print
            
    # This will help identify functions decorated with neena_task
    wrapper._is_neena_task = True
    return wrapper