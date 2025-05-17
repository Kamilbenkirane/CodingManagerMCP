# Manager Agent for Cursor Integration

[![Project Status: WIP](https://img.shields.io/badge/project%20status-WIP-yellow.svg)](https://your-project-status-url.com) <!-- Replace with actual badge/status URL if available -->

An AI-powered Manager Agent designed to integrate with the Cursor IDE via the Model-Controller-Protocol (MCP). This agent provides high-level project oversight, context-aware code validation, and intelligent assistance to enhance the developer's workflow within Cursor.

## Overview

The Manager Agent maintains deep context about a specific software project, including its architecture, coding standards, requirements, and goals. It uses this knowledge to:

*   Validate code developed in Cursor.
*   Provide contextual advice and guidance.
*   Offer proactive suggestions for improvements and best practices.

Communication with Cursor is facilitated through a defined MCP interface, allowing Cursor to leverage the Manager Agent's capabilities seamlessly.

## Features (Planned - based on MCP Capabilities)

*   **`validate_code`**: Validates code snippets or files against project context.
*   **`get_project_advice`**: Answers developer queries related to the project.
*   **`update_manager_context`**: Allows explicit updates to the agent's project knowledge.
*   **`get_task_starting_context`**: Provides relevant information before starting a new coding task.
*   **`stream_proactive_suggestions`**: Proactively sends contextual tips and warnings.

## Getting Started

(Instructions for setup, installation, and running the agent will be added here as development progresses.)

### Prerequisites

*   Python 3.9+
*   uv (for environment and package management)

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/manager-agent.git # Replace with your repo URL
    cd manager-agent
    ```

2.  **Create virtual environment and install dependencies:**
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    uv pip install -e '.[dev]'
    ```

3.  **Install pre-commit hooks:**
    ```bash
    uv run pre-commit install
    ```

4.  **Run the server (example):**
    ```bash
    # Detailed script/command will be provided in scripts/run_server.sh
    # For now, an example using uvicorn directly (once mcp_server.py is created):
    # uv run uvicorn src.manager_agent.mcp_server:app --reload
    ```

## Contributing

(Contribution guidelines will be added here.)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
