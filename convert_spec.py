"""NVMe 2.2 Spec PDF → Section-based Markdown files using pymupdf4llm."""
import pymupdf4llm
import pathlib

PDF_PATH = "NVM-Express-Base-Specification-Revision-2.2-2025.03.11-Ratified.pdf"
OUT_DIR = pathlib.Path("doc/spec")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Section definitions: (filename, start_page_1based, end_page_1based)
# Pages are 1-based inclusive, pymupdf4llm uses 0-based page_chunks
SECTIONS = [
    ("01_introduction",            23,   38),
    ("02_theory_of_operation",     39,   57),
    ("03_architecture",            58,  152),
    ("04_data_structures",        153,  188),
    ("05_admin_command_set",      189,  467),
    ("06_fabrics_command_set",    468,  477),
    ("07_io_commands",            478,  492),
    ("08_extended_capabilities",  493,  684),
    ("09_error_reporting",        685,  690),
    ("annex",                     691,  702),
]

for name, start, end in SECTIONS:
    out_path = OUT_DIR / f"nvme22_{name}.md"
    print(f"Converting {name} (p{start}-{end})...", end=" ", flush=True)
    try:
        md = pymupdf4llm.to_markdown(
            PDF_PATH,
            pages=list(range(start - 1, end)),  # 0-based
        )
        out_path.write_text(md, encoding="utf-8")
        size_mb = out_path.stat().st_size / 1024 / 1024
        print(f"OK ({size_mb:.1f} MB)")
    except Exception as e:
        print(f"ERROR: {e}")

print("\nDone! Files saved to:", OUT_DIR.resolve())
