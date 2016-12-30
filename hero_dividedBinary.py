import numpy
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import LSTM
from data_import import heroid_dict, rad_win_data, all_win_data
from keras.callbacks import ModelCheckpoint
from keras import optimizers
from keras.layers.embeddings import Embedding
from keras.preprocessing.sequence import pad_sequences
import random
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D

def sublists(s, i):
    length = len(s)
    for size in range(i, length + 1):
        for start in range(0, (length - size) + 1):
            yield s[start:start+size]
			
def seqSublists(s, i):
	try:
		length = len(s)
	except:
		length =0
		pass
	for size in range(i, length + 1):
		yield s[0:0+size]
		
def gen_epochData(inputD,sub_switch):
	print('generating training data')
	dataX = []
	dataY = []
	data_weight = []
	X = []
	comb = []
	for ind_heroInput in inputD:
		if ind_heroInput[0]>=116:
			#dire win
			rad_win = 0
			if ind_heroInput[0]==116:
				#rad pick first
				pick_seq = 118
			else:
				pick_seq = 119
		else:
			rad_win = 1
			if ind_heroInput[0]==114:
				#rad pick first
				pick_seq = 118
			else:
				pick_seq = 119
		#dataX.append(ind_heroInput[1::])
		raw_list = ind_heroInput[1::]
		raw_list.insert(0,pick_seq)
		if sub_switch:
			sub_list = seqSublists(raw_list, 1)
			for each_item in sub_list:
				dataX.append(each_item)
				dataY.append(rad_win)
				data_weight.append([len(each_item)])
				comb.append([each_item,rad_win])
		else:
			dataX.append(raw_list)
			dataY.append(rad_win)
			comb.append([raw_list,rad_win])
		
	#for ind_list in dataX:
		#norm_dataX = [ind_item/float(max_heroID) for ind_item in ind_list]
		#X.append(norm_dataX)
	#X = numpy.reshape(X, (len(dataX), max_len, 1))
		
	#dataY = np_utils.to_categorical(dataY,2)
	print('training data generation done, total processed match #: ',len(dataX))
	dataX = pad_sequences(dataX, maxlen=max_len, dtype='float32', padding='post')
	return dataX, dataY, numpy.array(data_weight).flatten(), comb

# fix random seed for reproducibility
numpy.random.seed(7)
# define the hero id dictionary for conversion
hero_to_id, id_to_hero = heroid_dict()
# ini variables for easy tweak
batch_size = 1
max_len = 11
sub_seq_len = 11
data_start = 0
data_limit = 10000
#test_limit = 500
max_heroID = 119+0
epoch_number = 10
droprate = 0.5
patient = 6*epoch_number*0.1 # training loop will exit after # of high accuracy epoch has reached
#rand_start = numpy.random.randint(0,data_limit-2*test_limit)

# prepare the dataset of input to output pairs encoded as integers
heroInput_pre,_ = all_win_data('all_win_training.csv',0,2000)
X, Y, _, comb = gen_epochData(heroInput_pre,True)
thefile = open('train.json', 'w+')
for item in comb:
  thefile.write("%s\n" % item)
"""print('prebalanced rad_win=1 :',Y.count(1))
print('prebalanced rad_win=0 :',Y.count(0))
over_count = Y.count(1)-Y.count(0)
if Y.count(1)>Y.count(0):
	delete_c = 0
	while delete_c < over_count:
		rand_del = random.randrange(len(Y))
		if Y[rand_del]==1:
			Y=numpy.delete(Y,rand_del,0)
			X=numpy.delete(X,rand_del,0)
			#data_weight=numpy.delete(data_weight,rand_del,0)
			delete_c += 1
		
print('result for rad_win data row: ',numpy.count_nonzero(Y))
#print(Y.count(0))"""

"""heroInput_pre,_ = all_win_data('all_win_test.csv',0,100000)
X_val, Y_val, _, comb = gen_epochData(heroInput_pre,False)
thefile = open('train_vali.json', 'w+')
for item in comb:
  thefile.write("%s\n" % item)
print('prebalanced valid rad_win=1 :',Y_val.count(1))
print('prebalanced valid rad_win=0 :',Y_val.count(0))"""

# ini keras LSTM model
model = Sequential()
# embedding layer [dictionary_size, input_size, max_time length]
model.add(Embedding(max_heroID+1, max_heroID+1, input_length=max_len))
model.add(Convolution1D(300, 11, border_mode='valid', activation='relu', subsample_length=2))
#67, 64 model.add(Convolution1D(300, 10, border_mode='valid', activation='relu', subsample_length=1))
model.add(MaxPooling1D(pool_length=1))
model.add(LSTM(100, return_sequences=True, dropout_W=droprate, dropout_U=droprate))
model.add(LSTM(100, return_sequences=True, dropout_W=droprate, dropout_U=droprate))
model.add(LSTM(100, return_sequences=False, dropout_W=droprate, dropout_U=droprate))
model.add(Dense(1, activation='sigmoid')) #binary output
cusAdam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(loss='binary_crossentropy', optimizer=cusAdam, metrics=['accuracy'])

checkpointer = ModelCheckpoint(filepath="bi_subSeq_{epoch:02d}.h5", monitor='acc', verbose=1, save_best_only=False)
model.fit(X, Y, nb_epoch=epoch_number, batch_size=64, verbose=1, validation_split=0.1, callbacks=[checkpointer])
#model.fit(X, Y, nb_epoch=epoch_number, batch_size=64, verbose=1, callbacks=[checkpointer,early_stop])
#model.save('test_model_binaryPredict-3500d.h5')
exit()