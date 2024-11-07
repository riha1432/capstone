# DI-RONE: 도주 차량 추적 AI 드론 시스템

## 프로젝트 소개

DI-RONE은 도주 차량을 추적하기 위해 설계된 AI 기반 드론 시스템이다.
최근 도주 차량으로 인한 교통사고, 재산 손실, 인명 피해가 증가함에 따라, 저희 팀은 이러한 문제를 해결하기 위해 드론을 이용한 실시간 추적 시스템을 개발하게 되었다.
DI-RONE은 인공지능(AI) 객체 탐지 모델을 통해 도주 차량을 식별하고, 드론을 이용해 실시간 위치를 추적하며, 웹 클라이언트를 통해 직관적인 인터페이스를 제공한다.

### 주요 목표
- **사회 안전망 강화**: 신속하고 정확한 도주 차량 추적을 통해 공공 안전을 증진하고 추가 피해를 방지
- **효율적인 추적 시스템**: LTE 통신을 통해 장거리 통신을 가능하게 하여 다양한 환경에서 안정적인 성능을 제공

---

## 서버
* 서버는 Node.js로 구현되어 있으며, **TCP 소켓**을 사용하여 드론과 실시간으로 통신
* 서버는 드론과 웹 클라이언트 사이에서 데이터를 중개하며, AI 모듈을 통해 도주 차량의 위치를 추적하고 이를 드론에 전달
* 서버는 또한 드론에서 전송된 영상을 수집하고 웹 클라이언트로 실시간으로 송출

주요 기능:
- **TCP 소켓 통신**: 드론 및 클라이언트와의 실시간 통신을 위한 데이터 송수신.
- **AI 처리**: YOLO 모델을 사용하여 도주 차량을 실시간으로 추적.
- **웹 인터페이스 제공**: 실시간 영상을 웹 클라이언트를 통해 제공하며, 드론 제어 명령을 수신

## 인공지능 클라이언트
* AI 클라이언트는 YOLO 객체 탐지 모델을 사용하여 실시간 영상에서 도주 차량을 탐지하고 추적
* 이 모델은 **학습된 데이터**를 기반으로 객체를 식별하고, 이를 서버에 전달하여 드론이 해당 차량을 추적

주요 기능:
- **객체 탐지**: YOLO 모델을 사용하여 실시간 영상에서 도주 차량을 인식.
- **객체 추적**: 차량의 위치를 추적하여, 드론이 정확한 위치를 실시간으로 업데이트
- **데이터 처리 및 송수신**: 서버와의 통신을 통해 차량 위치를 전송하고, 드론의 위치를 관리

a$\color{red}이 브랜치에서는 시스템의 V1.0기준으로 연결되어 있으며, 서버와 AI 클라이언트가 실시간으로 데이터를 교환하여 도주 차량 추적을 수행합니다.$
