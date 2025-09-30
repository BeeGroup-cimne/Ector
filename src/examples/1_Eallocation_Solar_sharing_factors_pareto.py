import pandas as pd
import datetime
import matplotlib.pyplot as plt
import pyomo.environ as pyo
import sys


sys.path.insert(1, './ECTOR/')
from  ECTOR.src.main import ECTOR

df_clients = pd.DataFrame([{"id":24,"price":"PVPC","price_sell":"SPOT","freq":1},
                           {"id":21,"price":"PVPC","price_sell":"SPOT","freq":4},
                           {"id":25,"price":"PVPC","price_sell":"SPOT","freq":2}])

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
                               {"id":21,"consumption":13362.0,"timestamp":datetime.datetime(2022,1,4,23)},
                               {"id":25,"consumption":2510.0,"timestamp":datetime.datetime(2022,1,4,0)},
                               {"id":25,"consumption":2568.0,"timestamp":datetime.datetime(2022,1,4,1)},
                               {"id":25,"consumption":2201.0,"timestamp":datetime.datetime(2022,1,4,2)},
                               {"id":25,"consumption":3207.0,"timestamp":datetime.datetime(2022,1,4,3)},
                               {"id":25,"consumption":3260.0,"timestamp":datetime.datetime(2022,1,4,4)},
                               {"id":25,"consumption":4489.0,"timestamp":datetime.datetime(2022,1,4,5)},
                               {"id":25,"consumption":3722.0,"timestamp":datetime.datetime(2022,1,4,6)},
                               {"id":25,"consumption":1951.0,"timestamp":datetime.datetime(2022,1,4,7)},
                               {"id":25,"consumption":0102.0,"timestamp":datetime.datetime(2022,1,4,8)},
                               {"id":25,"consumption":9707.0,"timestamp":datetime.datetime(2022,1,4,9)},
                               {"id":25,"consumption":3863.0,"timestamp":datetime.datetime(2022,1,4,10)},
                               {"id":25,"consumption":1225.0,"timestamp":datetime.datetime(2022,1,4,11)},
                               {"id":25,"consumption":9951.0,"timestamp":datetime.datetime(2022,1,4,12)},
                               {"id":25,"consumption":6087.0,"timestamp":datetime.datetime(2022,1,4,13)},
                               {"id":25,"consumption":5261.0,"timestamp":datetime.datetime(2022,1,4,14)},
                               {"id":25,"consumption":6309.0,"timestamp":datetime.datetime(2022,1,4,15)},
                               {"id":25,"consumption":6534.0,"timestamp":datetime.datetime(2022,1,4,16)},
                               {"id":25,"consumption":7127.0,"timestamp":datetime.datetime(2022,1,4,17)},
                               {"id":25,"consumption":3856.0,"timestamp":datetime.datetime(2022,1,4,18)},
                               {"id":25,"consumption":6453.0,"timestamp":datetime.datetime(2022,1,4,19)},
                               {"id":25,"consumption":2189.0,"timestamp":datetime.datetime(2022,1,4,20)},
                               {"id":25,"consumption":6497.0,"timestamp":datetime.datetime(2022,1,4,21)},
                               {"id":25,"consumption":5637.0,"timestamp":datetime.datetime(2022,1,4,22)},
                               {"id":25,"consumption":3362.0,"timestamp":datetime.datetime(2022,1,4,23)}])

df_price = pd.DataFrame([{"id_price":"PVPC","price":0.000058,"timestamp":datetime.datetime(2022,1,4,0)},
                         {"id_price":"PVPC","price":0.000060,"timestamp":datetime.datetime(2022,1,4,1)},
                         {"id_price":"PVPC","price":0.000062,"timestamp":datetime.datetime(2022,1,4,2)},
                         {"id_price":"PVPC","price":0.000064,"timestamp":datetime.datetime(2022,1,4,3)},
                         {"id_price":"PVPC","price":0.000064,"timestamp":datetime.datetime(2022,1,4,4)},
                         {"id_price":"PVPC","price":0.000063,"timestamp":datetime.datetime(2022,1,4,5)},
                         {"id_price":"PVPC","price":0.000059,"timestamp":datetime.datetime(2022,1,4,6)},
                         {"id_price":"PVPC","price":0.000052,"timestamp":datetime.datetime(2022,1,4,7)},
                         {"id_price":"PVPC","price":0.000078,"timestamp":datetime.datetime(2022,1,4,8)},
                         {"id_price":"PVPC","price":0.000074,"timestamp":datetime.datetime(2022,1,4,9)},
                         {"id_price":"PVPC","price":0.000124,"timestamp":datetime.datetime(2022,1,4,10)},
                         {"id_price":"PVPC","price":0.000124,"timestamp":datetime.datetime(2022,1,4,11)},
                         {"id_price":"PVPC","price":0.000124,"timestamp":datetime.datetime(2022,1,4,12)},
                         {"id_price":"PVPC","price":0.000124,"timestamp":datetime.datetime(2022,1,4,13)},
                         {"id_price":"PVPC","price":0.000075,"timestamp":datetime.datetime(2022,1,4,14)},
                         {"id_price":"PVPC","price":0.000075,"timestamp":datetime.datetime(2022,1,4,15)},
                         {"id_price":"PVPC","price":0.000075,"timestamp":datetime.datetime(2022,1,4,16)},
                         {"id_price":"PVPC","price":0.000075,"timestamp":datetime.datetime(2022,1,4,17)},
                         {"id_price":"PVPC","price":0.000124,"timestamp":datetime.datetime(2022,1,4,18)},
                         {"id_price":"PVPC","price":0.000122,"timestamp":datetime.datetime(2022,1,4,19)},
                         {"id_price":"PVPC","price":0.000124,"timestamp":datetime.datetime(2022,1,4,20)},
                         {"id_price":"PVPC","price":0.000131,"timestamp":datetime.datetime(2022,1,4,21)},
                         {"id_price":"PVPC","price":0.000077,"timestamp":datetime.datetime(2022,1,4,22)},
                         {"id_price":"PVPC","price":0.000076,"timestamp":datetime.datetime(2022,1,4,23)},
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


#import logging

#logging.basicConfig(level=logging.DEBUG)
#log = logging.getLogger('test')
#log.debug('debug') 

df_PV_inversion =  pd.DataFrame([{"id_PV":1,"id":24,"Inversion":1500,"CP":"EC1"},{"id_PV":1,"id":21,"Inversion":1500,"CP":"EC1"},{"id_PV":1,"id":25,"Inversion":500,"CP":"EC1"}])


EC = ECTOR(mode = "Eallocation",SF_Par = False)
EC.Input_clients(df_clients,df_consumption,df_price)
EC.Input_PV(df_PV_curbe,df_PV_inversion)

EC.Declarar_parametres_basics()
EC.constrain_P_Balance()
EC.constrain_cost()
EC.constrain_LP_required_charge_to_clients()
EC.constrain_sharing_factors()
EC.constrain_Payback_general()
EC.constrain_def_instanteneos_self_consumption()
#EC.Constrains_on_the_temporal_sharing_coeficients()
cost = []
mean_self_consumption = []
delta_list = []
for delta in range(1,100):
    EC.Pareto_Cost_self_consumption(delta/100)
    EC.get_data_ready()
    a,b = EC.solver('glpk')
    cost.append(pyo.value(sum(a.Cost[i] for i in a.I)))
    mean_self_consumption.append(pyo.value(a.mean_self_consumption))
    delta_list.append(delta)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(cost, mean_self_consumption, delta_list)
ax.set_xlabel('cost')
ax.set_ylabel('mean_self_consumption')
ax.set_zlabel('delta_list')
plt.plot(cost,mean_self_consumption)
plt.show()
#EC2,results2 = ECTOR().Std_sharing_factors(df_clients,
#                                           df_consumption,
#                                           df_price,
#                                           df_PV_curbe,
#                                           df_PV_inversion)

EC.model.pprint()
a.pprint()
results = EC.pyomo_to_df()
SF_as_Par = False
EC.plot_consumption_inputs(plot=True)
EC.plot_results_consumers(plot = True)
EC.plot_solar_inputs(plot=True)
EC.plot_price_inputs(plot=True)
EC.plot_results_sharing_factors(plot=True)
EC.plot_results_cost_one_consumer(plot=21)
EC.plot_results_cost_one_consumer(plot=24)
EC.plot_results_aggregated_consumption_PV_Bat(plot=True)
EC.plot_results_aggregated_consumption_PV_Bat(plot=True,profit=True)
plt.show()
