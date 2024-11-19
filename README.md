# baekgeunBot
디스코드 음악 봇


명령어 목록//

!play : 음성 채널 입장 / 대기열 재생

!play {검색어 / url / 플레이리스트 url} : 대기열 추가 후 재생

!autoplay : 자동 재생 (추천곡) 모드 활성화 / 비활성화

!repeat : 대기열 반복 활성화 / 비활성화

!skip : 현재 곡 스킵

!stop : 곡 정지 / 음성 채널 퇴장

!now : 현재 재생 곡 표시

!queue : 현재 대기열 표시

!shuffle : 대기열 셔플

!remove -1 : 대기열 전체 삭제

!remove {number} : 해당 number 대기열 삭제

!pause : 일시정지

!resume : 일시정지 해제

!reset : 모든 변수 초기화 (대기열, 플레이리스트, 자동재생 모드, 대기열 반복 등)

//

# 필요 패키지 및 파이썬 버전

Python 3.11.7

Python 3.11.10 (google cloud platform)


﻿beautifulsoup4==4.12.3
 
discord==2.3.2

discord.py==2.4.0

ffmpeg==1.4

lxml==5.3.0

PyNaCl==1.5.0

selenium==4.26.1

yt-dlp==2024.11.4
