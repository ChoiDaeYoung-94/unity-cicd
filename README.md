# Unity CI/CD

> Unity Android 빌드 자동화를 위한 GitHub Actions·에디터 스크립트·Python CLI와 설정 가이드입니다.

에디터 메뉴, 명령줄, 자체 빌드 PC에서 같은 빌드 스크립트를 활용하도록 구성한 템플릿입니다. 다른 게임 프로젝트에 파일을 복사하고 경로와 설정을 채워 사용합니다.

**현재 상태:** Android APK·AAB 빌드 코드가 있으며, iOS는 미구현입니다. App Center의 배포 기능은 2025년 3월 31일 종료되었습니다. 아래 App Center 연동은 기존 구현 기록이며, 현재 배포에 사용하려면 배포 단계를 교체해야 합니다. [Microsoft 안내](https://learn.microsoft.com/en-us/appcenter/retirement)

## 구성과 적용 위치

아래 경로는 모두 **게임 프로젝트 루트 기준 상대 경로**입니다.

| 저장소 파일·폴더 | 게임 프로젝트 내 위치 | 역할 |
| --- | --- | --- |
| [.github/workflows/cicd.yml](.github/workflows/cicd.yml) | `.github/workflows/cicd.yml` | GitHub Actions 템플릿 |
| [AssetDirectory/Editor](AssetDirectory/Editor) | `Assets/Editor` | Unity 빌드 스크립트 |
| [RootDirectory/BuildInfo](RootDirectory/BuildInfo) | `BuildInfo` | 빌드 버전 정보 |
| [RootDirectory/src](RootDirectory/src) | `src` | Python CLI와 키스토어 예시 |
| [RootDirectory/fastlane](RootDirectory/fastlane) | `fastlane` | 기존 App Center 배포 구성 |

`fastlane` 폴더 안의 `Gemfile`과 `Gemfile.lock`은 게임 프로젝트 루트에 배치합니다.

## 프로젝트 설정

1. 저장소를 복제합니다.

   ```bash
   git clone https://github.com/ChoiDaeYoung-94/unity-cicd.git
   ```

2. 위 표에 따라 파일을 게임 프로젝트로 옮깁니다.
3. [BuildScript.cs](AssetDirectory/Editor/BuildScript.cs)의 제품명, 앱 식별자, 키스토어·키 별칭 설정을 프로젝트에 맞게 구성합니다. `Keystore_ex.keystore`는 경로 설명용 예시 파일입니다.
4. `BuildInfo/buildinfo.txt`의 초기 버전을 설정합니다.
5. 프로젝트 루트에 `Build` 폴더를 준비합니다.
6. 자동 빌드를 사용할 경우 아래 빌드 PC와 GitHub Actions 설정을 적용합니다.

키스토어 비밀번호와 토큰 등 인증 정보는 공개 저장소에 기록하지 않고 별도로 관리합니다.

### 버전 정보

`buildinfo.txt`는 다음 세 값을 쉼표로 구분합니다.

```text
weekNumber,buildNumber,bundleVersionCode
```

| 값 | 의미 |
| --- | --- |
| `weekNumber` | `DAY_CALCULATEVERSION` 기준으로 계산한 주차 |
| `buildNumber` | 해당 주차의 빌드 번호 |
| `bundleVersionCode` | Android 버전 코드. AAB 빌드 시 증가 |

주차와 빌드 번호는 처음에 `0`으로 시작할 수 있습니다. 이미 배포한 앱은 Google Play Console에서 사용한 최신 버전 코드를 확인해 세 번째 값에 반영합니다.

## 빌드 방법

| 방식 | 실행 방법 | 출력 |
| --- | --- | --- |
| Unity 에디터 | `Build > AOS > APK` 또는 `Build > AOS > AAB` | 선택한 Android 형식 |
| Python CLI | `python src/build.py` | AAB와 APK |
| GitHub Actions | 아래 커밋 메시지 규칙 사용 | Android AAB |

Android 출력 경로는 게임 프로젝트 루트의 `Build/AOS`입니다. iOS 빌드는 아직 구현되지 않았습니다.

### Python CLI

Python과 Git을 준비한 뒤 필요한 패키지를 설치합니다.

```bash
pip install click GitPython paramiko scp
python src/build.py --help
python src/build.py
```

CLI는 저장소, 브랜치, Unity 실행 파일 경로와 빌드 PC의 프로젝트 저장 경로 등을 입력받습니다. 로컬 PC에서 실행할 때 IPv4 입력에는 **소문자 `skip`**을 사용합니다. 인수에 공백이 있으면 따옴표로 감쌉니다.

원격 빌드 결과를 로컬로 받을 경우에는 빌드 PC와 로컬 PC 사이의 SSH 연결 및 전송 경로를 준비해야 합니다. 빌드 PC는 자동화 적용 전부터 대상 Unity 프로젝트를 빌드할 수 있는 상태여야 합니다.

참고: [Python](https://www.python.org/downloads/) · [Click](https://click.palletsprojects.com/en/8.1.x/quickstart/) · [GitPython](https://gitpython.readthedocs.io/en/stable/intro.html) · [Paramiko](https://www.paramiko.org/installing.html) · [Windows OpenSSH](https://learn.microsoft.com/ko-kr/windows-server/administration/openssh/openssh_install_firstuse)

### GitHub Actions

1. 저장소에 [self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners)를 등록합니다.
2. 워크플로의 `runs-on` 라벨을 빌드 PC와 맞춥니다. 템플릿은 `self-hosted`, `buildpc`를 사용합니다.
3. `UNITY_APP_PATH`, `REPO_NAME`, `BUILD_PATH`, `AND_SETTING_PATH`를 입력합니다.
4. Unity 실행 명령의 `-projectPath`도 수정합니다. 템플릿에는 `Incremental` 경로가 직접 들어 있습니다.
5. 체크아웃에 사용할 `GIT_ACCESS_TOKEN`을 저장소 Actions Secrets에 설정합니다.
6. 배포 단계는 현재 사용할 서비스에 맞게 교체하고 작업 간 `needs`와 실행 조건도 점검합니다.

현재 템플릿은 `main` 브랜치 push 및 수동 실행 트리거를 선언하지만, 빌드 작업의 조건은 **push의 마지막 커밋 메시지**를 참조합니다. 수동 실행을 활용하려면 입력값과 조건을 별도로 조정해야 합니다.

| 마지막 커밋 메시지 | 설정된 동작 |
| --- | --- |
| `build_aos` 포함 | Android AAB 빌드 |
| `build_all` 포함 | Android 빌드와 iOS TODO 작업 |
| `build_ios` 포함 | iOS TODO 작업 |
| `ci skip` 포함 | Checkout 작업 건너뛰기 |

`ci skip`은 이 템플릿의 커스텀 조건입니다. 문서만 수정하는 커밋에는 `[skip ci]`를 사용하면 push 워크플로 자체를 건너뛸 수 있습니다.

## 기존 App Center 배포 구성

[Fastfile](RootDirectory/fastlane/Fastfile)은 `fastlane upload_aab`를 통해 AAB를 배포하도록 작성되어 있습니다.

| 설정 | 기존 용도 |
| --- | --- |
| `APP_CENTER_TOKEN` | App Center API 토큰 |
| `APPCENTER_OWNER_NAME` | 앱 소유자 |
| `APPCENTER_DISTRIBUTE_DESTINATIONS` | 배포 그룹 |
| `APPCENTER_DISTRIBUTE_NOTIFY_TESTERS` | 테스터 알림 여부 |

기존에는 `fastlane/.env`에서 배포 대상과 알림을 설정하고, 배포 그룹에 이메일로 알렸습니다. App Center 배포 종료로 이 단계는 현재 그대로 사용할 수 없습니다.

참고: [fastlane](https://docs.fastlane.tools/) · [fastlane-plugin-appcenter](https://github.com/microsoft/fastlane-plugin-appcenter)

## 참고 문서

- [Unity 특수 폴더](https://docs.unity3d.com/Manual/SpecialFolders.html)
- [Unity 명령줄 인수](https://docs.unity3d.com/kr/2021.3/Manual/EditorCommandLineArguments.html)
- [GitHub Actions](https://docs.github.com/actions)
