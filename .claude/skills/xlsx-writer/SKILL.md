# xlsx-writer 스킬

## 역할
`output/01_extracted.json`을 읽어 운영 시트 `.xlsx` 파일을 생성한다.

## 트리거 조건
[5] 출력 채널 결정 후 (v1: 항상 실행).

## 실행

```
python .claude/skills/xlsx-writer/scripts/create_xlsx.py
```

**입력**: `output/01_extracted.json`
**출력**: `output/{거래처명}_{행사명}.xlsx`

## 시트 구조

```
행1: 날짜 헤더 (N일)
행2: 요일 헤더 (월/화/수...)
행3+: 인력 행 (역할그룹 | 역할명 | 이름(빈) | 날짜별 근무시간 | 연락처(빈))
```

- 비용/단가 열 없음 (재경팀 별도 관리)
- 이름·연락처 셀: 빈 상태로 생성 (섭외팀 후처리)
- 수정 케이스(`is_amendment: true`): 기존 xlsx 탐색 → 탭명에 `_수정전` 추가 → 신규 파일 생성

## 참고
- `references/sheet_layout_spec.md`: 시트 레이아웃 상세
