# About

unity CI/CD 관련 스크립트, 가이드 관리

## About directory files

1. AssetDirectory
   - 본 폴더의 내부 파일들은 게임프로젝트 Assets 폴더 내부에 위치한다.
     - Editor ([참고](https://docs.unity3d.com/Manual/SpecialFolders.html))
       - BuildScript
         - CLI, Github action으로 build 할 때 사용한다.
2. RootDirectory
   - 본 폴더의 내부 파일들은 게임프로젝트 root path에 위치한다.
     - BuildInfo
       - buildinfo
         - buildinfo는 0,0,0 의 형식을 가지며 버전 자동화를 위해 사용된다.
         - 각 숫자는 "weekNumber,buildNumber,bundleVersionCode" 를 의미한다.
         - weekNumber, buildNumber의 경우 BuildScript의 SetVersion 메서드의 내용으로 분석할 수 있으며 처음 기입 시 0으로 해도 무방하다.
         - weekNumber는 BuildScript의 DAY_CALCULATEVERSION 상수로부터 주차를 계산하고 buildNumber는 그 주차의 몇 번 빌드를 했는지를 의미한다.
         - bundleVersionCode의 경우 게임프로젝트의 Google Console에서 App Bundle 탐색기의 버전 코드를 확인 후 최신 버전 코드를 입력하면 AOS에서 aab 빌드를 추출할 시 자동으로 1식 올라간다.
     - src
       - build.py ([참고](https://docs.unity3d.com/kr/2021.3/Manual/EditorCommandLineArguments.html))
         - 본 repo의 guide로 세팅된 unity project일 경우 Github에서 받아 build를 추출하는 CLI이다.
         - build.py를 사용하기 위해서 [python](https://www.python.org/downloads/)을 다운로드해야 한다.
         - build.py는 [click](https://click.palletsprojects.com/en/8.1.x/quickstart/), [git](https://gitpython.readthedocs.io/en/stable/intro.html?highlight=pip%20install%20gitpython#installing-gitpython) package를 포함한다.
         - python build.py --help 를 통해 build.py의 각 매개변수의 내용을 확인할 수 있다.
       - Keystore_ex
         - BuildScript에서 keystore을 불러오는 경로를 예시로 들기 위해 있는 임시 파일이다.

## Project settings

1. 본 repo의 AssetDirectory, RootDirectory 폴더 안의 파일을 게임프로젝트로 옮긴다.
      - AssetDirectory 폴더의 Editor 폴더를 게임프로젝트 Assets 폴더 내부에 위치한다. 
      - RootDirectory 폴더의 BuildInfo, src 폴더를 게임프로젝트의 root path에 위치한다.
2. 옮긴 파일을 게임프로젝트의 내용에 맞게 수정한다.
      - BuildScript
        - 본 script의 주석을 참고하여 13~25 line의 내용을 기입한다.
      - buildinfo
        - [About directory files](#About-directory-files) 을 참고하여 기입한다.
      - Keystore_ex
        - 본인이 사용하고 있는 keystore 파일로 대체한다.

## BuildPC settings

## Build

| platform  | output   |
| --------- | -------- |
| AOS       | apk, aab |
| iOS       |   TODO   |

build 추출물은 Project root/Build/AOS, Project root/Build/iOS 에 위치한다.

### Unity Scenario

시작 전 게임 프로젝트의 root 경로에 Build 폴더를 만든 뒤 진행한다.

- apk
  - Unity Menu - Build - AOS - APK
- aab
  - Unity Menu - Build - AOS - AAB

### CLI Scenario

build.py를 통해 build 시 aab, apk 모두 빌드된다.

terminal > python build.py > 매개변수 입력 > build

### Github Action Scenario