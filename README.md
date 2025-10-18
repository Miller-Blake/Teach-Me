# Teach-Me: Your AI-Powered Code Tutor CLI

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Test Status](https://img.shields.io/badge/tests-passing-brightgreen.svg) <!-- Placeholder for CI/CD test status -->

## Project Overview

`teach-me` (the `teach_me` Python module) is an innovative Command Line Interface (CLI) tool
 designed to transform your terminal into a dynamic and interactive code tutor. Leveraging the power of AI, it provides comprehensive, line-by-line explanations of your code, answers specific questions, and adapts its teaching style through various personas to match your unique learning preferences. This tool is ideal for developers seeking to deepen their understanding of code, debug complex logic, or simply explore new programming concepts with personalized guidance.

## Features

*   **Intelligent Code Explanation**: Receive detailed, line-by-line explanations for any code snippet, enhancing comprehension.
*   **Interactive Tutoring Sessions**: Engage in a conversational Q&A with an AI tutor about your code, facilitating deeper learning.
*   **Customizable Teaching Personas**: Choose from a range of personas (e.g., Professor, Peer, Debugger, Storyteller, Comedian, Minimalist) to tailor the learning experience to your style.
*   **Seamless Code Input**: Easily pipe code directly from files or other commands into `teach-me` for instant analysis.
*   **Rich Terminal Output**: Enjoy beautifully formatted and syntax-highlighted explanations directly in your terminal, powered by `rich`.

## Installation

This guide will walk you through setting up the `teach-me` CLI tool on your local machine.

### Prerequisites

Ensure you have the following installed:

*   **Python 3.8 or higher** (recommended for best compatibility)
*   **pip** (Python's package installer)
*   **Git** (for cloning the repository)

### 1. Clone the Repository

Start by cloning the project repository to your local machine:

```bash
git clone https://github.com/your-username/teach-me.git # Replace with actual repo URL
cd teach-me
```

### 2. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies, ensuring a clean and isolated development environment.

**Create a virtual environment:**

```bash
python -m venv venv
```

**Activate the virtual environment:**

*   **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
*   **On macOS and Linux:**
    ```bash
    source venv/bin/activate
    ```

### 3. Install Dependencies

With your virtual environment activated, install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Making `teach-me` Globally Accessible (Optional but Recommended)

To use `teach-me` as a command-line tool from any directory, you have two main options:

#### Option A: Using `py -m teach_me` (Recommended for Python Environments)

This method is generally more reliable and doesn't require modifying your system's PATH. It explicitly tells Python to run the `teach_me` module.

**Usage Example:**

Instead of `teach-me interactive my_script.py`, you would use:

```bash
py -m teach_me interactive my_script.py --lang python
```

This approach works well when calling `teach-me` from other Python scripts or when you prefer not to modify system-wide environment variables.

#### Option B: Adding to System PATH (For Direct CLI Access)

If you want to run `teach-me` directly as a command (e.g., `teach-me interactive my_script.py`) from any terminal, you need to add the directory containing the `teach-me.exe` executable to your system's PATH environment variable.

**For Windows Users:**

The `teach-me.exe` script is typically installed in your Python's `Scripts` directory. Based on your system, this path is likely:

`C:\Users\bmill\AppData\Local\Programs\Python\Python313\Scripts`

To add this to your system's PATH:

1.  **Search for "Environment Variables"** in the Windows search bar and select "Edit the system environment variables".
2.  Click the "**Environment Variables...**" button.
3.  Under "System variables", find and select the `Path` variable, then click "**Edit...**".
4.  Click "**New**" and add the path: `C:\Users\bmill\AppData\Local\Programs\Python\Python313\Scripts`
5.  Click "**OK**" on all open windows to save the changes.

**Important:** You might need to restart your command prompt or IDE for the changes to take effect.

### 5. Configure Your OpenAI API Key

`teach-me` utilizes the OpenAI API for its core AI capabilities. You must provide your API key for the tool to function.

1.  **Obtain an API Key**: If you don't have one, sign up and generate an API key from the [OpenAI Platform](https://platform.openai.com/account/api-keys).
2.  **Create `.env.local`**: In the root directory of the project, create a file named `.env.local`.
3.  **Add Your API Key**: Open `.env.local` and add the following line, replacing `your_openai_api_key_here` with your actual key:

    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Usage

Once installed and configured, you can use `teach-me` in two primary modes:

### 1. Explain Code (Default Mode)

Pipe code directly into `teach-me` to receive a line-by-line explanation.

**Syntax:**

```bash
cat <your_code_file> | python -m teach_me --lang <language> [--focus <focus_mode>] [--focus <focus_mode>]
```

**Example (explaining a Python script with a security focus):**

```bash
cat src/teach_me/__main__.py | python -m teach_me --lang python --focus security
```

**Expected Output (example snippet):**

```markdown
# Explanation for src/teach_me/__main__.py

## Line 1: `import os`
This line imports the `os` module, which provides a way of using operating system dependent functionality like reading or writing to the file system, or interacting with environment variables.

## Line 2: `import sys`
The `sys` module provides access to system-specific parameters and functions, such as `sys.stdin` for reading piped input or `sys.exit` for exiting the program.
...
```

### 2. Interactive Tutoring Session

Start an interactive session to ask questions about a specific code file.

**Syntax:**

```bash
python -m teach_me interactive <file_path> --lang <language> [--persona <persona>] [--focus <focus_mode>]
```

**Example (interactive session on a Python file with a 'debugger' persona and performance focus):**

```bash
python -m teach_me interactive my_script.py --lang python --persona debugger --focus performance
```

**Available Personas:**

*   `professor` (default): Formal and detailed explanations with analogies and mini-lectures.
*   `peer`: Friendly, concise, focuses on practical understanding.
*   `debugger`: Extremely technical, explains logic step-by-step with precision.
*   `storyteller`: Teaches through metaphors, analogies, and vivid examples.
*   `comedian`: Makes you laugh while you learn; lightens up complex topics.
*   `minimalist`: Only answers exactly what’s asked.

**Available Focus Modes:**

*   `logic`: Explain the control flow and reasoning step by step.
*   `performance`: Highlight bottlenecks or inefficiencies.
*   `style`: Comment on readability, naming, and structure.
*   `security`: Point out potential vulnerabilities or unsafe patterns.
*   `best-practices`: Explain how the code aligns (or not) with conventions.

**Interactive Session Example:**

```
Starting interactive session for my_script.py with persona debugger.
Type 'exit' or 'quit' to end the session.
You: What does the `main` function do?
Tutor (debugger): The `main` function serves as the entry point for the CLI application. It initializes environment variables, parses command-line arguments using `argparse`, and then dispatches control to either `explain_code_from_stdin` or `interactive_session` based on the provided arguments. Specifically, it ensures the `OPENAI_API_KEY` is present before proceeding.
You: exit
Interactive session ended.
```

## API Information

`teach-me` relies on the **OpenAI API** for its core AI capabilities, specifically utilizing the `gpt-3.5-turbo` model for generating code explanations and interactive responses.

*   **Provider**: [OpenAI](https://openai.com/)
*   **API Documentation**: [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
*   **Model Used**: `gpt-3.5-turbo`

## Testing

A comprehensive test suite is provided to ensure the reliability and correctness of `teach-me`. Tests cover various functionalities, including API interactions (with mocking), argument parsing, and error handling.

To run the tests locally, first ensure you have installed the development dependencies (including `pytest`) as described in the [Installation](#installation) section. Then, execute the following command from the project root:

```bash
pytest test/test.py
```

## Technologies Used

*   **Python**: The primary programming language.
*   **OpenAI Python Client**: For interacting with the OpenAI API.
*   **Rich**: For beautiful terminal output, including markdown rendering and colored text.
*   **python-dotenv**: For loading environment variables from `.env` files.
*   **Pytest**: The testing framework used for the comprehensive test suite.
*   **Argparse**: Python's standard library for parsing command-line arguments.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.