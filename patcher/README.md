# 패처 빌드

이 폴더에는 게임 한글화 자료를 적용하는 별도 Windows EXE의 소스가 있습니다. 이미지·대사 관리 도구와 구분한 배포용 패처입니다.

필요 항목:

- Python 3.10 이상과 Tk
- PyInstaller
- Xdelta 3.2.1 Windows x86-64의 **`xdelta3.exe`** 전체 실행 파일

Windows에서 저장소 루트를 기준으로 빌드합니다.

```powershell
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name Ashita-no-Joe-Kr-Patcher-v1.1 --add-binary "C:\tools\xdelta3.exe;runtime" patcher\patcher.py
```

`xdelta3decode.exe` 경량 빌드는 배포 패치에서 사용하는 LZMA 보조 압축을 지원하지 않으므로 사용하지 않습니다.

생성된 EXE와 릴리스의 `.xdelta`, `patch-manifest.json`을 같은 폴더에 둡니다. 원본 ISO에 적용되는 차분 파일은 Git 저장소 대신 릴리스 ZIP에 있습니다.

자동 검증을 위한 명령행 사용:

```powershell
.\Ashita-no-Joe-Kr-Patcher-v1.1.exe --source "original.iso" --output "Ashita-no-Joe-Kr-v1.1.iso" --package "." --report "result.json"
```

소스로 실행할 때는 `--decoder "C:\tools\xdelta3.exe"`로 디코더를 지정할 수 있습니다. 원본·차분·출력의 해시가 모두 맞아야 성공합니다. 결과가 확정되기 전까지는 출력 폴더에 임시 파일을 만들며, 실패하면 이 임시 파일만 제거합니다.

파일 보존 검사:

```powershell
python -m unittest discover -s patcher -p "test_*.py" -v
```

전체 ISO 적용 검증의 결과는 [검증 문서](../docs/VALIDATION.md)에 기록합니다.
