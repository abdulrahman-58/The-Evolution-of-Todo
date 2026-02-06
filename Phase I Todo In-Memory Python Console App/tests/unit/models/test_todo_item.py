"""Unit tests for the TodoItem model."""

import pytest
from src.models.todo_item import TodoItem


def test_todo_item_creation_valid():
    """Test creating a valid TodoItem."""
    todo = TodoItem(id=1, title="Test todo", completed=False)

    assert todo.id == 1
    assert todo.title == "Test todo"
    assert todo.completed is False


def test_todo_item_creation_defaults():
    """Test creating a TodoItem with default completed status."""
    todo = TodoItem(id=1, title="Test todo")

    assert todo.id == 1
    assert todo.title == "Test todo"
    assert todo.completed is False


def test_todo_item_mark_completed():
    """Test marking a TodoItem as completed."""
    todo = TodoItem(id=1, title="Test todo", completed=False)

    todo.mark_completed()

    assert todo.completed is True


def test_todo_item_mark_incomplete():
    """Test marking a TodoItem as incomplete."""
    todo = TodoItem(id=1, title="Test todo", completed=True)

    todo.mark_incomplete()

    assert todo.completed is False


def test_todo_item_update_title():
    """Test updating a TodoItem's title."""
    todo = TodoItem(id=1, title="Old title", completed=False)

    todo.update_title("New title")

    assert todo.title == "New title"


def test_todo_item_invalid_id():
    """Test that TodoItem raises error with invalid ID."""
    with pytest.raises(ValueError):
        TodoItem(id=-1, title="Test todo")

    with pytest.raises(ValueError):
        TodoItem(id=0, title="Test todo")

    with pytest.raises(ValueError):
        TodoItem(id="invalid", title="Test todo")


def test_todo_item_invalid_title_empty():
    """Test that TodoItem raises error with empty title."""
    with pytest.raises(ValueError):
        TodoItem(id=1, title="")


def test_todo_item_invalid_title_whitespace_only():
    """Test that TodoItem raises error with whitespace-only title."""
    with pytest.raises(ValueError):
        TodoItem(id=1, title="   ")

    with pytest.raises(ValueError):
        TodoItem(id=1, title="\t\n")


def test_todo_item_invalid_title_long():
    """Test that TodoItem raises error with very long title."""
    long_title = "a" * 1001  # More than 1000 characters

    with pytest.raises(ValueError):
        TodoItem(id=1, title=long_title)


def test_todo_item_invalid_title_type():
    """Test that TodoItem raises error with non-string title."""
    with pytest.raises(ValueError):
        TodoItem(id=1, title=123)


def test_todo_item_invalid_completed_type():
    """Test that TodoItem raises error with non-boolean completed."""
    with pytest.raises(ValueError):
        TodoItem(id=1, title="Test", completed="true")


def test_todo_item_update_title_validation():
    """Test that updating title validates the new title."""
    todo = TodoItem(id=1, title="Valid title")

    # Test updating with empty title
    with pytest.raises(ValueError):
        todo.update_title("")

    # Test updating with whitespace-only title
    with pytest.raises(ValueError):
        todo.update_title("   ")

    # Test updating with very long title
    with pytest.raises(ValueError):
        todo.update_title("a" * 1001)

    # Test updating with non-string title
    with pytest.raises(ValueError):
        todo.update_title(123)


def test_todo_item_repr():
    """Test the string representation of TodoItem."""
    todo = TodoItem(id=1, title="Test todo", completed=True)

    # Check that the repr contains the important attributes
    repr_str = repr(todo)
    assert "id=1" in repr_str
    assert "title='Test todo'" in repr_str
    assert "completed=True" in repr_str