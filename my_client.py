# Client(영상을 수집해서 분석을 요청)

import requests, json
import cv2 # openCV
from collections import OrderedDict
import time

import send_mod # send_mod.py

params = {'save_txt': 'T' }
url = 'http://127.0.0.1:5000/predict' # 분석서버 타겟 설정 # predict_api.py가 작동 된 상태에서 구동
file_path = './temp.jpg' # 임시적으로 프레임 이미지 생성 및 전송
data = OrderedDict() # dict 객체 생성

test_video = 'C:/sinheechan.github.io-master/Visual_inteligence_Hardhat/fallen.mp4' # 테스트 영상 링크
cap = cv2.VideoCapture(test_video) # 로컬 노트북 카메라 / input 수단 지정 / 네트워크 카메라 경로

while cap.isOpened(): # 입력수단이 열려있다면 프레임단위로 카메라를 읽는다.
    ret, color_frame = cap.read() # 카메라가 열려있다면 ret 구동
    cv2.imwrite('temp.jpg', color_frame) # 카메라를 읽어서 저장시킨다.
    if ret:
        # time.sleep(1)
        with open(file_path, "rb") as f:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, files={"myfile" : f}, data=params, verify=False)
            print(response.content)
        if response.status_code == 200:
        ### 분석끝 ###
        # 반환값을 읽는 과정
        # 여기서 내가 어떤 모델을 사용할 것인가에 따라 커스텀 진행
            try:
                res = response.json() # 서버의 반환값을 저장
                data['name'] = res['results'][0]['name']
                data['class'] = res['results'][0]['class']
                data['conf'] = res['results'][0]['confidence']
                data['x1'] = res['results'][0]['box']['x1']
                data['y1'] = res['results'][0]['box']['y1']
                data['x2'] = res['results'][0]['box']['x2']
                data['y2'] = res['results'][0]['box']['y2']
                json_data = json.dumps(data, indent=3)
                print(json_data)
            except json.decoder.JSONDecodeError:
                print("Error: JSON 포멧이 아닙니다.")
                continue
            except IndexError as e:
                print("Error: 인덱스가 범위를 벗어났습니다.")
                pass
            else:
                print("Error: 서버 응답 코드가 200이 아닙니다.")

        ### 시각화 전송 로직 시작 ###
        # Json => 시각화 로직
        last_data = OrderedDict()
        last_data['channel_id'] = send_mod.channel_id()
        last_data['metaInfo'] = data 
        last_data['req_id'] = send_mod.req_id()
        last_data['req_time'] = send_mod.req_time()
        last_data['res_time'] = send_mod.req_time()
        last_data['server_id'] = send_mod.server_id()
        last_data['req_image'] = send_mod.req_image('temp.jpg')
        
        temp = json.dumps(last_data)
        with open('base64.txt', 'w') as fd:
            fd.write(temp)
        #print(last_data)
        
        last_json_data = json.dumps(last_data, indent=2)
        last_url = 'http://127.0.0.1:5000/predict' # base64 인코딩 URL 서버로 전송
        response = requests.post(last_url, data=last_json_data)
        print(response.content)
        ### 시각화 전송 로직 종료 ###

    else:
        break   
cap.release()
cv2.destroyAllWindows()