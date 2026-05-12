# DI-RONE: 도주 차량 추적용 지능형 자율 드론 시스템 (Comprehensive Technical Manual)

**DI-RONE** 프로젝트는 LTE/TCP 통신 환경에서 AI 객체 탐지 기술을 활용하여 도주 차량을 실시간으로 추적하고, 이를 통합 관제 센터에서 모니터링 및 제어할 수 있는 End-to-End 시스템입니다.

---

## 1. 시스템 아키텍처 및 계층 구조

본 시스템은 데이터의 실시간성과 신뢰성을 보장하기 위해 3개의 주요 계층으로 설계되었습니다.

### 📶 Network Layer (TCP/IP & Socket.io)
- **High-Speed Telemetry**: 드론-서버 간 데이터 송수신은 **TCP 소켓**을 통해 이루어지며, 유실 없는 제어 명령 전달을 보장합니다.
- **Web Bridge**: 서버-웹 클라이언트 간은 **Socket.io**를 사용하여 실시간 양방향 이벤트를 처리합니다.

### 🧠 Intelligence Layer (AI & CV)
- **Object Detection**: YOLOv8 모델을 사용하여 고해상도 영상에서 차량을 실시간 식별합니다.
- **Coordinate Transformation**: 2D 영상 좌표를 실제 지구 좌표계(WGS84)로 변환하는 기하학적 알고리즘을 수행합니다.

### 🚁 Control Layer (MAVLink & Pixhawk)
- **Flight Control**: MAVLink 프로토콜을 통해 기체의 모드 변경, 고도 유지, 기수 방향(Yaw) 제어를 수행합니다.

---

## 2. 상세 통신 프로토콜 (Packet Specification)

드론 클라이언트와 서버는 효율적인 데이터 전송을 위해 **20바이트 고정 길이 패킷**과 7비트 단위 인코딩을 사용합니다.

### 📊 텔레메트리 패킷 맵 (Drone ➡️ Server)
| Byte Index | Field | Description | Encoding |
| :--- | :--- | :--- | :--- |
| 0 ~ 4 | Latitude | 드론의 현재 위도 | 7-bit Shift (Total 35-bit) |
| 5 ~ 9 | Longitude | 드론의 현재 경도 | 7-bit Shift (Total 35-bit) |
| 10 ~ 11 | Altitude | 드론의 현재 고도 (m) | 7-bit Shift (Total 14-bit) |
| 12 ~ 13 | Battery | 배터리 잔량 (V/10) | 7-bit Shift (Total 14-bit) |
| 14 ~ 15 | Speed | 지표 속도 (km/h * 10) | 7-bit Shift (Total 14-bit) |
| 16 ~ 19 | Reserved | 향후 확장용 데이터 영역 | - |

- **Protocol Framing**: 모든 데이터는 `[Video Data] + "_D_" + [Telemetry Data] + "_E_"` 형식으로 캡슐화되어 전송됩니다.

---

## 3. 핵심 알고리즘: 좌표 역추산 및 거리 측정

영상의 중심점에서 탐지된 객체의 위치를 기반으로 실제 GPS 좌표를 계산하는 기하학적 모델을 적용합니다.

### 📐 거리 및 위치 계산 (`Video.py`, `Convert.py`)
1.  **화각(FOV) 기반 각도 계산**:
    - `pixelAngleH = (Vertical_FOV / Resolution_H)`
    - 객체의 픽셀 위치를 기반으로 카메라 광학축과의 사잇각 산출.
2.  **기하학적 거리 측정**:
    - 드론의 현재 피치(Pitch)와 카메라 마운트 각도를 고려하여 지면까지의 직선 거리($D$) 계산.
    - $D = Height / \cos(\text{Camera\Angle} + \text{Pixel\Angle})$
3.  **GPS 좌표 변환 (WGS84)**:
    - 산출된 수평 거리와 드론의 현재 기수(Yaw)를 기반으로 북방(dNorth) 및 동방(dEast) 오프셋 계산.
    - $newLat = currentLat + (dNorth / R_{earth}) \times (180/\pi)$
    - $newLon = currentLon + (dEast / (R_{earth} \times \cos(Lat))) \times (180/\pi)$

---

## 4. 운영 시나리오 (Operational Sequence)

1.  **System Initialization**: 서버 가동 및 드론 클라이언트 TCP 접속 (Port 8484).
2.  **Pre-flight Check**: MAVLink를 통한 기체 상태(GPS Lock, Battery) 확인.
3.  **Arm & Takeoff**: 웹 대시보드에서 'Start' 명령 하달 ➡️ 기체 시동 및 고도 10m 도달.
4.  **Target Pursuit**: 
    - AI가 도주 차량 탐지 시 `GUIDED` 모드로 전환.
    - 객체가 화면 중앙에서 벗어날 경우 Yaw 제어를 통해 기수 고정.
    - `get_location_metres`로 계산된 타겟 좌표로 실시간 이동 명령 전송.
5.  **Return & Land**: 추적 종료 또는 배터리 부족 시 `RTL` 모드로 안전하게 복귀.

---

## 5. 상세 기술 스택 (Full Stack)

### Client Side (On-board Computer)
- **Language**: Python 3.x
- **Core Libs**: 
  - `opencv-python`: 영상 처리 및 코덱 인코딩
  - `pymavlink`: Pixhawk FC 인터페이스
  - `numpy`: 행렬 연산 및 좌표 변환
  - `socket`: TCP 스트리밍

### Server Side (Control Tower)
- **Runtime**: Node.js
- **Framework**: Express.js
- **Communication**: 
  - `net`: TCP 소켓 핸들링
  - `socket.io`: 브라우저 실시간 데이터 브릿지
  - `child_process`: Python AI 엔진(YOLO)과의 IPC 통신

### AI Engine
- **Model**: YOLOv8 (Best.pt / ONNX 지원)
- **Logic**: Base64 스트림 디코딩 ➡️ 추론(Inference) ➡️ 결과 렌더링 ➡️ 스트림 복원

---

## 📸 시스템 이미지

### 웹 대시보드 (GUI)
<img src="https://github.com/user-attachments/assets/54204847-d9d7-4c4b-943b-5dc4772aed61" width="500px">

### 인공지능 객체 탐지
<img src="https://github.com/user-attachments/assets/c1b14978-ff29-4034-ac8e-6c4893137fdf" width="500px">

---
