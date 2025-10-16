# 🧠 teach-me — Context & Roadmap

## Overview
`teach-me` is a creative CLI tool that turns your terminal into a **code tutor**.  
It explains code line by line, answers questions about how it works, and even adapts its teaching style to match your learning vibe.

Or enter interactive tutoring mode:

teach-me interactive script.py

You can pipe code directly:
```bash
cat script.py | teach-me --lang python
```
## 🏗️ Core Features (v1.0 MVP)

✅ Explain Code (Base Command)

```bash
cat script.py | teach-me --lang python
```

Reads code from stdin, sends it to the OpenAI API, and prints a line-by-line explanation.

✅ Language Flag Support
--lang js, --lang go, --lang java — gives the AI the right context.

✅ Formatted Terminal Output
Uses rich for colorized headers, syntax highlighting, and better readability.

✅ Configurable API Key
Uses environment variable OPENAI_API_KEY or a local .env file.

## 💬 teach-me interactive (v1.5)

A conversational mode where you can talk to your AI tutor about code.

Example:
```bash
teach-me interactive script.py --focus security
```

Or with a persona and focus:
```bash
teach-me interactive script.py --persona debugger --focus performance
```

Then:
```bash
You: What does the main() function do?
Tutor: The main() function initializes the config and starts the app loop.
You: Why did the author use recursion here?
Tutor: It’s likely to simplify the tree traversal. Here's a non-recursive alternative…
``` 
### 🎭 Teaching Personas (v2.0)

Every developer learns differently — some prefer deep theory, others want humor or brevity.
The Teaching Personas system lets you choose how your tutor behaves and speaks.

Example:
```bash
teach-me interactive script.py --persona professor
```
# Available Personas (Planned)
Persona	Description	Tone
🎓 Professor    Formal and detailed explanations with analogies and mini-lectures.
Academic, patient
🧑‍💻 Peer	        Friendly, concise, focuses on practical understanding.  
Casual, relatable
🤖 Debugger	     Extremely technical, explains logic step-by-step with precision. 
Analytical
🪶 Storyteller	 Teaches through metaphors, analogies, and vivid examples.          
Creative
😄 Comedian	     Makes you laugh while you learn; lightens up complex topics.       
Humorous
⚡ Minimalist	Only answers exactly what’s asked.	                      
Concise, efficient

## --focus (v2.1)

Purpose: control what aspect of the code the tutor emphasizes.
For example:
```bash
teach-me --lang python --persona professor --focus performance
```

Focus modes:

Mode	        Description
logic	        Explain the control flow and reasoning step by step
performance	    Highlight bottlenecks or inefficiencies
style	        Comment on readability, naming, and structure
security	    Point out potential vulnerabilities or unsafe patterns
best-practices	Explain how the code aligns (or not) with conventions

🔧 Implementation idea:
Send the focus as part of the system prompt:

“Focus your explanation primarily on code performance and efficiency.”
