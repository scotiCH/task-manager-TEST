from enum import Enum
from pydantic import BaseModel
from uuid import UUID

class Status(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"

class Task(BaseModel):
    id: UUID
    title: str
    description: str
    status: Status

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None