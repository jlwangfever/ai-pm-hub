#!/usr/bin/env python3
"""
PRD Word 文档解析脚本
读取 .docx 文件，提取结构化文本输出，供风格分析使用。
"""

import sys
import os

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    print("ERROR: python-docx not installed. Run: pip install python-docx", file=sys.stderr)
    sys.exit(1)


def parse_docx(file_path):
    """Parse a .docx file and output structured text."""
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    doc = Document(file_path)
    
    print(f"=== PRD 文档解析结果 ===")
    print(f"文件: {file_path}")
    print(f"段落数: {len(doc.paragraphs)}")
    print(f"表格数: {len(doc.tables)}")
    print()
    
    # Extract paragraphs with style info
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if not text:
            continue
        
        style_name = para.style.name if para.style else "Normal"
        
        # Identify heading level
        heading_level = None
        if style_name.startswith("Heading"):
            try:
                heading_level = int(style_name.replace("Heading", "").replace(" ", "").strip())
            except ValueError:
                heading_level = 0
        elif style_name == "Title":
            heading_level = 0
        
        if heading_level is not None:
            prefix = "#" * (heading_level + 1) if heading_level > 0 else "#"
            print(f"\n{prefix} {text}")
        elif style_name.startswith("List"):
            print(f"  - {text}")
        else:
            # Check alignment
            print(f"{text}")
    
    # Extract tables
    for t_idx, table in enumerate(doc.tables):
        print(f"\n[TABLE {t_idx + 1}] ({len(table.rows)} rows x {len(table.columns)} cols)")
        for r_idx, row in enumerate(table.rows):
            cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
            print(f"  | {' | '.join(cells)} |")
    
    print(f"\n=== 解析结束 ===")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_docx.py <path_to_docx_file>", file=sys.stderr)
        sys.exit(1)
    
    for file_path in sys.argv[1:]:
        parse_docx(file_path)
        print()
