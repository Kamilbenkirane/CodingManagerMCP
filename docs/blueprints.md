# Project Blueprints: Manager Agent with Cursor Integration via MCP

## 1. Overview

This document outlines the architecture for an AI-assisted coding system. The system features a **Manager Agent** that integrates with the **Cursor IDE** (used by the developer). Cursor, with its built-in AI code generation capabilities and the developer's guidance, serves as the primary code generation and editing environment. The Manager Agent provides high-level oversight, context awareness, and validation.

Communication between Cursor and the Manager Agent will be facilitated by the **Model-Controller-Protocol (MCP)**, allowing Cursor (as the controller) to leverage the Manager Agent (as a specialized model/tool).

The primary goal is to enhance the developer's workflow within Cursor by providing an intelligent assistant (the Manager Agent) that helps maintain project integrity, ensures alignment with goals, and validates code against a broader project context.

## 2. Core Components

### 2.1. Developer & Cursor IDE
*   **Developer**: The primary actor, writing and guiding code generation.
*   **Cursor IDE**: The development environment, providing AI-assisted code generation, editing, and version control capabilities. Cursor effectively acts as the "coding engine."

### 2.2. Manager Agent
An AI-powered agent responsible for:
*   Maintaining deep context about the specific software project.
*   Validating code developed in Cursor against project goals, architecture, and quality standards.
*   Providing feedback and contextual advice to the developer via Cursor.
*   Proactive suggestion generation.

### 2.3. Model-Controller-Protocol (MCP)
The communication standard enabling Cursor to interact with the Manager Agent.
*   Cursor acts as an MCP Controller.
*   The Manager Agent exposes its functionalities as MCP Tools/Capabilities.

## 3. Manager Agent Architecture

**Purpose**: To serve as an intelligent, project-aware assistant to the developer within Cursor.

**Key Responsibilities:**

*   **Project Context Management**:
    *   Stores and understands the overall project architecture, key modules, coding standards, specific requirements, and long-term goals.
    *   This context can be initialized (e.g., by analyzing the existing codebase or design documents) and updated by the developer via MCP calls. Initialization could involve the Manager Agent processing a curated set of project documentation (like READMEs, architectural diagrams, and key source files identified by the developer) or through a guided interactive setup process.
*   **On-Demand Code Validation & Analysis**:
    *   Receives code snippets or references to code sections from Cursor.
    *   Analyzes the code in the context of the overall project.
    *   Checks for alignment with project goals, architectural patterns, potential integration issues, and adherence to coding standards.
*   **Contextual Advice & Guidance**:
    *   Responds to specific queries from the developer (via Cursor) about how to implement features, use existing modules, or adhere to project conventions.
*   **Feedback Delivery**:
    *   Provides structured feedback (validation results, suggestions, warnings, errors) back to Cursor for display to the developer.
*   **Proactive Suggestion Generation**:
    *   Continuously analyzes ongoing code changes, developer activity patterns (if available and permitted), and the overall project context to identify potential improvements, risks, or relevant information.
    *   Generates suggestions, warnings, or tips that can be proactively offered to the developer.

### 3.1. Implementation Notes and Scalability
*   Likely powered by a Large Language Model (LLM) fine-tuned or prompted with project-specific information.
*   Will require a persistent or easily loadable state to maintain project context.
*   The project context storage and retrieval mechanisms should be architected for scalability to effectively support large and complex codebases.

## 4. MCP Interface for Manager Agent

The Manager Agent will expose the following MCP capabilities (Tools) for Cursor to consume:

### 4.1. Capability: `validate_code`
*   **Description**: Validates a given code snippet or file against the project's context, standards, and goals.
*   **MCP Request from Cursor**:
    *   `code_content: string` (The code to validate)
    *   `file_path: string` (Path of the file being edited/validated)
    *   `selection_range: object` (Optional: {start_line, end_line} if only a snippet is being validated)
    *   `developer_intent: string` (Optional: A brief description from the developer about what this code is supposed to do. This can be provided by the developer via a dedicated input in Cursor when triggering validation, or potentially inferred/pre-filled from the active task's description if `get_task_starting_context` was previously invoked.)
    *   `additional_context_paths: list[string]` (Optional: List of other relevant file paths for broader context. These paths can be specified by the developer or potentially suggested by Cursor based on code analysis or the task's scope.)
*   **MCP Response to Cursor**:
    *   `validation_id: string` (A unique ID for this validation request)
    *   `status: enum (valid, valid_with_suggestions, needs_revision, error)`
    *   `feedback_items: list[object]`
        *   `item_id: string`
        *   `severity: enum (info, suggestion, warning, error)`
        *   `message: string` (Detailed feedback text)
        *   `file_path: string` (File the feedback pertains to)
        *   `line_range: object` (Optional: {start_line, end_line} for specific code locations)
        *   `suggested_code_fix: string` (Optional: A proposed code change. This aims to be a concrete code snippet or a diff, facilitating easy review and application within the IDE.)

### 4.2. Capability: `get_project_advice`
*   **Description**: Provides contextual advice or answers questions related to the project.
*   **MCP Request from Cursor**:
    *   `query: string` (The developer's question, e.g., "What's the standard way to implement logging in this project?")
    *   `current_file_path: string` (Optional: The file the developer is currently working on)
    *   `related_code_snippet: string` (Optional: A snippet of code related to the query)
*   **MCP Response to Cursor**:
    *   `advice_id: string`
    *   `response_text: string` (The advice, explanation, or answer)
    *   `references: list[object]` (Optional: Pointers to relevant documentation, files, or code examples within the project)
        *   `reference_type: enum (documentation, file, code_example)`
        *   `path_or_url: string`
        *   `description: string`
    *   `suggested_sub_tasks: list[string]` (Optional: High-level sub-tasks the manager thinks might be involved)

### 4.3. Capability: `update_manager_context`
*   **Description**: Allows the developer to explicitly provide new information or updates to the Manager Agent's project context.
*   **MCP Request from Cursor**:
    *   `update_type: enum (new_dependency, architectural_decision, style_guide_change, feature_specification, file_annotation)`
    *   `summary: string` (A brief summary of the update)
    *   `details_uri_or_text: string` (URI to a document or the full text of the update)
    *   `relevant_file_paths: list[string]` (Optional: Files affected or related to this update)
*   **MCP Response to Cursor**:
    *   `update_id: string`
    *   `status: enum (context_updated, update_queued, error)`
    *   `message: string` (Optional: Confirmation or error details)

### 4.4. Capability: `get_task_starting_context`
*   **Description**: Provides relevant project context, guidelines, and pointers to assist the developer *before* they begin coding a specific task.
*   **MCP Request from Cursor**:
    *   `task_id: string` (Optional: A unique ID for the task if tracked)
    *   `task_description: string` (A clear description of what the developer intends to build or modify)
    *   `target_file_path: string` (The primary file path where the work will be done)
    *   `related_file_paths: list[string]` (Optional: Other file paths the developer or Cursor deems relevant for this task)
    *   `user_query_for_llm: string` (Optional: If the user has a specific query that they would use to prompt an LLM, this can be passed to the manager)
*   **MCP Response to Cursor**:
    *   `context_id: string` (A unique ID for this context response)
    *   `context_summary: string` (A brief textual summary of key considerations, e.g., "For this task, remember to use the `UserService` for data access and ensure all new API endpoints are registered in `routes.py`.")
    *   `relevant_modules_or_interfaces: list[object]`
        *   `name: string` (e.g., "UserService.create_user", "OrderProcessingQueue")
        *   `description: string` (Brief explanation or usage hint)
        *   `usage_example_snippet: string` (Optional: A very short example)
    *   `key_design_patterns_to_follow: list[string]` (e.g., "Repository Pattern for DB access", "Observer Pattern for event notifications")
    *   `code_style_reminders: list[string]` (e.g., "Ensure docstrings for all public methods", "Use f-strings for string formatting")
    *   `data_models_to_use: list[object]`
        *   `name: string` (e.g., "UserSchema", "ProductRecord")
        *   `definition_path_or_snippet: string` (Path to schema file or a snippet of the definition)
    *   `warnings_or_common_pitfalls: list[string]` (e.g., "Avoid direct database calls in controller logic", "Remember to handle potential `None` values from `get_item()`")
    *   `suggested_sub_tasks: list[string]` (Optional: High-level sub-tasks the manager thinks might be involved)

### 4.5. Capability: `stream_proactive_suggestions`
*   **Description**: Enables the Manager Agent to proactively send contextual suggestions, warnings, or opportunities to Cursor. These are derived from its continuous analysis of ongoing code changes, developer activity (where available), and the overall project context. This capability provides a stream of insights rather than a response to a direct, one-off developer request.
*   **MCP Interaction Model**:
    *   Cursor can subscribe to a stream of suggestions for a specific project or context.
    *   The Manager Agent pushes suggestions to Cursor through an established MCP channel as they are generated.
*   **MCP Data Pushed from Manager Agent to Cursor (Example Items in the Stream)**:
    *   `suggestion_id: string` (Unique ID for the suggestion)
    *   `type: enum (refactoring_opportunity, potential_bug, style_inconsistency, relevant_module_reminder, best_practice_tip, efficiency_improvement, new_api_usage, documentation_reminder)`
    *   `message: string` (Detailed description of the suggestion)
    *   `file_path: string` (Optional: The file the suggestion pertains to)
    *   `line_range: object` (Optional: {start_line, end_line} for specific code locations)
    *   `priority: enum (low, medium, high)` (To help Cursor prioritize display)
    *   `supporting_context_snippets: list[string]` (Optional: Short code snippets or references illustrating the point)
    *   `related_documentation_links: list[string]` (Optional: Links to relevant internal or external documentation)
*   **MCP Request from Cursor (to initiate or manage subscription)**:
    *   `action: enum (subscribe, unsubscribe, update_filters)`
    *   `project_id: string` (Identifier for the project context)
    *   `filter_preferences: object` (Optional: e.g., {min_priority: 'medium', types_to_include: ['potential_bug', 'refactoring_opportunity']})
*   **MCP Response to Cursor (on subscription management actions)**:
    *   `subscription_id: string` (If successful subscription/update)
    *   `status: enum (subscribed, unsubscribed, updated, error)`
    *   `message: string` (Optional: Confirmation or error details)

### 4.6. MCP Operational Considerations
*   **Communication Robustness**: To ensure reliable interaction between Cursor and the Manager Agent, strategies for handling MCP communication should be defined. This includes implementing appropriate retry mechanisms for transient network issues, setting reasonable timeouts for requests, and ensuring clear error propagation and reporting in case of failures.

## 5. Workflow Example

1.  **Developer in Cursor**: The developer is working on a new feature in `feature_x.py` and defines the task (e.g., "Implement user login logic").
2.  **Request Initial Context (MCP Call to `get_task_starting_context`)**:
    *   The developer (or an automated Cursor action) triggers the `get_task_starting_context` MCP capability of the Manager Agent.
    *   Cursor sends the `task_description` (e.g., "Implement user login logic") and `target_file_path` (`feature_x.py`) to the Manager Agent.
3.  **Manager Agent Processing (Context Provision)**:
    *   The Manager Agent analyzes the request and consults its project context.
    *   It returns a structured context, including relevant modules (e.g., `AuthService`), design patterns, data models, and potential pitfalls.
4.  **Developer Reviews Context & Codes with Cursor AI**:
    *   Cursor displays this context to the developer.
    *   The developer uses this information to write a more effective prompt for Cursor's AI and to guide the AI in generating the initial code for the login function.
5.  **Request Validation (MCP Call to `validate_code`)**:
    *   Once an initial version of the code is ready, the developer (or an automated Cursor action) triggers the `validate_code` MCP capability.
    *   Cursor sends the content of `feature_x.py` (or the selected function) to the Manager Agent.
6.  **Manager Agent Processing (Validation)**:
    *   The Manager Agent receives the MCP request.
    *   It analyzes the provided code against its knowledge of `project_architecture.md`, `auth_module.py`, `coding_standards.txt`, the overall goals for "feature_x", and the initial context it provided.
7.  **Feedback to Developer (MCP Response)**:
    *   The Manager Agent sends an MCP response back to Cursor.
    *   Example feedback:
        *   `status: valid_with_suggestions`
        *   `feedback_items: [`
            *   `{severity: suggestion, message: "Consider using the centralized 'AuthService.login()' instead of direct DB access, as suggested in initial context.", line_range: {start: 10, end: 15}}`,
            *   `{severity: warning, message: "Missing error handling for invalid credentials."}`
            *   `]`
8.  **Developer Action**:
    *   Cursor displays this feedback to the developer, potentially highlighting the relevant code sections.
    *   The developer reviews the feedback and refines the code in Cursor.
9.  **Request Advice (MCP Call - Optional)**:
    *   Developer is unsure about a specific aspect, e.g., "How to handle session tokens securely?"
    *   Developer triggers `get_project_advice` capability via Cursor. Manager Agent provides guidance based on project standards and the initial context provided for the task.
10. **Cycle Repeats**: The developer continues coding (potentially requesting more context for sub-tasks), validating, and seeking advice until the feature is complete and meets the Manager Agent's validation criteria. Throughout this process, the `stream_proactive_suggestions` capability may also provide continuous, ambient feedback and tips.

## 6. Future Considerations

*   **Deeper Cursor Integration**: UI elements within Cursor specifically designed to interact with the Manager Agent's MCP capabilities (e.g., dedicated panels, right-click menu options, seamless display of proactive suggestions).
*   **Automated Context Updates**: Manager Agent could attempt to automatically update its context by observing file changes or version control history (with appropriate safeguards).
*   **Team Collaboration**: If multiple developers use similar Manager Agents, exploring ways to share or synchronize relevant project context.
*   **MCP Versioning and Evolution**: Establish a strategy for versioning the MCP API and managing updates to the Manager Agent's core logic or context interpretation to ensure smooth evolution and backward compatibility where feasible.
*   **Feedback Granularity and User Control**: Explore allowing developers to customize the types, verbosity, or severity levels of feedback they receive from the `validate_code` and `stream_proactive_suggestions` capabilities to better suit individual preferences or specific tasks.
*   **Security and Privacy**: As the project matures or if it handles more sensitive information/is used in a team context, conduct an in-depth analysis and implement robust security and privacy measures. This would include data encryption, access controls, and defining clear data handling policies.

This revised blueprint provides a foundation for building a Manager Agent that works in tandem with the developer and Cursor IDE.
