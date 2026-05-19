# 개발 환경 세팅 가이드 (Windows 11)

## 1. Python 설치

1. [https://www.python.org/downloads/](https://www.python.org/downloads/) 접속
2. **Python 3.12** 다운로드 (Windows installer 64-bit)
3. 설치 시 반드시 **"Add Python to PATH"** 체크 후 설치
4. 설치 완료 후 PowerShell에서 확인:
   ```powershell
   python --version
   # Python 3.12.x 출력되면 완료
   ```

## 2. 프로젝트 폴더로 이동

```powershell
cd "C:\Users\jopdp\OneDrive\바탕 화면\빅터자동화"
```

## 3. 가상환경 생성 및 활성화

```powershell
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
.\.venv\Scripts\Activate.ps1
```

> ⚠️ PowerShell 실행 정책 오류가 나면:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> 입력 후 `.\.venv\Scripts\Activate.ps1` 다시 실행.

활성화되면 터미널 앞에 `(.venv)` 표시가 생김.

## 4. 패키지 설치

```powershell
pip install -r requirements.txt
```

설치 내용:
- `openpyxl` — xlsx 파일 생성
- `python-dotenv` — 환경변수 관리
- `jsonschema` — JSON 스키마 검증

## 5. Claude Code 설치 확인

```powershell
claude --version
```

없으면 [Claude Code 설치 가이드](https://docs.anthropic.com/ko/docs/claude-code) 참조.

## 6. 에이전트 실행

```powershell
# 가상환경 활성화 상태에서
claude
```

슬랙 메시지를 붙여넣고 Enter 입력.

## 7. 재실행 시 주의

- `output/` 폴더에 이전 작업 파일이 있으면 이어서 시작됨
- 처음부터 다시 시작하려면 `output/` 내 파일 삭제 후 실행:
  ```powershell
  Remove-Item output\*.txt, output\*.json, output\*.xlsx
  ```

## 8. 가상환경 비활성화 (종료 시)

```powershell
deactivate
```
