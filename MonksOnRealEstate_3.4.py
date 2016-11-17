###Credit for this problem: https://www.hackerearth.com/practice/algorithms/graphs/graph-representation/practice-problems/algorithm/monk-in-the-real-estate/
T_Legal = False
while not T_Legal:
	print('\n')
	print("Enter the number of test cases:")
	T = int(input())
	print('\n')
    
	if T > 100 or T < 1 or T==None:
		print("Please enter a value from 1 to 100.")
	else:
		T_Legal = True
    

E_Legal = False
CityX_Legal = False
CityY_Legal = False

for i in range(T):
	bucket = {}
	Count = 0
	while not E_Legal: 
		print('\n')
		print("Enter the number of roads:")
		E = int(input())
		print('\n')
        
		if E > 1000 or E < 1 or E==None:
			print("Please enter a value from 1 to 1000.")
		else:
			E_Legal = True

	for j in range(E):
		CityX_Legal = False
		CityY_Legal = False
		while not CityX_Legal or not CityY_Legal:
			print('\n')
			print("Enter X and Y respectively in the format X-Number-City, Y-Number-City")
			print("Enter the values on the same line, separated by a space, please. No commas, 2 numbers only.")
			#CityX = int(input())
			#CityY = int(input())
			CityX, CityY = [int(x) for x in input("Enter two Numbers:").split()]
			###Implement two space seperated integers and will be ready. 
			###x, y = raw_input("Enter two strings").split(' ')
			###print type(x)
			###print x
			###print type(y)
			###print y
			print('\n')
            
			if CityX > 10000 or CityY > 10000 or CityX < 1 or CityY < 1 or CityX == None or CityY == None:
				print("Make sure your numbers for X-Number-City and Y-Number-City are")
				print("from a range of 1 to 10000.")
			else:
				CityX_Legal = True
				CityY_Legal = True
            
        
		if CityX not in bucket:
			bucket[CityX] = CityX
			Count = Count + 1

		if CityY not in bucket:
			bucket[CityY] = CityY
			Count = Count + 1              
		print("(Note:The current total of cities at this point if still asking")
		print("for which two numbered cities that are being entered.)")
		print(Count)
        
print('\n')
print ("The monk bought ", Count, " cities.")

