"""Import requirements from CSV file into the database."""
import argparse
import asyncio
import csv
import sys
from pathlib import Path

# Add backend dir to path
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, async_session
from models import Requirement
from sqlalchemy import select


async def seed(csv_path: str):
    await init_db()

    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No data found in CSV.")
        return

    async with async_session() as db:
        count = 0
        for row in rows:
            req_id = row.get("id", "").strip()
            if not req_id:
                continue
            # Skip if already exists
            existing = await db.execute(select(Requirement).where(Requirement.id == req_id))
            if existing.scalar_one_or_none():
                print(f"  SKIP (exists): {req_id}")
                continue

            req = Requirement(
                id=req_id,
                category=row.get("category", "").strip(),
                level1=row.get("level1", "").strip(),
                derived_from=row.get("derived_from", "").strip() or None,
                spec_section=row.get("spec_section", "").strip() or None,
                spec_text=row.get("spec_text", "").strip(),
                spec_text_ko=row.get("spec_text_ko", "").strip() or None,
                keyword=row.get("keyword", "").strip() or None,
                controller_type=row.get("controller_type", "").strip() or None,
                mandatory=row.get("mandatory", "M").strip() or "M",
                support_status=row.get("support_status", "UNKNOWN").strip() or "UNKNOWN",
                support_note=row.get("support_note", "").strip() or None,
                fw_version=row.get("fw_version", "").strip() or None,
                status=row.get("status", "OPEN").strip() or "OPEN",
                priority=row.get("priority", "NORMAL").strip() or "NORMAL",
                assigned_to=row.get("assigned_to", "").strip() or None,
            )
            db.add(req)
            count += 1
            print(f"  ADD: {req_id}")

        await db.commit()
        print(f"\nImported {count} requirements.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed NVMe requirements from CSV")
    parser.add_argument("--input", required=True, help="Path to CSV file")
    args = parser.parse_args()
    asyncio.run(seed(args.input))
