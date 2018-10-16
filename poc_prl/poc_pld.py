### PRIORITY LIST DEFINER / RZ - 2018 ###

## LIBRARIES

from Adafruit_IO import MQTTClient
import datetime
import time

## DICTIONARIES

ter_dir = {

    # Dictionary containing as key the flight codes and their departure hour.'''

    'HV6787': [2018,10,16,18,30,0,0],
    'FR2576': [2018,10,16,17,35,0,0],
    'FR9274': [2018,10,16,16,40,0,0],
    'HV5235': [2018,10,16,17,20,0,0],
    'TB2801': [2018,10,16,19,55,0,0],

    }

tkn_dir = {

    #Dictionary containing as key token number and the name, type,
    #passenger number and flight code of passengers. Frequent flyers = 0.'''

    '0001':['MARTY MCFLY    ',0,1,'FR9274'],
    '0002':['GEORGE COSTANZA',1,1,'FR2576'],
    '0003':['FRODO BAGGINGS ',1,3,'HV6787'],
    '0004':['MARSHAL MATTERS',0,3,'HV5235'],
    '0005':['RON OBVIOUS    ',1,2,'TB2801'],
    '0006':['MARK RENTON    ',1,4,'HV5235']
    
    }

col_dic = {

    0 : 'WHITE',
    1 : 'GREEN',
    2 : 'YELLOW',
    3 : 'RED',
    4 : 'BLUE',
    5 : 'PURPLE'

            }

## DEFINITIONS

ter_bsw = 20        #The basetime/weight of the terminal
ter_ptw = 10        #The weight added per type of passenger. Frequent = 0
ter_pnw = 5        #The weight added per extra passenger

aio_key = '6d2080fc57374353ba8a59d11dcefbb3'
aio_user = 'rogzam'

aio_client = MQTTClient(aio_user, aio_key ,secure=False)

## FUNCTIONS

def cal_pbt(tkn_id):
    '''Calculates the personal boarding time approximation, depending on
       the type of passenger, number of passengers and base time of the terminal.
       Returns personal boarding time in minutes.'''

    pas_typ = tkn_dir[tkn_id][1]
    pas_nps = tkn_dir[tkn_id][2]

    pas_pbt = (ter_bsw + (pas_typ * ter_ptw) + (pas_nps * ter_pnw))

    return pas_pbt

def cal_pbh(tkn_id):
    '''Calculates the current time, extracts the flight hour from flight dictionary,
       calculates minutes to flight, the passenger boardfing hour, boarding time
       and the delta between the boarding time and the minutes to flight.'''
    
    tim_now = datetime.datetime.now()                        #Time now
    
    fli_cod = tkn_dir[tkn_id][3]                             #Flight code
    fli_hou = datetime.datetime(ter_dir[fli_cod][0],         #Flight hour
                                ter_dir[fli_cod][1],
                                ter_dir[fli_cod][2],
                                ter_dir[fli_cod][3],
                                ter_dir[fli_cod][4],
                                ter_dir[fli_cod][5],
                                ter_dir[fli_cod][6])

    fli_ttf = fli_hou - tim_now                              #Time to flight.
    fli_mtf = int(fli_ttf.total_seconds()/60)                #Minutes to flight.
    pas_pbt = cal_pbt(tkn_id)                                #Personal boarding time.
    
    pas_pbh = fli_hou - datetime.timedelta(minutes=pas_pbt)  #Personal boarding hour

    pas_mtb = fli_mtf - pas_pbt                              #Minutes to boarding

    return tim_now, fli_hou, fli_mtf, pas_pbh, pas_pbt, pas_mtb

def tkn_col(pas_mtb):
    
    if pas_mtb >= 10:
        tkn_sts = 0
            
    elif (pas_mtb < 10) and (pas_mtb >= 5):
        tkn_sts = 1
        
    elif (pas_mtb < 5) and (pas_mtb >= 0):
        tkn_sts = 2
        
    elif pas_mtb < 0:
        tkn_sts = 3
        
    else:
        tkn_sts = 5

    return tkn_sts    

aio_client.connect()
aio_client.loop_background()

time.sleep(2)

while True:

    pas_lst = []

    print ('COORDINATED BOARDING PASSENGER LIST AT ({}):\n'.format(datetime.datetime.now()))

    for key,value in tkn_dir.items():
        
        tim_now, fli_hou, fli_mtf, pas_pbh, pas_pbt, pas_mtb = cal_pbh(key)
        
        tkn_sts = tkn_col(pas_mtb)
        
        pas_lst.append([key,tkn_dir[key][0],fli_hou.strftime('%H:%M'),tkn_dir[key][3],pas_pbt,pas_pbh.strftime('%H:%M'),pas_mtb,tkn_sts])

    pas_pri = sorted(pas_lst, key=lambda x: x[5])
    
    for i in pas_pri:
        
        print ('[{}]: {} | DEPARTURE: {} ({}) | TRANSIT TIME: {} MINS | GO TO SECURITY AT {} | TOKEN IS {}.'.format(i[0],i[1],i[2],i[3],i[4],i[5],col_dic[i[7]]))

        aio_sts = 'poc-ein.tkn-sts-'+ str(i[0])
        aio_con = 'poc-ein.tkn-con-'+ str(i[0])

        aio_client.publish(aio_sts, i[7])

        time.sleep(2)

    print ('\n')
    
    time.sleep(30)
                       
