# requirement-formatter 스킬

## 역할
`output/01_extracted.json`을 읽어 표준 인원요청서 텍스트(`output/02_requirement.txt`)를 생성한다.

## 트리거 조건
[2] 검증 통과 직후. `output/01_extracted.json` 존재, `output/02_requirement.txt` 없을 때.

## 처리 방법

`references/output_format_template.md`의 양식을 참고해 JSON 데이터를 텍스트로 변환.

**생성 원칙**:
- 모든 필드는 JSON 값 그대로 사용 (임의 수정 금지)
- 빈 값/미정 필드는 `-` 또는 `미정`으로 표기
- 날짜별 스케줄 표는 인력구분 × 날짜 행렬 구조
- 부가 일정(세팅 등)이 있으면 별도 섹션으로 포함
- 수정 케이스(`is_amendment: true`)면 상단에 `[수정본]` 표시

## 자기검증
생성 후 JSON의 핵심 값이 모두 텍스트에 반영됐는지 확인:
- 거래처명, 행사명, 날짜 범위, 모든 인력구분, 인원수, 근무시간

## 참고
- `references/output_format_template.md`: 양식 템플릿
