#!/usr/bin/env python3
"""
PRD PDF 文档解析脚本
读取 .pdf 文件，提取结构化文本（含表格），供风格分析使用。
支持文本型 PDF；扫描型 PDF（纯图片）会提示无文本层。
"""

import sys
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)


def parse_pdf(file_path):
    """Parse a PDF file and output structured text with table extraction."""

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(file_path)
    total_pages = len(doc)
    total_tables = 0

    print(f"=== PRD 文档解析结果 ===")
    print(f"文件: {file_path}")
    print(f"页数: {total_pages}")
    print()

    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text("text")

        if not text or not text.strip():
            # Check if page has images (scanned PDF)
            img_list = page.get_images()
            if img_list:
                print(f"--- 第 {page_num + 1} 页 (图片页，无文本层) ---")
                print(f"[此页包含 {len(img_list)} 张图片，可能为扫描页，建议 OCR 处理]")
                print()
            continue

        print(f"--- 第 {page_num + 1} 页 ---")
        print(text.strip())
        print()

        # Try to extract tables using pdfplumber-style approach
        # PyMuPDF has find_tables() in newer versions
        try:
            tables = page.find_tables()
            if tables and tables.tables:
                for t_idx, table in enumerate(tables.tables):
                    rows = table.extract()
                    if rows:
                        total_tables += 1
                        print(f"[TABLE {total_tables}] ({len(rows)} rows x {len(rows[0]) if rows[0] else 0} cols)")
                        for row in rows:
                            cells = [(cell or "").strip().replace("\n", " ") for cell in row]
                            print(f"  | {' | '.join(cells)} |")
                        print()
        except Exception:
            # find_tables not available or failed; tables already in text output
            pass

    # If no text was extracted at all, it's likely a scanned PDF
    all_text = "".join(page.get_text("text") for page in doc)
    if not all_text.strip():
        print("⚠️ 未提取到任何文本。此 PDF 可能是扫描件（纯图片），需要 OCR 处理。")
        print("   建议使用 OCR 工具（如 Tesseract、PaddleOCR）先转为文本，再进行分析。")

    print(f"=== 解析结束（共 {total_pages} 页，提取到 {total_tables} 张表格）===")
    doc.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_pdf.py <path_to_pdf_file> [<file2.pdf> ...]", file=sys.stderr)
        sys.exit(1)

    for file_path in sys.argv[1:]:
        parse_pdf(file_path)
        print()
