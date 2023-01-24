# About

unity CI/CD 관련 스크립트, 가이드 관리

## User Guide

### Settings

1. 본 repo의 AssetDirectory, RootDirectory 폴더 안의 파일을 게임프로젝트로 옮긴다.
      - AssetDirectory 폴더의 Editor 폴더를 게임프로젝트 Assets 폴더 내부에 위치한다. ([참고](https://docs.unity3d.com/Manual/SpecialFolders.html))
      - RootDirectory 폴더의 BuildInfo, src 폴더를 게임프로젝트의 root path에 위치한다.
2. 옮긴 파일을 게임프로젝트의 내용에 맞게 수정한다.
      - BuildScript
        - 주석을 참고하여 13~25 line의 내용을 기입한다.
      - buildinfo
        - buildinfo는 0,0,0 의 형식을 가지며 버전 자동화를 위해 사용된다.
        - 각 숫자는 "weekNumber,buildNumber,bundleVersionCode" 를 의미한다.
        - weekNumber, buildNumber의 경우 BuildScript의 SetVersion 메서드의 내용으로 분석할 수 있으며 처음 기입 시 0으로 해도 무방하다.
          - weekNumber는 BuildScript의 DAY_CALCULATEVERSION 상수로부터 주차를 계산하고 buildNumber는 그 주차의 몇 번 빌드를 했는지를 의미한다.
        - bundleVersionCode의 경우 게임프로젝트의 Google Console에서 App Bundle 탐색기의 버전 코드를 확인 후 최신 버전 코드를 입력하면 AOS에서 aab 빌드를 추출할 시 자동으로 1식 올라간다.
      - Keystore_ex
        - 본인이 사용하고 있는 keystore 파일로 대체한다.

## Build

| platform  | output   |
| --------- | -------- |
| AOS       | apk, aab |
| iOS       |          |

### Command Scenario

### Github Action Scenario