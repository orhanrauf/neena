from enum import Enum
from functools import wraps
import time
from typing import Callable, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')

class TaskStatus(Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'
    RETRY = 'retry'

class TaskResponse(BaseModel, Generic[T]):
    status: TaskStatus
    data: Optional[T] = None
    error: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)

    @classmethod
    def success(cls, data: T, **metadata) -> 'TaskResponse':
        return cls(status=TaskStatus.SUCCESS, data=data, metadata=metadata)

    @classmethod
    def failure(cls, error: str, **metadata) -> 'TaskResponse':
        return cls(status=TaskStatus.FAILURE, error=error, metadata=metadata)

R = TypeVar('R', bound=Callable[..., TaskResponse])

def task(task_name: str, max_attempts: int = 3, delay_seconds: int = 2):
    """
    Decorator to mark a method as a Neena task. 
    Allows for automatic retrying of the task in case of failure.
    
    :param task_name: The name of the task as 
    :param max_attempts: The maximum number of attempts to retry the task.
    :param delay_seconds: The delay between retries in seconds.
    """
    def decorator(func: R) -> R:
        @wraps(func)
        def wrapper(*args, **kwargs) -> TaskResponse:
            runtime_config = kwargs.get('runtime_config', {})
            max_retries = runtime_config.get('max_attempts', max_attempts)
            delay = runtime_config.get('delay_seconds', delay_seconds)

            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    # Automatically pack raw return into TaskResponse if necessary
                    if not isinstance(result, TaskResponse):
                        return TaskResponse.success(data=result)
                    return result
                except Exception as e:
                    if attempt == max_retries:
                        return TaskResponse.failure(error=str(e))
                    time.sleep(delay)
        wrapper._is_task = True
        return wrapper
        
    return decorator


def integration(cls):
    """
    Class decorator to mark a class as representing a Neena integration.
    """
    cls.is_integration = True
    return cls
