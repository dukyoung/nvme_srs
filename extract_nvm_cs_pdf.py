"""Extract NVM Command Set Specification PDF to markdown files, split by chapter."""
import fitz
import re
import os

PDF_PATH = "NVM-Express-NVM-Command-Set-Specification-Revision-1.2-2025.08.01-Ratified.pdf"
OUT_DIR = "doc/spec"

doc = fitz.open(PDF_PATH)
toc = doc.get_toc()

# Build chapter boundaries from TOC (level-1 entries)
chapters = []
for level, title, page in toc:
    if level == 1:
        chapters.append((title, page))

# Add end sentinel
chapters.append(("END", doc.page_count + 1))

# Map chapter number to output filename
CHAPTER_FILES = {
    "1": "nvm_cs12_01_introduction.md",
    "2": "nvm_cs12_02_command_set_model.md",
    "3": "nvm_cs12_03_io_commands.md",
    "4": "nvm_cs12_04_admin_commands.md",
    "5": "nvm_cs12_05_extended_capabilities.md",
}

os.makedirs(OUT_DIR, exist_ok=True)


def extract_page_text(page):
    """Extract text from a page, preserving structure."""
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
    lines = []
    for block in blocks:
        if block["type"] != 0:  # skip images
            continue
        for line in block["lines"]:
            spans = line["spans"]
            if not spans:
                continue
            text = "".join(s["text"] for s in spans)
            # Detect headings by font size
            max_size = max(s["size"] for s in spans)
            is_bold = any("Bold" in (s.get("font", "") or "") or "bold" in (s.get("font", "") or "").lower() for s in spans)
            lines.append({
                "text": text,
                "size": max_size,
                "bold": is_bold,
                "y": line["bbox"][1],
            })
    return lines


def detect_table_rows(page):
    """Detect table structures using line detection."""
    tables = page.find_tables()
    result = []
    if tables and tables.tables:
        for table in tables.tables:
            md_rows = []
            data = table.extract()
            if not data:
                continue
            for ri, row in enumerate(data):
                cells = []
                for cell in row:
                    c = (cell or "").replace("\n", "<br>")
                    c = c.replace("|", "\\|")
                    cells.append(c)
                md_rows.append("|" + "|".join(cells) + "|")
                if ri == 0:
                    md_rows.append("|" + "|".join(["---"] * len(cells)) + "|")
            result.append("\n".join(md_rows))
    return result


def lines_to_markdown(lines):
    """Convert extracted lines to markdown text."""
    md_parts = []
    prev_y = None
    for ln in lines:
        text = ln["text"].strip()
        if not text:
            continue
        # Skip page headers/footers
        if re.match(r"^NVM Express.*Specification", text):
            continue
        if re.match(r"^\d+$", text) and ln["size"] < 10:
            continue

        # Heading detection
        if ln["size"] >= 14 and ln["bold"]:
            md_parts.append(f"\n\n**{text}**\n")
        elif ln["size"] >= 12 and ln["bold"]:
            md_parts.append(f"\n\n**{text}**\n")
        elif ln["bold"] and len(text) < 120 and re.match(r"^[\d.]+ ", text):
            md_parts.append(f"\n\n**{text}**\n")
        elif ln["bold"] and len(text) < 100:
            md_parts.append(f"\n**{text}**\n")
        else:
            # Add paragraph break if large Y gap
            if prev_y is not None and (ln["y"] - prev_y) > 20:
                md_parts.append("\n")
            md_parts.append(text + "\n")
        prev_y = ln["y"]
    return "".join(md_parts)


for i in range(len(chapters) - 1):
    title, start_page = chapters[i]
    _, end_page = chapters[i + 1]

    # Get chapter number
    ch_match = re.match(r"^(\d+)", title)
    if not ch_match:
        continue
    ch_num = ch_match.group(1)
    if ch_num not in CHAPTER_FILES:
        continue

    filename = CHAPTER_FILES[ch_num]
    filepath = os.path.join(OUT_DIR, filename)

    print(f"Extracting Chapter {ch_num}: {title} (pages {start_page}-{end_page-1})...")

    chapter_md = f"NVM Express NVM Command Set Specification, Revision 1.2\n\n\n"

    for pg_num in range(start_page - 1, min(end_page - 1, doc.page_count)):
        page = doc[pg_num]

        # Extract tables
        tables_md = detect_table_rows(page)

        # Extract text
        lines = extract_page_text(page)
        text_md = lines_to_markdown(lines)

        # If tables found, append them after the text
        if tables_md:
            # Try to integrate tables into the text flow
            chapter_md += text_md + "\n"
            for tbl in tables_md:
                chapter_md += "\n" + tbl + "\n\n"
        else:
            chapter_md += text_md

    # Clean up excessive newlines
    chapter_md = re.sub(r"\n{4,}", "\n\n\n", chapter_md)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(chapter_md)

    file_size = os.path.getsize(filepath)
    print(f"  -> {filepath} ({file_size:,} bytes)")

doc.close()
print("\nDone! All chapters extracted.")
