<!-- Claude is Work to Build this Project -->
---
sidebar_position: 8
title: "Real Project Setup and Troubleshooting"
chapter: 7
lesson: 8
duration_minutes: 50

skills:
  - name: "Project Setup and Scaffolding"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Information"
    measurable_at_this_level: "Learner can set up project structure with AI guidance; create folders and files; install dependencies"

  - name: "Error Interpretation and Troubleshooting"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Analyze"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Learner encounters real errors; asks AI for clarification; understands error messages; follows debugging steps"

  - name: "Integrated Bash Workflow"
    proficiency_level: "A2→B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Learner integrates navigation, safety pattern, file ops, configuration, packages, pipelines in realistic workflow"

  - name: "Resilience and Problem-Solving Mindset"
    proficiency_level: "B1"
    category: "Soft"
    bloom_level: "Understand"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Learner recognizes errors as learning opportunities; develops confidence debugging with AI"

cognitive_load:
  new_concepts: 7
  assessment: "7 new concepts (project structure, error messages, troubleshooting, debugging, logs, testing, deployment) within B1 transition limit ✓"
---

# Real Project Setup and Troubleshooting—The Capstone

## This Lesson Brings Everything Together

You've learned individual bash concepts:
- How to navigate (paths, directories)
- How to operate on files safely (5-step pattern)
- How to configure projects (environment variables)
- How to install packages (dependencies)
- How to build complex operations (pipes)

This capstone lesson shows you **bash orchestration**—directing your AI to execute complete multi-step workflows through bash commands. You'll supervise project setup, error handling, and troubleshooting, all through bash collaboration.

**This is where learning transforms into capability.** You're not learning Python or any specific language—you're learning to **orchestrate bash workflows** that set up projects, handle configuration, manage dependencies, and debug errors. The Python code in this lesson is secondary; **the bash commands are what you're supervising**.

---

## What is Bash Orchestration?

**Orchestration** means directing multiple bash commands to work together as a coordinated workflow. Instead of running one command at a time, you supervise your AI as it executes:

- **10+ bash commands** to create a complete project structure
- **Sequential operations** (create folder → enter folder → create files → configure secrets)
- **Error handling** (when commands fail, understand why and fix it)
- **Validation steps** (verify each part works before moving to the next)

**In this lesson**, you'll watch a full project setup orchestrated through bash. The project happens to be Python-based, but **the skills you're learning are bash supervision skills**—applicable to any project in any language.

**Key insight**: Professional developers don't manually type 50 bash commands. They direct AI to orchestrate the entire workflow, supervise execution, and validate results. That's what you're learning here.

---

## The Real Workflow: Setup → Error → Debug → Succeed

In professional work, this is the pattern:

**Step 1: Set up project** (orchestrate structure creation, install dependencies through bash)
**Step 2: Encounter an error** (something doesn't work—read bash error messages)
**Step 3: Interpret the error** (understand what bash/system is telling you)
**Step 4: Troubleshoot with AI** (ask questions, AI adjusts bash commands)
**Step 5: Verify success** (bash commands confirm the fix worked)
**Step 6: Document the solution** (remember what bash pattern solved it)

This lesson guides you through all 6 steps using bash orchestration.

---

## Set Up a Real Project Structure

Let's watch a realistic conversation where you and your AI set up a Python project from scratch.

**You**: "I want to create a new Python project to fetch weather data and save it to a file. Can you help me set it up?"

**Agent**: "Absolutely. I'll create the project structure step by step. Let me start with the directories and files we'll need."

**Step 1: Create project structure**

```
$ mkdir weather-project
$ cd weather-project
$ mkdir src tests data
$ ls -la
drwxr-xr-x   4 user  staff    128 Nov  2 10:00 src
drwxr-xr-x   3 user  staff     96 Nov  2 10:00 tests
drwxr-xr-x   3 user  staff     96 Nov  2 10:00 data
```

**Agent**: "I've created the project folder with subdirectories:
- `src/` for source code
- `tests/` for test files
- `data/` for output data files"

**Step 2: Create initial files**

```
$ cat > src/main.py << 'EOF'
import requests
import json
import os

api_key = os.getenv('WEATHER_API_KEY')
if not api_key:
    raise ValueError("WEATHER_API_KEY environment variable not set")

response = requests.get(
    f'https://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}'
)
data = response.json()
print(json.dumps(data, indent=2))
EOF

$ cat > README.md << 'EOF'
# Weather Project

Fetches current weather data and saves to file.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set API key: `export WEATHER_API_KEY="your-key-here"`
3. Run: `python src/main.py`
EOF

#### 💬 AI Colearning Prompt
> "When setting up a Python project, why create both `requirements.txt` AND a `.env` file? What problem does each one solve?"

$ cat > .env << 'EOF'
WEATHER_API_KEY=test-key-12345
EOF

$ cat > .gitignore << 'EOF'
.env
__pycache__/
*.pyc
EOF
```

**Agent**: "I've created the main project files. Now let's install dependencies."

**Step 3: Install dependencies**

```
$ cat > requirements.txt << 'EOF'
requests==2.31.0
python-dotenv==1.0.0
EOF

$ pip install -r requirements.txt
Collecting requests==2.31.0
...
Successfully installed requests-2.31.0 python-dotenv-1.0.0
```

**Agent**: "Dependencies installed. The project is ready to test. But first, let me check we have everything..."

**Step 4: Verify setup**

```
$ ls -la
total 48
-rw-r--r--   1 user  staff   1500 Nov  2 10:00 README.md
-rw-r--r--   1 user  staff     150 Nov  2 10:00 .env
-rw-r--r--   1 user  staff      60 Nov  2 10:00 .gitignore
-rw-r--r--   1 user  staff     300 Nov  2 10:00 requirements.txt
drwxr-xr-x   3 user  staff     96 Nov  2 10:00 src
drwxr-xr-x   3 user  staff     96 Nov  2 10:00 tests
drwxr-xr-x   3 user  staff     96 Nov  2 10:00 data

$ pip list | grep -E "requests|dotenv"
python-dotenv   1.0.0
requests        2.31.0
```

**Agent**: "Setup complete. The project structure is ready, dependencies are installed, and configuration is set."

---

## Encounter and Interpret Real Errors

Now let's test the project and encounter a realistic error.

**You**: "Let's run the script and see if it works."

**Agent**: "Running the main script..."

```
$ python src/main.py
Traceback (most recent call last):
  File "/Users/mjs/weather-project/src/main.py", line 8, in <module>
    response = requests.get(
  File "/Users/mjs/weather-project/src/main.py", line 9, in <module>
    f'https://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}'
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.openweathermap.org', port=443):
Max retries exceeded with url: /api.openweathermap.org/data/2.5/weather?q=London&appid=test-key-12345
(Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x...>'))
```

**You**: "Oh no! There's an error. What does this mean?"

**Agent**: "Let me break down the error:

1. **Error type**: `requests.exceptions.ConnectionError`
2. **What it means**: The code tried to connect to the weather API but failed
3. **Why it failed**: Either no internet connection, or the URL is wrong, or the API server is down

Looking at the error, the API key in the URL shows `test-key-12345`, which is our test value. The real issue is: we're using a test API key that the service doesn't recognize, so the request fails. This is expected because we haven't set up a real API key yet."

**You**: "So the error is expected? The code is working?"

**Agent**: "The error is expected because we used a test key. The code structure is correct. To make it work with a real API, you'd:
1. Get a real API key from openweathermap.org
2. Set it: `export WEATHER_API_KEY='your-real-key'`
3. Run the script again

Let me modify the code to handle this more gracefully."

---

## Debug and Fix Errors with AI Guidance

Let's fix the code to handle errors better.

**You**: "How would you make the error message clearer?"

**Agent**: "I'll modify the code to catch the connection error and provide helpful feedback:"

```
$ cat > src/main.py << 'EOF'
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')

if not api_key:
    print("ERROR: WEATHER_API_KEY environment variable not set")
    print("Set it with: export WEATHER_API_KEY='your-key-here'")
    exit(1)

try:
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}',
        timeout=5
    )
    if response.status_code == 401:
        print("ERROR: Invalid API key. Check your WEATHER_API_KEY.")
        print(f"Response: {response.json()}")
    elif response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"ERROR: API returned status {response.status_code}")

except requests.exceptions.Timeout:
    print("ERROR: Request timed out. Check your internet connection.")
except requests.exceptions.ConnectionError:
    print("ERROR: Cannot connect to API server. Check internet connection or API status.")
except Exception as e:
    print(f"ERROR: Unexpected error: {e}")
EOF

$ python src/main.py
ERROR: Invalid API key. Check your WEATHER_API_KEY.
Response: {'cod': '401', 'message': 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.'}
```

**Agent**: "Much better! Now the error message is clear: the API key is invalid. When you get a real key and set it, the script will work."

**You**: "So you added error handling so the user knows what went wrong instead of seeing a cryptic traceback?"

**Agent**: "Exactly. Error handling makes debugging easier. Users (and you, when troubleshooting) get clear messages about what's wrong and how to fix it."

#### 🎓 Expert Insight
> In AI-native development, troubleshooting isn't about memorizing error codes—it's about pattern recognition. When you see "ModuleNotFoundError", you don't need to remember pip syntax. You understand the PATTERN (missing dependency), tell AI "install this package", and verify it's resolved. Errors become conversations, not obstacles.

---

## Integrate All Concepts in a Real Workflow

Now let's add complexity that integrates everything you've learned.

**You**: "I want the script to save weather data to a file, with different output locations for development vs. production. How do I set that up?"

**Agent**: "I'll modify .env and the code to support both environments. This integrates configuration, file operations, and error handling."

**First, update .env**:

```
$ cat > .env << 'EOF'
WEATHER_API_KEY=test-key-12345
ENVIRONMENT=development
OUTPUT_FILE=data/weather.json
EOF
```

**Then update the code**:

```
$ cat > src/main.py << 'EOF'
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')
environment = os.getenv('ENVIRONMENT', 'development')
output_file = os.getenv('OUTPUT_FILE', 'data/weather.json')

if not api_key:
    print("ERROR: WEATHER_API_KEY not set")
    exit(1)

try:
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}',
        timeout=5
    )

    if response.status_code == 200:
        data = response.json()

        # Save to file
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Weather data saved to {output_file}")
        print(f"✓ Environment: {environment}")
    else:
        print(f"ERROR: API returned {response.status_code}")

except requests.exceptions.ConnectionError:
    print("ERROR: Cannot connect to API")
except IOError as e:
    print(f"ERROR: Cannot write to {output_file}: {e}")
EOF

$ python src/main.py
✓ Weather data saved to data/weather.json
✓ Environment: development
```

**Agent**: "The script now:
1. Reads configuration from .env (configuration lesson)
2. Validates input and handles errors (troubleshooting)
3. Saves output safely to the correct file (file operations with error handling)
4. Works differently based on environment settings (applied configuration)"

---

## Understanding Error Messages

Real errors fall into categories. Here's how to interpret them:

| Error Type | Example | What It Means | First Step |
|------------|---------|---------------|-----------|
| **Import Error** | `ModuleNotFoundError: No module named 'requests'` | Package not installed | `pip install requests` |
| **Syntax Error** | `SyntaxError: invalid syntax` | Typo in code | Check the code on that line |
| **File Error** | `FileNotFoundError: [Errno 2] No such file` | File/folder doesn't exist | Check the path |
| **Connection Error** | `ConnectionError: Max retries exceeded` | Can't reach external service | Check internet, URL, credentials |
| **Permission Error** | `PermissionError: [Errno 13] Permission denied` | No permission to read/write | Check file permissions, sudo |

**Your job**: Read the error type and message, then ask your AI "What does this mean?" before trying random fixes.

---

## Lesson in Practice: A Complete Session

Let's watch a realistic troubleshooting conversation:

**You**: "I'm trying to run my Python script but it's not working. The error says something about a module."

**Agent**: "Show me the error message."

**You**: (Copies error)
```
ModuleNotFoundError: No module named 'requests'
```

**Agent**: "The module `requests` isn't installed. Let me check what's in requirements.txt and install it."

```
$ cat requirements.txt
requests==2.31.0
python-dotenv==1.0.0

$ pip install -r requirements.txt
```

**Agent**: "Installed. Now let's test the script again."

**You**: (Runs script, gets different error)
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/weather.json'
```

**Agent**: "The script is trying to write to `data/weather.json` but the `data` folder doesn't exist. Let me create it:"

```
$ mkdir -p data
$ python src/main.py
ERROR: Invalid API key...
```

**Agent**: "Good! Now we're getting the expected API key error (because we used a test key). The infrastructure is working. You'd set a real API key to complete setup."

**You**: "So we went from 'module missing' → 'folder missing' → 'API key missing'. Each error was real?"

**Agent**: "Yes. Each revealed a real setup issue. The workflow is:
1. Hit error
2. Read error message
3. Ask 'What does this mean?'
4. Fix one issue
5. Run again, hit next issue
6. Repeat until success

This is completely normal. Troubleshooting is an essential skill."

---

## The Mindset: Errors Are Learning

**Important**: In professional development, encountering errors is not failure. It's progress.

- **No error** → Your code never ran (missing setup)
- **Error** → Your code ran, hit a problem, produced a useful message
- **Debugging error** → You understand what's wrong and how to fix it

Each error message is your AI telling you what to fix next.

#### 🤝 Practice Exercise

> **Ask your AI**: "Set up a Python project with: directory structure (src/, tests/), requirements.txt with requests, .env for an API key, .gitignore to protect secrets, and a main.py that reads the API key from environment. Then verify everything is configured correctly."

**Expected Outcome**: You understand complete project setup workflow integrating navigation, file operations, configuration, secrets management, and verification.

---

## The Bash Commands You Just Supervised

In this lesson, you watched bash orchestrate a complete project. Here are the key bash commands that made it happen:

**Project Structure** (bash file operations):
```bash
mkdir -p weather-project/{src,tests,data}  # Brace expansion creates 3 folders at once
cd weather-project                           # Navigate into project
```

**File Creation** (bash heredocs):
```bash
cat > src/main.py << 'EOF'                  # Create file with content
[Python code here]
EOF
```

**Configuration** (bash environment):
```bash
cat > .env << 'EOF'                          # Create secrets file
WEATHER_API_KEY=test-key-12345
EOF

export $(cat .env | xargs)                   # Load environment variables
```

**Security** (bash gitignore):
```bash
cat > .gitignore << 'EOF'                    # Protect secrets from git
.env
__pycache__/
*.pyc
EOF
```

**Validation** (bash checks):
```bash
ls -la                                       # Verify structure created
python3 -m py_compile src/main.py           # Verify syntax valid
echo $WEATHER_API_KEY                        # Verify environment loaded
```

**What you learned**: How to supervise AI orchestrating **15+ bash commands** to create a complete project. The Python code was just the payload—**the bash workflow was what you supervised**.

---

## Try With AI: Real Project Setup and Troubleshooting

Now that you understand the complete project setup workflow, let's apply it with your AI.

### Full Project Setup Prompt

Open your AI tool and ask:

**Prompt:**
```
Help me set up a complete Python project.
Project: A simple weather data fetcher.

Walk me through:
1. Project structure (folders and files)
2. Code to implement the functionality
3. Dependencies to install
4. How to run it

After setup, I'll run it and see what errors appear.
I want to understand the full workflow: setup → run → error → debug → success.
```

**What to Expect**:
- Your AI creates the project structure
- Shows dependencies and installs them
- You run the project and encounter real errors
- Your AI explains each error and guides you through fixing it
- By the end, you have a working project

**Key Insight**: This is the real developer workflow. Errors are normal. The skill is understanding and fixing them with AI guidance.

---

## Try With AI: Troubleshooting Real Errors

When your project encounters errors, ask your AI:

**Prompt:**
```
I got this error: [paste the error message]

Walk me through:
1. What does this error mean in plain language?
2. What caused it?
3. How do I fix it?
4. After I fix it, what should I try next?
```

**Expected Response**:
Your AI will explain the error, show you the fix, and help you understand why the error occurred. This builds your debugging confidence.

**Key Principle**: Every error is a learning opportunity. Your AI is your guide through the troubleshooting process.

---

## Try With AI: Orchestration at Scale (Advanced)

Now that you've mastered single project setup, try orchestrating bash workflows at scale:

**Prompt 1: Parallel Project Setup**
```
Create 3 project directories simultaneously: project-1, project-2, project-3.

In each directory:
1. Create src/ and tests/ folders
2. Create a README.md with the project name
3. Create a .env file template
4. Create a .gitignore protecting .env
5. List each directory's structure to verify

What bash commands would you use to do this efficiently?
```

**What to Expect**: Your AI uses bash loops, brace expansion, or command chaining to create all 3 projects with a few commands instead of repeating 20+ commands manually.

**Prompt 2: Batch File Operations**
```
I have 5 Python files in a directory.

Orchestrate this workflow:
1. Check if each file has valid syntax
2. Count lines of code in each file
3. Create a summary report showing file names and line counts
4. Save the report to project-summary.txt

What bash pipeline would accomplish this?
```

**What to Expect**: Your AI uses bash tools (`find`, `xargs`, pipes, redirects) to process multiple files automatically in one workflow.

**Key Insight**: Professional developers orchestrate repetitive tasks through bash. Instead of "set up 10 projects manually," you direct AI to create a bash workflow once and execute it 10 times. **This is the power of bash orchestration—and you now have the supervision skills to make it work safely.**

---

You can now supervise sophisticated bash workflows. Your AI is the expert in commands and syntax. **You're the expert in understanding, verifying, and catching mistakes.**

This is the foundation of productive collaboration with AI tools.

---


