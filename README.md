# About

unity CI/CD 관련 스크립트, 가이드 관리

## About directory files

1. .github
   - 본 폴더의 내부 yml 파일들은 Github Actions에 사용되며 .github/workflows 의 경로는 절대 경로이다.
     - workflows
       - cicd.yml
         - Github Actions yml script 틀이다.
         - 해당 script의 주석에 간략한 설명이 있다.
2. AssetDirectory
   - 본 폴더의 내부 파일들은 게임프로젝트 Assets 폴더 내부에 위치한다.
     - Editor ([참고](https://docs.unity3d.com/Manual/SpecialFolders.html))
       - BuildScript
         - CLI, Github Actions으로 빌드 할 때 사용한다.
         - 해당 script의 주석에 간략한 설명이 있다.
3. RootDirectory
   - 본 폴더의 내부 파일들은 게임프로젝트 root path에 위치한다.
     - BuildInfo
       - buildinfo
         - buildinfo는 0,0,0 의 형식을 가지며 버전 자동화를 위해 사용된다.
         - 각 숫자는 "weekNumber,buildNumber,bundleVersionCode" 를 의미한다.
         - weekNumber, buildNumber의 경우 BuildScript의 SetVersion 메서드의 내용으로 분석할 수 있으며 처음 기입 시 0으로 해도 무방하다.
         - weekNumber는 BuildScript의 DAY_CALCULATEVERSION 상수로부터 주차를 계산하고 buildNumber는 그 주차의 몇 번 빌드를 했는지를 의미한다.
         - bundleVersionCode의 경우 게임프로젝트의 Google Console에서 App Bundle 탐색기의 버전 코드를 확인 후 최신 버전 코드를 입력하면 AOS에서 aab 빌드를 추출할 시 자동으로 1식 올라간다.
     - fastlane (참고 - [fastlane-plugin-appcenter](https://github.com/microsoft/fastlane-plugin-appcenter), [fastlane](https://docs.fastlane.tools/))
       - 빌드 추출물을 Appcenter에 배포하기 위해 사용된다.
       - 본 폴더는 폴더명 그대로 게임프로젝트 root path에 위치한다. 단, 폴더 내부에 있는 Gemfile, Gemfile.lock 은 폴더 밖(게임프로젝트 root path)으로 옮긴다.
       - .env, Pluginfile, Gemfile, Gemfile.lock 은 fastlane-plugin-appcenter 세팅 시 자동으로 생성되며, .env를 통해 APPCENTER_OWNER_NAME, APPCENTER_DISTRIBUTE_DESTINATIONS(Group)), APPCENTER_DISTRIBUTE_NOTIFY_TESTERS 를 설정한다. 
       - Fastfile은 yml에서 fastlane 명령어를 통해 실행할 수 있는 자동화 구성이다.
     - src
       - build.py ([참고](https://docs.unity3d.com/kr/2021.3/Manual/EditorCommandLineArguments.html))
         - 본 repo의 guide로 세팅된 unity project일 경우 Github에서 clone 받아 빌드하여 apk, aab를 추출하는 CLI이다.
         - BuildPC(remote server)에서 사용 시 빌드 추출물을 Local로 받을 수 있다.
         - build.py를 사용하기 위해서 필요한 package
           - [python](https://www.python.org/downloads/)
           - [click](https://click.palletsprojects.com/en/8.1.x/quickstart/)
           - [git](https://gitpython.readthedocs.io/en/stable/intro.html?highlight=pip%20install%20gitpython#installing-gitpython)
           - [paramiko](https://www.paramiko.org/installing.html)
           - scp:
           ```
           pip install scp
           ```
         - python build.py --help 를 통해 build.py의 각 매개변수의 내용을 확인할 수 있다.
       - Keystore_ex
         - BuildScript에서 keystore을 불러오는 경로를 예시로 들기 위해 있는 임시 파일이다.

## Project settings

1. 본 repo의 .github/workflows/cicd.yml 을 본 경로 그대로 게임프로젝트 root path에 위치한다. [참고](https://docs.github.com/en/actions/quickstart)
2. 본 repo의 AssetDirectory, RootDirectory 폴더 안의 파일을 게임프로젝트로 옮긴다.
      - AssetDirectory 폴더의 Editor 폴더를 게임프로젝트 Assets 폴더 내부에 위치한다.
      - RootDirectory 폴더의 BuildInfo, src 폴더를 게임프로젝트의 root path에 위치한다.
        - fastlane의 폴더의 경우 [About directory files](#about-directory-files)를 참고한다.
3. 옮긴 파일을 게임프로젝트의 내용에 맞게 수정한다.
      - cicd
        - 본 script의 주석을 참고하여 빈 경로들을 기입한다.
          - 기입 전 [Github Actions Settings](#github-actions-settings) 을 반드시 읽고 세팅한다.
      - BuildScript
        - 본 script의 주석을 참고하여 13~25 line의 내용을 기입한다.
      - buildinfo
        - [About directory files](#about-directory-files) 을 참고하여 기입한다.
      - Keystore_ex
        - 본인이 사용하고 있는 keystore 파일로 대체한다.

## BuildPC(Remote Server) settings

BuildPC는 기본적으로 본인의 게임 프로젝트가 본 repo와는 상관없이 빌드 될 수 있도록 세팅되어있어야 한다.

### CLI Settings

CLI는 본 repo에 있는 build.py 를 사용한다.

1. 본 repo에 있는 build.py을 BuildPC에 다운로드한다.
2. [About directory files](#About-directory-files)의 build.py 부분을 반드시 읽고 세팅한다.
3. BuildPC(remote server), LocalPC를 SSH로 연결한다. [참고](https://learn.microsoft.com/ko-kr/windows-server/administration/openssh/openssh_install_firstuse)

### Github Actions Settings

Github acriton 관련 내용은 모두 [GitHub Actions Documentation](https://docs.github.com/actions) 을 참고한다.

- 빌드하려는 게임프로젝트 root path에 .github/workflows/cicd.yml 이 반드시 존재해야 한다.
- 게임 프로젝트 repo의 Settings에서 runner를 생성 한다. [참고](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners)
- Actions secrets and variables 등록한다. [참고](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
  - 본 repo의 cicd.yml에서 secrets.GIT_ACCESS_TOKEN, secrets.APP_CENTER_TOKEN 부분처럼 민감할 수 있는 정보들을 담아둘 수 있다.

## Build

| platform  | output   |
| --------- | -------- |
| AOS       | apk, aab |
| iOS       |   TODO   |

빌드 추출물은 Project root/Build/AOS, Project root/Build/iOS 에 위치한다.

AOS ouput의 경우 Github Actions Scenario에서는 Appcenter를 통해 업로드된 aab를 다운로드 할 수 있기 때문에 apk는 추출하지 않는다.

### Unity Scenario

시작 전 게임 프로젝트의 root 경로에 Build 폴더를 만든 뒤 진행한다.

- apk
  - Unity Menu - Build - AOS - APK
- aab
  - Unity Menu - Build - AOS - AAB

### CLI Scenario

build.py를 통해 빌드 시 aab, apk 모두 빌드된다.

terminal > python build.py > 매개변수 입력 > build

**build.py 주의사항**
- 매개변수 중 띄어쓰기가 포함될 경우 " or ' 로 묶어주어야 한다.
- BuildPC가 아닌 LocalPC에서 사용할 경우 "Enter IPv4 of your pc" 부분을 입력할 때 Skip을 입력한다.

### Github Actions Scenario

main branch에 push 할 경우 Github Action이 작동하고 BuildPC에서 빌드를 진행한다.

빌드 추출물의 경우 마지막 commit message에 따라 나뉠 수 있다. (build_all, build_aos, build_ios, ci skip)

- build_all 이 마지막 commit message에 포함되어 있을 경우
  - aab, ios output(TODO)를 추출한다.
- build_aos 이 마지막 commit message에 포함되어 있을 경우
  - aab를 추출한다.
- build_ios 이 마지막 commit message에 포함되어 있을 경우
  - ios output(TODO)를 추출한다.
- ci skip 이 마지막 commit message에 포함되어 있을 경우
  - skip

빌드 추출물은 Appcenter에 upload 되며 fastlane/.env의 APPCENTER_DISTRIBUTE_NOTIFY_TESTERS이 true라면 APPCENTER_DISTRIBUTE_DESTINATIONS(group)에 등록되어 있는 사용자에게 알림(e-mail)을 보낸다.

** trigger 방식과 빌드 규칙 등은 [GitHub Actions Documentation](https://docs.github.com/actions)을 참고하여 수정하여도 무관하다. **
