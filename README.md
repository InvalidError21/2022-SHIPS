# 2022-KABOAT-MOKPO

* 2021년도 2회 KABOAT 대회 ROS PACKAGE
* Ubuntu 18.04 Desktop / ROS Melodic 에서 테스트 되었음.
* 사용에 필요한 종속 패키지는 미포함.

* 사용 시 해야하는 내용들
1. Ubuntu 설치
2. ROS 설치
3. 종속성 패키지 설치

* 추가/수정할거 : 시각인식(도킹), 좌표이동(딜레이 대신 좌표점 도달여부 전송), 추진기 회전속도 변환(선/각속도 매핑), Navigation 옵션 최적화, 기타(22년도 대회에 맞춰서)
* 없어진 파일 : 원격조종(파일 분실)

*
*
* 이거는 이름 달라서 gbot_core 대신 ships임
* roslaunch ships navigaion.launch / slam.launch
* rosrun ships go.py / gps.py
* rosrun map_server map_saver -f 맵이름
* 
