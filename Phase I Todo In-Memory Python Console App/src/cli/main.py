"""
Main CLI interface for the todo application.

This module provides the command-line interface for interacting with the todo application.
"""

import sys
from typing import Optional
from ..services.todo_service import TodoService


class TodoCLI:
    """
    Command-line interface for the todo application.

    Provides methods for user interaction with the todo service.
    """

    def __init__(self) -> None:
        """Initialize the CLI with a TodoService instance."""
        self.service = TodoService()
        self.running = True

    def display_menu(self) -> None:
        """Display the main menu options to the user."""
        print("\n" + "="*40)
        print("           TODO APPLICATION")
        print("="*40)
        print("1. Add Todo")
        print("2. View Todos")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Mark Complete/Incomplete")
        print("6. Exit")
        print("="*40)

    def get_user_choice(self) -> str:
        """
        Get the user's menu choice.

        Returns:
            The user's choice as a string
        """
        try:
            choice = input("Enter your choice (1-6): ").strip().lower()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting application...")
            return "6"  # Return exit choice

    def handle_add_todo(self) -> None:
        """Handle the add todo functionality."""
        try:
            title = input("Enter todo description: ").strip()

            if not title:
                print("Error: Todo description cannot be empty.")
                return

            if len(title) > 1000:
                print("Error: Todo description is too long (max 1000 characters).")
                return

            todo = self.service.add_todo(title)
            print(f"Todo added successfully with ID {todo.id}!")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error adding todo: {e}")

    def handle_view_todos(self) -> None:
        """Handle the view todos functionality."""
        todos = self.service.get_all_todos()

        if not todos:
            print("\nNo todos found.")
            return

        print(f"\nTodos ({len(todos)} total):")
        print("-" * 50)

        for todo in todos:
            status = "[x]" if todo.completed else "[ ]"
            print(f"{status} {todo.id}. {todo.title}")

    def handle_update_todo(self) -> None:
        """Handle the update todo functionality."""
        try:
            if self.service.get_todo_count() == 0:
                print("No todos available to update.")
                return

            todo_id_str = input("Enter todo ID to update: ").strip()

            if not todo_id_str:
                print("Error: Todo ID cannot be empty.")
                return

            try:
                todo_id = int(todo_id_str)
            except ValueError:
                print(f"Error: '{todo_id_str}' is not a valid number.")
                return

            # Check if todo exists
            existing_todo = self.service.get_todo_by_id(todo_id)
            if not existing_todo:
                print(f"Error: Todo with ID {todo_id} not found.")
                return

            new_title = input(f"Enter new title for todo {todo_id} ('{existing_todo.title}'): ").strip()

            if not new_title:
                print("Error: New title cannot be empty.")
                return

            if len(new_title) > 1000:
                print("Error: New title is too long (max 1000 characters).")
                return

            success = self.service.update_todo(todo_id, new_title)
            if success:
                print(f"Todo {todo_id} updated successfully!")
            else:
                print(f"Error: Failed to update todo {todo_id}.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error updating todo: {e}")

    def handle_delete_todo(self) -> None:
        """Handle the delete todo functionality."""
        try:
            if self.service.get_todo_count() == 0:
                print("No todos available to delete.")
                return

            todo_id_str = input("Enter todo ID to delete: ").strip()

            if not todo_id_str:
                print("Error: Todo ID cannot be empty.")
                return

            try:
                todo_id = int(todo_id_str)
            except ValueError:
                print(f"Error: '{todo_id_str}' is not a valid number.")
                return

            # Check if todo exists
            existing_todo = self.service.get_todo_by_id(todo_id)
            if not existing_todo:
                print(f"Error: Todo with ID {todo_id} not found.")
                return

            confirm = input(f"Are you sure you want to delete todo '{existing_todo.title}'? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                success = self.service.delete_todo(todo_id)
                if success:
                    print(f"Todo {todo_id} deleted successfully!")
                else:
                    print(f"Error: Failed to delete todo {todo_id}.")
            else:
                print("Deletion cancelled.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error deleting todo: {e}")

    def handle_mark_complete(self) -> None:
        """Handle the mark complete/incomplete functionality."""
        try:
            if self.service.get_todo_count() == 0:
                print("No todos available to mark.")
                return

            todo_id_str = input("Enter todo ID to toggle completion status: ").strip()

            if not todo_id_str:
                print("Error: Todo ID cannot be empty.")
                return

            try:
                todo_id = int(todo_id_str)
            except ValueError:
                print(f"Error: '{todo_id_str}' is not a valid number.")
                return

            # Check if todo exists
            existing_todo = self.service.get_todo_by_id(todo_id)
            if not existing_todo:
                print(f"Error: Todo with ID {todo_id} not found.")
                return

            success = self.service.toggle_completion_status(todo_id)
            if success:
                new_status = "completed" if existing_todo.completed else "incomplete"
                print(f"Todo {todo_id} status updated to: {new_status}")
            else:
                print(f"Error: Failed to update todo {todo_id} status.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error updating completion status: {e}")

    def handle_exit(self) -> None:
        """Handle the exit functionality."""
        print("Goodbye!")
        self.running = False

    def execute_choice(self, choice: str) -> None:
        """
        Execute the action based on the user's choice.

        Args:
            choice: The user's menu choice
        """
        if choice in ['1', 'add']:
            self.handle_add_todo()
        elif choice in ['2', 'view', 'list']:
            self.handle_view_todos()
        elif choice in ['3', 'update']:
            self.handle_update_todo()
        elif choice in ['4', 'delete']:
            self.handle_delete_todo()
        elif choice in ['5', 'complete', 'toggle']:
            self.handle_mark_complete()
        elif choice in ['6', 'exit', 'quit']:
            self.handle_exit()
        else:
            print(f"Invalid choice: '{choice}'. Please enter a number between 1-6.")

    def run(self) -> None:
        """Run the main application loop."""
        print("Welcome to the Todo App!")

        while self.running:
            self.display_menu()
            choice = self.get_user_choice()
            self.execute_choice(choice)


def main() -> None:
    """Entry point for the application."""
    try:
        cli = TodoCLI()
        cli.run()
    except Exception as e:
        print(f"Fatal error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()