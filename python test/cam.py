import cv2

cap = cv2.VideoCapture(1)
if cap.isOpened():
	print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))

while True:
	ret, fram = cap.read()
	
	if ret:
		cv2.imshow('video', fram)
		k = cv2.waitKey(1) & 0xFF
		if k == 27:
			break
	else:
		print('error')

cap.release()
cv2.destroyAllWindows()	