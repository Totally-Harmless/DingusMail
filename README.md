# DingusMail - Smart Email Handling for Dumb AI
### 🤖💌📬 *Your email is in ***GREAT*** hands!* 😃👍

 **WOAH, MATE!**
A basic MCP server for parsing`.eml` email files, Extracting the metadata, content, and attachments, **AND** it puts them into folders!?
***IT MUST BE CHRISTMAS!*** 🎄

## You heard me right, folks.
It's a tool for your robot - that can read and handle your electronic mail. The future is here and it is beautiful. 🥺

*tl;dr:*

`this tool connects to local ai and allow the ai to read and extract from raw .eml files both on and offline, this means tracking emails can be summarized with ai, all content extracted, and the sender left on 'delivered' like your messages to your ex`

## Earth Shattering Features

- **Parse email metadata**  Is it an email from your aunt wishing you a happy holidays? Is it your monthly bank statement? *is it your renewal for the premium hub?*  - WHO CARES!?  That's robot work now. 
- **Extract attachments** with [smart organisation](https://c.tenor.com/6dO29HKTiNIAAAAd/tenor.gif): it takes your emails, it makes a folder, it puts the emails... ***IN THE FOLDER***. *simply incredible*
  - Small files (<10KB) → `small_files/`
  - Documents (PDFs, Office) → `documents/`
  - Images (inline + regular) → `images/`
  - Everything else → `attachments/`
  -*that is 4 whole new levels of organization you could only dream of!*
- **Efficient parsing** - uses `GOVCERT-LU/eml_parser` for reliable email parsing.... *this code is actually quite good so I can't even make a joke here* Thank you to the author for making such a great bit of open source software!

## Installation

We use [UV](https://docs.astral.sh/uv/) in this house. ***If you don't like it?*** You can find regular Python instructions below. *i'm not mad, i'm disappointed*:

```bash
# Install UV (one-liner for Unix/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Clone or download this repository, then install dependencies:

```bash
# Navigate to the project directory
cd eml_parser_mcp

# Create virtual environment and install dependencies
uv venv
uv pip install -e .
```

## How to make it work!*
*...no refunds*

### Run the MCP Server

```bash
uv run eml_parser_mcp.py
```

##  Plug it into Claude or your Local AI 🔌

Add to your `claude_desktop_config.json` (or equivalent like your `mcp.json` file in LM Studio):

```json
{
  "mcpServers": {
    "eml-parser": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/eml_parser_mcp/",
        "run",
        "eml_parser_mcp.py"
      ]
    }
  }
}
```

### For LM studio 🔨
This code is currently untested on Local AI! Future versions will be optimized for local AI if required, but the code does most of the heavy lifting for the bot - if your bot can call tools and read? This ***SHOULD*** work.


I will be using this with my local AI when my new PC is running but ***if you want to be the first to try:***


[![Add MCP Server eml-parser to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)](https://lmstudio.ai/install-mcp?name=eml-parser&config=eyJjb21tYW5kIjoidXYiLCJhcmdzIjpbIi0tZGlyZWN0b3J5IiwiL2Fic29sdXRlL3BhdGgvdG8vZW1sX3BhcnNlcl9tY3AvIiwicnVuIiwiZW1sX3BhcnNlcl9tY3AucHkiXX0%3D)


This should add the connector to your `mcp.json` file in LM studio!

**NOTE:** ***you will need to set the install directory manually***


*It probably works with Docker and the rest too idk I just wanted Claude to read .emls without writing a conversion script every time*

---

### The Tool Calls

### Tool 1: `parse_eml`

Get metadata and attachment info WITHOUT downloading files:

```python
{
    "filepath": "path/to/email.eml"
}
```

Returns:
- Full metadata (subject, from, to, cc, dates)
- Message content (text/HTML)
- Attachment metadata (filename, size, type)
- Inline image metadata
- Summary counts

### Tool 2: `extract_eml_attachments`

Takes files, puts them into folders, *like its PEOPLE!*
Your bot just fills out this small questionnaire;

```python
{
    "filepath": "path/to/email.eml",
    "output_dir": "extracted_files",  # optional
    "organize": true,                 # optional, smart organization
    "create_zip": false              # optional, zip everything
}
```

And it gets:
- List of all extracted files with paths
- Category breakdown
- ZIP file path *you can ask it to zip it all up! Wish it was my idea!*
- Size summaries - Actually very useful if you don't want your bot pulling a 200,000 token attachment directly into context.

### *"But wait you said it can zip and sort email..."*

***Ah, There's the thing!*** **IT CAN!** Let me tell you about **Tool-bloat** and how your code can achieve more with less!

<!-- CLAUDE_GENERATED_SUGGESTION_START -->

Instead of having separate tools for every tiny action (one for sorting, one for zipping, one for filtering by size, one for...), this MCP uses TWO well-designed tools that can be combined in your instructions:

- `parse_eml` → Preview before you commit
- `extract_eml_attachments` → Extract, organize, AND zip

**The secret?** The `organize` and `create_zip` parameters! Your AI can decide:
- "Just dump everything" → `organize: false, create_zip: false`
- "Sort it properly" → `organize: true, create_zip: false`  
- "Sort AND zip for easy sharing" → `organize: true, create_zip: true`

This means you get 6+ potential workflows from 2 tools instead of needing 6 separate tool calls. Less tool-bloat, more flexibility, cleaner code.

**Translation:** Good foundational tools + smart parameters > 20 hyper-specific tools that do one thing each.

<!-- CLAUDE_GENERATED_SUGGESTION_END -->

## Example Workflow

<!-- CLAUDE_GENERATED_SUGGESTION_START -->

**The MCP doesn't assume how you want to work—you tell it:**

```plaintext
"Hey Claude, there's a suspicious email at suspicious.eml. 
Can you preview it first, tell me if it looks legit, 
then extract any attachments to a folder called 'dodgy_stuff' 
but DON'T open any executables."
```

1. **Preview email**: Uses `parse_eml` to check sender, subject, attachment types
2. **Decide**: AI evaluates if it looks safe based on metadata
3. **Extract**: Uses `extract_eml_attachments` to sort files into categories
4. **Analyze**: AI can now safely examine non-executable files and summarize

*Some assembly required—but that's the beauty of it. YOUR workflow, not ours.*

<!-- CLAUDE_GENERATED_SUGGESTION_END -->

## TELL ME ABOUT THE ENDLESS POSSIBILITIES

- **AI Email Filtering without tracking**: Emails have trackers! .eml can be downloaded without activating them and summarized offline. Imagine instead of signing for a parcel, you kidnap the postman. That's basically it.
- **Smart organization**: *CAN MAKE FOLDERS!* **CAN PUT THINGS FROM THE EMAILS IN THE FOLDERS!** - ***REVOLUTIONARY!***
- **Efficient**: If your email contains Malware? Your bot can spot it, ignore it, and download it anyway!
- **Clean code**: Simple instructions, for the humble email bot.

## Dependencies
###  duct taped together for your inconvenience

- `fastmcp>=2.0.0` - It's like a custom MCP server - but someone else made it and let you use it!
- `eml_parser>=1.17.0` - This is an "*email parser with full RFC compliance*. So if you were worried about RFC compliance? ***We got you covered!***
                                                                                                                                                                                                                                                                                                                                                                                      *....what the hell is RFC ?*

Just run `uv pip install -e .` sit back, and then sit back up again because uv is VERY quick.

## Can I Use Regular Python instead of uv?

*i mean yeah i guess* Just replace the uv commands with Python/venv/pip. 

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

***but how can you live with yourself?***


## Proudly Vibe Coded 🛌🤖💻

This was AI generated!... well not this bit (though how can you really know? Y'know?) But all python language elements of this were AI Generated under instruction and supervision (*Claude likes to overwrite files without looking*)

### Here were the prompts:

`claude make email mcp`

`make better`

`no make better`

`make github`

`make better`

`commit`

*Okay, jokes aside...* 

Vibe coding is amazing for translating code to English! But at the end of the day if you let an AI run wild with no direction, it will;
- `Create spaghetti code at best`
- `Remove useful code constantly at worst`

This was a case of me having a simple problem, I could have made this MCP with a single prompt and have been done with it, but because I listened to what actual programmers advice, I continued to refine it. The initial version used an entirely different email parsing dependency called `eml-extractor`, which wasn't working in my use case at all, so I searched the hub and that got replaced with `eml_parser`. Eventually 4 tool calls became 2, and it all happened though *"augmented AI use"*. 

[Anthropic is looking heavily into Augmentation vs Automation, you can read more here!](https://www.anthropic.com/research/anthropic-economic-index-september-2025-report)

But in short;
- `Augmentation is a back and forth collaboration`
- `Automation is a 'set it and forget it' system`

**Here's what they don't tell you:** ***both are totally valid methods of creating code***

You will only get out what you put in, I have spent entire **DAYS** *augmenting* a prompt with one model, to then *automate* a second AI to code it autonomously.

So yeah, vibe coding is easy! I mean the *only* problems I've had
The only issues during vibe coding this tiny MCP:
1. First wrote the entire thing with filesystem one file at a time instead of using my custom sandbox (*coming soon, hide your dingus-bots*) that was literally designed for making stuff like this... 
2. Installed the entirely wrong MCP dependency *almost making it incompatible with its actual purpose*
3. Suggested the wrong dependencies from the onset leading to a total restructure midway.
4. Kept trying install features the Claude sandbox would not permit.
5. Repeatedly reversed the load order causing the initial install to fail - *between trying to delete all my other MCP links*...
6. Literally forgot what a file structure was and spent a few minutes in a loop wondering what `/mnt/` meant.
7. Then failed to call the tool it literally just built.

*See?* ***IT'S EASY!***

## License
 This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU Affero General Public License as
        published by the Free Software Foundation, either version 3 of the
        License, or (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU Affero General Public License for more details.

        You should have received a copy of the GNU Affero General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.

###     Addendum
     
             This MCP server primarily utilizes the following dependencies:
     - [eml_parser](https://github.com/GOVCERT-LU/eml_parser) - **GNU GPL License** - Core email parsing engine
     - [FastMCP](https://github.com/jlowin/fastmcp) - **Apache 2.0 License** - MCP server framework
     
Architecture and smart organization logic designed with Claude (Anthropic).
     