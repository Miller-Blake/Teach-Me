import os
import sys
import argparse
import openai
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

PERSONAS = {
    "professor": "Formal and detailed explanations with analogies and mini-lectures.",
    "peer": "Friendly, concise, focuses on practical understanding.",
    "debugger": "Extremely technical, explains logic step-by-step with precision.",
    "storyteller": "Teaches through metaphors, analogies, and vivid examples.",
    "comedian": "Makes you laugh while you learn; lightens up complex topics. Isn't afraid to get raunchy",
    "minimalist": "Only answers exactly what’s asked."
}

FOCUS_MODES = {
    "logic": "Explain the control flow and reasoning step by step.",
    "performance": "Highlight bottlenecks or inefficiencies.",
    "style": "Comment on readability, naming, and structure.",
    "security": "Point out potential vulnerabilities or unsafe patterns.",
    "best-practices": "Explain how the code aligns (or not) with conventions."
}

def explain_code_from_stdin(console, lang, focus=None):
    """Explains code piped in from stdin.

    Args:
        console: The Rich Console object for printing.
        lang: The programming language of the code.
        focus: The aspect of the code to emphasize.
    """
    if sys.stdin.isatty():
        console.print("[bold yellow]Usage:[/bold yellow] Pipe code into the script, e.g., `cat script.py | teach-me --lang python`")
        sys.exit(0)

    code = sys.stdin.read()
    if not code:
        console.print("[bold red]Error:[/bold red] No code provided via stdin.")
        sys.exit(1)

    try:
        system_message = "You are a helpful code tutor."
        if focus and focus in FOCUS_MODES:
            system_message += f" Focus your explanation primarily on {FOCUS_MODES[focus].lower()}"

        prompt = f'''
        You are an expert code tutor. Explain the following {lang} code line by line.
        Provide clear, concise explanations for each part of the code.
        Format your output in markdown.

        Code:
        ```{lang}
        {code}
        ```
        '''

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )

        explanation = response.choices[0].message.content
        console.print(Markdown(explanation))

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")
        sys.exit(1)

def interactive_session(console, file_path, lang, persona="professor", focus=None):
    """Starts an interactive tutoring session for a given file.

    Args:
        console: The Rich Console object for printing.
        file_path: The path to the code file.
        lang: The programming language of the code.
        persona: The teaching persona to use.
        focus: The aspect of the code to emphasize.
    """
    try:
        with open(file_path, "r") as f:
            code = f.read()
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File not found: {file_path}")
        sys.exit(1)

    console.print(f"Starting interactive session for [bold green]{file_path}[/bold green] with persona [bold blue]{persona}[/bold blue].")
    console.print("Type 'exit' or 'quit' to end the session.")

    system_prompt = f"You are an expert code tutor. Your persona is: {PERSONAS[persona]}. A user is asking a question about the following code. Provide a clear and concise answer in your persona's style."

    while True:
        try:
            question = console.input("[bold yellow]You:[/bold yellow] ")
            if question.lower() in ["exit", "quit"]:
                break

            prompt = f'''
            Code ({lang}):
            ```{lang}
            {code}
            ```

            User's question: {question}
            '''

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            explanation = response.choices[0].message.content
            console.print(f"[bold green]Tutor ({persona}):[/bold green]")
            console.print(Markdown(explanation))

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")
            break
    
    console.print("\nInteractive session ended.")

def main():
    """Main function to run the CLI.
    
    Parses arguments and calls the appropriate function.
    """
    load_dotenv()
    if os.path.exists(".env.local"):
        load_dotenv(dotenv_path=".env.local")

    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_CHAT_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY or OPEN_AI_CHAT_KEY not found in environment variables or .env file.")
        sys.exit(1)
    
    openai.api_key = api_key

    parser = argparse.ArgumentParser(description="Teach-Me: A CLI code tutor.", prog="teach-me")
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        # Setup for interactive command
        parser.add_argument("command", choices=["interactive"])
        parser.add_argument("file", help="The path to the code file to discuss.")
        parser.add_argument("--lang", help="Language of the code.", default="text")
        parser.add_argument("--persona", help="The teaching persona to use.", choices=PERSONAS.keys(), default="professor")
        parser.add_argument("--focus", help="The aspect of the code to emphasize during the interactive session.", choices=FOCUS_MODES.keys(), default=None)
        args = parser.parse_args()
        
        console = Console()
        interactive_session(console, args.file, args.lang, args.persona, args.focus)
    else:
        # Setup for default stdin command
        parser.add_argument("--lang", help="Language of the code being explained.", default="text")
        parser.add_argument("--focus", help="The aspect of the code to emphasize.", choices=FOCUS_MODES.keys(), default=None)
        args = parser.parse_args()

        console = Console()
        explain_code_from_stdin(console, args.lang, args.focus)

if __name__ == "__main__":
    main()