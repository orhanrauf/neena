from abc import ABC, abstractmethod


class ValidationMessageBase(ABC):
    core_message: str
    
    @abstractmethod
    def __str__(self):
        pass
    

class TaskValidationFailureMessage(ValidationMessageBase):
    task_name: str
    
    def __init__(self, core_message: str, task_name: str):
        self.core_message = core_message
        self.task_name = task_name
    
    def __str__(self):
        return f"Task validation failed for task '{self.task_name}': {self.core_message}"


class FlowValidationFailureMessage(ValidationMessageBase):
    def __init__(self, core_message: str):
        self.core_message = core_message
    
    def __str__(self):
        return f"Flow validation failed: {self.core_message}"


class TaskValidationWarningMessage(ValidationMessageBase):
    def __init__(self, core_message: str):
        self.core_message = core_message
    
    def __str__(self):
        return f"Task validation warning for task '{self.task_name}': {self.core_message}"


class FlowValidationWarningMessage(ValidationMessageBase):
    def __init__(self, core_message: str):
        self.core_message = core_message
    
    def __str__(self):
        return f"Flow validation warning: {self.core_message}"
