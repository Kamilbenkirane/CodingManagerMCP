# Coding Plan: Manager Agent with Cursor Integration

This document outlines the repository structure and the development tasks for building the Manager Agent.

## 1. Repository Structure

The project will be organized as follows:

```
.
├── .gitattributes                 # Handles line endings
├── .gitignore                     # Specifies intentionally untracked files
├── .pre-commit-config.yaml        # Configuration for pre-commit hooks
├── LICENSE                        # Project license (e.g., MIT, Apache 2.0)
├── README.md                      # Main project overview and setup instructions
├── pyproject.toml                 # For project metadata, dependencies (incl. dev), and tool configurations (Black, isort, Flake8, uv)
├── docs/                          # General documentation
│   ├── blueprints.md              # System architecture and MCP specification
│   └── coding_plan.md             # This file
├── data/                          # For sample data, e.g., initial project context
│   └── sample_project_context.json # Example context for testing ContextManager
├── scripts/                       # Utility and helper scripts
│   └── run_server.sh              # Example script to start the MCP server
├── src/                           # Source code for the Manager Agent
│   └── manager_agent/             # Main Python package for the agent
│       ├── __init__.py
│       ├── agent.py               # Core ManagerAgent class and logic
│       ├── mcp_server.py          # FastAPI server exposing MCP capabilities
│       ├── context_manager.py     # Manages loading, storing, and updating project context
│       ├── llm_interface.py       # Interface for communication with an LLM
│       ├── models.py              # Pydantic models for MCP request/response data structures
│       ├── enums.py               # Common enumeration types used across the agent
│       └── capabilities/          # Modules for each MCP capability
│           ├── __init__.py
│           ├── validate_code.py
│           ├── get_project_advice.py
│           ├── update_manager_context.py
│           ├── get_task_starting_context.py
│           └── stream_proactive_suggestions.py
└── tests/                         # Unit and integration tests
    ├── __init__.py
    ├── conftest.py                # Pytest fixtures and configuration
    ├── test_models.py             # Tests for Pydantic models
    ├── test_context_manager.py    # Tests for ContextManager
    └── capabilities/
        ├── __init__.py
        └── test_validate_code.py  # Example test file for a capability
```

## 2. Development Phases and Tasks

The development will proceed in the following phases and tasks. Each task aims to be specific and contribute to a functional increment.

### Phase 0: Project Governance & Foundation

*   **Task 0.1: Confirm Requirements & Version Control Strategy**
    *   [x] Thoroughly review `docs/blueprints.md` to ensure full understanding of requirements.
    *   [x] Establish and document a version control strategy (e.g., Gitflow, feature branches, PR templates). Chosen strategy: **Gitflow**.

### Phase 1: Core Setup & Environment

*   **Task 1.1: Initialize Git & Base Directories**
    *   [x] Initialize Git repository.
    *   [x] Create base directory structure: `src/manager_agent/capabilities`, `docs/`, `scripts/`, `data/`, `tests/capabilities/`.
    *   [x] Move `blueprints.md` and `coding_plan.md` into `docs/`.
*   **Task 1.2: Create Standard Project Files**
    *   [x] Create `.gitignore` (Python, IDE specifics, OS files).
    *   [x] Add `LICENSE` file (e.g., MIT or Apache 2.0).
    *   [x] Add `.gitattributes` to enforce LF line endings.
*   **Task 1.3: Setup Python Environment (uv)**
    *   [x] Create virtual environment: `uv venv`
    *   [x] Activate environment (e.g., `source .venv/bin/activate`)
*   **Task 1.4: Configure Linters, Formatters & Pre-commit Hooks**
    *   [x] Create `pyproject.toml`; configure `black`, `isort`, `flake8` (with plugins like `flake8-bugbear`, `flake8-comprehensions`), `mypy`, and `uv` (e.g., for dev dependencies if not using optional groups).
    *   [x] Create `.pre-commit-config.yaml`.
    *   [x] Include hooks for `black`, `isort`, `flake8`, `mypy`, `check-yaml`, `check-toml`, `end-of-file-fixer`, `trailing-whitespace`.
    *   [x] Install pre-commit hooks into the environment: `uv run pre-commit install`
    *   [x] Install project dependencies (defined in `pyproject.toml`): `uv pip install -e .[dev]` (assuming dev dependencies are in an optional group)
*   **Task 1.5: Initial Documentation**
    *   [x] Create a basic `README.md` with project title, brief description, and initial setup badge.

### Phase 2: Define Data Structures & Core Interfaces

*   **Task 2.1: Define MCP Enums**
    *   [x] In `src/manager_agent/enums.py`, define all `Enum` types specified in `blueprints.md`:
        *   [x] `StatusEnum` (for `ValidateCodeResponse`, `UpdateManagerContextResponse`, `StreamProactiveSuggestionsSubscriptionResponse`)
        *   [x] `SeverityEnum` (for `ValidationFeedbackItem`)
        *   [x] `ReferenceTypeEnum` (for `ReferenceItem`)
        *   [x] `UpdateTypeEnum` (for `UpdateManagerContextRequest`)
        *   [x] `SuggestionTypeEnum` (for `ProactiveSuggestionItem`)
        *   [x] `PriorityEnum` (for `ProactiveSuggestionItem`)
        *   [x] `SubscriptionActionEnum` (for `StreamProactiveSuggestionsSubscriptionRequest`)
*   **Task 2.2: Define MCP Pydantic Models**
    *   [x] In `src/manager_agent/models.py`, define Pydantic models for all MCP request/response structures (as per `blueprints.md`), importing enums from `enums.py`.
        *   [x] `ValidateCodeRequest`, `ValidationFeedbackItem`, `ValidateCodeResponse`
        *   [x] `GetProjectAdviceRequest`, `ReferenceItem`, `GetProjectAdviceResponse`
        *   [x] `UpdateManagerContextRequest`, `UpdateManagerContextResponse`
        *   [x] `GetTaskStartingContextRequest`, `RelevantModuleOrInterface`, `DataModelToUse`, `GetTaskStartingContextResponse`
        *   [x] `StreamProactiveSuggestionsSubscriptionRequest`, `ProactiveSuggestionItem`, `StreamProactiveSuggestionsSubscriptionResponse`
*   **Task 2.3: Define `ProjectContext` Schema and Sample**
    *   [x] Define a Pydantic model for `ProjectContext` in `src/manager_agent/context_manager.py`. This model should be capable of storing various context elements (architecture details, key modules, coding standards, requirements, goals).
    *   [x] Create a `data/sample_project_context.json` file representing a minimal, valid project context for development and testing.
*   **Task 2.4: Design `LLMInterface`**
    *   [x] In `src/manager_agent/llm_interface.py`, define the `LLMInterface` class.
    *   [x] Define abstract or placeholder method signatures based on interactions needed for MCP capabilities (e.g., `async def analyze_code_for_validation(code: str, file_path: str, project_context: ProjectContext, developer_intent: str | None) -> list[ValidationFeedbackItem]`, `async def generate_advice(query: str, project_context: ProjectContext) -> GetProjectAdviceResponse`).
    *   [x] Implement initial mock responses for these methods that return predictable, structured data according to Pydantic models.

### Phase 3: Implement Core Agent Logic & Server

*   **Task 3.1: Implement `ContextManager`**
    *   [ ] In `src/manager_agent/context_manager.py`:
        *   [ ] Implement `ContextManager` class.
        *   [ ] Method: `async def load_context(project_id: str) -> ProjectContext` (initially loads from `data/sample_project_context.json`).
        *   [ ] Method: `async def update_context(project_id: str, update_details: UpdateManagerContextRequest) -> None` (updates in-memory context; persistence is a future enhancement).
        *   [ ] Method: `async def get_context(project_id: str) -> ProjectContext` (retrieves in-memory context).
*   **Task 3.2: Implement Core `ManagerAgent`**
    *   [ ] In `src/manager_agent/agent.py`:
        *   [ ] Implement `ManagerAgent` class.
        *   [ ] Constructor to initialize `ContextManager` and `LLMInterface`.
        *   [ ] Placeholder methods for each MCP capability, e.g., `async def validate_code_capability(self, request: ValidateCodeRequest) -> ValidateCodeResponse:`. These will delegate to specific capability handlers.
*   **Task 3.3: Implement MCP Server (FastAPI)**
    *   [ ] In `src/manager_agent/mcp_server.py`:
        *   [ ] Implement FastAPI server.
        *   [ ] Define routes for each MCP capability, e.g., `/validate_code`, `/get_project_advice`, `/update_manager_context`, `/get_task_starting_context`, `/stream_proactive_suggestions`.
        *   [ ] Implement request validation and response serialization using Pydantic models.
        *   [ ] Implement error handling and logging.
