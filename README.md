# Wazoku Framework

A framework designed for web automation and testing, built using Python.

## Table of Contents
- [ ] Installation
- [ ] Setup Environment
- [ ] Usage Guide
- [ ] Project Structure

## Table of Contents
- [ ] Installation
- [ ] Setup Environment
- [ ] Usage Guide
- [ ] Project Structure

## Installation

This project is set up for running tests and automating web interactions.

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd wazoku_framework
    ```

2.  **Install dependencies**:
    The project uses `pyproject.toml` for dependency management. Install required packages using pip:
    ```bash
    pip install -r requirements.txt  # Assuming requirements.txt exists or use poetry/pipenv if configured via pyproject.toml
    # If using Poetry:
    # poetry install
    ```

3.  **Setup Testing Environment**:
    Ensure you have the necessary environment variables and configuration files (like `conftest.py`) set up for pytest to run correctly.

## Setup Environment

To run tests and utilize the framework components, ensure your environment is properly configured.

1.  **Dependencies**: Install all necessary Python packages listed in `pyproject.toml`.
2.  **Configuration**: Verify that configuration files like `pytest.ini` and `conftest.py` are present and correctly configured for test execution.
3.  **Data Files**: Ensure data payloads (`data_driven_datasets/*.json`) are accessible if they are used by the tests.

## Usage Guide

### Running Tests
Tests can be executed using `pytest`:
```bash
pytest
```
Specific API or UI tests can be targeted using the structure under `test/API/` and `test/UI/`.

### Framework Components
*   **Pages**: Files in the `pages/` directory (e.g., `base_page.py`, `home_page.py`) contain reusable page objects or base classes for web interactions.
*   **Utilities**: Files in the `utils/` directory (e.g., `api_client.py`, `helpers.py`) provide utility functions for making API calls and general helper operations.
*   **Conftest**: The `conftest.py` file configures pytest hooks and fixtures for the entire framework.

## Project Structure

The project is organized as follows:

```
wazoku_framework/
├── conftest.py          # Pytest configuration and fixtures
├── jenkinsfile          # CI/CD pipeline definition
├── pyproject.toml       # Project dependencies and build system configuration
├── pytest.ini           # Pytest configuration settings
├── README.md            # This file
├── data_driven_datasets/ # JSON data files used for testing
│   ├── api_payloads.json
│   └── ui_data.json
├── pages/               # Reusable page object definitions
│   ├── base_page.py
│   └── home_page.py
├── test/                # Test files
│   ├── API/             # API related tests
│   └── UI/              # UI related tests
└── utils/               # Utility functions
    ├── api_client.py
    └── helpers.py