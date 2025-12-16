import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import pyomo.environ as pyo


class plotter():
    def plot_consumption_inputs(self,plot=True):
        P_consumed  = pd.melt(self.P_Consumed.reset_index(), 
            id_vars='time_index', 
            value_vars = self.P_Consumed.columns, # list of days of the week
            var_name='i', 
            value_name='consumption')
        P_consumed = pd.merge(pd.merge(P_consumed,self.timestamps,on="time_index"),self.clients_info[["id","i"]],on="i").drop(columns=["i","time_index"])
        if plot:
            pd.pivot_table(P_consumed,values="consumption",index=["timestamp"],columns="id").plot(title ="Consumption input")
        else:
            return P_consumed
    
    def plot_solar_inputs(self,plot=True):
        P_PV  = pd.melt(self.P_PV.reset_index(), 
            id_vars='time_index', 
            value_vars = self.P_PV.columns, # list of days of the week
            var_name='PV_index', 
            value_name='P')
        P_PV = pd.merge(pd.merge(P_PV,self.timestamps,on="time_index"),self.PV_info,on="PV_index").drop(columns=["PV_index","time_index"])
        if plot:
            pd.pivot_table(P_PV,values="P",index=["timestamp"],columns="id_PV").plot(title ="PV Generated Energy")
        else:
            return P_PV
        
    def plot_price_inputs(self,plot=True):
        Price  = pd.melt(self.Ecost.reset_index(), 
            id_vars='time_index', 
            value_vars = self.Ecost.columns,
            var_name='price_index', 
            value_name='price')
        Price = pd.merge(pd.merge(Price,self.timestamps,on="time_index"),self.id_price,on="price_index").drop(columns=["price_index","time_index"])
        if plot:
            pd.pivot_table(Price,values="price",index=["timestamp"],columns="id_price").plot(title ="Price of energy")
        else:
            return Price
    
    def get_and_adapt_sharing_factors(self,CP=False,results_SF_in = None):
        if self.mode == "Eallocation":
            index = [i for i,x in enumerate([("E_shared" in i.columns)==True for i in self.list_df_results]) if x]
            results_SF = self.list_df_results[index[0]].reset_index().set_index(["id","timestamp","CP"]).round(0).reset_index()
            
            Energy_produced =self.get_energy_CP_plot().reset_index()
            
            results_SF = pd.merge(Energy_produced,results_SF,on=["timestamp","CP"])
            results_SF["SF"] = results_SF["E_shared"]/results_SF["Energy_CP"]
            results_SF = results_SF.fillna(0)
            results_SF = results_SF.drop(columns=["E_shared","Energy_CP"]).set_index(["id","timestamp","CP"])
            
            index = [i for i,x in enumerate([("E_shared_CP" in i.columns)==True for i in self.list_df_results]) if x]
            results_SF_CP = self.list_df_results[index[0]].reset_index()
            
            Energy_produced = self.get_energy_CP_plot().reset_index()
            
            results_SF_CP = pd.merge(Energy_produced,results_SF_CP,on=["timestamp","CP"])
            results_SF_CP["SF_CP"] = results_SF_CP["E_shared_CP"]/results_SF_CP["Energy_CP"]
            results_SF_CP = results_SF_CP.fillna(0)
            results_SF_CP = results_SF_CP.drop(columns=["E_shared_CP","Energy_CP"]).set_index(["CP_where_energy_is_generated","timestamp","CP"])
            if CP:
                return results_SF_CP.round(6)

            results_SF_val = pd.concat([results_SF.round(6).reset_index(),results_SF_CP.round(6).reset_index().rename(columns={"CP":"id","CP_where_energy_is_generated":"CP","SF_CP":"SF"})]).fillna(0)
            results_SF_val = results_SF_val.loc[:,["timestamp","CP","SF"]].groupby(["timestamp","CP"]).sum().round(6)
            results_SF_val.loc[results_SF_val.SF != 1,:]
            error = 1 - results_SF_val.loc[results_SF_val.SF != 1,:]
            big_error = error.loc[(error.SF>10**-5)|(error.SF<-1*10**-5),:]

            df_aux = results_SF.reset_index().groupby(["CP","id"]).first().reset_index().drop(columns=["timestamp","SF"])
            big_error = pd.merge(pd.merge(df_aux,df_aux.groupby("CP").size().reset_index().rename(columns={0:"size"})),big_error.reset_index(),on="CP")
            big_error["SF"] = (big_error["SF"]/big_error["size"]).round(6)
            
            results_SF = pd.merge(big_error.drop(columns="size").rename(columns={"SF":"error"}),results_SF.reset_index(),on=["CP","timestamp","id"],how = "outer").fillna(0)

            results_SF["SF"] = results_SF["error"]+results_SF["SF"]

            results_SF =results_SF.drop(columns="error").round(6)

            results_SF_val = pd.concat([results_SF,results_SF_CP.round(6).reset_index().rename(columns={"CP":"id","CP_where_energy_is_generated":"CP","SF_CP":"SF"})])
            results_SF_val = results_SF_val.loc[:,["timestamp","CP","SF"]].groupby(["timestamp","CP"]).sum().round(6)
            results_SF_val.loc[results_SF_val.SF != 1,:]
            error = 1 - results_SF_val.loc[results_SF_val.SF != 1,:]
            small_error = error.loc[error.SF<=1*10**-5,:]
            CP_ID = results_SF.groupby(["CP"]).first().reset_index().drop(columns=["timestamp","SF"])
            small_error = pd.merge(small_error.reset_index(),CP_ID,on="CP",how = "right")
            results_SF = pd.merge(small_error.rename(columns={"SF":"error"}),results_SF,on=["CP","timestamp","id"],how = "outer").fillna(0)

            results_SF["SF"] = results_SF["error"]+results_SF["SF"]

            results_SF =results_SF.drop(columns="error")

            return results_SF.set_index(["id","timestamp","CP"])

        elif self.mode == "SF":
            if CP:
                index = [i for i,x in enumerate([("SF_CP" in i.columns)==True for i in self.list_df_results]) if x]
                results_SF_CP = self.list_df_results[index[0]].reset_index()
                return results_SF_CP.set_index(["CP_where_energy_is_generated","timestamp","CP"])
            
            if hasattr(self,"freq_SF"):
                if results_SF_in is not None:
                    results_SF = results_SF_in.set_index("timestamp").reset_index()
                else:
                    index = [i for i,x in enumerate([("SF" in i.columns)==True for i in self.list_df_results]) if x]
                    results_SF = self.list_df_results[index[0]].reset_index()
                    results_SF = pd.merge(results_SF,self.timestamps,on="timestamp")
                results_SF = pd.merge(results_SF,self.clients_info[["id","i"]],on="id")
                results_SF["new_SF"] = 0.0
                #for i in freq_SF.id:
                #    print(i)
                #    freq = freq_SF.loc[freq_SF.id == i,"freq"]
                #    for t in results_SF.time_index:
                #        results_SF.iloc[(results_SF.id == i) & (results_SF.time_index == t),"new_SF"] = int((t-(t % freq))/freq)
                for i,row in results_SF.iterrows():
                    t = self.sharing_factors_disc(row.i,row.timestamp,counting=False)
                    results_SF.loc[i,"new_SF"] = results_SF.loc[(results_SF.id == row.id) & (results_SF.time_index == t),"SF"].values[0]

                return results_SF.drop(columns=["SF","time_index"]).rename(columns={"new_SF":"SF"}).set_index(["id","timestamp","CP"])
            else:
                index = [i for i,x in enumerate([("SF" in i.columns)==True for i in self.list_df_results]) if x]
                return self.list_df_results[index[0]]

    def get_energy_CP_plot(self):
        dict_value_CT = {}
        for t in self.model.T:
            dict_value_CT[t] = {}
            for k,v in self.get_energy_CP(self.instance,t).items():
                dict_value_CT[t][k] = pyo.value(v)
        energy_CP = pd.DataFrame(dict_value_CT)
        Energy_produced = pd.melt(energy_CP.reset_index(), 
                                    id_vars="index",
                                    value_vars = energy_CP.columns,
                                    var_name='time_index', 
                                    value_name='Energy_CP').rename(columns={"index":"CP"})
        Energy_produced = pd.merge(Energy_produced,self.timestamps,on="time_index").drop(columns="time_index").rename(columns={"CP":"CP_id"})
        df_CP_names = pd.DataFrame.from_dict(self.list_CP["names"], orient='index').reset_index().rename(columns={"index":"CP",0:"CP_id"})

        return pd.merge(Energy_produced,df_CP_names,on="CP_id").drop(columns="CP_id").set_index(["timestamp","CP"])



    def plot_results_sharing_factors(self,plot=False,SF_required="None"):
        SF_as_Par = self.SF_Par
        df_CP_names = pd.DataFrame.from_dict(self.list_CP["names"], orient='index').reset_index().rename(columns={"index":"CP",0:"CP_id"})
        if SF_required == "None":
            if not SF_as_Par:
                results_SF = self.get_and_adapt_sharing_factors()
                
                results_SF_CP = self.get_and_adapt_sharing_factors(CP = True)
                if (results_SF_CP.sum() > 0).any():
                    results_SF_CP = results_SF_CP.reset_index().rename(columns={"CP":"id","CP_where_energy_is_generated":"CP","SF_CP":"SF"})
                    results_SF_CP = results_SF_CP.loc[results_SF_CP.id != results_SF_CP.CP]
                    results_SF = pd.concat([results_SF,results_SF_CP.set_index(results_SF.index.names)])
                if plot:
                    results_SF = results_SF.reset_index()
                    for CP in results_SF.CP.unique():
                        results_SF.loc[results_SF.CP == CP].reset_index().pivot(index=["timestamp"], columns=["id"], values="SF").plot(title = "Sharing Factor "+CP,legend=False)
                else:
                    return results_SF
            else:
                SF = pd.melt(self.SF.reset_index(), 
                                id_vars=['time_index','CP_id'], 
                                value_vars = self.SF.columns, 
                                var_name='i', 
                                value_name='SF')
                results_SF = pd.merge(pd.merge(pd.merge(SF,self.timestamps,on="time_index"),self.clients_info[["id","i"]],on="i"),df_CP_names,on="CP_id").drop(columns=["i","time_index","CP_id"]).set_index(["CP","timestamp","id"])
                if hasattr(self,"df_Sharing_Between_CP_id"):
                    SF = pd.merge(pd.merge(pd.merge(self.df_Sharing_Between_CP_id,df_CP_names,on="CP_id").rename(columns={"CP":"id"}).drop(columns=["CP_id"])\
                                ,df_CP_names,left_on="CP_id2",right_on="CP_id").drop(columns=["CP_id2","CP_id"]),self.timestamps,on="time_index").drop(columns=["time_index"]).set_index(["CP","timestamp","id"])
                    results_SF = pd.concat([SF,results_SF])

                if plot:
                    results_SF = results_SF.reset_index()
                    for CP in results_SF.CP.unique():
                        results_SF.loc[results_SF.CP == CP].reset_index().pivot(index=["timestamp"], columns=["id"], values="SF").plot(title = "Sharing Factor "+CP,legend=False)
                else:
                    return results_SF
        elif SF_required == "CP":
            if not SF_as_Par:
                results_SF_CP = self.get_and_adapt_sharing_factors(CP = True)
                results_SF_CP = results_SF_CP.reset_index().rename(columns={"CP":"id","CP_where_energy_is_generated":"CP","SF_CP":"SF"})
                return results_SF_CP.loc[results_SF_CP.id != results_SF_CP.CP].set_index(["CP","timestamp","id"])
            else:
                if hasattr(self,"df_Sharing_Between_CP_id"):
                    return pd.merge(pd.merge(pd.merge(self.df_Sharing_Between_CP_id,df_CP_names,on="CP_id").rename(columns={"CP":"id"}).drop(columns=["CP_id"])\
                                ,df_CP_names,left_on="CP_id2",right_on="CP_id").drop(columns=["CP_id2","CP_id"]),self.timestamps,on="time_index").drop(columns=["time_index"]).set_index(["CP","timestamp","id"])
                #else:


        elif SF_required == "Consumers":
            if not SF_as_Par:
                return self.get_and_adapt_sharing_factors()
            else:
                SF = pd.melt(self.SF.reset_index(), 
                                id_vars=['time_index','CP_id'], 
                                value_vars = self.SF.columns, 
                                var_name='i', 
                                value_name='SF')
                return pd.merge(pd.merge(pd.merge(SF,self.timestamps,on="time_index"),self.clients_info[["id","i"]],on="i"),df_CP_names,on="CP_id").drop(columns=["i","time_index","CP_id"]).set_index(["CP","timestamp","id"])      

    def plot_result_CP(self,plot=False):
        SF_as_Par = self.SF_Par
        SF_CP = self.plot_results_sharing_factors(plot=False,SF_required="CP").reset_index()
        result = {k: {"value":0,"Obtained":False,"elements":{}} for k,v in self.list_CP["names"].items()}
        count = 0
        if self.PV > 0:
            solar = pd.merge(self.plot_solar_inputs(plot=False),self.PV_info,on="id_PV")
        if self.Bat > 0:
            Bat = pd.merge(self.plot_results_Bat(plot=False).reset_index(),self.Bat_info[["Bat_index","id_Bat"]],on="id_Bat")
        while True:
            count += 1
            if count > 100:
                raise Exception("Problem calculating the energy of the CP")
            elif sum([not result[CP]["Obtained"]for CP,id in self.list_CP["names"].items()])==0: 
                break
            for CP,id in self.list_CP["names"].items():
                if result[CP]["Obtained"]:
                    continue
                if "CP_uses_CP" in self.list_CP[CP].keys():
                    if sum([not result[cp_check]["Obtained"] for cp_check in [k for k,v in self.list_CP["names"].items() if v in self.list_CP[CP]["CP_uses_CP"]]]) < 0:
                        continue
                for k,i in self.list_CP[CP].items():
                    if k == "PV" and self.PV > 0:
                        if isinstance(result[CP]["value"],pd.DataFrame):
                            result[CP]["value"] = pd.merge(result[CP]["value"],pd.pivot_table(solar.loc[solar.PV_index.isin(i)],values="P",index=["timestamp"],columns="id_PV"),left_index=True,right_index=True,how = "outer")
                        else:
                            result[CP]["value"] = pd.pivot_table(solar.loc[solar.PV_index.isin(i)],values="P",index=["timestamp"],columns="id_PV")
                    elif k == "Bat" and self.Bat > 0:
                        if isinstance(result[CP]["value"],pd.DataFrame):
                            result[CP]["value"] = pd.merge(result[CP]["value"],pd.pivot_table(Bat.loc[solar.PV_index.isin(i),["PBat","timestamp","id_Bat"]],values="PBat",index=["timestamp"],columns="id_Bat")*-1,left_index=True,right_index=True,how = "outer")
                        else:
                            result[CP]["value"] = pd.pivot_table(Bat.loc[Bat.Bat_index.isin(i),["PBat","timestamp","id_Bat"]],values="PBat",index=["timestamp"],columns="id_Bat")*-1
                    elif k == "CP_uses_CP":
                        
                        if len(i)<1:
                            continue
                        else:
                            CP_used = [k for k,v in self.list_CP["names"].items() if v in i]
                            CP_uses_CP_SF = SF_CP.loc[(SF_CP.id == CP) & (SF_CP.CP.isin(CP_used))].drop(columns=["id"])
                            CP_uses_CP = pd.concat([result[CP_used_i]["value"].loc[:,["resulting"]].rename(columns ={"resulting":CP_used_i}) for CP_used_i in CP_used])
                            CP_uses_CP = pd.melt(CP_uses_CP.reset_index(), 
                                            id_vars='timestamp', 
                                            value_vars = CP_uses_CP.columns, 
                                            var_name='CP', 
                                            value_name='consumption')
                            CP_uses_CP = pd.merge(CP_uses_CP_SF,CP_uses_CP,on=["timestamp","CP"])
                            CP_uses_CP["result"] = CP_uses_CP["SF"] * CP_uses_CP["consumption"]
                            CP_uses_CP = pd.pivot_table(CP_uses_CP,values="result",index=["timestamp"],columns="CP")
                        if isinstance(result[CP]["value"],pd.DataFrame):
                            result[CP]["value"] = pd.merge(result[CP]["value"],CP_uses_CP,left_index=True,right_index=True,how = "outer")
                        else:
                            result[CP]["value"] = CP_uses_CP
                result[CP]["value"]["resulting"] = result[CP]["value"].sum(1)
                result[CP]["Obtained"]  = True
            result_CP = pd.concat([result[CP]["value"].loc[:,["resulting"]].rename(columns={"resulting":CP}) for CP in result.keys()],axis =1)
        
        results_energy_CP = pd.pivot_table(self.get_energy_CP_plot().reset_index(),values="Energy_CP",index=["timestamp"],columns="CP")
        #pd.pivot_table(self.list_df_results[index[0]].loc[:,["energy_CP"]]
        if (results_energy_CP.compare(result_CP).diff(axis=1)>1).any().any():
            raise Exception("Validation of CP not correct to the Watt")
        if plot:
            for CP in result.keys():
                result[CP]["value"].plot()
        else:
            return result_CP


    def plot_results_cost_one_consumer(self,plot=False):
        SF_as_Par = self.SF_Par
        #plot = "Comunitat"
        # should be tested
        Price = self.plot_price_inputs(plot=False)
        df_result = pd.merge(self.clients_info,Price.rename(columns={"price":"price_buy","id_price":"price"}), how="left",on=["price"])
        df_result = pd.merge(df_result,Price.rename(columns={"price":"price_s","id_price":"price_sell"}), how="left",on=["timestamp","price_sell"])
        count_timestamp = pd.merge(self.count_timestamp.reset_index(), self.timestamps, on="time_index").drop(columns="time_index")
        df_result = pd.merge(df_result,count_timestamp, how="left",on=["timestamp"])
        df_result = df_result.drop(columns=["i","price","price_sell"]).rename(columns={"price_s":"price_sell"})
        P_consumed = self.plot_consumption_inputs(plot=False)
        df_result = pd.merge(df_result,P_consumed,on=["timestamp","id"])
        df_result["Cost_consumption"] = np.where(df_result.consumption > 0, df_result.consumption*df_result.price_buy*df_result.count_timestamp, df_result.consumption*df_result.price_sell*df_result.count_timestamp)
        colums_to_plot = ["timestamp","Cost_consumption","Cost_Final_cost"]
        colums_to_plot_energy = ["timestamp","consumption","Final_Consumption"]
        result_CP = self.plot_result_CP(plot=False)
        result_CP = pd.melt(result_CP.reset_index(),
                    id_vars='timestamp', 
                    value_vars = result_CP.columns, 
                    var_name='CP', 
                    value_name='CP_production').set_index(["timestamp","CP"])*-1
        result_CP = pd.concat([self.plot_results_sharing_factors(plot=False,SF_required="Consumers").reset_index().set_index(["timestamp","CP"]),result_CP],axis =1)
        result_CP["CP_asigned"] = result_CP["SF"]*result_CP["CP_production"]
        result_CP = pd.pivot_table(result_CP.reset_index(),values="CP_asigned",index=["timestamp","id"],columns="CP")
        #result = pd.concat([result.reset_index().set_index(["timestamp","CP"]),result_CP],axis=1)
        df_result = pd.concat([df_result.set_index(["timestamp","id"]),result_CP],axis=1)
        df_result["Final_Consumption"] = df_result.loc[:,"consumption"]+df_result.loc[:,result_CP.columns].sum(1)
        df_result["Cost_Final_cost"] = np.where(df_result.Final_Consumption > 0, df_result.Final_Consumption*df_result.price_buy*df_result.count_timestamp, df_result.Final_Consumption*df_result.price_sell*df_result.count_timestamp)
        for CP in result_CP.columns:
            df_result["Final_Consumption_"+ CP] = df_result.loc[:,"consumption"]+df_result.loc[:,CP]
            df_result["Cost_Final_cost_"+CP] = np.where(df_result.loc[:,"Final_Consumption_"+ CP] > 0, df_result.loc[:,"Final_Consumption_"+ CP]*df_result.price_buy*df_result.count_timestamp, df_result.loc[:,"Final_Consumption_"+ CP]*df_result.price_sell*df_result.count_timestamp)
            colums_to_plot.append("Cost_Final_cost_"+CP) 
            colums_to_plot_energy.append("Final_Consumption_"+ CP)
        #df_result.drop(columns=["price_buy","price_sell"])
        df_check = self.plot_results_consumers(plot = False).loc[:,["P_bill"]].rename(columns = {"P_bill":"Final_Consumption"}).reset_index().set_index(["timestamp","id"])
        if (df_result.loc[:,["Final_Consumption"]].compare(df_check).diff(axis=1)>1).any().any():
            raise Exception("Validation of Consumption after sharing energy not correct to the Watt")
        # Older versons had segregated cost for Solar and Bateries. They mainly worked for one client.
        if not isinstance(plot,bool):
            df_result = df_result.reset_index()
            fig, axs = plt.subplots(3, 1)
            df_result[df_result.id == plot][colums_to_plot].set_index("timestamp").plot(title ="Puntual cost",ax = axs.flatten()[0])
            df_result[df_result.id == plot][colums_to_plot_energy].set_index("timestamp").plot(title ="Energy sources",ax = axs.flatten()[1])
            df_result[df_result.id == plot][colums_to_plot].set_index("timestamp").cumsum().plot(title ="Acumulated cost",ax = axs.flatten()[2])
        else:
            return df_result
        
    #def plot_results_cost_Bat_chargingPV_EC(self,plot=True,SF_as_Par=True):
    #    df_result = self.plot_results_cost_one_consumer(plot=False)
    #    df_result = df_result.groupby("timestamp").sum().drop(columns="id")
    #    colums_to_plot = ["timestamp","Cost_consumption","Cost_consumption_solar","Cost_consumption_Solar_Battery"]
    #    PBat = self.plot_results_Bat(plot=False)
    #    df_result = pd.merge(df_result,PBat.reset_index()[["timestamp","PBat"]],on="timestamp")
    #    df_result["Consumption_Solar_Battery"] = df_result.consumption-df_result.Solar_assignated + df_result.PBat
    #    df_result["Cost_consumption_Solar_Battery"] = np.where(df_result.Consumption_Solar_Battery > 0, df_result.Consumption_Solar_Battery*df_result.price_buy, df_result.Consumption_Solar_Battery*df_result.price_sell)
    #    if plot:
    #        df_result[colums_to_plot].set_index("timestamp").plot(title ="Puntual cost")
    #        df_result[colums_to_plot].set_index("timestamp").cumsum().plot(title ="Acumulated cost")
    #        df_result[["timestamp","consumption","Consumption_solar","Consumption_Solar_Battery"]].set_index("timestamp").plot(title ="Resulting energy")
    #        #plt.show()
    #    else:
    #        return df_result

        
    def plot_results_Bat(self,plot=True):
        P_index = [i for i,x in enumerate([("PBat_dch" in i.columns)==True for i in self.list_df_results]) if x]
        results_P = self.list_df_results[P_index[0]]
        results_P["PBat"] = results_P["PBat_ch"] - results_P["PBat_dch"]
        results_P.loc[(results_P.PBat_ch > 1) & (results_P.PBat_dch > 1),:]
        #Check for charging and discharging at the same time presition to the W
        if (results_P["PBat_dch"][results_P.PBat_ch > 1]>1).any() or (results_P["PBat_ch"][results_P.PBat_dch > 1]>1).any():
            raise Exception("Charging while discharging in W")
        if plot:
            fig, axs = plt.subplots(2, 1)
            pd.pivot_table(results_P,values="PBat",index=["timestamp"],columns="id_Bat").plot(title ="Battery Power",ax = axs.flatten()[0])
            pd.pivot_table(results_P,values="EBat",index=["timestamp"],columns="id_Bat").plot(title ="Battery Energy",ax = axs.flatten()[1])
            #plt.show()
        else:
            return results_P
        
    def plot_results_consumers(self,plot=True):
        P_index = [i for i,x in enumerate([("P_Injected_bill" in i.columns)==True for i in self.list_df_results]) if x]
        results_P = self.list_df_results[P_index[0]]
        #Check for charging and discharging at the same time presition to the W
        results_P.loc[(results_P.P_Consumed_bill > 1) & (results_P.P_Injected_bill > 1),:]
        if (results_P["P_Injected_bill"][results_P.P_Consumed_bill > 1]>1).any() or (results_P["P_Consumed_bill"][results_P.P_Injected_bill > 1]>1).any():
            raise Exception("Consuming and injecting in W")
        results_P["P_bill"] = results_P["P_Consumed_bill"] - results_P["P_Injected_bill"]
        if plot:
            pd.pivot_table(results_P,values="P_bill",index=["timestamp"],columns="id").plot(title ="Consumption after the energy sharing")
            #plt.show()
        else:
            return results_P

    def plot_results_aggregated_consumption_PV_Bat(self,plot=True,profit=False):
        SF_as_Par = self.SF_Par
        P_consumed = self.plot_consumption_inputs(plot=False)
        P_consumed = P_consumed.groupby("timestamp").sum().drop(columns=["id"])
        P_consumed["type"] = "Consumption"
        P_consumed = P_consumed.rename(columns = {"consumption":"Power"})
        aggregated_data= [P_consumed]
        if self.PV >0:
            P_PV = self.plot_solar_inputs(plot=False)
            P_PV = P_PV.groupby("timestamp").sum().drop(columns=["id_PV"])
            P_PV["type"] = "PV"
            P_PV = P_PV.rename(columns = {"P":"Power"})
            aggregated_data.append(P_PV)

        if self.Bat >0:
            PBat = self.plot_results_Bat(plot=False)
            PBat = PBat.reset_index()[["timestamp","PBat"]]
            PBat = PBat.groupby("timestamp").sum()
            PBat["type"] = "Batery"
            PBat = PBat.rename(columns = {"PBat":"Power"})
            PBat["Power"] = PBat["Power"]*-1
            aggregated_data.append(PBat)

        P_bill = self.plot_results_consumers(plot=False).reset_index()[["timestamp","P_bill"]]
        P_bill = P_bill.groupby("timestamp").sum()
        P_bill["type"] = "Billed"
        P_bill = P_bill.rename(columns = {"P_bill":"Power"})
        aggregated_data.append(P_bill)
        aggregated_data = pd.concat(aggregated_data)
        aggregated_data = pd.pivot_table(aggregated_data,values="Power",index=["timestamp"],columns="type")
        mean_price = self.plot_results_cost_one_consumer(plot = False).reset_index().loc[:,["price_buy","price_sell","timestamp"]].groupby("timestamp").mean()
        
        colums_to_plot = aggregated_data.columns
        colums_to_plot_cost = []
        aggregated_data = pd.concat([aggregated_data,mean_price],axis=1)

        for column in colums_to_plot:
            if column == "PV":
                aggregated_data["Consumption_"+ column] = aggregated_data["Consumption"]-aggregated_data[column]
                column2 = "Consumption_"+ column
            elif column == "Batery":
                aggregated_data["Consumption_"+ column] = aggregated_data["Consumption"]-aggregated_data[column]
                column2 = "Consumption_"+ column
            else:
                column2 = column
            aggregated_data["Cost_"+ column] = np.where(aggregated_data.loc[:,column2] > 0, aggregated_data.loc[:,column2]*aggregated_data.price_buy, aggregated_data.loc[:,column2]*aggregated_data.price_sell)
            colums_to_plot_cost.append("Cost_"+ column) 

        if plot:
            if profit:
                fig, axs = plt.subplots(3, 1)
                aggregated_data.loc[:,colums_to_plot].plot(title ="EC Energy Flow",ax=axs.flatten()[0])
                aggregated_data.loc[:,colums_to_plot_cost].plot(title ="EC Energy Cost",ax=axs.flatten()[1])
                aggregated_data.loc[:,colums_to_plot_cost].cumsum().plot(title ="EC Energy Cost",ax=axs.flatten()[2])
            else:
                aggregated_data.loc[:,colums_to_plot].plot(title ="EC Energy Flow")
            #plt.show()
        else:
            return aggregated_data
        
    def plot_self_consumption_rate_instantly(self,plot=True):
        P_consumed = self.plot_consumption_inputs(plot=False)
        Energy_Allocated = pd.merge(self.get_energy_CP_plot().reset_index(),self.plot_results_sharing_factors(plot=False,SF_required="None").reset_index(),on=["timestamp","CP"])
        Energy_Allocated["Energy_Allocated"] = Energy_Allocated["SF"]*Energy_Allocated["Energy_CP"]
        Energy_Allocated = pd.merge(Energy_Allocated,P_consumed,on=["timestamp","id"])
        Energy_Allocated["self_consumption_rate_instantly"] = Energy_Allocated["Energy_Allocated"]/Energy_Allocated["consumption"]
        Energy_Allocated = pd.pivot_table(Energy_Allocated,values="self_consumption_rate_instantly",index=["timestamp","id"],columns="CP")
        first = True
        for i in Energy_Allocated.columns:
            divisio = 0.1
            binsize = np.arange(-1,(2+divisio)/divisio)*divisio
            binsize = np.append(binsize, float("inf"))
            bins = pd.cut(Energy_Allocated[i], bins= binsize, labels= [float(round(i,2)) for i in binsize][1:],right=True)
            if first:
                first = False
                res_df = Energy_Allocated[[i]].groupby(bins, observed=True).agg("count")/len(Energy_Allocated)
            else:
                res_df = pd.concat([res_df, Energy_Allocated[[i]].groupby(bins, observed=True).agg("count")/len(Energy_Allocated)], axis=1)
        if plot:
            ax = res_df.plot()
            ax.vlines(x=(1/divisio),ymin=0 ,ymax =res_df.max().values[0], color='b', linestyle='--', lw=2)
        else:
            col = Energy_Allocated.columns[0]
            mean_grater0 = Energy_Allocated.loc[(Energy_Allocated.loc[:,col] > 0) & (
                        Energy_Allocated.loc[:,col] < float("inf"))].mean().values[0]
            mean = Energy_Allocated.loc[
                        Energy_Allocated.loc[:,col] < float("inf")].mean().values[0]
            return res_df, mean, mean_grater0

    def resulting_kpi(self):
        df = self.plot_results_cost_one_consumer()
        df_inv=pd.DataFrame()
        if self.PV>0:
            inv_pv_ = pd.melt(self.Inv_PV, var_name="PV_index").reset_index(names="i")
            inv_pv_ = pd.merge(inv_pv_, self.clients_info, on="i")
            inv_pv_ = pd.merge(self.PV_info, inv_pv_, on="PV_index")
            inv_pv_ = inv_pv_.loc[:, ["id_PV", "id", "value"]]
            inv_pv_["id_resource"] = "PV_" + inv_pv_["id_PV"]
            df_inv = pd.concat([df_inv,inv_pv_])
        if hasattr(self, "df_bat_curve_val"):
            print("To Implement")
            ## implement battery inversion
        df_inv = df_inv.groupby("id").sum().rename(columns={"value":"Total_Inversion"}).loc[:,["Total_Inversion"]]

        df["Surplus"] = np.where(df.Final_Consumption<0,-1*df.Final_Consumption,0 )
        df["savings"] = df["Cost_consumption"] -df["Cost_Final_cost"]
        df_summary = df.reset_index().groupby("id").sum()
        df_summary = df_summary.loc[:,["Final_Consumption","Surplus","Cost_Final_cost","Cost_consumption","savings"]].rename(columns={"Cost_Final_cost":"Final_Cost","Cost_consumption": "Original_Cost"})
        df_summary = pd.merge(df_summary, df_inv,on="id")

        number_of_points2year=len(df.reset_index().timestamp.unique()) * self.At/(24*365)
        df_summary["ROI_yearly"] = df_summary["Total_Inversion"] / (
                    df_summary["savings"] / number_of_points2year)

        return df_summary


