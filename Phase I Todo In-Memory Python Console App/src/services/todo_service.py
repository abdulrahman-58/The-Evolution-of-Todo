"""
TodoService class containing the core business logic for managing todo items.

This service encapsulates all business logic for todo operations while maintaining
separation from data models and CLI presentation.
"""

from typing import Dict, List, Optional
from ..models.todo_item import TodoItem


class TodoService:
    """
    Service class for managing todo items with core business logic.

    Provides methods for adding, retrieving, updating, and deleting todo items.
    All data is maintained in-memory only as per Phase I requirements.
    """

    def __init__(self) -> None:
        """Initialize the TodoService with an empty todo list."""
        self._todos: Dict[int, TodoItem] = {}
        self._next_id: int = 1

    def get_next_available_id(self) -> int:
        """Get the next available ID for a new todo item."""
        while self._next_id in self._todos:
            self._next_id += 1
        return self._next_id

    def add_todo(self, title: str) -> TodoItem:
        """
        Add a new todo item with the given title.

        Args:
            title: The title/text of the todo item

        Returns:
            The created TodoItem with assigned ID

        Raises:
            ValueError: If the title is invalid
        """
        if not isinstance(title, str):
            raise ValueError(f"Title must be a string, got {type(title)}")

        if not title.strip():
            raise ValueError("Title cannot be empty or consist only of whitespace")

        if len(title) > 1000:
            raise ValueError("Title length should be less than 1000 characters")

        # Create a new todo item with the next available ID
        new_id = self.get_next_available_id()
        todo_item = TodoItem(id=new_id, title=title.strip(), completed=False)

        # Add to the collection
        self._todos[new_id] = todo_item

        # Update the next ID to be used
        self._next_id = new_id + 1

        return todo_item

    def get_todo_by_id(self, todo_id: int) -> Optional[TodoItem]:
        """
        Retrieve a todo item by its ID.

        Args:
            todo_id: The ID of the todo item to retrieve

        Returns:
            The TodoItem if found, None otherwise
        """
        if not isinstance(todo_id, int):
            raise ValueError(f"ID must be an integer, got {type(todo_id)}")

        return self._todos.get(todo_id)

    def get_all_todos(self) -> List[TodoItem]:
        """
        Retrieve all todo items in the order they were added.

        Returns:
            A list of all TodoItem objects
        """
        # Return todos in the order of their IDs (which corresponds to addition order)
        return [self._todos[todo_id] for todo_id in sorted(self._todos.keys())]

    def get_pending_todos(self) -> List[TodoItem]:
        """
        Retrieve all pending (not completed) todo items.

        Returns:
            A list of pending TodoItem objects
        """
        return [todo for todo in self.get_all_todos() if not todo.completed]

    def get_completed_todos(self) -> List[TodoItem]:
        """
        Retrieve all completed todo items.

        Returns:
            A list of completed TodoItem objects
        """
        return [todo for todo in self.get_all_todos() if todo.completed]

    def update_todo(self, todo_id: int, new_title: str) -> bool:
        """
        Update the title of an existing todo item.

        Args:
            todo_id: The ID of the todo item to update
            new_title: The new title for the todo item

        Returns:
            True if the update was successful, False if the todo item was not found

        Raises:
            ValueError: If the new title is invalid
        """
        if not isinstance(todo_id, int):
            raise ValueError(f"ID must be an integer, got {type(todo_id)}")

        if not isinstance(new_title, str):
            raise ValueError(f"Title must be a string, got {type(new_title)}")

        if not new_title.strip():
            raise ValueError("Title cannot be empty or consist only of whitespace")

        if len(new_title) > 1000:
            raise ValueError("Title length should be less than 1000 characters")

        if todo_id not in self._todos:
            return False

        # Update the title
        self._todos[todo_id].update_title(new_title)
        return True

    def mark_complete(self, todo_id: int) -> bool:
        """
        Mark a todo item as complete.

        Args:
            todo_id: The ID of the todo item to mark as complete

        Returns:
            True if the update was successful, False if the todo item was not found
        """
        if not isinstance(todo_id, int):
            raise ValueError(f"ID must be an integer, got {type(todo_id)}")

        if todo_id not in self._todos:
            return False

        # Mark as complete
        self._todos[todo_id].mark_completed()
        return True

    def mark_incomplete(self, todo_id: int) -> bool:
        """
        Mark a todo item as incomplete.

        Args:
            todo_id: The ID of the todo item to mark as incomplete

        Returns:
            True if the update was successful, False if the todo item was not found
        """
        if not isinstance(todo_id, int):
            raise ValueError(f"ID must be an integer, got {type(todo_id)}")

        if todo_id not in self._todos:
            return False

        # Mark as incomplete
        self._todos[todo_id].mark_incomplete()
        return True

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo item by its ID.

        Args:
            todo_id: The ID of the todo item to delete

        Returns:
            True if the deletion was successful, False if the todo item was not found
        """
        if not isinstance(todo_id, int):
            raise ValueError(f"ID must be an integer, got {type(todo_id)}")

        if todo_id not in self._todos:
            return False

        # Remove the todo item
        del self._todos[todo_id]

        # Update the next_id if necessary
        if todo_id < self._next_id:
            self._next_id = min(todo_id, self._next_id)

        return True

    def toggle_completion_status(self, todo_id: int) -> bool:
        """
        Toggle the completion status of a todo item.

        Args:
            todo_id: The ID of the todo item to toggle

        Returns:
            True if the toggle was successful, False if the todo item was not found
        """
        if not isinstance(todo_id, int):
            raise ValueError(f"ID must be an integer, got {type(todo_id)}")

        if todo_id not in self._todos:
            return False

        # Toggle the completion status
        if self._todos[todo_id].completed:
            self._todos[todo_id].mark_incomplete()
        else:
            self._todos[todo_id].mark_completed()

        return True

    def get_todo_count(self) -> int:
        """
        Get the total count of todos.

        Returns:
            The number of todo items
        """
        return len(self._todos)

    def get_pending_count(self) -> int:
        """
        Get the count of pending todos.

        Returns:
            The number of pending todo items
        """
        return len(self.get_pending_todos())

    def get_completed_count(self) -> int:
        """
        Get the count of completed todos.

        Returns:
            The number of completed todo items
        """
        return len(self.get_completed_todos())