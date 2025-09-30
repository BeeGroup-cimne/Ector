import pandas as pd
import datetime
import pyomo.environ as pyo
from pyomo.environ import *
import matplotlib.pyplot as plt
import sys

sys.path.insert(1, './ECTOR/')
from ECTOR.src.main import ECTOR


df_clients = pd.DataFrame([{"id":24,"price":"PVPC","price_sell":"SPOT"},
                           {"id":21,"price":"PVPC","price_sell":"SPOT"}])
df_consumption = pd.DataFrame([{"id":24,"consumption":18499.0,"timestamp":datetime.datetime(2022,1,4,0)},
                               {"id":24,"consumption":17986.0,"timestamp":datetime.datetime(2022,1,4,1)},
                               {"id":24,"consumption":18224.0,"timestamp":datetime.datetime(2022,1,4,2)},
                               {"id":24,"consumption":17579.0,"timestamp":datetime.datetime(2022,1,4,3)},
                               {"id":24,"consumption":18028.0,"timestamp":datetime.datetime(2022,1,4,4)},
                               {"id":24,"consumption":18307.0,"timestamp":datetime.datetime(2022,1,4,5)},
                               {"id":24,"consumption":22750.0,"timestamp":datetime.datetime(2022,1,4,6)},
                               {"id":24,"consumption":27332.0,"timestamp":datetime.datetime(2022,1,4,7)},
                               {"id":24,"consumption":34836.0,"timestamp":datetime.datetime(2022,1,4,8)},
                               {"id":24,"consumption":34204.0,"timestamp":datetime.datetime(2022,1,4,9)},
                               {"id":24,"consumption":32194.0,"timestamp":datetime.datetime(2022,1,4,10)},
                               {"id":24,"consumption":25880.0,"timestamp":datetime.datetime(2022,1,4,11)},
                               {"id":24,"consumption":22850.0,"timestamp":datetime.datetime(2022,1,4,12)},
                               {"id":24,"consumption":20552.0,"timestamp":datetime.datetime(2022,1,4,13)},
                               {"id":24,"consumption":23205.0,"timestamp":datetime.datetime(2022,1,4,14)},
                               {"id":24,"consumption":21715.0,"timestamp":datetime.datetime(2022,1,4,15)},
                               {"id":24,"consumption":24508.0,"timestamp":datetime.datetime(2022,1,4,16)},
                               {"id":24,"consumption":28273.0,"timestamp":datetime.datetime(2022,1,4,17)},
                               {"id":24,"consumption":32667.0,"timestamp":datetime.datetime(2022,1,4,18)},
                               {"id":24,"consumption":36870.0,"timestamp":datetime.datetime(2022,1,4,19)},
                               {"id":24,"consumption":36491.0,"timestamp":datetime.datetime(2022,1,4,20)},
                               {"id":24,"consumption":33106.0,"timestamp":datetime.datetime(2022,1,4,21)},
                               {"id":24,"consumption":28053.0,"timestamp":datetime.datetime(2022,1,4,22)},
                               {"id":24,"consumption":22409.0,"timestamp":datetime.datetime(2022,1,4,23)},
                               {"id":21,"consumption":12510.0,"timestamp":datetime.datetime(2022,1,4,0)},
                               {"id":21,"consumption":12568.0,"timestamp":datetime.datetime(2022,1,4,1)},
                               {"id":21,"consumption":12201.0,"timestamp":datetime.datetime(2022,1,4,2)},
                               {"id":21,"consumption":13207.0,"timestamp":datetime.datetime(2022,1,4,3)},
                               {"id":21,"consumption":13260.0,"timestamp":datetime.datetime(2022,1,4,4)},
                               {"id":21,"consumption":44489.0,"timestamp":datetime.datetime(2022,1,4,5)},
                               {"id":21,"consumption":43722.0,"timestamp":datetime.datetime(2022,1,4,6)},
                               {"id":21,"consumption":41951.0,"timestamp":datetime.datetime(2022,1,4,7)},
                               {"id":21,"consumption":40102.0,"timestamp":datetime.datetime(2022,1,4,8)},
                               {"id":21,"consumption":39707.0,"timestamp":datetime.datetime(2022,1,4,9)},
                               {"id":21,"consumption":43863.0,"timestamp":datetime.datetime(2022,1,4,10)},
                               {"id":21,"consumption":41225.0,"timestamp":datetime.datetime(2022,1,4,11)},
                               {"id":21,"consumption":39951.0,"timestamp":datetime.datetime(2022,1,4,12)},
                               {"id":21,"consumption":36087.0,"timestamp":datetime.datetime(2022,1,4,13)},
                               {"id":21,"consumption":35261.0,"timestamp":datetime.datetime(2022,1,4,14)},
                               {"id":21,"consumption":36309.0,"timestamp":datetime.datetime(2022,1,4,15)},
                               {"id":21,"consumption":36534.0,"timestamp":datetime.datetime(2022,1,4,16)},
                               {"id":21,"consumption":37127.0,"timestamp":datetime.datetime(2022,1,4,17)},
                               {"id":21,"consumption":33856.0,"timestamp":datetime.datetime(2022,1,4,18)},
                               {"id":21,"consumption":36453.0,"timestamp":datetime.datetime(2022,1,4,19)},
                               {"id":21,"consumption":42189.0,"timestamp":datetime.datetime(2022,1,4,20)},
                               {"id":21,"consumption":46497.0,"timestamp":datetime.datetime(2022,1,4,21)},
                               {"id":21,"consumption":15637.0,"timestamp":datetime.datetime(2022,1,4,22)},
                               {"id":21,"consumption":13362.0,"timestamp":datetime.datetime(2022,1,4,23)}])

df_price = pd.DataFrame([{"id_price":"PVPC","price":0.0058,"timestamp":datetime.datetime(2022,1,4,0)},
                         {"id_price":"PVPC","price":0.0060,"timestamp":datetime.datetime(2022,1,4,1)},
                         {"id_price":"PVPC","price":0.0062,"timestamp":datetime.datetime(2022,1,4,2)},
                         {"id_price":"PVPC","price":0.0064,"timestamp":datetime.datetime(2022,1,4,3)},
                         {"id_price":"PVPC","price":0.0064,"timestamp":datetime.datetime(2022,1,4,4)},
                         {"id_price":"PVPC","price":0.0063,"timestamp":datetime.datetime(2022,1,4,5)},
                         {"id_price":"PVPC","price":0.0059,"timestamp":datetime.datetime(2022,1,4,6)},
                         {"id_price":"PVPC","price":0.0052,"timestamp":datetime.datetime(2022,1,4,7)},
                         {"id_price":"PVPC","price":0.0078,"timestamp":datetime.datetime(2022,1,4,8)},
                         {"id_price":"PVPC","price":0.0074,"timestamp":datetime.datetime(2022,1,4,9)},
                         {"id_price":"PVPC","price":0.0124,"timestamp":datetime.datetime(2022,1,4,10)},
                         {"id_price":"PVPC","price":0.0124,"timestamp":datetime.datetime(2022,1,4,11)},
                         {"id_price":"PVPC","price":0.0124,"timestamp":datetime.datetime(2022,1,4,12)},
                         {"id_price":"PVPC","price":0.0124,"timestamp":datetime.datetime(2022,1,4,13)},
                         {"id_price":"PVPC","price":0.0075,"timestamp":datetime.datetime(2022,1,4,14)},
                         {"id_price":"PVPC","price":0.0075,"timestamp":datetime.datetime(2022,1,4,15)},
                         {"id_price":"PVPC","price":0.0075,"timestamp":datetime.datetime(2022,1,4,16)},
                         {"id_price":"PVPC","price":0.0075,"timestamp":datetime.datetime(2022,1,4,17)},
                         {"id_price":"PVPC","price":0.0124,"timestamp":datetime.datetime(2022,1,4,18)},
                         {"id_price":"PVPC","price":0.0122,"timestamp":datetime.datetime(2022,1,4,19)},
                         {"id_price":"PVPC","price":0.0124,"timestamp":datetime.datetime(2022,1,4,20)},
                         {"id_price":"PVPC","price":0.0131,"timestamp":datetime.datetime(2022,1,4,21)},
                         {"id_price":"PVPC","price":0.0077,"timestamp":datetime.datetime(2022,1,4,22)},
                         {"id_price":"PVPC","price":0.0076,"timestamp":datetime.datetime(2022,1,4,23)},
                         {"id_price":"SPOT","price": 4.400000e-07,"timestamp":datetime.datetime(2022,1,4,0)},
                         {"id_price":"SPOT","price": 0.000000e+00,"timestamp":datetime.datetime(2022,1,4,1)},
                         {"id_price":"SPOT","price": 0.000000e+00,"timestamp":datetime.datetime(2022,1,4,2)},
                         {"id_price":"SPOT","price": 0.000000e+00,"timestamp":datetime.datetime(2022,1,4,3)},
                         {"id_price":"SPOT","price": 0.000000e+00,"timestamp":datetime.datetime(2022,1,4,4)},
                         {"id_price":"SPOT","price": 0.000000e+00,"timestamp":datetime.datetime(2022,1,4,5)},
                         {"id_price":"SPOT","price": 8.000000e-08,"timestamp":datetime.datetime(2022,1,4,6)},
                         {"id_price":"SPOT","price": 6.000000e-06,"timestamp":datetime.datetime(2022,1,4,7)},
                         {"id_price":"SPOT","price": 4.470000e-06,"timestamp":datetime.datetime(2022,1,4,8)},
                         {"id_price":"SPOT","price": 0.000000e+00,"timestamp":datetime.datetime(2022,1,4,9)},
                         {"id_price":"SPOT","price":-1.000000e-08,"timestamp":datetime.datetime(2022,1,4,10)},
                         {"id_price":"SPOT","price":-1.000000e-08,"timestamp":datetime.datetime(2022,1,4,11)},
                         {"id_price":"SPOT","price":-3.000000e-08,"timestamp":datetime.datetime(2022,1,4,12)},
                         {"id_price":"SPOT","price":-1.000000e-07,"timestamp":datetime.datetime(2022,1,4,13)},
                         {"id_price":"SPOT","price":-1.000000e-07,"timestamp":datetime.datetime(2022,1,4,14)},
                         {"id_price":"SPOT","price":-1.000000e-07,"timestamp":datetime.datetime(2022,1,4,15)},
                         {"id_price":"SPOT","price":-1.300000e-07,"timestamp":datetime.datetime(2022,1,4,16)},
                         {"id_price":"SPOT","price":-1.000000e-07,"timestamp":datetime.datetime(2022,1,4,17)},
                         {"id_price":"SPOT","price":-1.000000e-08,"timestamp":datetime.datetime(2022,1,4,18)},
                         {"id_price":"SPOT","price": 0.000000e+00,"timestamp":datetime.datetime(2022,1,4,19)},
                         {"id_price":"SPOT","price": 4.150000e-06,"timestamp":datetime.datetime(2022,1,4,20)},
                         {"id_price":"SPOT","price": 1.001000e-05,"timestamp":datetime.datetime(2022,1,4,21)},
                         {"id_price":"SPOT","price": 5.000000e-06,"timestamp":datetime.datetime(2022,1,4,22)},
                         {"id_price":"SPOT","price": 3.250000e-06,"timestamp":datetime.datetime(2022,1,4,23)},])


df_PV_curbe = pd.DataFrame([{"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,0)},
                            {"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,1)},
                            {"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,2)},
                            {"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,3)},
                            {"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,4)},
                            {"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,5)},
                            {"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,6)},
                            {"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,7)},
                            {"id_PV":1,"P":   77.0,"timestamp":datetime.datetime(2022,1,4,8)},
                            {"id_PV":1,"P": 2077.0,"timestamp":datetime.datetime(2022,1,4,9)},
                            {"id_PV":1,"P": 6113.0,"timestamp":datetime.datetime(2022,1,4,10)},
                            {"id_PV":1,"P":11873.0,"timestamp":datetime.datetime(2022,1,4,11)},
                            {"id_PV":1,"P":14232.0,"timestamp":datetime.datetime(2022,1,4,12)},
                            {"id_PV":1,"P":15214.0,"timestamp":datetime.datetime(2022,1,4,13)},
                            {"id_PV":1,"P":15336.0,"timestamp":datetime.datetime(2022,1,4,14)},
                            {"id_PV":1,"P":14378.0,"timestamp":datetime.datetime(2022,1,4,15)},
                            {"id_PV":1,"P":13206.0,"timestamp":datetime.datetime(2022,1,4,16)},
                            {"id_PV":1,"P":10654.0,"timestamp":datetime.datetime(2022,1,4,17)},
                            {"id_PV":1,"P": 7221.0,"timestamp":datetime.datetime(2022,1,4,18)},
                            {"id_PV":1,"P": 3016.0,"timestamp":datetime.datetime(2022,1,4,19)},
                            {"id_PV":1,"P":  721.0,"timestamp":datetime.datetime(2022,1,4,20)},
                            {"id_PV":1,"P":    2.0,"timestamp":datetime.datetime(2022,1,4,21)},
                            {"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,22)},
                            {"id_PV":1,"P":    0.0,"timestamp":datetime.datetime(2022,1,4,23)}])


df_PV_inversion =  pd.DataFrame([{"id_PV":1,"id":24,"Inversion":500,"CP":"EC1"},
                                 {"id_PV":1,"id":21,"Inversion":500,"CP":"EC1"}])

df_Bat_characteristics= pd.DataFrame([{"id_Bat":"PEUSA", "PBat_max":40000,"EBat_min":2000,"EBat_max":80000 ,"EBat_0":3000,"nmax":0.8,"CP":"EC1"}])

df_Bat_inversion =  pd.DataFrame([{"id_Bat":"PEUSA" ,"id":24,"Inversion":200},
                                  {"id_Bat":"PEUSA" ,"id":21,"Inversion":25}])


df_Sharing =  pd.DataFrame([{"id":24,"timestamp":datetime.datetime(2022,1,4,0),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,1),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,2),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,3),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,4),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,5),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,6),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,7),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,8),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,9),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,10),"CP":"EC1","SF":0.5353},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,11),"CP":"EC1","SF":0.5698},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,12),"CP":"EC1","SF":0.5602},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,13),"CP":"EC1","SF":0.5493},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,14),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,15),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,16),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,17),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,18),"CP":"EC1","SF":0.578},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,19),"CP":"EC1","SF":0.5186},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,20),"CP":"EC1","SF":0.548},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,21),"CP":"EC1","SF":0.7},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,22),"CP":"EC1","SF":0.5},
                            {"id":24,"timestamp":datetime.datetime(2022,1,4,23),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,0),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,1),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,2),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,3),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,4),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,5),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,6),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,7),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,8),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,9),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,10),"CP":"EC1","SF":0.4647},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,11),"CP":"EC1","SF":0.4302},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,12),"CP":"EC1","SF":0.4398},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,13),"CP":"EC1","SF":0.4507},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,14),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,15),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,16),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,17),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,18),"CP":"EC1","SF":0.422},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,19),"CP":"EC1","SF":0.4814},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,20),"CP":"EC1","SF":0.452},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,21),"CP":"EC1","SF":0.3},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,22),"CP":"EC1","SF":0.5},
                            {"id":21,"timestamp":datetime.datetime(2022,1,4,23),"CP":"EC1","SF":0.5}])

[{"id":24,"timestamp":1641254400000,"CP":"EC1","SF":0.0},{"id":24,"timestamp":1641254400000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641258000000,"CP":"EC1","SF":0.0},{"id":24,"timestamp":1641258000000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641261600000,"CP":"EC1","SF":1.0},{"id":24,"timestamp":1641261600000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641265200000,"CP":"EC1","SF":0.0},{"id":24,"timestamp":1641265200000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641268800000,"CP":"EC1","SF":0.0},{"id":24,"timestamp":1641268800000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641272400000,"CP":"EC1","SF":1.0},{"id":24,"timestamp":1641272400000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641276000000,"CP":"EC1","SF":0.0},{"id":24,"timestamp":1641276000000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641279600000,"CP":"EC1","SF":0.0},{"id":24,"timestamp":1641279600000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641283200000,"CP":"EC1","SF":0.0000029435},{"id":24,"timestamp":1641283200000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641286800000,"CP":"EC1","SF":0.0000000856},{"id":24,"timestamp":1641286800000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641290400000,"CP":"EC1","SF":0.3233962053},{"id":24,"timestamp":1641290400000,"CP":"EC2","SF":0.5202898726},{"id":24,"timestamp":1641294000000,"CP":"EC1","SF":0.331259289},{"id":24,"timestamp":1641294000000,"CP":"EC2","SF":0.5335997759},{"id":24,"timestamp":1641297600000,"CP":"EC1","SF":0.3207705791},{"id":24,"timestamp":1641297600000,"CP":"EC2","SF":0.5323475773},{"id":24,"timestamp":1641301200000,"CP":"EC1","SF":0.3144708007},{"id":24,"timestamp":1641301200000,"CP":"EC2","SF":0.5303355638},{"id":24,"timestamp":1641304800000,"CP":"EC1","SF":0.0000000111},{"id":24,"timestamp":1641304800000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641308400000,"CP":"EC1","SF":0.0000000119},{"id":24,"timestamp":1641308400000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641312000000,"CP":"EC1","SF":0.0000000129},{"id":24,"timestamp":1641312000000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641315600000,"CP":"EC1","SF":0.000000016},{"id":24,"timestamp":1641315600000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641319200000,"CP":"EC1","SF":0.3470660966},{"id":24,"timestamp":1641319200000,"CP":"EC2","SF":0.5629991578},{"id":24,"timestamp":1641322800000,"CP":"EC1","SF":0.278710313},{"id":24,"timestamp":1641322800000,"CP":"EC2","SF":0.5099318268},{"id":24,"timestamp":1641326400000,"CP":"EC1","SF":0.3343900229},{"id":24,"timestamp":1641326400000,"CP":"EC2","SF":0.5492716906},{"id":24,"timestamp":1641330000000,"CP":"EC1","SF":0.3693838437},{"id":24,"timestamp":1641330000000,"CP":"EC2","SF":0.6114722214},{"id":24,"timestamp":1641333600000,"CP":"EC1","SF":0.0},{"id":24,"timestamp":1641333600000,"CP":"EC2","SF":0.5},{"id":24,"timestamp":1641337200000,"CP":"EC1","SF":0.0},{"id":24,"timestamp":1641337200000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641254400000,"CP":"EC1","SF":1.0},{"id":21,"timestamp":1641254400000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641258000000,"CP":"EC1","SF":0.0},{"id":21,"timestamp":1641258000000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641261600000,"CP":"EC1","SF":0.0},{"id":21,"timestamp":1641261600000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641265200000,"CP":"EC1","SF":1.0},{"id":21,"timestamp":1641265200000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641268800000,"CP":"EC1","SF":0.0},{"id":21,"timestamp":1641268800000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641272400000,"CP":"EC1","SF":0.0},{"id":21,"timestamp":1641272400000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641276000000,"CP":"EC1","SF":1.0},{"id":21,"timestamp":1641276000000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641279600000,"CP":"EC1","SF":0.0},{"id":21,"timestamp":1641279600000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641283200000,"CP":"EC1","SF":0.0000029436},{"id":21,"timestamp":1641283200000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641286800000,"CP":"EC1","SF":0.0000000856},{"id":21,"timestamp":1641286800000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641290400000,"CP":"EC1","SF":0.2721672729},{"id":21,"timestamp":1641290400000,"CP":"EC2","SF":0.4797101274},{"id":21,"timestamp":1641294000000,"CP":"EC1","SF":0.2481936715},{"id":21,"timestamp":1641294000000,"CP":"EC2","SF":0.4664002241},{"id":21,"timestamp":1641297600000,"CP":"EC1","SF":0.2456822052},{"id":21,"timestamp":1641297600000,"CP":"EC2","SF":0.4676524227},{"id":21,"timestamp":1641301200000,"CP":"EC1","SF":0.2473626728},{"id":21,"timestamp":1641301200000,"CP":"EC2","SF":0.4696644362},{"id":21,"timestamp":1641304800000,"CP":"EC1","SF":0.0000000111},{"id":21,"timestamp":1641304800000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641308400000,"CP":"EC1","SF":0.0000000119},{"id":21,"timestamp":1641308400000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641312000000,"CP":"EC1","SF":0.0000000129},{"id":21,"timestamp":1641312000000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641315600000,"CP":"EC1","SF":0.000000016},{"id":21,"timestamp":1641315600000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641319200000,"CP":"EC1","SF":0.2820417349},{"id":21,"timestamp":1641319200000,"CP":"EC2","SF":0.4370008422},{"id":21,"timestamp":1641322800000,"CP":"EC1","SF":0.2570683334},{"id":21,"timestamp":1641322800000,"CP":"EC2","SF":0.4900681732},{"id":21,"timestamp":1641326400000,"CP":"EC1","SF":0.3273734955},{"id":21,"timestamp":1641326400000,"CP":"EC2","SF":0.4507283094},{"id":21,"timestamp":1641330000000,"CP":"EC1","SF":0.3693743107},{"id":21,"timestamp":1641330000000,"CP":"EC2","SF":0.3885277786},{"id":21,"timestamp":1641333600000,"CP":"EC1","SF":0.0},{"id":21,"timestamp":1641333600000,"CP":"EC2","SF":0.5},{"id":21,"timestamp":1641337200000,"CP":"EC1","SF":0.0},
 {"id":21,"timestamp":1641337200000,"CP":"EC2","SF":0.5}]

### Només ECTOR


EC = ECTOR(mode = "SF",SF_Par = True)
EC.Input_clients(df_clients.reset_index(drop=True),
                 df_consumption,
                 df_price)
EC.Input_PV(df_PV_curbe,df_PV_inversion)
EC.Input_Bateries(df_Bat_characteristics,df_Bat_inversion)
EC.Input_sharing_Factors_CP(df_Sharing)


EC.Declarar_parametres_basics()
EC.constrain_Battery_limits()
EC.constrain_Bat_degradation()
EC.constrain_P_Balance()
EC.constrain_cost()
EC.constrain_LP_required_charge_to_clients()
#Falta tornar a pensar aixo
#EC.constrain_Payback_by_element(element="Bat")#optional to fix the Payback of the Bat between all the users


EC.constrain_Payback_general()


#EC.Cost_Function_cost()
EC.Cost_Function_Cost_bat_operation()
EC.get_data_ready()
a,b = EC.solver('gurobi')
EC.model.pprint()

# Extract data
results = EC.pyomo_to_df()

#EC2,results2 = ECTOR().Std_EC_Batery_with_already_SF(df_clients,
#                                                  df_consumption,
#                                                  df_price,
#                                                  df_PV_curbe,
#                                                  df_PV_inversion,
#                                                  df_Bat_characteristics,
#                                                  df_Bat_inversion,
#                                                  df_Sharing)

results = EC.pyomo_to_df()
EC.plot_consumption_inputs(plot=True)
EC.plot_results_consumers(plot = True)
EC.plot_solar_inputs(plot=True)
EC.plot_solar_inputs(plot=True)
EC.plot_price_inputs(plot=True)
EC.plot_results_sharing_factors(plot=True)
EC.plot_results_cost_one_consumer(plot=24)
EC.plot_results_aggregated_consumption_PV_Bat(plot=True)
EC.plot_results_aggregated_consumption_PV_Bat(plot=True,profit=True)
plt.show()

import logging
from pyomo.util.infeasible import log_infeasible_constraints
log_infeasible_constraints(a)
log_infeasible_constraints(a, log_expression=True, log_variables=True)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
