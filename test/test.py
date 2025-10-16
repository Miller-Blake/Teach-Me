import pytest
from unittest.mock import patch, MagicMock, ANY
import sys
import io
import os
import openai
from rich.markdown import Markdown
from src.teach_me.__main__ import explain_code_from_stdin, interactive_session, main, PERSONAS

# Mock the rich.console.Console for testing output
@pytest.fixture
def mock_console():
    with patch('rich.console.Console') as mock_console_class:
        mock_instance = mock_console_class.return_value
        mock_instance.print = MagicMock()
        mock_instance.input = MagicMock()
        yield mock_instance

# Test explain_code_from_stdin
def test_explain_code_from_stdin_success(mock_console, monkeypatch):
    monkeypatch.setattr(openai, "api_key", "dummy_key")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    with patch('openai.chat.completions.create') as mock_create:
        mock_create.return_value.choices[0].message.content = "Mocked explanation"
        
        # Simulate stdin input
        sys.stdin = io.StringIO("print('hello')")
        
        explain_code_from_stdin(mock_console, "python")
        
        mock_create.assert_called_once()
        assert isinstance(mock_console.print.call_args[0][0], Markdown) # Checks if Markdown was printed
        assert "Mocked explanation" in mock_console.print.call_args[0][0].markup

def test_explain_code_from_stdin_no_code(mock_console):
    # Simulate empty stdin
    sys.stdin = io.StringIO("")
    
    with pytest.raises(SystemExit) as excinfo:
        explain_code_from_stdin(mock_console, "python")
    
    assert excinfo.value.code == 1
    mock_console.print.assert_called_with("[bold red]Error:[/bold red] No code provided via stdin.")

def test_explain_code_from_stdin_api_error(mock_console, monkeypatch):
    monkeypatch.setattr(openai, "api_key", "dummy_key")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    with patch('openai.chat.completions.create', side_effect=Exception("API Error")) as mock_create:
        sys.stdin = io.StringIO("print('hello')")
        
        with pytest.raises(SystemExit) as excinfo:
            explain_code_from_stdin(mock_console, "python")
        
        assert excinfo.value.code == 1
        mock_console.print.assert_called_with("[bold red]An error occurred:[/bold red] API Error")

# Test interactive_session
def test_interactive_session_file_not_found(mock_console):
    with pytest.raises(SystemExit) as excinfo:
        interactive_session(mock_console, "non_existent_file.py", "python")
    
    assert excinfo.value.code == 1
    mock_console.print.assert_called_with("[bold red]Error:[/bold red] File not found: non_existent_file.py")

def test_interactive_session_success(mock_console, tmp_path, monkeypatch):
    monkeypatch.setattr(openai, "api_key", "dummy_key")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    # Create a dummy file
    dummy_file = tmp_path / "dummy_code.py"
    dummy_file.write_text("def func(): pass")

    mock_console.input.side_effect = ["What does func do?", "exit"]

    with patch('openai.chat.completions.create') as mock_create:
        mock_create.return_value.choices[0].message.content = "Mocked interactive explanation"
        
        interactive_session(mock_console, str(dummy_file), "python", "professor")
        
        mock_console.input.assert_any_call("[bold yellow]You:[/bold yellow] ")
        # Check if any of the print calls contain the mocked explanation in a Markdown object
        found_explanation = False
        for call_args in mock_console.print.call_args_list:
            if isinstance(call_args[0][0], Markdown) and "Mocked interactive explanation" in call_args[0][0].markup:
                found_explanation = True
                break
        assert found_explanation
        mock_create.assert_called_once()

def test_interactive_session_api_error(mock_console, tmp_path, monkeypatch):
    monkeypatch.setattr(openai, "api_key", "dummy_key")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    dummy_file = tmp_path / "dummy_code.py"
    dummy_file.write_text("def func(): pass")

    mock_console.input.side_effect = ["What does func do?", "exit"]

    with patch('openai.chat.completions.create', side_effect=Exception("Interactive API Error")):
        interactive_session(mock_console, str(dummy_file), "python", "professor")
        
        mock_console.print.assert_any_call("[bold red]An error occurred:[/bold red] Interactive API Error")

# Test main function
def test_main_no_api_key(mock_console):
    with patch('os.getenv', return_value=None), \
         patch('sys.exit') as mock_exit, \
         patch('builtins.print') as mock_print:
        
        main()
        
        mock_print.assert_called_with("Error: OPENAI_API_KEY or OPEN_AI_CHAT_KEY not found in environment variables or .env file.")
        mock_exit.assert_called_with(1)

def test_main_explain_code_mode(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['teach-me', '--lang', 'python'])
    with patch('os.getenv', return_value="dummy_key"), \
         patch('src.teach_me.__main__.explain_code_from_stdin') as mock_explain, \
         patch('src.teach_me.__main__.Console') as mock_console_class:

        mock_console_instance = mock_console_class.return_value
        main()

        mock_explain.assert_called_once_with(mock_console_instance, 'python', None)

def test_main_interactive_mode(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['teach-me', 'interactive', 'test_file.py', '--lang', 'python', '--persona', 'peer'])
    with patch('os.getenv', return_value="dummy_key"), \
         patch('src.teach_me.__main__.interactive_session') as mock_interactive, \
         patch('src.teach_me.__main__.Console') as mock_console_class:
        
        mock_console_instance = mock_console_class.return_value
        main()
        
        mock_interactive.assert_called_once_with(mock_console_instance, 'test_file.py', 'python', 'peer', None)

def test_main_load_dotenv_called():
    with patch('os.getenv', return_value="dummy_key"), \
         patch('src.teach_me.__main__.explain_code_from_stdin'), \
         patch('sys.argv', ['teach-me', '--lang', 'python']), \
         patch('src.teach_me.__main__.load_dotenv') as mock_load_dotenv:
        
        main()
        
        assert mock_load_dotenv.call_count >= 1 # Called at least once for default, potentially again for .env.local
