



def search(keyword):
	f = open('past-twitter.json','r')
	l = f.readline()
	result = []
	print("Opened")
	for i in f.readlines():
		#print(i)
		if keyword in i:
			result.append(i)

	f.close()
	return result

###

keyword = input("What do you want to search: ")

print(search(keyword))
