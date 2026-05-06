# MiniMax MCP for Claude Desktop — Windows

Use **MiniMax M2.7** (one of the best coding AI models) inside Claude Desktop on Windows — automatically. Just ask Claude to write code and it silently routes the request to MiniMax behind the scenes.

- **Coding tasks** (write, debug, review, test) → MiniMax M2.7 via SambaNova Cloud
- **Planning / design / architecture** → Claude Opus/Sonnet

No switching apps. No copying prompts. It just works.

**Cost comparison:**

| Model | Input $/M tokens | Output $/M tokens |
|---|---|---|
| MiniMax M2.7 (SambaNova) | $0.30 | $1.20 |
| Claude Sonnet 4.6 | $3.00 | $15.00 |
| Claude Opus 4.7 | $5.00 | $25.00 |

MiniMax is ~20x cheaper than Opus for coding tasks.

---

## What you need before starting

- Windows 10 or 11
- [Claude Desktop for Windows](https://claude.ai/download) installed
- Python 3.8 or above — check by opening Command Prompt and running:
  ```
  python --version
  ```
  If not installed, download from [python.org](https://python.org/downloads) — during install, **check the box "Add Python to PATH"**
- Git installed — download from [git-scm.com](https://git-scm.com/download/win)
- A free SambaNova API key — sign up at [cloud.sambanova.ai](https://cloud.sambanova.ai), go to **API Keys**, and create one

---

## Step 1 — Open Command Prompt

Press `Windows + R`, type `cmd`, hit Enter.

---

## Step 2 — Clone this repo

```cmd
git clone https://github.com/nitinkore-sn/minimax-mcp-windows.git
```

Move into the folder:

```cmd
cd minimax-mcp-windows
```

---

## Step 3 — Install dependencies

```cmd
pip install "mcp[cli]" httpx
```

---

## Step 4 — Find the full path to the repo

Run this and copy the output — you'll need it in the next step:

```cmd
cd
```

It'll print something like `C:\Users\yourname\minimax-mcp-windows`. Copy that.

---

## Step 5 — Configure Claude Desktop

The Claude Desktop config file lives here:

```
C:\Users\yourname\AppData\Roaming\Claude\claude_desktop_config.json
```

Quickest way to open it — paste this into Command Prompt:

```cmd
notepad "%APPDATA%\Claude\claude_desktop_config.json"
```

> If the file doesn't exist yet, Notepad will ask to create it — click **Yes**.

Paste this into the file (replace the placeholders):

```json
{
  "mcpServers": {
    "minimax": {
      "command": "python",
      "args": [
        "C:\\Users\\yourname\\minimax-mcp-windows\\server.py"
      ],
      "env": {
        "MINIMAX_API_KEY": "paste-your-sambanova-key-here",
        "MINIMAX_BASE_URL": "https://api.sambanova.ai/v1",
        "MINIMAX_MODEL": "MiniMax-M2.7"
      }
    }
  }
}
```

> **Important:**
> - Replace `C:\\Users\\yourname\\minimax-mcp-windows\\server.py` with the path from Step 4. Use **double backslashes** `\\` in the path.
> - Replace `paste-your-sambanova-key-here` with your actual SambaNova API key.

Save the file (`Ctrl + S`).

---

## Step 6 — Add routing instructions to Claude Desktop

This tells Claude when to use MiniMax vs handle things itself.

**How to open Custom Instructions:**
1. Open Claude Desktop
2. Click your **profile icon** (bottom-left corner)
3. Click **Settings**
4. Click **Custom Instructions** in the left sidebar
5. Paste the text below and click **Save**

```
ROUTING RULES — follow strictly:

ALWAYS call a MiniMax tool for:
- Writing, generating, or scaffolding any code
- Debugging or fixing code errors
- Reviewing or refactoring code
- Explaining what code does
- Writing tests, scripts, SQL, regex, shell commands

NEVER call MiniMax for (handle directly):
- Planning, roadmaps, task breakdowns
- Architecture and design decisions
- Tradeoff analysis or comparisons
- Research, summaries, documentation
```

---

## Step 7 — Restart Claude Desktop

> **This step is required — skipping it means the MiniMax server won't load.**

1. Right-click the Claude icon in the **system tray** (bottom-right of taskbar)
2. Click **Quit**
3. Reopen Claude Desktop from the Start menu or desktop shortcut

---

## Step 8 — Verify it's working

In Claude Desktop, click the **hammer icon** (🔨) near the input box. You should see the MiniMax tools listed:

- `minimax_generate_code`
- `minimax_debug_code`
- `minimax_code_review`
- `minimax_explain_code`
- `minimax_write_tests`

Then test it — type:

```
Write a Python function that reverses a string
```

Claude will call the MiniMax tool and return the code.

---

## Troubleshooting

**"python is not recognized as an internal or external command"**
→ Python is not on your PATH. Reinstall from [python.org](https://python.org/downloads) and check **"Add Python to PATH"** during setup. Then restart Command Prompt.

**"ModuleNotFoundError: mcp"**
→ Run `pip install "mcp[cli]" httpx` again in Command Prompt

**MiniMax tools not showing in Claude Desktop**
→ Double-check the path in the config uses double backslashes `\\`
→ Make sure you fully quit Claude Desktop (Step 7) and reopened it

**API error / authentication failed**
→ Check your SambaNova API key has no extra spaces
→ Make sure you saved the config file before restarting

**"No such file or directory" error in Claude Desktop logs**
→ The path in the config doesn't match where you cloned the repo. Re-run `cd` in Command Prompt inside the folder to get the exact path.

---

## What each tool does

| Tool | When Claude uses it |
|---|---|
| `minimax_generate_code` | You ask it to write code |
| `minimax_debug_code` | You ask it to fix a bug |
| `minimax_code_review` | You ask it to review / refactor |
| `minimax_explain_code` | You ask it to explain code |
| `minimax_write_tests` | You ask it to write tests |

---

*Author: Nitin Kore — [github.com/nitinkore-sn](https://github.com/nitinkore-sn)*
