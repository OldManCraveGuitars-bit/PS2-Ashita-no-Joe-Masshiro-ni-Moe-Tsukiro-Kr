# 전체 챕터 개방 세이브 — v1.1

일본판 SLPM-65441과 이 한글 패치용입니다. 기존 챕터 선택의 **143개 항목을 개방**한 세이브입니다. 새 SELECT 메뉴의 **제1~14장 시작 지점 이동**과는 별개이며, SELECT 메뉴를 쓰는 데 이 세이브가 필수는 아닙니다.

카드에는 내일의 죠 세이브만 담았습니다. 개방 비트 외 원본 옵션·캐릭터 해금 정보·스토리 진행 슬롯을 유지합니다. 완주 기록이나 모든 캐릭터 개방을 새로 만든 파일은 아닙니다.

## 파일 선택

| 파일 | 용도 |
| --- | --- |
| `Ashita-no-Joe-All-Chapters.ps2` | 별도 PS2 메모리카드 이미지. PCSX2·AetherSX2·NetherSX2 등에서 카드로 연결하거나, 기존 카드 방식의 RetroArch에 적용합니다. |
| `Ashita-no-Joe-All-Chapters.psu` | mymc/mymc++ 등으로 본인의 기존 카드에 이 게임 세이브를 가져올 때 사용합니다. |
| `verification.json` | 개방 비트·체크값·카드 ECC·왕복 검사와 파일 해시 기록입니다. |

**게임과 에뮬레이터를 완전히 종료하고 기존 카드를 먼저 다른 곳에 백업하세요.** 카드 전체 교체는 그 카드에 있던 다른 게임 세이브에도 영향을 줍니다. PSU를 가져올 때에도 같은 `BISLPM-65441` 폴더가 있으면 내일의 죠 진행 데이터가 교체되므로 백업이 필요합니다.

## PCSX2 / AetherSX2 / NetherSX2

1. `.ps2` 파일을 기기로 복사합니다.
2. 해당 앱의 메모리카드 설정에서 별도 카드로 불러와 **슬롯 1**에 연결합니다. 앱 버전에 따라 가져오기/카드 선택 메뉴 이름은 다릅니다.
3. 게임을 새로 부팅하고 게임 안의 챕터 선택을 확인합니다.

기존 카드의 다른 게임 세이브도 계속 사용하려면, 카드 전체 교체 대신 백업한 카드에 `.psu`를 가져오는 방법을 사용하세요.

## RetroArch — LRPS2/PCSX2 기존 메모리카드 방식

1. **설정 → 디렉터리 → 시스템/BIOS**에서 실제 시스템 폴더를 확인합니다.
2. 그 아래 `pcsx2/memcards/`를 엽니다. 기존 카드 방식의 슬롯 1 파일은 `Mcd001.ps2`입니다.
3. RetroArch를 완전히 종료하고 기존 `Mcd001.ps2`를 백업합니다.
4. 제공한 `.ps2` 파일의 이름을 `Mcd001.ps2`로 바꿔 해당 위치에 복사합니다.
5. RetroArch와 게임을 새로 실행합니다.

이전에 연결했던 Android 게임기 설정의 예시는 다음과 같습니다.

```text
내부 저장소/RetroArch/system/pcsx2/memcards/Mcd001.ps2
/storage/emulated/0/RetroArch/system/pcsx2/memcards/Mcd001.ps2
```

사용 중인 코어가 다른 카드 폴더·파일 이름을 만들거나 게임별 메모리카드 옵션을 사용한다면 그 설정을 우선하세요. 모든 RetroArch PS2 코어가 같은 방식인 것은 아닙니다. [LRPS2 공식 경로 안내](https://docs.libretro.com/library/lrps2/#directories)

## 적용 후 확인

- 이전 중간 저장 상태(savestate)를 불러오면 예전 메모리와 코드가 돌아올 수 있습니다. 처음에는 자동 상태 불러오기를 끄고 새로 부팅하세요.
- 이 파일은 게임 내 메모리카드 세이브입니다. RetroArch의 상태 불러오기 메뉴에서 여는 파일이 아닙니다.
- 원본 게임의 개방 판정 코드 286회, 카드 전체 16,384페이지 ECC, PSU 가져오기/내보내기 왕복 검사를 통과했습니다. PC에서 카드 부팅 읽기를 확인했으며 실제 메뉴 전체 탐색·모든 기기에서의 동작까지 확인한 것은 아닙니다.

[v1.1 배포 페이지](https://github.com/OldManCraveGuitars-bit/PS2-Ashita-no-Joe-Masshiro-ni-Moe-Tsukiro-Kr/releases/tag/v1.1) · [검증 범위](https://github.com/OldManCraveGuitars-bit/PS2-Ashita-no-Joe-Masshiro-ni-Moe-Tsukiro-Kr/blob/v1.1/docs/VALIDATION.md)
