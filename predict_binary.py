import numpy
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from data_import import heroid_dict, all_win_data
import random
from keras import metrics
import itertools

def sublistCheck(list1, list2):
    return ''.join(map(str, list2)) in ''.join(map(str, list1))
	
def multSublistCheck(list1, list2):
	#list1 contains multiple list ex: [ [], [], ... ]
	#print('list1: ')
	#print('checking list: ', list2)
	for single_list in list1:
		if ''.join(map(str, list2)) in ''.join(map(str, single_list)):
			#print('matching result: ', list2, 'with ',single_list)
			return True
		else:
			#print('continue to next')
			pass
	return False

#special sublists function that exclude last element
def sublists(s, i):
	try:
		length = len(s)
	except:
		length =0
		pass
	for size in range(i, length):
		start = 0
		#for start in range(0, (length - size)):
		yield s[start:start+size]

def permu_list(inputList,p_limit):
	outcome = inputList[0] #result of the match
	out_permu = []
	for i in range(p_limit):
		permu = numpy.random.permutation(inputList[1::])
		ap_list = list(permu)
		ap_list.insert(0,outcome)
		out_permu.append(ap_list)
	return out_permu
		
def gen_epochData_predict(inputD):
	# input is single list
	#print('generating training data')
	dataX = []
	dataY = []
	X = []
	
	if inputD[0]>=116:
		#dire win
		rad_win = 0
		if inputD[0]==116:
			#rad pick first
			pick_seq = 118
		else:
			pick_seq = 119
	else:
		rad_win = 1
		if inputD[0]==114:
			#rad pick first
			pick_seq = 118
		else:
			pick_seq = 119
	raw_list = inputD[1::]
	raw_list.insert(0,pick_seq)
	dataX.append(raw_list)
	dataY.append(rad_win)
		
	#for ind_list in dataX:
		#norm_dataX = [ind_item/float(max_heroID) for ind_item in ind_list]
		#X.append(norm_dataX)
	#X = numpy.reshape(X, (len(dataX), max_len, 1))
	X = pad_sequences(dataX, maxlen=max_len, dtype='float32', padding='post')
	#X = numpy.reshape(dataX, (len(dataX), max_len))
	#dataY = np_utils.to_categorical(dataY,2)
	#print('training data generation done, total processed match #: ',len(dataX))
	return X, dataY

max_heroID = 119
test_num = 300
max_len = 11
d_upper_limit = 100000
mode = 2 # 1-normal prediction 2-subsequence 3-random permutation
permu_length = 10 #limit permutation length

"""import h5py
f = h5py.File('test.h5', 'r+')
del f['optimizer_weights']
f.close()"""

model = load_model('test.h5')
hero_to_id, id_to_hero = heroid_dict()

heroInput_pre, sorted_withMatchID = all_win_data('all_win_test.csv',0,100000)
#print(len(heroInput_pre))
#exit()
acc_track = []

for iter_count in range(0,len(heroInput_pre)):

	test = random.choice(sorted_withMatchID)
	sorted_withMatchID.remove(test)
	#test[1] format: [116, 26, 110, ...]
	if mode==2:
		test_sub = sublists(test[1],2)
		mode_coi = 5.5
	elif mode==3:
		test_sub = permu_list(test[1],permu_length)
		mode_coi = 11
	elif mode==1:
		test_sub = [test[1]]
		mode_coi = 11
	print('#', iter_count+1, test)
	for ind_sub in test_sub:
		X, dataY = gen_epochData_predict(ind_sub)
		prediction = model.predict(X, verbose=0)

		if prediction >=0.5:
			out = 1
		else:
			out = 0
			
		if out == dataY[0]:
			"""#predictin correct
			if out == 1:
				#rad win predicion
				acc_track.extend(prediction[0])
			else:
				acc_track.extend([1-prediction[0][0]])"""
			acc_track.extend([1])
		else:
			"""#predictin wrong
			if out == 1:
				acc_track.extend([1-prediction[0][0]])
			else:
				acc_track.extend(prediction[0])"""
			acc_track.extend([0])
			#print('append',1-len(ind_sub)/6)
		print(X,'prediction: ',out,' true outcome: ',dataY[0],'raw prediction: ',prediction)

print('overall accuracy: ',sum(acc_track)/len(acc_track))