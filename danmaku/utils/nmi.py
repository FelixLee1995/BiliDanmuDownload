from sklearn.metrics.cluster import normalized_mutual_info_score


def fuc():
	arr_1 = []
	arr_2 = []
	with open('kdd10_Label','r') as file_1:
		for line in file_1.readlines():
			arr_1.append(int(line))
	with open('kdd10_output','r') as file_2:
		for line in file_2.readlines():
			arr_2.append(int(line))
	print(normalized_mutual_info_score(arr_1, arr_2))


fuc()
