from dataclasses import dataclass, field
from functools import update_wrapper
from typing import Any, Dict
import datetime
import builtins

@dataclass
class TaskResult:
    result: Any = None
    logs: Dict = field(default_factory=dict)
    success: bool = False

class Task:
    def __init__(self, func):
        self.func = func
        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        wrap_func = kwargs.pop('wrap_func', False)

        # If the wrap_func flag is not provided, execute the function and return the result directly
        if not wrap_func:
            return self.func(*args, **kwargs)

        # Otherwise, perform the decorated logic
        # Create a dictionary to store log messages
        self.logs = {}  

        def custom_print(*args, **kwargs):
            # Instead of printing, append the message to the log dict
            message = " ".join(map(str, args))
            
            # Get the current datetime and convert it to milliseconds
            now = datetime.datetime.now()
            timestamp = now.timestamp() * 1000
            self.logs[timestamp] = message

            # Call original print function
            original_print(*args, **kwargs)

        # Save original print
        original_print = builtins.print
        
        # Override print
        builtins.print = custom_print

        try:
            result = self.func(*args, **kwargs)
            # Mark the task as completed successfully
            return TaskResult(result, self.logs, True)
        except Exception as e:
            # If there's an error, log it and return a TaskResult indicating failure
            now = datetime.datetime.now()
            timestamp = now.timestamp() * 1000
            self.logs[timestamp] = f"Error: {e}"
            return TaskResult(None, self.logs, False)
        finally:
            # Restore original print
            builtins.print = original_print

    @property
    def _is_neena_task(self):
        return True
