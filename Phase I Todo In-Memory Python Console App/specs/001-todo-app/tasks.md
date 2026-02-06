---
description: "Task list for Phase I: In-Memory Python Console Todo App"
---

# Tasks: Phase I: In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: The feature specification requests testing, so test tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan
- [x] T002 [P] Initialize Python project with proper directory structure
- [x] T003 [P] Create src/models/, src/services/, src/cli/, tests/unit/, tests/integration/ directories

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create TodoItem data model in src/models/todo_item.py
- [x] T005 Create TodoService class skeleton in src/services/todo_service.py
- [x] T006 [P] Create basic CLI structure in src/cli/main.py
- [x] T007 Create initial test directory structure for unit tests
- [x] T008 [P] Create pytest configuration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Todo Item (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new todo items to their list

**Independent Test**: Can be fully tested by launching the application, adding a todo item, and verifying it appears in the list.

### Tests for User Story 1
- [x] T009 [P] [US1] Create unit test for TodoItem model in tests/unit/models/test_todo_item.py
- [x] T010 [P] [US1] Create unit test for adding todo functionality in tests/unit/services/test_todo_service.py
- [x] T011 [US1] Create integration test for adding todo via CLI in tests/integration/test_cli_flow.py

### Implementation for User Story 1
- [x] T012 [P] [US1] Implement TodoItem data model with id, title, completed fields in src/models/todo_item.py
- [x] T013 [US1] Implement add_todo method in TodoService class in src/services/todo_service.py
- [x] T014 [US1] Implement add todo functionality in CLI interface in src/cli/main.py
- [x] T015 [US1] Add input validation for adding todo items

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Todo Items (Priority: P2)

**Goal**: Allow users to see all their current todo items

**Independent Test**: Can be fully tested by adding some items and then viewing the complete list to verify they're displayed properly.

### Tests for User Story 2
- [x] T016 [P] [US2] Create unit test for viewing todos in tests/unit/services/test_todo_service.py
- [x] T017 [US2] Create integration test for viewing todos via CLI in tests/integration/test_cli_flow.py

### Implementation for User Story 2
- [x] T018 [US2] Implement get_all_todos method in TodoService class in src/services/todo_service.py
- [x] T019 [US2] Implement display todos functionality in CLI interface in src/cli/main.py
- [x] T020 [US2] Add visual distinction for completed vs pending items in display

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Todo as Complete (Priority: P3)

**Goal**: Allow users to mark a todo item as complete when they finish a task

**Independent Test**: Can be fully tested by adding items, marking one as complete, and verifying the status change is reflected when viewing the list.

### Tests for User Story 3
- [x] T021 [P] [US3] Create unit test for marking todo as complete in tests/unit/services/test_todo_service.py
- [x] T022 [US3] Create integration test for marking todo complete via CLI in tests/integration/test_cli_flow.py

### Implementation for User Story 3
- [x] T023 [US3] Implement mark_complete method in TodoService class in src/services/todo_service.py
- [x] T024 [US3] Implement mark todo complete functionality in CLI interface in src/cli/main.py
- [x] T025 [US3] Add input validation for marking todo complete

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Todo Item (Priority: P4)

**Goal**: Allow users to modify an existing todo item

**Independent Test**: Can be fully tested by adding an item, updating its content, and verifying the change is reflected when viewing the list.

### Tests for User Story 4
- [x] T026 [P] [US4] Create unit test for updating todo in tests/unit/services/test_todo_service.py
- [x] T027 [US4] Create integration test for updating todo via CLI in tests/integration/test_cli_flow.py

### Implementation for User Story 4
- [x] T028 [US4] Implement update_todo method in TodoService class in src/services/todo_service.py
- [x] T029 [US4] Implement update todo functionality in CLI interface in src/cli/main.py
- [x] T030 [US4] Add input validation for updating todo items

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Todo Item (Priority: P5)

**Goal**: Allow users to remove a todo item from their list

**Independent Test**: Can be fully tested by adding items, deleting one, and verifying it no longer appears when viewing the list.

### Tests for User Story 5
- [x] T031 [P] [US5] Create unit test for deleting todo in tests/unit/services/test_todo_service.py
- [x] T032 [US5] Create integration test for deleting todo via CLI in tests/integration/test_cli_flow.py

### Implementation for User Story 5
- [x] T033 [US5] Implement delete_todo method in TodoService class in src/services/todo_service.py
- [x] T034 [US5] Implement delete todo functionality in CLI interface in src/cli/main.py
- [x] T035 [US5] Add input validation for deleting todo items

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T036 [P] Add comprehensive error handling for all operations
- [x] T037 [P] Add input validation for all user inputs
- [x] T038 [P] Add handling for edge cases (invalid indices, empty inputs, etc.)
- [x] T039 [P] Improve CLI user experience with clear menus and prompts
- [x] T040 [P] Add comprehensive docstrings and comments
- [x] T041 [P] Run all tests to ensure everything works together
- [x] T042 [P] Update quickstart guide with complete usage instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2 → P3 → P4 → P5)
  - Some components within stories can be developed in parallel
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) can be written alongside implementation
- Models implemented first in Phase 2
- Services contain business logic for each operation
- CLI implements user interface for each operation
- Story complete when all components are implemented and tested

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in priority order
- Cross-cutting concerns in Phase 8 can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Todo)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Run tests for US1 and verify functionality

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP!
3. Add User Story 2 → Test independently → Enhanced functionality
4. Add User Story 3 → Test independently → Enhanced functionality
5. Add User Story 4 → Test independently → Enhanced functionality
6. Add User Story 5 → Test independently → Complete functionality
7. Each story adds value without breaking previous stories

### Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Create unit test for TodoItem model in tests/unit/models/test_todo_item.py"
Task: "Create unit test for adding todo functionality in tests/unit/services/test_todo_service.py"
Task: "Create integration test for adding todo via CLI in tests/integration/test_cli_flow.py"

# Launch all components for User Story 1 together:
Task: "Implement TodoItem data model with id, title, completed fields in src/models/todo_item.py"
Task: "Implement add_todo method in TodoService class in src/services/todo_service.py"
Task: "Implement add todo functionality in CLI interface in src/cli/main.py"
```

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence