# EML Parser MCP Server

 **WOAH, MATE!**
A basic MCP server for parsing`.eml` email files, Extracting the metadata, content, and attachments, **AND** it puts them into folders!?
***IT MUST BE CHRISTMAS!*** 

## You heard me right, folks.
It's a robot - that can read your electronic mail. The future is here and it is beautiful.

## Earth Shattering Features

- **Parse email metadata**  Is it an email from your aunt wishing you a happy holidays? Is it your monthly bank statement? *is it your renewal for the premium hub?*  - WHO CARES!?  That's robot work now. 
- **Extract attachments** with [smart organisation](https://c.tenor.com/6dO29HKTiNIAAAAd/tenor.gif): it takes your emails, it makes a folder, it puts the emais... ***IN THE FOLDER***. *simply incredible*
  - Small files (<10KB) → `small_files/`
  - Documents (PDFs, Office) → `documents/`
  - Images (inline + regular) → `images/`
  - Everything else → `attachments/`
  -*that is 4 whole new levels of organization you could only dream of!*
- **Efficient parsing** - uses `GOVCERT-LU/eml_parser` for reliable email parsing.... *this code is actually quite good so I can't even make a joke here* Thank you to the author for making such a great bit of open source software!

## Installation

We use [UV](https://docs.astral.sh/uv/) in this house. ***If you don't like it?*** You can find regular Python instructions below. *i'm not mad, i'm dissapointed*:

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

##  Plug it into Claude or your Local AI

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

It probably works with Docker and the rest too idk I just wanted it to read .emls without writing a conversion script every time.

This code is currently untested on Local AI! Future versions will be optimized for local AI if required, but the code does most of the heavy lifting for the bot - if your bot can call tools and read? This ***SHOULD*** work.

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
Your bot just fills out this small questionairre;

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
- Size summaries - Actually very useful if you don't want yout bot pulling a 200,000 token attachment directly into context.

### AND MORE - APPARENTLY
*see this is where Claude got lazy and didn't even add any detail about the file handling instructions but hey this is just a tool duct taped to a stick if I'm honest.This project wll be polished a bit - but will be intergrated into something bigger soon!*

## Example Workflow
*you need to tell it how you want it to use the tool, some assembly required.

1. **Preview email**: Uses `parse_eml` to take a whiff of whats inside!
2. **Decide**:  Decides if it likes the smell or not.
3. **Extract**: Use `extract_eml_attachments` to pour our the .eml into its sandbox and organize them into neat lil boxes.
4. **Analyze**: The dingus can now summarise your email! ... *maybe*

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

*i mean yeah i guess* Just replace the uv commands with Pythton/venv/pip. 

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

***but how can you live with yourself?***

##Proudly Vibe Coded
This was AI generated!... well not this bit (though how can you really know? Y'know?) But all python language elements of this were AI Generated under instruction and supervision (*Claude likes to overwrite without looking*)
With most of the code already existing and Claud's new "Skills" feaure it took almost no effort! The only issues during vibe coding this tiny MCP:
1. First wrote the entire thing with filessystem one file at a time instead of using my custom sandbox (*coming soon, hide your dingus-bots*) that was literally designed for making stuff like this... 
2. Installed the entirely wrong MCP dependancy *almost making it incompatible with its actual purpose*
3. Kept trying install features the Claude sandvox would not permit,
4. Repeatedly reversed the load order causing the initial install to fail - *between trying to delete all my other MCP links*...
5. Literally forgot what a file structure was and spent a few minutes in a loop wondering what `/mnt/` meant.
6. Then failed to call the tool it literally just built.
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
     
             This MCP server primairily utilizes the following dependencies:
     - [eml_parser](https://github.com/GOVCERT-LU/eml_parser) - **GNU GPL License** - Core email parsing engine
     - [FastMCP](https://github.com/jlowin/fastmcp) - **Apache 2.0 License** - MCP server framework
     
Architecture and smart organization logic designed with Claude (Anthropic).
     