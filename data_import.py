import numpy
import csv
import json

def heroid_dict():
	with open('heroes.json') as raw_heroid:
	    data = json.load(raw_heroid)
	data = data['heroes']

	#create new dictionary
	hero_to_id = {}
	id_to_hero = {}
	for ind_dict in data:
		#update 2 dictionaries based on imported json
		hero_to_id.update({ind_dict['name']:ind_dict['id']})
		id_to_hero.update({ind_dict['id']:ind_dict['name']})
	#print(hero_to_id)
	#print(id_to_hero)
	return hero_to_id, id_to_hero

def rad_win_data(limit):
	count_limit = 0
	with open('rad_win.csv', 'r', encoding = 'utf-8') as f:
	  reader = csv.reader(f)
	  data_list = list(reader)
	  #form: [ [], [], [], ...]
	  for i, s in enumerate(data_list):
		  #replace \t with space
		  s[0] = s[0].replace('\t',' ')
		  #split string into list for easier access
		  data_list[i] = s[0].split(' ')
	#convert all str to int within lists
	data_list = [list(map(int, ind_list)) for ind_list in data_list]
	error_count = 0
	sorted_heroid = []
	sorted_withMatchID = []

	for ind_node in data_list:
		count_limit = count_limit + 1
		if count_limit>limit:
			break
		del ind_node[0] #delete table id
		del ind_node[1:3] #delete game_mode and lobby_type
		del ind_node[21] #delete rad_win
		#check for duplicate hero entry in each row
		heroid_list = list(ind_node[k] for k in [1,3,5,7,9,11,13,15,17,19])

		if len(heroid_list) != len(set(heroid_list)):
			#print(heroid_list)
			#print(len(heroid_list))
			#print(len(set(heroid_list)))
			#print('error match id: '+str(ind_node[0]))
			del ind_node[0:22]
			error_count = error_count + 1
			continue

		temp = []
		temp.append(ind_node[0])
		del ind_node[0] #remove match_id
		
		#for dire_index in range(10,20,2):
			#add 500 to distinguish dire and radiant
			#ind_node[dire_index] = ind_node[dire_index]+500

		# create two lists and sort heroid list according to sequence list
		heroid_list = list(ind_node[k] for k in [0,2,4,6,8,10,12,14,16,18])
		herosel_sequence = list(ind_node[j] for j in [1,3,5,7,9,11,13,15,17,19])
		# determine classification for rad/dire win pick sequence
		try:
			seq_verif = herosel_sequence.index(1)
		except:
			try:
				seq_verif = herosel_sequence.index(2)
			except:
				print('fatal error for matchid: ',temp)
				exit()
		if seq_verif >4:
			#dire pick first
			rd_class = 115
		else:
			rd_class = 114
			
		temp2 = [x for (y,x) in sorted(zip(herosel_sequence,heroid_list))]
		#temp.append([x for (y,x) in sorted(zip(herosel_sequence,heroid_list))])
		#temp.insert(0,rd_class)
		
		temp2.insert(0,rd_class)
		temp.append(temp2)
		
		sorted_heroid.append(temp2)
		sorted_withMatchID.append(temp)
		
		#sorted_heroid.insert(0,rd_class)
	#print('total duplicate hero entries: '+str(error_count))
	data_list = list(filter(None, data_list))
	#print('example output list: ', data_list[0])
	#print('example sorted list: ', sorted_heroid[0])
	#print('total # of list: ', len(data_list))
	return sorted_heroid, sorted_withMatchID

def all_win_data(filename,lower_limit,upper_limit):
	count_limit = 0
	with open(filename, 'r', encoding = 'utf-8') as f:
	  reader = csv.reader(f)
	  data_list = list(reader)
	  #form: [ [], [], [], ...]
	  for i, s in enumerate(data_list):
		  #replace \t with space
		  s[0] = s[0].replace('\t',' ')
		  #split string into list for easier access
		  data_list[i] = s[0].split(' ')
	#convert all str to int within lists
	data_list = [list(map(int, ind_list)) for ind_list in data_list]
	error_count = 0
	sorted_heroid = []
	sorted_withMatchID = []

	for ind_node in data_list:
		count_limit = count_limit + 1
		if count_limit>upper_limit:
			break
		elif count_limit<lower_limit:
			continue
		del ind_node[0] #delete table id
		del ind_node[1:3] #delete game_mode and lobby_type
		rad_win = ind_node[21] #win status for radiant
		del ind_node[21] #delete rad_win
		#check for duplicate hero entry in each row
		heroid_list = list(ind_node[k] for k in [1,3,5,7,9,11,13,15,17,19])

		if len(heroid_list) != len(set(heroid_list)):
			#print(heroid_list)
			#print(len(heroid_list))
			#print(len(set(heroid_list)))
			#print('error match id: '+str(ind_node[0]))
			del ind_node[0:22]
			error_count = error_count + 1
			continue

		temp = []
		temp.append(ind_node[0])
		del ind_node[0] #remove match_id
		
		for dire_index in range(10,20,2):
			#add 117 to distinguish dire and radiant
			#ind_node[dire_index] = ind_node[dire_index]+117
			ind_node[dire_index] = ind_node[dire_index]+0

		# create two lists and sort heroid list according to sequence list
		heroid_list = list(ind_node[k] for k in [0,2,4,6,8,10,12,14,16,18])
		herosel_sequence = list(ind_node[j] for j in [1,3,5,7,9,11,13,15,17,19])
		# determine classification for rad/dire win pick sequence
		try:
			seq_verif = herosel_sequence.index(1)
		except:
			try:
				seq_verif = herosel_sequence.index(2)
			except:
				print('fatal error for matchid: ',temp)
				exit()
		if rad_win == 1:
			#rad win
			if seq_verif >4:
				#dire pick first
				rd_class = 115
			else:
				rd_class = 114
		else:
			if seq_verif >4:
				#dire pick first
				rd_class = 117
			else:
				rd_class = 116
			
		temp2 = [x for (y,x) in sorted(zip(herosel_sequence,heroid_list))]
		#temp.append([x for (y,x) in sorted(zip(herosel_sequence,heroid_list))])
		#temp.insert(0,rd_class)
		
		temp2.insert(0,rd_class)
		temp.append(temp2)
		
		sorted_heroid.append(temp2)
		sorted_withMatchID.append(temp)
		
		#sorted_heroid.insert(0,rd_class)
	#print('total duplicate hero entries: '+str(error_count))
	data_list = list(filter(None, data_list))
	#print('example output list: ', data_list[0])
	#print('example sorted list: ', sorted_heroid[0])
	#print('total # of list: ', len(data_list))
	return sorted_heroid, sorted_withMatchID
