import sys
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

def detect_image(image):
    # dino를 통한 객체 탐색 코드
    
    
    
	return image    

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
	data = sys.stdin.readline()

	# base64 텍스트를 이미지로 변환
	data = data + '=' * (4 - len(data) % 4)
	img = base64.b64decode(data)
	img = Image.open(BytesIO(img))
	img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
	ret, img = cv2.imencode('.jpg', img, encode_param)

	# 이미지를 Ai 연산
	processing_img = detect_image(img)
 
	# 이미지를 base64 string으로 변환 후 server로 전달
	image_base64 = base64.b64encode(processing_img)
	print(image_base64.decode('utf8') + "_E_")
	sys.stdout.flush()

print("end")
sys.stdout.flush()