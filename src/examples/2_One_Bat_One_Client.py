import pandas as pd
import datetime
import matplotlib.pyplot as plt
import sys

sys.path.insert(1, './ECTOR/')
from ECTOR.src.main import ECTOR

df_clients = pd.DataFrame([{"id":24,"price":"PVPC","price_sell":"SPOT"}])

df_consumption = pd.DataFrame([{"id":24,"consumption":18499.0,"timestamp":datetime.datetime(2022,1,4,00)},
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
                               {"id":24,"consumption":22409.0,"timestamp":datetime.datetime(2022,1,4,23)}])


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


df_PV_inversion =  pd.DataFrame([{"id_PV":1,"id":24,"Inversion":500,"CP":"EC1"}])

df_CP_Sharing =  pd.DataFrame([ {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,0)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,1)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,2)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,3)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,4)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,5)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,6)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,7)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,8)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,9)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,10)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,11)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,12)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,13)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,14)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,15)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,16)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,17)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,18)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,19)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,20)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,21)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,22)},
                                {"CP":"EC1","id":24,"Inversion":1,"timestamp":datetime.datetime(2022,1,4,23)}])



df_Bat_characteristics= pd.DataFrame([{"id_Bat":"PEUSA", "PBat_max":40000,"EBat_min":2000,"EBat_max":80000 ,"EBat_0":30000,"nmax":0.8,"CP":"EC1"}])

df_Bat_inversion =  pd.DataFrame([{"id_Bat":"PEUSA" ,"id":24,"Inversion":200}])


df_Sharing =  pd.DataFrame([{"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,0)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,1)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,2)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,3)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,4)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,5)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,6)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,7)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,8)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,9)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,10)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,11)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,12)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,13)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,14)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,15)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,16)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,17)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,18)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,19)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,20)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,21)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,22)},
                            {"CP":"EC1" ,"id":24,"SF":1,"timestamp":datetime.datetime(2022,1,4,23)}])

df_Sharing_Between_CP =  pd.DataFrame([{"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,0)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,1)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,2)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,3)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,4)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,5)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,6)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,7)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,8)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,9)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,10)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,11)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,12)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,13)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,14)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,15)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,16)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,17)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,18)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,19)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,20)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,21)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,22)},
                                       {"CP":"EC1" ,"CP_where_energy_is_generated":"EC1","SF":0,"timestamp":datetime.datetime(2022,1,4,23)}])

EC = ECTOR(mode = "SF",SF_Par = True)
EC.Input_clients(df_clients,df_consumption,df_price)
EC.Input_PV(df_PV_curbe,df_PV_inversion)
EC.Input_Bateries(df_Bat_characteristics,df_Bat_inversion)
EC.Input_sharing_Factors_CP(df_Sharing)


EC.Declarar_parametres_basics()
EC.constrain_Battery_limits()
EC.constrain_Bat_degradation()
EC.constrain_P_Balance()
EC.constrain_cost()
EC.constrain_LP_required_charge_to_clients()


EC.Cost_Function_cost()


EC.get_data_ready()
a,b = EC.solver('glpk')

#EC2,results2 = ECTOR().Std_Batery_Optimitzation(df_clients,
#                                              df_consumption,
#                                              df_price,
#                                              df_PV_curbe,
#                                              df_PV_inversion,
#                                              df_Bat_characteristics,
#                                              df_Bat_inversion,
#                                              df_Sharing)

results = EC.pyomo_to_df()
EC.plot_consumption_inputs(plot=True)
EC.plot_results_consumers(plot = True)
EC.plot_solar_inputs(plot=True)
EC.plot_results_Bat(plot=True)
EC.plot_price_inputs(plot=True)
EC.plot_results_sharing_factors(plot=True)
EC.plot_results_cost_one_consumer(plot=24)
EC.plot_results_aggregated_consumption_PV_Bat(plot=True)
EC.plot_results_aggregated_consumption_PV_Bat(plot=True,profit=True)
plt.show()
