import random
import getch
import os
import time
import json
import sys

sys.stdout.flush()
print('\033[?25l', end="")
hp=10
atk=1
deff=1
current_atk=atk
current_deff=deff
current_hp=hp
wish=5
rarity = ["legendary","rare","dull"]
item = ["sword","armour","artifact"]
bag=[]
equipped=[]
enemy_hp1=hp
enemy_atk1=atk
enemy_def1=deff
enemies_killed = 0
enemies_killed_check=0
once=True
save_file="saves.json"
should_save=False

def save():
	dic={
		"hp":enemy_hp1,
		"atk":enemy_atk1,
		"def":enemy_def1,
		"kill":enemies_killed,
		"wish":wish,
		"inv":bag,
		"equ":equipped
	}
	f2=open(save_file,'w')
	json.dump(dic,f2)

def load():
	global enemy_hp1,enemy_atk1,enemy_def1,enemies_killed,wish,bag,equipped
	if os.path.exists(save_file)==False:
		return
	f=open(save_file,'r')
	data=json.load(f)
	for a in data:
		if a=="hp":
			enemy_hp1=data[a]
		elif a=="atk":
			enemy_atk1=data[a]
		elif a=="def":
			enemy_def1=data[a]
		elif a=="kill":
			enemies_killed=data[a]
		elif a=="wish":
			wish=data[a]
		elif a=="inv":
			bag=data[a]
		elif a=="equ":
			equipped=data[a]
	
def menu():
	global once,should_save
	if once:
		load()
		once=False
	else:
		if should_save:
			save()
			should_save=False
	while(1):
		clear()
		print("1.Inventory 2.Battle 3.Gatcha 4.Stats")
		char= getch.getch()
		if char=='1':
			inventory()
		elif char=='2':
			battle()
		elif char=='3':
			gacha()
		elif char=='4':
			stats()
			
def inventory():
	global current_hp,current_atk,current_deff,should_save
	equip_mode= True
	a1=""
	a2="inventory"
	b="un"
	while(1):
		if len(equipped)<=0:
			equip_mode=True
		c="|press u to " + b + "equip"
		if len(equipped)>0:d=c
		else:d=""
		clear()
		print("0.back "+d)
		if len(bag)>0 or len(equipped)>0:
			print("\npress number to "+a1+"equip from "+a2)
			counter=1
			for a in bag:
				print(str(counter)+". "+a[1]+" "+a[0])
				counter+=1
			if len(equipped)>0:
				print("\nEquipped ")
				counter=1
				for a in equipped:
					print(str(counter)+". "+a[1]+" "+a[0])
					counter+=1
		else:
			print("\ninventory empty")
		final_hp=final_atk=final_def=0
		char=getch.getch()
		if char=='0':
			if len(equipped)>0:
				for i in equipped:
					if i[0]==item[0]:
						if i[1]==rarity[0]:
							final_atk+=atk*10
						elif i[1]==rarity[1]:
							final_atk+=atk*5
						elif i[1]==rarity[2]:
							final_atk+=atk*2
					elif i[0]==item[1]:
						if i[1]==rarity[0]:
							final_def+=deff*10
						elif i[1]==rarity[1]:
							final_def+=deff*5
						elif i[1]==rarity[2]:
							final_def+=deff*2
					elif i[0]==item[2]:
						if i[1]==rarity[0]:
							final_hp+=hp*10
						elif i[1]==rarity[1]:
							final_hp+=hp*5
						elif i[1]==rarity[2]:
							final_hp+=hp*2	
			current_hp=final_hp+hp
			current_deff=final_def+deff
			current_atk=final_atk+atk
			should_save=True
			break
		elif char=='u':
			if equip_mode:
				equip_mode = False
				a1="un"
				b=""
				a2="equipped"
			elif equip_mode==False:
				equip_mode = True
				a1=""
				b="un"
				a2="inventory"
		if equip_mode==False:
			if len(bag)<9:
				for i in range(0,len(equipped)):
					if char == str(i+1):
						items=equipped[i]
						equipped.remove(items)
						bag.append(items)
			else:
				print("inventory full")
				time.sleep(0.2)
		else:
			if len(equipped)<9:
				for i in range(0,len(bag)):
					if char == str(i+1):
						items=bag[i]
						bag.remove(items)
						equipped.append(items)
			else:
				print("equipment full")
				time.sleep(0.2)
	menu()

def gacha():
	global wish,should_save
	clear()
	word=""
	while(1):
		clear()
		if len(word)>0:
			print(word)
		print("0.back\npress any key to roll for chest| wish:"+str(wish))
		a=getch.getch()
		if a=='0':
			menu()
			break
		elif wish<=0:
			print("wish count insufficient to roll")
			getch.getch()
		else:
			should_save=True
			wish-=1	
			aquired=[]
			aquired.append(random.choice(item))
			aquired.append(random.choice(rarity))
			result=["item added to inventory","item trashed"]
			while(1):
				clear()
				print("you got "+aquired[1]+" "+aquired[0])
				print("\n\n1.Keep 2.Discard")
				char=getch.getch()
				if char=='1':
					if len(bag)<9:
						bag.append(aquired)
						word=result[0]
						break
					else:
						print("inventory full")
						getch.getch()
				elif char=='2':
					word=result[1]
					break
				elif char=='0':
					menu()
				else:
					word=""
	menu()

def battle():
	global should_save,current_hp,wish,enemy_hp1,enemy_atk1,enemy_def1,enemies_killed,enemies_killed_check
	enemy_hp=enemy_hp1
	enemy_atk=enemy_atk1
	enemy_def=enemy_def1
	actual_atk=0
	if current_atk<=enemy_def:
		actual_atk=int(enemy_hp/10)
	else:
		actual_atk=int(current_atk-enemy_def/current_atk)
	clear()
	print("press any key to atk | 0.retreat")
	do=True
	time.sleep(0.5)
	while 1:
		if enemies_killed!=enemies_killed_check:
			enemy_atk1=5+enemy_atk1
			enemy_def1=2+enemy_def1
			enemy_hp1=10+enemy_hp1
			enemies_killed_check=enemies_killed
			enemy_hp=enemy_hp1
			enemy_atk=enemy_atk1
			enemy_def=enemy_def1
			if current_atk<=enemy_def:
				actual_atk=int(enemy_hp/10)
			else:
				actual_atk=int(current_atk-enemy_def)
		if do:
			print("player's turn...")
			print("\nPlayer: Hp="+str(current_hp)+" || Enemy: Hp="+str(enemy_hp))
			do=False
		char=getch.getch()
		if char=='0':
			break
		else:
			enemy_hp-=actual_atk
			if enemy_hp<0:
				enemy_hp=0
			clear()
			print("press any key to atk | 0.retreat")
			print("player's turn...\n")
			print("Player: Hp="+str(current_hp)+" || Enemy: Hp="+str(enemy_hp))
			print("You dealt "+str(actual_atk)+" damage")
			if enemy_hp==0:
				should_save=True
				print("Enemy killed")
				time.sleep(1)
				word=""
				rand=random.randint(0,1)
				if rand==0:
					aquired=[]
					aquired.append(random.choice(item))
					aquired.append(random.choice(rarity))
					result=["item added to inventory","item trashed"]
					while 1:
						clear()
						print("you got "+aquired[1]+" "+aquired[0]+" from enemy")
						print("\n\n1.Keep 2.Discard")
						char=getch.getch()
						if char=='1':
							if len(bag)<9:
								word=result[0]
								bag.append(aquired)
								print(word)
								time.sleep(1)
								break
							else:
								print("\ninventory full")
						elif char=='2':
							word=result[1]
							print(word)
							time.sleep(1)
							break
						elif char=='0':
							menu()
						else:
							word=""
				else:
					print("you got 1 wish")
					wish+=1
					time.sleep(0.3)
				enemies_killed+=1
				battle_next()
			else:
				time.sleep(1)
				clear()
				print("press any key to atk | 0.retreat")
				print("enemy's turn...\n")		
				print("Player: Hp="+str(current_hp)+" || Enemy: Hp="+str(enemy_hp))
				time.sleep(1)
				current_hp-=enemy_atk
				clear()
				if current_hp<0:
					current_hp=0
				print("press any key to atk | 0.retreat")
				print("enemy's turn...\n")	
				print("Player: Hp="+str(current_hp)+" || Enemy: Hp="+str(enemy_hp))
				print("Enemy dealt "+str(enemy_atk)+" damage")
				time.sleep(1.0)
				if current_hp==0:
					print("you lost")
					getch.getch()
					break
				clear()
				print("press any key to atk | 0.retreat")
				print("player's turn...\n")		
				print("Player: Hp="+str(current_hp)+" || Enemy: Hp="+str(enemy_hp))
	menu()
	
def battle_next():
	clear()
	print("continue battle ?\n1.Yes 2.No")
	a = getch.getch()
	if a=='1':
		battle()
	elif a=='2':
		menu()
	else:
		clear()
		battle_next()
			
def stats():
	while(1):
		clear()
		print("0.back")
		print("hp :"+str(current_hp))	
		print("atk:"+str(current_atk))	
		print("def:"+str(current_deff))
		char=getch.getch()
		if char=='0':
			break
	menu()
	
def clear():
	os.system('clear')

menu()