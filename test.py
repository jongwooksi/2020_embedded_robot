
count = 0
receiving_exit = 1

while True:
	receiving_exit == 1
	print("a")
	while True:
		if receiving_exit == 0:
			break
		print("b")
		
		while True:
			receiving_exit == 2
			count += 1
			print("c")
			if count > 50:
				receiving_exit = 0
				break
