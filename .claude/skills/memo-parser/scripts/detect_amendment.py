"""
Detects whether a message is an amendment (수정/변경) and finds the existing xlsx file.

Usage:
    python detect_amendment.py <message_file_path>

Output (stdout):
    NEW                          - no amendment keywords found
    AMENDMENT:<xlsx_path>        - amendment found, existing file renamed (_수정전)
    AMENDMENT:NOT_FOUND          - amendment keywords found but no existing xlsx
"""
import sys
import re
from pathlib import Path

OUTPUT_DIR = Path(__file__).parents[4] / "output"

AMENDMENT_KEYWORDS = re.compile(r"수정사항|수정|변경|변동사항|변동")


def find_existing_xlsx(client: str, event_name: str) -> Path | None:
    pattern = f"{client}_{event_name}"
    for f in sorted(OUTPUT_DIR.glob("*.xlsx")):
        if "_수정전" in f.stem:
            continue
        if pattern in f.stem:
            return f
    return None


def rename_sheet_to_amended(xlsx_path: Path) -> None:
    try:
        from openpyxl import load_workbook
    except ImportError:
        return

    wb = load_workbook(xlsx_path)
    for ws in wb.worksheets:
        if "_수정전" not in ws.title:
            new_title = (ws.title + "_수정전")[:31]  # Excel 31자 제한
            ws.title = new_title
    wb.save(xlsx_path)


def extract_client_event(message_text: str) -> tuple[str, str]:
    """Extract client and event name from message for file lookup."""
    client = ""
    event = ""

    for line in message_text.splitlines():
        line = line.strip()
        if "거래처명:" in line:
            parts = line.split("|")
            for p in parts:
                if "거래처명:" in p:
                    client = p.split(":", 1)[1].strip()
        if "행사명:" in line:
            parts = line.split("|")
            for p in parts:
                if "행사명:" in p:
                    event = p.split(":", 1)[1].strip()
        if client and event:
            break

    # Sanitize for filesystem
    client = re.sub(r'[\\/*?:"<>|]', "_", client)
    event = re.sub(r'[\\/*?:"<>|]', "_", event)
    return client, event


def main():
    if len(sys.argv) < 2:
        print("사용법: python detect_amendment.py <message_file>")
        sys.exit(1)

    msg_path = Path(sys.argv[1])
    if not msg_path.exists():
        print(f"오류: 파일을 찾을 수 없습니다: {msg_path}")
        sys.exit(1)

    text = msg_path.read_text(encoding="utf-8")

    # Check first 5 lines and full text for amendment keywords
    first_lines = "\n".join(text.splitlines()[:5])
    is_amendment = bool(AMENDMENT_KEYWORDS.search(first_lines)) or bool(
        AMENDMENT_KEYWORDS.search(text)
    )

    if not is_amendment:
        print("NEW")
        return

    # Extract client/event for file lookup
    client, event = extract_client_event(text)

    if not client or not event:
        print("AMENDMENT:NOT_FOUND")
        return

    existing = find_existing_xlsx(client, event)
    if existing:
        rename_sheet_to_amended(existing)
        print(f"AMENDMENT:{existing}")
    else:
        print("AMENDMENT:NOT_FOUND")


if __name__ == "__main__":
    main()
