"""
Validates output/01_extracted.json against the staffing request schema.
Exit code 0 = valid, 1 = invalid (prints errors to stdout).
"""
import json
import sys
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parents[4] / "output"
JSON_PATH = OUTPUT_DIR / "01_extracted.json"

REQUIRED_TOP = ["client", "event_name", "start_date", "end_date", "venue", "is_amendment", "schedule"]
TIME_PATTERN_RE = r"^(\d{2}:\d{2}|익일 \d{2}:\d{2})$"


def validate(data: dict) -> list[str]:
    errors = []

    # Required top-level keys
    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"필수 필드 누락: '{key}'")

    # Date format
    for field in ("start_date", "end_date"):
        val = data.get(field, "")
        try:
            datetime.strptime(val, "%Y-%m-%d")
        except (ValueError, TypeError):
            errors.append(f"날짜 형식 오류 ({field}): '{val}' — YYYY-MM-DD 형식이어야 합니다")

    # end_date >= start_date
    start = data.get("start_date", "")
    end = data.get("end_date", "")
    if start and end:
        try:
            if datetime.strptime(end, "%Y-%m-%d") < datetime.strptime(start, "%Y-%m-%d"):
                errors.append(f"종료일({end})이 시작일({start})보다 앞섭니다")
        except ValueError:
            pass

    # schedule validation
    schedule = data.get("schedule", [])
    if not isinstance(schedule, list):
        errors.append("'schedule' 필드는 배열이어야 합니다")
    else:
        for i, item in enumerate(schedule):
            prefix = f"schedule[{i}]"

            if "date" not in item:
                errors.append(f"{prefix}: 'date' 필드 누락")
            else:
                try:
                    datetime.strptime(item["date"], "%Y-%m-%d")
                except ValueError:
                    errors.append(f"{prefix}: 날짜 형식 오류 '{item['date']}'")

            staff_list = item.get("staff", [])
            if not isinstance(staff_list, list):
                errors.append(f"{prefix}: 'staff' 필드는 배열이어야 합니다")
                continue

            for j, staff in enumerate(staff_list):
                sp = f"{prefix}.staff[{j}]"
                for field in ("role", "count", "start", "end"):
                    if field not in staff:
                        errors.append(f"{sp}: '{field}' 필드 누락")

                count = staff.get("count")
                if count is not None and (not isinstance(count, int) or count <= 0):
                    errors.append(f"{sp}: 'count'는 양의 정수여야 합니다 (현재값: {count})")

    return errors


def main():
    if not JSON_PATH.exists():
        print(f"오류: {JSON_PATH} 파일이 없습니다.")
        sys.exit(1)

    try:
        with open(JSON_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        sys.exit(1)

    errors = validate(data)
    if errors:
        print(f"검증 실패 ({len(errors)}개 오류):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("검증 통과")
        sys.exit(0)


if __name__ == "__main__":
    main()
