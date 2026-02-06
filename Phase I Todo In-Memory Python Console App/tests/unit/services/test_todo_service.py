"""Unit tests for the TodoService class."""

import pytest
from src.services.todo_service import TodoService
from src.models.todo_item import TodoItem


class TestTodoService:
    """Test suite for TodoService functionality."""

    def test_initial_state(self):
        """Test that TodoService starts with no todos."""
        service = TodoService()

        assert service.get_todo_count() == 0
        assert service.get_all_todos() == []
        assert service.get_pending_todos() == []
        assert service.get_completed_todos() == []

    def test_add_todo_basic(self):
        """Test adding a basic todo item."""
        service = TodoService()

        result = service.add_todo("Buy groceries")

        assert isinstance(result, TodoItem)
        assert result.id == 1
        assert result.title == "Buy groceries"
        assert result.completed is False

        # Check that the todo is in the service
        todos = service.get_all_todos()
        assert len(todos) == 1
        assert todos[0].id == 1
        assert todos[0].title == "Buy groceries"

    def test_add_multiple_todos(self):
        """Test adding multiple todo items with sequential IDs."""
        service = TodoService()

        first = service.add_todo("First todo")
        second = service.add_todo("Second todo")
        third = service.add_todo("Third todo")

        assert first.id == 1
        assert second.id == 2
        assert third.id == 3

        todos = service.get_all_todos()
        assert len(todos) == 3
        assert todos[0].id == 1
        assert todos[1].id == 2
        assert todos[2].id == 3

    def test_add_todo_invalid_title_empty(self):
        """Test that adding a todo with empty title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.add_todo("")

    def test_add_todo_invalid_title_whitespace(self):
        """Test that adding a todo with whitespace-only title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.add_todo("   ")

        with pytest.raises(ValueError):
            service.add_todo("\t\n")

    def test_add_todo_invalid_title_long(self):
        """Test that adding a todo with very long title raises ValueError."""
        service = TodoService()
        long_title = "a" * 1001  # More than 1000 characters

        with pytest.raises(ValueError):
            service.add_todo(long_title)

    def test_get_todo_by_id_exists(self):
        """Test retrieving an existing todo by ID."""
        service = TodoService()
        added_todo = service.add_todo("Test todo")

        retrieved_todo = service.get_todo_by_id(added_todo.id)

        assert retrieved_todo is not None
        assert retrieved_todo.id == added_todo.id
        assert retrieved_todo.title == added_todo.title
        assert retrieved_todo.completed == added_todo.completed

    def test_get_todo_by_id_not_exists(self):
        """Test retrieving a non-existent todo by ID."""
        service = TodoService()

        result = service.get_todo_by_id(999)

        assert result is None

    def test_get_todo_by_id_invalid_type(self):
        """Test that getting todo by non-integer ID raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.get_todo_by_id("invalid")

        with pytest.raises(ValueError):
            service.get_todo_by_id(1.5)

    def test_get_all_todos_order(self):
        """Test that get_all_todos returns todos in the correct order."""
        service = TodoService()

        third = service.add_todo("Third")
        first = service.add_todo("First")
        second = service.add_todo("Second")

        todos = service.get_all_todos()

        # Should be ordered by ID, not insertion order
        assert len(todos) == 3
        assert todos[0].id == 1  # First added
        assert todos[1].id == 2  # Second added
        assert todos[2].id == 3  # Third added

    def test_get_all_todos_empty(self):
        """Test that get_all_todos returns empty list when no todos exist."""
        service = TodoService()

        todos = service.get_all_todos()

        assert todos == []

    def test_get_pending_todos_empty(self):
        """Test that get_pending_todos returns empty list when no pending todos exist."""
        service = TodoService()

        pending = service.get_pending_todos()

        assert pending == []

    def test_get_completed_todos_empty(self):
        """Test that get_completed_todos returns empty list when no completed todos exist."""
        service = TodoService()

        completed = service.get_completed_todos()

        assert completed == []

    def test_get_pending_and_completed_todos(self):
        """Test filtering todos by completion status."""
        service = TodoService()

        # Add some todos
        todo1 = service.add_todo("Pending 1")
        todo2 = service.add_todo("Pending 2")
        todo3 = service.add_todo("Completed 1")

        # Mark one as complete
        service.mark_complete(todo3.id)

        pending = service.get_pending_todos()
        completed = service.get_completed_todos()

        assert len(pending) == 2
        assert len(completed) == 1

        pending_ids = [t.id for t in pending]
        completed_ids = [t.id for t in completed]

        assert todo1.id in pending_ids
        assert todo2.id in pending_ids
        assert todo3.id in completed_ids

    def test_update_todo_success(self):
        """Test successfully updating a todo's title."""
        service = TodoService()
        original_todo = service.add_todo("Original title")

        success = service.update_todo(original_todo.id, "Updated title")

        assert success is True

        # Check that the todo was updated
        updated_todo = service.get_todo_by_id(original_todo.id)
        assert updated_todo.title == "Updated title"

    def test_update_todo_not_found(self):
        """Test updating a non-existent todo."""
        service = TodoService()

        success = service.update_todo(999, "New title")

        assert success is False

    def test_update_todo_invalid_new_title(self):
        """Test that updating with invalid title raises ValueError."""
        service = TodoService()
        todo = service.add_todo("Original title")

        # Test with empty title
        with pytest.raises(ValueError):
            service.update_todo(todo.id, "")

        # Test with whitespace-only title
        with pytest.raises(ValueError):
            service.update_todo(todo.id, "   ")

        # Test with very long title
        with pytest.raises(ValueError):
            service.update_todo(todo.id, "a" * 1001)

    def test_update_todo_invalid_id_type(self):
        """Test that updating with non-integer ID raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.update_todo("invalid", "New title")

        with pytest.raises(ValueError):
            service.update_todo(1.5, "New title")

    def test_update_todo_preserves_completion_status(self):
        """Test that updating a todo preserves its completion status."""
        service = TodoService()
        original_todo = service.add_todo("Original title")
        service.mark_complete(original_todo.id)  # Mark as complete first

        # Verify it's complete before update
        assert service.get_todo_by_id(original_todo.id).completed is True

        success = service.update_todo(original_todo.id, "Updated title")
        assert success is True

        # Check that the todo was updated but completion status is preserved
        updated_todo = service.get_todo_by_id(original_todo.id)
        assert updated_todo.title == "Updated title"
        assert updated_todo.completed is True  # Should remain completed

    def test_update_todo_with_different_completion_statuses(self):
        """Test updating todos with different completion statuses."""
        service = TodoService()

        # Add two todos
        pending_todo = service.add_todo("Pending todo")
        completed_todo = service.add_todo("Completed todo")
        service.mark_complete(completed_todo.id)

        # Verify initial states
        assert service.get_todo_by_id(pending_todo.id).completed is False
        assert service.get_todo_by_id(completed_todo.id).completed is True

        # Update both
        success1 = service.update_todo(pending_todo.id, "Updated pending todo")
        success2 = service.update_todo(completed_todo.id, "Updated completed todo")

        assert success1 is True
        assert success2 is True

        # Check that titles and completion statuses are preserved correctly
        updated_pending = service.get_todo_by_id(pending_todo.id)
        updated_completed = service.get_todo_by_id(completed_todo.id)

        assert updated_pending.title == "Updated pending todo"
        assert updated_pending.completed is False  # Should remain pending

        assert updated_completed.title == "Updated completed todo"
        assert updated_completed.completed is True  # Should remain completed

    def test_update_todo_special_characters(self):
        """Test updating a todo with special characters in the title."""
        service = TodoService()
        original_todo = service.add_todo("Original title")

        special_titles = [
            "Title with spaces and numbers 123",
            "Title with symbols !@#$%^&*()",
            "Title with accented chars: café résumé naïve",
            "Title with unicode: 🐍 🚀 📝",
            "Title with punctuation: Hello, world! How are you?",
        ]

        for i, special_title in enumerate(special_titles):
            # Add a new todo for each test
            test_todo = service.add_todo(f"Test todo {i}")
            success = service.update_todo(test_todo.id, special_title)

            assert success is True

            updated_todo = service.get_todo_by_id(test_todo.id)
            assert updated_todo.title == special_title

    def test_mark_complete_success(self):
        """Test successfully marking a todo as complete."""
        service = TodoService()
        todo = service.add_todo("Test todo")

        success = service.mark_complete(todo.id)

        assert success is True

        # Check that the todo is now complete
        updated_todo = service.get_todo_by_id(todo.id)
        assert updated_todo.completed is True

    def test_mark_complete_not_found(self):
        """Test marking a non-existent todo as complete."""
        service = TodoService()

        success = service.mark_complete(999)

        assert success is False

    def test_mark_complete_invalid_id_type(self):
        """Test that marking complete with non-integer ID raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.mark_complete("invalid")

        with pytest.raises(ValueError):
            service.mark_complete(1.5)

    def test_mark_incomplete_success(self):
        """Test successfully marking a todo as incomplete."""
        service = TodoService()
        todo = service.add_todo("Test todo")
        service.mark_complete(todo.id)  # First mark as complete

        success = service.mark_incomplete(todo.id)

        assert success is True

        # Check that the todo is now incomplete
        updated_todo = service.get_todo_by_id(todo.id)
        assert updated_todo.completed is False

    def test_mark_incomplete_not_found(self):
        """Test marking a non-existent todo as incomplete."""
        service = TodoService()

        success = service.mark_incomplete(999)

        assert success is False

    def test_mark_incomplete_invalid_id_type(self):
        """Test that marking incomplete with non-integer ID raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.mark_incomplete("invalid")

        with pytest.raises(ValueError):
            service.mark_incomplete(1.5)

    def test_toggle_completion_status(self):
        """Test toggling completion status."""
        service = TodoService()
        todo = service.add_todo("Test todo")

        # Initially incomplete
        assert todo.completed is False

        # Toggle to complete
        success = service.toggle_completion_status(todo.id)
        assert success is True
        assert service.get_todo_by_id(todo.id).completed is True

        # Toggle back to incomplete
        success = service.toggle_completion_status(todo.id)
        assert success is True
        assert service.get_todo_by_id(todo.id).completed is False

    def test_mark_complete_then_mark_incomplete(self):
        """Test the complete flow of marking complete then incomplete."""
        service = TodoService()
        todo = service.add_todo("Test todo")

        # Initially pending
        assert todo.completed is False

        # Mark as complete
        success = service.mark_complete(todo.id)
        assert success is True
        assert service.get_todo_by_id(todo.id).completed is True

        # Mark as incomplete again
        success = service.mark_incomplete(todo.id)
        assert success is True
        assert service.get_todo_by_id(todo.id).completed is False

    def test_delete_todo_success(self):
        """Test successfully deleting a todo."""
        service = TodoService()
        todo = service.add_todo("Test todo")

        success = service.delete_todo(todo.id)

        assert success is True
        assert service.get_todo_by_id(todo.id) is None
        assert service.get_todo_count() == 0

    def test_delete_todo_not_found(self):
        """Test deleting a non-existent todo."""
        service = TodoService()

        success = service.delete_todo(999)

        assert success is False

    def test_delete_todo_invalid_id_type(self):
        """Test that deleting with non-integer ID raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.delete_todo("invalid")

        with pytest.raises(ValueError):
            service.delete_todo(1.5)

    def test_delete_todo_removes_correct_item(self):
        """Test that deleting a todo removes the correct item and leaves others."""
        service = TodoService()

        # Add multiple todos
        todo1 = service.add_todo("First todo")
        todo2 = service.add_todo("Second todo")
        todo3 = service.add_todo("Third todo")

        # Verify all exist
        assert service.get_todo_count() == 3
        assert service.get_todo_by_id(todo1.id) is not None
        assert service.get_todo_by_id(todo2.id) is not None
        assert service.get_todo_by_id(todo3.id) is not None

        # Delete the middle one
        success = service.delete_todo(todo2.id)
        assert success is True

        # Verify correct items remain
        assert service.get_todo_count() == 2
        assert service.get_todo_by_id(todo1.id) is not None
        assert service.get_todo_by_id(todo2.id) is None  # Deleted
        assert service.get_todo_by_id(todo3.id) is not None

    def test_delete_todo_with_different_completion_statuses(self):
        """Test deleting todos with different completion statuses."""
        service = TodoService()

        # Add todos with different completion statuses
        pending_todo = service.add_todo("Pending todo")
        completed_todo = service.add_todo("Completed todo")
        service.mark_complete(completed_todo.id)

        # Verify initial states
        assert service.get_todo_by_id(pending_todo.id).completed is False
        assert service.get_todo_by_id(completed_todo.id).completed is True

        # Delete the pending todo
        success = service.delete_todo(pending_todo.id)
        assert success is True

        # Verify only completed todo remains
        assert service.get_todo_count() == 1
        assert service.get_todo_by_id(pending_todo.id) is None
        assert service.get_todo_by_id(completed_todo.id) is not None
        assert service.get_todo_by_id(completed_todo.id).completed is True

        # Delete the completed todo
        success = service.delete_todo(completed_todo.id)
        assert success is True

        # Verify no todos remain
        assert service.get_todo_count() == 0
        assert service.get_todo_by_id(completed_todo.id) is None

    def test_delete_todo_repeated_deletion(self):
        """Test attempting to delete the same todo twice."""
        service = TodoService()
        todo = service.add_todo("Test todo")

        # First deletion should succeed
        success1 = service.delete_todo(todo.id)
        assert success1 is True
        assert service.get_todo_by_id(todo.id) is None

        # Second deletion should fail
        success2 = service.delete_todo(todo.id)
        assert success2 is False

    def test_delete_all_todos(self):
        """Test deleting all todos from the service."""
        service = TodoService()

        # Add multiple todos
        todo1 = service.add_todo("First todo")
        todo2 = service.add_todo("Second todo")
        todo3 = service.add_todo("Third todo")

        # Verify all exist
        assert service.get_todo_count() == 3

        # Delete all
        success1 = service.delete_todo(todo1.id)
        success2 = service.delete_todo(todo2.id)
        success3 = service.delete_todo(todo3.id)

        assert success1 is True
        assert success2 is True
        assert success3 is True
        assert service.get_todo_count() == 0

        # Verify all are gone
        assert service.get_todo_by_id(todo1.id) is None
        assert service.get_todo_by_id(todo2.id) is None
        assert service.get_todo_by_id(todo3.id) is None

    def test_counters_after_operations(self):
        """Test that counters are accurate after various operations."""
        service = TodoService()

        # Add some todos
        todo1 = service.add_todo("Pending 1")
        todo2 = service.add_todo("Pending 2")
        todo3 = service.add_todo("Pending 3")

        # Check initial counters
        assert service.get_todo_count() == 3
        assert service.get_pending_count() == 3
        assert service.get_completed_count() == 0

        # Mark one as complete
        service.mark_complete(todo1.id)

        # Check counters after marking complete
        assert service.get_todo_count() == 3
        assert service.get_pending_count() == 2
        assert service.get_completed_count() == 1

        # Delete a pending todo
        service.delete_todo(todo2.id)

        # Check counters after deletion
        assert service.get_todo_count() == 2
        assert service.get_pending_count() == 1
        assert service.get_completed_count() == 1

        # Delete the completed todo
        service.delete_todo(todo1.id)

        # Check final counters
        assert service.get_todo_count() == 1
        assert service.get_pending_count() == 1
        assert service.get_completed_count() == 0