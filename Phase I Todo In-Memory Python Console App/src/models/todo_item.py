"""
TodoItem data model representing a single todo task in the application.

This module defines the TodoItem class with id, title, and completed fields
as specified in the data model documentation.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TodoItem:
    """
    Represents a single todo task in the application.

    Attributes:
        id (int): Unique identifier for the todo item; assigned sequentially starting from 1
        title (str): Text content of the todo item; descriptive text entered by the user
        completed (bool): Status indicator; True if the task is completed, False otherwise
    """

    id: int
    title: str
    completed: bool = False

    def __post_init__(self):
        """Validate the TodoItem after initialization."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError(f"ID must be a positive integer, got {self.id}")

        if not isinstance(self.title, str):
            raise ValueError(f"Title must be a string, got {type(self.title)}")

        if not self.title.strip():
            raise ValueError("Title cannot be empty or consist only of whitespace")

        if len(self.title) > 1000:
            raise ValueError("Title length should be less than 1000 characters")

        if not isinstance(self.completed, bool):
            raise ValueError(f"Completed must be a boolean, got {type(self.completed)}")

    def mark_completed(self) -> None:
        """Mark the todo item as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the todo item as incomplete."""
        self.completed = False

    def update_title(self, new_title: str) -> None:
        """Update the title of the todo item."""
        if not isinstance(new_title, str):
            raise ValueError(f"Title must be a string, got {type(new_title)}")

        if not new_title.strip():
            raise ValueError("Title cannot be empty or consist only of whitespace")

        if len(new_title) > 1000:
            raise ValueError("Title length should be less than 1000 characters")

        self.title = new_title.strip()