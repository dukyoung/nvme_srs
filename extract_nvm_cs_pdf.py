"""NVM Command Set Spec 1.2 PDF → Section-based Markdown files using pymupdf4llm."""
import pymupdf4llm
import pathlib

PDF_PATH = "NVM-Express-NVM-Command-Set-Specification-Revision-1.2-2025.08.01-Ratified.pdf"
OUT_DIR = pathlib.Path("doc/spec")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Section definitions: (filename, start_page_1based, end_page_1based)
# Total 158 pages. TOC:
#   Ch1 Introduction: p8-11
#   Ch2 NVM Command Set Model: p12-23
#   Ch3 I/O Commands: p24-63
#   Ch4 Admin Commands: p64-115
#   Ch5 Extended Capabilities: p116-158
SECTIONS = [
    ("01_introduction",          8,   11),
    ("02_command_set_model",    12,   23),
    ("03_io_commands",          24,   63),
    ("04_admin_commands",       64,  115),
    ("05_extended_capabilities",116, 158),
]

for name, start, end in SECTIONS:
    out_path = OUT_DIR / f"nvm_cs12_{name}.md"
    print(f"Converting {name} (p{start}-{end})...", end=" ", flush=True)
    try:
        md = pymupdf4llm.to_markdown(
            PDF_PATH,
            pages=list(range(start - 1, end)),  # 0-based
        )
        out_path.write_text(md, encoding="utf-8")
        size_kb = out_path.stat().st_size / 1024
        print(f"OK ({size_kb:.1f} KB)")
    except Exception as e:
        print(f"ERROR: {e}")

print("\nDone! Files saved to:", OUT_DIR.resolve())
