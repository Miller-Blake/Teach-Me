from rich.console import Console
from teach_me.__main__ import interactive_session

# Create a console object
console = Console()

# Start an interactive session
# Replace 'path/to/your/code.py' with the actual path to your code file
# and 'python' with the language of your code.
interactive_session(console, 'path/to/your/code.py', 'python')
