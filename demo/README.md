# Demo

Demo that receives rgbd data from D435 sensor, inference the data in server (AWS or Local PC), and pushes the result through FCM.

- RGBD data acquisition and transmission to server
- Scene Difference Recognition
- Object Detection
- Object Tracking (Identification)
- RoI Proximity
- FCM cloud messaging
- AWS (Kinesis, SQS, SNS, API Gateway, Lambda, DynamoDB, etc.)

## Result

## Architecture

### #1

![demo-architecture-1](../docs/demo-architecture-1.png)

심플하게 생각했을 때
- RGBD 데이터를 Web Server로 전송
- Client가 inference 결과를 요청하면 해당 request를 message queue에 넣고 차례대로 처리
- 공통된 데이터로 두개의 AI 모델을 돌려서 결과물을 return
- 처리된 결과값을 client에게 response

---

### #2

![demo-architecture-2](../docs/demo-architecture-2.png)

Local Server에서 inference를 하고 결과값만 FCM cloud messaging으로 push 날려주자
- 매 frame 마다 inference 하는 것은 overhead가 크니까 scene difference가 감지됐을 때만 inference

---

### #3

![demo-architecture-3](../docs/demo-architecture-3.png)

코드로 짜는게 훨씬 더 간단하긴 하지만 굳이 불편하고 느리게 AWS 서비스를 사용해보자
- 데이터 전송은 Kinesis Stream으로 하고 해당 데이터는 SQS queue에 쌓아둔다
- inference 할 raw 데이터는 ElasticCache (Redis)에 담아둔다 
- infernece 결과값은 API Gateway를 통해서 Lambda 함수로 FCM 수행

---

### #4

![demo-architecture-4](../docs/demo-architecture-4.png)

Edge 디바이스를 AWS의 IoT Core 서비스를 붙여보는건 어떨까?
- 서버단은 AWS 서비스 사용하는 것 보다 직접 구성하는게 훨씬 간편하고 빠르니 EC2에 올리자
- 결과값만 lambda를 통해 처리하도록 하자

---

### #5

![demo-architecture-5](../docs/demo-architecture-5.png)

완전히 AWS 서비스로 만들어 보는건 어떨까?
