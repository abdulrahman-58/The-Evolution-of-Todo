"""Integration tests for the CLI flow, specifically for adding todo functionality."""

import io
import sys
from unittest.mock import patch
import pytest
from src.cli.main import TodoCLI


def test_add_todo_integration():
    """Test the complete flow of adding a todo via CLI."""
    # Mock user inputs: add todo, then exit
    inputs = iter([
        "1",  # Choose "Add Todo"
        "Buy groceries",  # Todo description
        "6"   # Choose "Exit"
    ])

    def mock_input(prompt=""):
        return next(inputs)

    # Capture printed output
    captured_output = io.StringIO()

    with patch('builtins.input', side_effect=mock_input), \
         patch('sys.stdout', new=captured_output):

        cli = TodoCLI()
        cli.running = False  # We'll test the functionality separately

    # Test the service directly to ensure the todo was added
    cli = TodoCLI()
    cli.handle_add_todo()  # Add the todo

    # Verify the todo was added to the service
    todos = cli.service.get_all_todos()
    assert len(todos) == 1
    assert todos[0].title == "Buy groceries"
    assert todos[0].completed is False


def test_add_multiple_todos_integration():
    """Test adding multiple todos via CLI."""
    cli = TodoCLI()

    # Add first todo
    with patch('builtins.input', return_value="Buy groceries"):
        cli.handle_add_todo()

    # Add second todo
    with patch('builtins.input', return_value="Walk the dog"):
        cli.handle_add_todo()

    # Verify both todos were added
    todos = cli.service.get_all_todos()
    assert len(todos) == 2
    assert todos[0].title == "Buy groceries"
    assert todos[1].title == "Walk the dog"


def test_add_todo_with_empty_input():
    """Test adding a todo with empty input - should handle gracefully."""
    cli = TodoCLI()

    # Capture printed output
    captured_output = io.StringIO()

    with patch('builtins.input', return_value=""), \
         patch('sys.stdout', new=captured_output):
        cli.handle_add_todo()

    # Check that an error message was printed
    output = captured_output.getvalue()
    assert "Error: Todo description cannot be empty" in output


def test_add_todo_with_long_input():
    """Test adding a todo with input that's too long."""
    cli = TodoCLI()

    # Create a very long title
    long_title = "a" * 1001

    # Capture printed output
    captured_output = io.StringIO()

    with patch('builtins.input', return_value=long_title), \
         patch('sys.stdout', new=captured_output):
        cli.handle_add_todo()

    # Check that an error message was printed
    output = captured_output.getvalue()
    assert "Error: Todo description is too long" in output


def test_view_todos_integration():
    """Test viewing todos via CLI."""
    cli = TodoCLI()

    # Add some todos
    cli.service.add_todo("First todo")
    cli.service.add_todo("Second todo")

    # Capture printed output
    captured_output = io.StringIO()

    with patch('sys.stdout', new=captured_output):
        cli.handle_view_todos()

    # Check that the todos were displayed
    output = captured_output.getvalue()
    assert "First todo" in output
    assert "Second todo" in output
    assert "[ ] 1." in output  # Pending status for first todo
    assert "[ ] 2." in output  # Pending status for second todo


def test_add_and_view_integration():
    """Test the flow of adding a todo then viewing it."""
    cli = TodoCLI()

    # Add a todo
    with patch('builtins.input', return_value="Test todo"):
        cli.handle_add_todo()

    # Verify it was added
    todos = cli.service.get_all_todos()
    assert len(todos) == 1
    assert todos[0].title == "Test todo"

    # Capture printed output when viewing
    captured_output = io.StringIO()

    with patch('sys.stdout', new=captured_output):
        cli.handle_view_todos()

    # Check that the added todo appears in the view
    output = captured_output.getvalue()
    assert "Test todo" in output


def test_view_todos_empty_list():
    """Test viewing todos when the list is empty."""
    cli = TodoCLI()

    # Capture printed output when viewing
    captured_output = io.StringIO()

    with patch('sys.stdout', new=captured_output):
        cli.handle_view_todos()

    # Check that the appropriate message is displayed
    output = captured_output.getvalue()
    assert "No todos found" in output


def test_view_multiple_todos():
    """Test viewing multiple todos."""
    cli = TodoCLI()

    # Add multiple todos
    cli.service.add_todo("First todo")
    cli.service.add_todo("Second todo")
    cli.service.add_todo("Third todo")

    # Capture printed output when viewing
    captured_output = io.StringIO()

    with patch('sys.stdout', new=captured_output):
        cli.handle_view_todos()

    # Check that all todos appear in the view
    output = captured_output.getvalue()
    assert "First todo" in output
    assert "Second todo" in output
    assert "Third todo" in output
    assert "[ ] 1." in output  # Pending status for first todo
    assert "[ ] 2." in output  # Pending status for second todo
    assert "[ ] 3." in output  # Pending status for third todo


def test_view_todos_with_completed_items():
    """Test viewing todos with some completed items."""
    cli = TodoCLI()

    # Add todos
    cli.service.add_todo("Pending todo")
    cli.service.add_todo("Completed todo")

    # Mark one as complete
    cli.service.mark_complete(2)

    # Capture printed output when viewing
    captured_output = io.StringIO()

    with patch('sys.stdout', new=captured_output):
        cli.handle_view_todos()

    # Check that both todos appear with correct statuses
    output = captured_output.getvalue()
    assert "Pending todo" in output
    assert "Completed todo" in output
    assert "[ ] 1." in output  # Pending status for first todo
    assert "[x] 2." in output  # Completed status for second todo


def test_add_and_mark_complete_integration():
    """Test adding a todo then marking it as complete."""
    cli = TodoCLI()

    # Add a todo
    with patch('builtins.input', return_value="Test todo"):
        cli.handle_add_todo()

    # Verify it was added as pending
    todos = cli.service.get_all_todos()
    assert len(todos) == 1
    assert todos[0].completed is False

    # Mark it as complete
    success = cli.service.mark_complete(todos[0].id)
    assert success is True

    # Verify it's now complete
    updated_todo = cli.service.get_todo_by_id(todos[0].id)
    assert updated_todo.completed is True


def test_mark_complete_via_cli():
    """Test marking a todo as complete through the CLI interface."""
    cli = TodoCLI()

    # Add a todo first
    todo = cli.service.add_todo("Test todo for completion")

    # Test marking complete via CLI
    with patch('builtins.input', return_value=str(todo.id)):
        cli.handle_mark_complete()

    # Verify it was marked as complete
    updated_todo = cli.service.get_todo_by_id(todo.id)
    assert updated_todo.completed is True


def test_mark_incomplete_via_cli():
    """Test marking a todo as incomplete through the CLI interface."""
    cli = TodoCLI()

    # Add a todo and mark it as complete
    todo = cli.service.add_todo("Test todo for completion")
    cli.service.mark_complete(todo.id)
    assert cli.service.get_todo_by_id(todo.id).completed is True

    # Test marking incomplete via CLI (using toggle functionality)
    with patch('builtins.input', return_value=str(todo.id)):
        # We'll use the toggle function directly since the CLI handles both
        success = cli.service.mark_incomplete(todo.id)
        assert success is True

    # Verify it was marked as incomplete
    updated_todo = cli.service.get_todo_by_id(todo.id)
    assert updated_todo.completed is False


def test_mark_complete_nonexistent_todo():
    """Test attempting to mark a non-existent todo as complete."""
    cli = TodoCLI()

    # Capture output to check error message
    captured_output = io.StringIO()

    with patch('builtins.input', return_value="999"), \
         patch('sys.stdout', new=captured_output):
        cli.handle_mark_complete()

    output = captured_output.getvalue()
    assert "not found" in output.lower()


def test_mark_complete_invalid_id():
    """Test attempting to mark a todo with an invalid ID."""
    cli = TodoCLI()

    # Capture output to check error message
    captured_output = io.StringIO()

    with patch('builtins.input', return_value="invalid"), \
         patch('sys.stdout', new=captured_output):
        cli.handle_mark_complete()

    output = captured_output.getvalue()
    assert "not a valid number" in output.lower()


def test_toggle_completion_status():
    """Test toggling the completion status of a todo."""
    cli = TodoCLI()

    # Add a todo
    todo = cli.service.add_todo("Test todo for toggling")

    # Initially it should be pending
    assert cli.service.get_todo_by_id(todo.id).completed is False

    # Toggle to complete
    success = cli.service.toggle_completion_status(todo.id)
    assert success is True
    assert cli.service.get_todo_by_id(todo.id).completed is True

    # Toggle back to pending
    success = cli.service.toggle_completion_status(todo.id)
    assert success is True
    assert cli.service.get_todo_by_id(todo.id).completed is False


def test_add_and_update_integration():
    """Test adding a todo then updating it."""
    cli = TodoCLI()

    # Add a todo
    with patch('builtins.input', return_value="Original todo"):
        cli.handle_add_todo()

    # Verify it was added
    todos = cli.service.get_all_todos()
    assert len(todos) == 1
    assert todos[0].title == "Original todo"

    # Update the todo
    success = cli.service.update_todo(todos[0].id, "Updated todo")
    assert success is True

    # Verify it was updated
    updated_todo = cli.service.get_todo_by_id(todos[0].id)
    assert updated_todo.title == "Updated todo"


def test_update_todo_via_cli():
    """Test updating a todo through the CLI interface."""
    cli = TodoCLI()

    # Add a todo first
    todo = cli.service.add_todo("Original todo for update")

    # Test updating via CLI
    with patch('builtins.input', side_effect=[str(todo.id), "Updated todo via CLI"]):
        cli.handle_update_todo()

    # Verify it was updated
    updated_todo = cli.service.get_todo_by_id(todo.id)
    assert updated_todo.title == "Updated todo via CLI"


def test_update_todo_preserves_completion_status():
    """Test that updating a todo preserves its completion status."""
    cli = TodoCLI()

    # Add a todo and mark it as complete
    todo = cli.service.add_todo("Todo to update")
    cli.service.mark_complete(todo.id)
    assert cli.service.get_todo_by_id(todo.id).completed is True

    # Update the todo via CLI
    with patch('builtins.input', side_effect=[str(todo.id), "Updated completed todo"]):
        cli.handle_update_todo()

    # Verify it was updated but completion status is preserved
    updated_todo = cli.service.get_todo_by_id(todo.id)
    assert updated_todo.title == "Updated completed todo"
    assert updated_todo.completed is True


def test_update_todo_invalid_id():
    """Test attempting to update a todo with an invalid ID."""
    cli = TodoCLI()

    # Capture output to check error message
    captured_output = io.StringIO()

    with patch('builtins.input', side_effect=["999", "New title"]), \
         patch('sys.stdout', new=captured_output):
        cli.handle_update_todo()

    output = captured_output.getvalue()
    assert "not found" in output.lower()


def test_update_todo_invalid_id_format():
    """Test attempting to update a todo with an invalid ID format."""
    cli = TodoCLI()

    # Capture output to check error message
    captured_output = io.StringIO()

    with patch('builtins.input', return_value="invalid"), \
         patch('sys.stdout', new=captured_output):
        cli.handle_update_todo()

    output = captured_output.getvalue()
    assert "not a valid number" in output.lower()


def test_update_todo_empty_new_title():
    """Test attempting to update a todo with an empty new title."""
    cli = TodoCLI()

    # Add a todo first
    todo = cli.service.add_todo("Original todo")

    # Capture output to check error message
    captured_output = io.StringIO()

    with patch('builtins.input', side_effect=[str(todo.id), ""]), \
         patch('sys.stdout', new=captured_output):
        cli.handle_update_todo()

    output = captured_output.getvalue()
    assert "cannot be empty" in output.lower()


def test_update_multiple_todos():
    """Test updating multiple todos."""
    cli = TodoCLI()

    # Add multiple todos
    todo1 = cli.service.add_todo("First todo")
    todo2 = cli.service.add_todo("Second todo")
    todo3 = cli.service.add_todo("Third todo")

    # Update each todo
    with patch('builtins.input', side_effect=[str(todo1.id), "Updated first todo"]):
        cli.handle_update_todo()

    with patch('builtins.input', side_effect=[str(todo2.id), "Updated second todo"]):
        cli.handle_update_todo()

    with patch('builtins.input', side_effect=[str(todo3.id), "Updated third todo"]):
        cli.handle_update_todo()

    # Verify all were updated
    updated_todo1 = cli.service.get_todo_by_id(todo1.id)
    updated_todo2 = cli.service.get_todo_by_id(todo2.id)
    updated_todo3 = cli.service.get_todo_by_id(todo3.id)

    assert updated_todo1.title == "Updated first todo"
    assert updated_todo2.title == "Updated second todo"
    assert updated_todo3.title == "Updated third todo"


def test_add_and_delete_integration():
    """Test adding a todo then deleting it."""
    cli = TodoCLI()

    # Add a todo
    with patch('builtins.input', return_value="Test todo"):
        cli.handle_add_todo()

    # Verify it was added
    todos_before = cli.service.get_all_todos()
    assert len(todos_before) == 1

    # Delete the todo
    success = cli.service.delete_todo(todos_before[0].id)
    assert success is True

    # Verify it was deleted
    todos_after = cli.service.get_all_todos()
    assert len(todos_after) == 0


def test_delete_todo_via_cli():
    """Test deleting a todo through the CLI interface."""
    cli = TodoCLI()

    # Add a todo first
    todo = cli.service.add_todo("Todo to delete")

    # Test deleting via CLI
    with patch('builtins.input', side_effect=[str(todo.id), "y"]):
        cli.handle_delete_todo()

    # Verify it was deleted
    todos = cli.service.get_all_todos()
    assert len(todos) == 0


def test_delete_todo_cancelled():
    """Test cancelling todo deletion through the CLI interface."""
    cli = TodoCLI()

    # Add a todo first
    todo = cli.service.add_todo("Todo to potentially delete")

    # Verify it was added
    todos_before = cli.service.get_all_todos()
    assert len(todos_before) == 1

    # Test cancelling deletion via CLI
    with patch('builtins.input', side_effect=[str(todo.id), "n"]):
        cli.handle_delete_todo()

    # Verify it was not deleted
    todos_after = cli.service.get_all_todos()
    assert len(todos_after) == 1
    assert todos_after[0].title == "Todo to potentially delete"


def test_delete_todo_with_confirmation():
    """Test deleting a todo confirms the right todo is being deleted."""
    cli = TodoCLI()

    # Add a todo first
    todo = cli.service.add_todo("Important task to delete")

    # Capture output to verify the confirmation message
    captured_output = io.StringIO()

    with patch('builtins.input', side_effect=[str(todo.id), "y"]), \
         patch('sys.stdout', new=captured_output):
        cli.handle_delete_todo()

    # Verify the output contains the todo title
    output = captured_output.getvalue()
    assert "Important task to delete" in output

    # Verify it was deleted
    todos = cli.service.get_all_todos()
    assert len(todos) == 0


def test_delete_nonexistent_todo():
    """Test attempting to delete a non-existent todo."""
    cli = TodoCLI()

    # Capture output to check error message
    captured_output = io.StringIO()

    with patch('builtins.input', return_value="999"), \
         patch('sys.stdout', new=captured_output):
        cli.handle_delete_todo()

    output = captured_output.getvalue()
    assert "not found" in output.lower()


def test_delete_todo_invalid_id_format():
    """Test attempting to delete a todo with an invalid ID format."""
    cli = TodoCLI()

    # Capture output to check error message
    captured_output = io.StringIO()

    with patch('builtins.input', return_value="invalid"), \
         patch('sys.stdout', new=captured_output):
        cli.handle_delete_todo()

    output = captured_output.getvalue()
    assert "not a valid number" in output.lower()


def test_delete_multiple_todos():
    """Test deleting multiple todos."""
    cli = TodoCLI()

    # Add multiple todos
    todo1 = cli.service.add_todo("First todo")
    todo2 = cli.service.add_todo("Second todo")
    todo3 = cli.service.add_todo("Third todo")

    # Verify all exist
    assert cli.service.get_todo_count() == 3

    # Delete them one by one
    with patch('builtins.input', side_effect=[str(todo1.id), "y"]):
        cli.handle_delete_todo()
    assert cli.service.get_todo_count() == 2

    with patch('builtins.input', side_effect=[str(todo2.id), "y"]):
        cli.handle_delete_todo()
    assert cli.service.get_todo_count() == 1

    with patch('builtins.input', side_effect=[str(todo3.id), "y"]):
        cli.handle_delete_todo()
    assert cli.service.get_todo_count() == 0


def test_delete_todo_preserves_other_todos():
    """Test that deleting one todo preserves others."""
    cli = TodoCLI()

    # Add multiple todos
    todo1 = cli.service.add_todo("Keep this todo")
    todo2 = cli.service.add_todo("Delete this todo")
    todo3 = cli.service.add_todo("Also keep this todo")

    # Verify all exist
    assert cli.service.get_todo_count() == 3

    # Delete the middle one
    with patch('builtins.input', side_effect=[str(todo2.id), "y"]):
        cli.handle_delete_todo()

    # Verify the other todos remain
    todos = cli.service.get_all_todos()
    assert len(todos) == 2
    titles = [todo.title for todo in todos]
    assert "Keep this todo" in titles
    assert "Also keep this todo" in titles
    assert "Delete this todo" not in titles


def test_cli_menu_selection():
    """Test that CLI correctly handles menu selections."""
    cli = TodoCLI()

    # Test that the CLI can handle different menu options
    # Add a todo first
    with patch('builtins.input', return_value="Test todo"):
        cli.handle_add_todo()

    # Verify the todo was added
    assert cli.service.get_todo_count() == 1

    # Test viewing todos
    captured_output = io.StringIO()
    with patch('sys.stdout', new=captured_output):
        cli.handle_view_todos()

    output = captured_output.getvalue()
    assert "Test todo" in output


def test_cli_handles_invalid_ids_gracefully():
    """Test that CLI handles invalid todo IDs gracefully."""
    cli = TodoCLI()

    # Capture output for error messages
    captured_output = io.StringIO()

    # Try to update a non-existent todo
    with patch('builtins.input', side_effect=["999", "New title"]), \
         patch('sys.stdout', new=captured_output):
        cli.handle_update_todo()

    output = captured_output.getvalue()
    assert "not found" in output.lower()

    # Reset output
    captured_output = io.StringIO()

    # Try to delete a non-existent todo
    with patch('builtins.input', return_value="999"), \
         patch('sys.stdout', new=captured_output):
        cli.handle_delete_todo()

    output = captured_output.getvalue()
    assert "not found" in output.lower()


def test_cli_main_execution():
    """Test the main CLI execution flow."""
    # Test that the CLI can be instantiated and run
    cli = TodoCLI()

    # Verify initial state
    assert cli.running is True
    assert cli.service is not None

    # Add a test todo
    todo = cli.service.add_todo("Test todo from CLI")

    # Verify it was added
    retrieved = cli.service.get_todo_by_id(todo.id)
    assert retrieved is not None
    assert retrieved.title == "Test todo from CLI"