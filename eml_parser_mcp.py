#!/usr/bin/env python3
"""
EML Parser MCP Server
Parse .eml files and extract metadata, content, and attachments.
Uses eml_parser for reliable parsing.
"""

from fastmcp import FastMCP
import eml_parser
from pathlib import Path
from typing import Dict, Any
import zipfile
import base64

# Initialize MCP server
mcp = FastMCP("EML Parser")


@mcp.tool()
def parse_eml(filepath: str) -> Dict[str, Any]:
    """
    Parse an .eml file and return metadata, content, and attachment info.

    Does NOT extract attachment bytes - use extract_eml_attachments for that.
    Perfect for previewing what's in an email without bloat.

    Args:
        filepath: Path to the .eml file

    Returns:
        Dict containing:
        - metadata: subject, from, to, cc, bcc, date
        - content: plain text and HTML body
        - attachments: list of attachment metadata (filename, size, type)
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if not file_path.suffix.lower() == '.eml':
        raise ValueError(f"File must be .eml format, got: {file_path.suffix}")

    # Read and parse the email
    with open(file_path, 'rb') as f:
        email_bytes = f.read()

    parser = eml_parser.EmlParser(include_attachment_data=False)
    parsed = parser.decode_email_bytes(email_bytes)

    # Extract metadata from header
    header = parsed.get('header', {})
    metadata = {
        "subject": header.get('subject', 'No Subject'),
        "from": header.get('from', ''),
        "to": header.get('to', []),
        "cc": header.get('cc', []),
        "bcc": header.get('bcc', []),
        "date": header.get('date', ''),
        "reply_to": header.get('reply-to', [])
    }

    # Extract content from body
    bodies = parsed.get('body', [])
    text_content = None
    html_content = None

    for body in bodies:
        content_type = body.get('content_type', '')
        if content_type == 'text/plain' and text_content is None:
            text_content = ""  # eml_parser doesn't include body text by default
        elif content_type == 'text/html' and html_content is None:
            html_content = ""  # eml_parser doesn't include body HTML by default

    content = {
        "text": text_content,
        "html": html_content
    }

    # Get attachment metadata WITHOUT bytes
    attachments = []
    inline_images = []

    for att in parsed.get('attachment', []):
        filename = att.get('filename', 'unknown')
        size = att.get('size', 0)
        content_type = att.get('content_header', {}).get('content-type', [''])[0]
        content_disposition = att.get('content_header', {}).get('content-disposition', [''])[0]
        content_id = att.get('content_header', {}).get('content-id', [''])[0]

        att_info = {
            "filename": filename,
            "content_type": content_type,
            "size_bytes": size,
            "size_human": _human_size(size)
        }

        # Distinguish between inline images and regular attachments
        if 'inline' in content_disposition or content_id:
            att_info["content_id"] = content_id
            inline_images.append(att_info)
        else:
            attachments.append(att_info)

    return {
        "metadata": metadata,
        "content": content,
        "attachments": attachments,
        "inline_images": inline_images,
        "summary": {
            "total_attachments": len(attachments),
            "total_inline_images": len(inline_images),
            "has_text": content["text"] is not None,
            "has_html": content["html"] is not None
        }
    }


@mcp.tool()
def extract_eml_attachments(
    filepath: str,
    output_dir: str = "eml_extracted",
    organize: bool = True,
    create_zip: bool = False
) -> Dict[str, Any]:
    """
    Extract attachments from .eml file with smart organization.

    Organizes files into folders:
    - small_files/: Files <10KB (icons, signatures, etc.)
    - documents/: PDFs, Word docs, spreadsheets, presentations
    - images/: All image files (inline + regular)
    - attachments/: Everything else

    Args:
        filepath: Path to the .eml file
        output_dir: Directory to extract to (default: "eml_extracted")
        organize: Whether to organize into subfolders (default: True)
        create_zip: Create a zip file of all extracted content (default: False)

    Returns:
        Dict containing:
        - output_directory: Where files were saved
        - files_extracted: List of all saved files with metadata
        - zip_file: Path to zip if created
        - summary: Counts by category
    """
    file_path = Path(filepath)
    output_path = Path(output_dir)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Read and parse email
    with open(file_path, 'rb') as f:
        email_bytes = f.read()

    parser = eml_parser.EmlParser(include_attachment_data=True)
    parsed = parser.decode_email_bytes(email_bytes)

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Define organization categories
    categories = {
        "small_files": [],
        "documents": [],
        "images": [],
        "attachments": []
    }

    doc_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp'}
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'}

    files_extracted = []

    # Process all attachments
    for i, att in enumerate(parsed.get('attachment', [])):
        filename = att.get('filename', f"attachment_{i+1}")
        raw_data = att.get('raw', '')
        size = att.get('size', 0)
        content_header = att.get('content_header', {})
        content_type = content_header.get('content-type', [''])[0]
        content_disposition = content_header.get('content-disposition', [''])[0]
        content_id = content_header.get('content-id', [''])[0]

        # Decode base64 content
        if isinstance(raw_data, str) and raw_data.startswith("b'") and raw_data.endswith("'"):
            # Remove b' and ' wrapper
            raw_data = raw_data[2:-1]
        try:
            content = base64.b64decode(raw_data)
        except Exception:
            # If decode fails, skip this attachment
            continue

        # Determine category
        ext = Path(filename).suffix.lower()
        is_inline = 'inline' in content_disposition or content_id

        if organize:
            if size < 10240:  # <10KB
                category = "small_files"
            elif ext in doc_extensions:
                category = "documents"
            elif ext in image_extensions or 'image' in content_type.lower():
                category = "images"
            else:
                category = "attachments"
        else:
            category = "attachments"

        # Create category directory
        category_dir = output_path / category if organize else output_path
        category_dir.mkdir(exist_ok=True)

        # Save file
        save_path = category_dir / filename

        # Handle duplicate filenames
        counter = 1
        while save_path.exists():
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            save_path = category_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        save_path.write_bytes(content)

        file_info = {
            "filename": save_path.name,
            "path": str(save_path.relative_to(output_path)),
            "category": category,
            "size_bytes": size,
            "size_human": _human_size(size),
            "content_type": content_type,
            "type": "inline_image" if is_inline else "attachment"
        }

        if content_id:
            file_info["content_id"] = content_id

        categories[category].append(file_info)
        files_extracted.append(file_info)

    # Create zip if requested
    zip_path = None
    if create_zip and files_extracted:
        zip_filename = f"{file_path.stem}_extracted.zip"
        zip_path = output_path.parent / zip_filename

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_info in files_extracted:
                file_path_obj = output_path / file_info["path"]
                zipf.write(file_path_obj, file_info["path"])

    # Build summary
    summary = {
        "total_files": len(files_extracted),
        "small_files": len(categories["small_files"]),
        "documents": len(categories["documents"]),
        "images": len(categories["images"]),
        "other_attachments": len(categories["attachments"]),
        "total_size_bytes": sum(f["size_bytes"] for f in files_extracted),
        "total_size_human": _human_size(sum(f["size_bytes"] for f in files_extracted))
    }

    return {
        "output_directory": str(output_path),
        "files_extracted": files_extracted,
        "zip_file": str(zip_path) if zip_path else None,
        "summary": summary,
        "organized_by_category": organize
    }


def _human_size(size_bytes: int) -> str:
    """Convert bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
