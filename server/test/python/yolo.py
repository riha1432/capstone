import sys

print("start")
sys.stdout.flush()
while True:
	data = sys.stdin.readline() 
	if not data:
		continue
	print("파이썬 : ",data)
	sys.stdout.flush()

print("end")
sys.stdout.flush()
