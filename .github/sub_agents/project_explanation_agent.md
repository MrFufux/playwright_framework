# Project Explanation Agent Setup

This file contains the instructions and prompts for an agent designed to thoroughly analyze and explain the structure and functionality of the `interview_framework` project.

## Agent Goal
The primary goal of this agent is to read all relevant files in the workspace, understand the architectural patterns (e.g., POM, Fixture-based DI), and generate a comprehensive, easy-to-understand explanation of the entire framework.

## Execution Prompts

When executing this agent, use the following sequence of steps:

### Step 1: Code Archaeology & Analysis
1.  **Analyze Core Configuration**: Read `conftest.py` to understand how pytest fixtures manage Playwright context setup (`browser_context_args`, `ui_page`, `api_client`).
2.  **Analyze UI Abstraction**: Read `pages/base_page.py` to understand the Object-Oriented Programming (OOP) abstraction for UI interactions (e.g., `click_element()`, `fill_text()`).
3.  **Analyze API Layer**: Read `utils/api_client.py` to understand standardized HTTP client initialization with `httpx`.
4.  **Review Fixtures**: Examine the placeholder fixture files (`fixtures/api_fixture.py`, `fixtures/llm.py`, `fixtures/ui_fixture.py`) to identify areas requiring implementation.
5.  **Examine Structure**: Scan the entire directory structure to map out the project layout (e.g., `build/`, `data_driven_datasets/`).

### Step 2: Explanation Generation
1.  **Synthesize Architecture**: Based on the analysis from Step 1, synthesize a high-level architectural overview, focusing on the separation of concerns and dependency injection patterns used in the framework.
2.  **Detail Components**: Provide detailed explanations for each core component: Playwright setup, API handling, UI abstraction layer, and data handling.
3.  **Identify Next Steps**: Conclude by listing the pending implementation tasks (e.g., implementing logic within fixture files).

## Output Format
The final output should be a single, cohesive Markdown document that includes:
1.  A **High-Level Overview** of the framework's architecture.
2.  **Component Breakdown**: Detailed descriptions of `conftest.py`, `base_page.py`, `api_client.py`, and the fixture roles.
3.  **Actionable Summary**: A clear list of what is complete and what needs further development.