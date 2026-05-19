# memo-parser 스킬

## 역할
슬랙 워크플로우 메시지 정규화 텍스트에서 인원요청 표준 필드를 추출해 `output/01_extracted.json`으로 저장한다.

## 트리거 조건
`output/00_raw_message.txt` 생성 직후, `output/01_extracted.json`이 없을 때.

## 처리 흐름

### 1단계: 수정 여부 감지
```
python .claude/skills/memo-parser/scripts/detect_amendment.py output/00_raw_message.txt
```
출력:
- `NEW` → 신규 케이스
- `AMENDMENT:<파일경로>` → 수정 케이스, 기존 파일 경로 반환
- `AMENDMENT:NOT_FOUND` → 수정 키워드 있으나 기존 파일 없음

### 2단계: LLM 필드 추출
`output/00_raw_message.txt` 내용을 읽어 `CLAUDE.md`의 JSON 스키마에 맞게 추출.

**추출 원칙**:
- `role` 필드: 원문 표기 그대로 보존 (임의 표준화 금지)
- 날짜 표기 정규화: "5월 21일" → "2026-05-21" (연도는 start_date 기준)
- `end` 시간: "익일 02:00" 형태 허용
- 메시지에 날짜별 상세 없으면 `schedule` 빈 배열, `additional_schedules`에 단서 기록
- `is_amendment`: detect_amendment.py 결과가 AMENDMENT면 true

**부가 일정 단서 탐색 대상**:
- `고객 요청사항`, `상담 특이사항` 필드
- "세팅", "사전교육", "리허설", "설치", "철수" 등 키워드

### 3단계: 스키마 검증
```
python .claude/skills/memo-parser/scripts/validate_schema.py
```
실패 시 오류 목록 확인 후 JSON 재작성 1회 재시도.

## 참고 자료
- `references/slack_workflow_message_spec.md`: 슬랙 메시지 파싱 규칙
