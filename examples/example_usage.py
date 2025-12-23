#!/usr/bin/env python3
"""
Example usage of the EML Parser MCP tools
This shows how to use the tools programmatically (outside of MCP context)
"""

from eml_parser_mcp import parse_eml, extract_eml_attachments
from pathlib import Path

def test_parser(eml_file: str):
    """Test the EML parser with a sample file."""
    
    print("=" * 60)
    print(f"Testing EML Parser with: {eml_file}")
    print("=" * 60)
    
    # Step 1: Preview the email
    print("\n[1] Parsing email metadata...")
    result = parse_eml(eml_file)
    
    print(f"\nSubject: {result['metadata']['subject']}")
    print(f"From: {result['metadata']['from']}")
    print(f"To: {result['metadata']['to']}")
    print(f"Date: {result['metadata']['date']}")
    print(f"\nType: {result['metadata']['type']}")
    
    # Show content preview
    if result['content']['text']:
        text_preview = result['content']['text'][:200]
        print(f"\nText Preview: {text_preview}...")
    
    # Show attachments without downloading
    print(f"\n📎 Attachments: {result['summary']['total_attachments']}")
    for att in result['attachments']:
        print(f"  - {att['filename']} ({att['size_human']}) [{att['content_type']}]")
    
    print(f"\n🖼️  Inline Images: {result['summary']['total_inline_images']}")
    for img in result['inline_images']:
        print(f"  - {img['filename']} ({img['size_human']})")
    
    # Step 2: Extract if there are attachments
    if result['summary']['total_attachments'] > 0 or result['summary']['total_inline_images'] > 0:
        print("\n[2] Extracting attachments...")
        
        extract_result = extract_eml_attachments(
            eml_file,
            output_dir="test_extracted",
            organize=True,
            create_zip=True
        )
        
        print(f"\nExtracted to: {extract_result['output_directory']}")
        print(f"Files extracted: {extract_result['summary']['total_files']}")
        print(f"Total size: {extract_result['summary']['total_size_human']}")
        
        print("\nBreakdown:")
        print(f"  Small files: {extract_result['summary']['small_files']}")
        print(f"  Documents: {extract_result['summary']['documents']}")
        print(f"  Images: {extract_result['summary']['images']}")
        print(f"  Other: {extract_result['summary']['other_attachments']}")
        
        if extract_result['zip_file']:
            print(f"\n📦 ZIP created: {extract_result['zip_file']}")
        
        print("\nExtracted files:")
        for file in extract_result['files_extracted']:
            print(f"  [{file['category']}] {file['path']} ({file['size_human']})")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <path_to_eml_file>")
        print("\nExample: python example_usage.py sample.eml")
        sys.exit(1)
    
    eml_file = sys.argv[1]
    
    if not Path(eml_file).exists():
        print(f"Error: File not found: {eml_file}")
        sys.exit(1)
    
    test_parser(eml_file)
