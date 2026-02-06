# Data Model: Phase I: In-Memory Python Console Todo App

**Date**: 2026-02-06
**Feature**: 001-todo-app
**Input**: Feature specification from `/specs/001-todo-app/spec.md`

## Overview

This document defines the data models for the in-memory Python console todo application. All models comply with the functional requirements from the specification and follow clean code principles with clear separation of concerns.

## Primary Data Model

### TodoItem

**Definition**: Represents a single todo task in the application

**Fields**:
- `id` (int): Unique identifier for the todo item; assigned sequentially starting from 1
- `title` (str): Text content of the todo item; descriptive text entered by the user
- `completed` (bool): Status indicator; True if the task is completed, False otherwise

**Data Types**:
- `id`: Python int type
- `title`: Python str type
- `completed`: Python bool type

**Validation Rules**:
- `id` must be a positive integer
- `title` must be non-empty string (after stripping whitespace)
- `title` length should be reasonable (less than 1000 characters)
- `completed` must be boolean value

**State Transitions**:
- `completed` can transition from False to True (marking as complete)
- `completed` can transition from True to False (marking as incomplete) - if feature is implemented
- `title` can be updated while maintaining the same `id`
- `id` remains constant throughout the lifecycle of the item

**Relationships**:
- Belongs to a single TodoList (collection of TodoItem objects)

## Collection Model

### TodoList

**Definition**: Container for multiple TodoItem objects; represents the user's collection of tasks

**Composition**:
- Contains zero or more TodoItem objects
- Maintains order of items as they are added
- Provides methods for adding, removing, updating, and querying TodoItem objects

**Operations**:
- Add TodoItem: Creates new item with next available ID
- Remove TodoItem: Deletes item by ID
- Update TodoItem: Modifies existing item by ID
- Find TodoItem: Retrieves item by ID
- List all items: Returns all TodoItem objects
- Filter by status: Returns TodoItem objects with specific completion status

## Data Lifecycle

### Creation
1. User provides title text
2. System assigns next available sequential ID
3. System sets completed status to False
4. TodoItem is added to TodoList

### Reading
1. User requests to view items
2. System returns formatted list of all TodoItem objects
3. Completed items are visually distinguished from pending items

### Update
1. User specifies item ID and new title text
2. System validates input
3. System updates title field of corresponding TodoItem
4. ID and completion status remain unchanged (unless specifically changing completion status)

### Deletion
1. User specifies item ID
2. System validates that ID exists
3. System removes TodoItem from TodoList
4. Remaining items retain their original IDs

### Completion Status Change
1. User specifies item ID
2. System validates that ID exists
3. System toggles completed status of corresponding TodoItem
4. Other fields remain unchanged

## Constraints

### Data Integrity
- Each TodoItem must have a unique ID within the TodoList
- IDs must be sequential positive integers starting from 1
- No duplicate IDs allowed
- Deleted IDs are not reused (next ID continues sequence)

### Validation
- Title cannot be empty or consist only of whitespace
- Title must be a valid string (no control characters that would break console display)
- ID must exist when performing operations on specific items
- ID must be a positive integer

### Memory Management
- Data exists only in memory during application runtime
- No persistence to files or external storage
- All data is lost when application terminates