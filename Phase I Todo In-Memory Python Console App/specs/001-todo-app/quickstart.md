# Quickstart Guide: Phase I: In-Memory Python Console Todo App

**Date**: 2026-02-06
**Feature**: 001-todo-app

## Overview

This guide provides instructions for setting up, running, and using the in-memory Python console todo application. The application implements five core todo operations: add, delete, update, view, and mark complete.

## Prerequisites

- Python 3.13+ installed
- UV package manager installed (for environment management)

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# For this Phase I application, no external dependencies are required
# The application uses only Python standard library
```

## Running the Application

### Direct Execution
```bash
cd src/cli
python main.py
```

### From Project Root
```bash
python -m src.cli.main
```

## Using the Application

Once launched, the application presents a menu-driven interface:

### Available Commands

1. **Add Todo**
   - Command: `add` or `1`
   - Prompts for: Todo description
   - Creates a new todo item with the next available ID

2. **View Todos**
   - Command: `view` or `2`
   - Displays all todos with their ID, status, and description
   - Completed items are visually distinguished

3. **Update Todo**
   - Command: `update` or `3`
   - Prompts for: Todo ID and new description
   - Updates the description of the specified todo

4. **Delete Todo**
   - Command: `delete` or `4`
   - Prompts for: Todo ID
   - Removes the specified todo from the list

5. **Mark Complete/Incomplete**
   - Command: `complete` or `5`
   - Prompts for: Todo ID
   - Toggles the completion status of the specified todo

6. **Exit**
   - Command: `exit`, `quit`, or `6`
   - Exits the application (all data will be lost)

### Example Usage Session

```
Welcome to the Todo App!
1. Add Todo
2. View Todos
3. Update Todo
4. Delete Todo
5. Mark Complete/Incomplete
6. Exit

Enter your choice: 1
Enter todo description: Buy groceries

Todo added successfully with ID 1!

Enter your choice: 2
Todos:
[ ] 1. Buy groceries

Enter your choice: 5
Enter todo ID to toggle: 1

Todo 1 status updated to: completed

Enter your choice: 2
Todos:
[x] 1. Buy groceries

Enter your choice: 6
Goodbye!
```

## Project Structure

```
src/
├── models/
│   └── todo_item.py      # TodoItem data model
├── services/
│   └── todo_service.py   # Core business logic
└── cli/
    └── main.py           # CLI interface and application entry point

tests/
├── unit/
│   ├── models/
│   │   └── test_todo_item.py
│   └── services/
│       └── test_todo_service.py
└── integration/
    └── test_cli_flow.py
```

## Testing

### Run All Tests
```bash
# From project root
python -m pytest tests/
```

### Run Specific Test Categories
```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# Specific test file
python -m pytest tests/unit/models/test_todo_item.py
```

## Development

### Adding New Features
1. Update the data model if new fields are needed
2. Add business logic to the service layer
3. Update the CLI interface to expose new functionality
4. Write tests for new functionality

### Architecture Principles
- Models: Data representation only (no business logic)
- Services: Business logic only (no UI concerns)
- CLI: User interaction only (no business logic)

## Troubleshooting

### Common Issues
- **Invalid command**: Ensure command is spelled correctly and is one of the available options
- **Invalid ID**: Verify the ID exists in the current list of todos
- **Empty input**: The application validates against empty todo descriptions

### Error Messages
- "Invalid command" - Command not recognized, see available commands
- "Todo with ID X not found" - The specified ID doesn't exist in the current list
- "Invalid ID" - ID is not a valid number
- "Todo description cannot be empty" - Input validation failed