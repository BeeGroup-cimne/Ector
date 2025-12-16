from pyomo.environ import *
import pandas as pd

class Parameters:
        
    def change_period(self,new_period:float):
        """Modifies the standard input of time o one hour.

            Parameters:
                    new_period (float): New period of the optimitzation in hours.
        """
        self.At = new_period

    def Input_clients(self,df_clients,df_consumption,df_price):
        """Function to upload all the consumers information of a energy comunity.

            Parameters:
                    df_clients (pandas.Dataframe): Basic information of the consumers.
                    df_consumption (pandas.Dataframe): Timeseries of consumption or forecast
                    df_price (pandas.Dataframe): Timeseries of the price.
        """
        self.I = df_clients.id.nunique()
        self.clients_info = df_clients.reset_index().rename(columns={"index":"i"}).loc[:,["i","id","price","price_sell"]] #pd.DataFrame(data=df_clients.id.unique(),columns=["id"])
        #self.clients_info = pd.merge(clients_info,df_clients,on = "id")
        self.timestamps = pd.DataFrame(data=df_consumption.sort_values("timestamp").timestamp.unique(),columns=["timestamp"]).reset_index().rename(columns={"index":"time_index"})
        self.P_Consumed = pd.pivot_table(pd.merge(pd.merge(df_consumption,self.timestamps,on="timestamp"),self.clients_info[["i","id"]],on= "id").drop(columns=["timestamp","id"]),values="consumption",index=["time_index"],columns="i")
        self.id_price = pd.DataFrame(data=pd.concat([df_clients["price"],df_clients["price_sell"]]).unique(),columns=["id_price"]).reset_index().rename(columns={"index":"price_index"})
        self.Ecost = pd.pivot_table(pd.merge(pd.merge(df_price,self.timestamps,on="timestamp"),self.id_price,on="id_price"),values="price",index=["time_index"],columns="price_index")

        if "freq" in df_clients.columns:
            columns_freq = ["id","freq"]
            if "type_freq" in df_clients.columns:
                columns_freq.append("type_freq")
            self.freq_SF = pd.concat([df_clients.loc [:,columns_freq].set_index("id"),self.clients_info.set_index("id").loc [:,["i"]]],axis=1).reset_index(drop=True)
        if not self.id_price.price_index.isin(self.Ecost.columns).all():
            not_included_price = self.id_price.id_price[~self.id_price.price_index.isin(self.Ecost.columns)]
            raise Exception("Price {} is not in the input".format(', '.join(str(x) for x in not_included_price) ))
        elif self.Ecost.isna().any().any() : 
            na_in_price = self.id_price.id_price[self.id_price.price_index.isin(self.Ecost.columns[self.Ecost.isna().any()])]
            raise Exception("There are NaN in price {}".format(', '.join(str(x) for x in na_in_price) ))
    
        if not self.clients_info.i.isin(self.P_Consumed.columns).all():
            not_included_consumption = self.clients_info.id[~self.clients_info.i.isin(self.P_Consumed.columns)].values
            raise Exception("No consumption curbe is introduced for client {}".format(', '.join(str(x) for x in not_included_consumption) ))
        elif self.P_Consumed.isna().any().any() : 
            na_in_consumption = self.clients_info.id[self.clients_info.i.isin(self.P_Consumed.isna().any().index[self.P_Consumed.isna().any()])]
            raise Exception("There are Na in client's {} consumption".format(', '.join(str(x) for x in na_in_consumption) ))
        
        if "count_timestamp" in df_price.columns:
            self.count_timestamp = pd.merge(pd.merge(df_price,self.timestamps,on="timestamp"),self.id_price,on="id_price").drop(columns="id_price").groupby("time_index").mean().loc[:,["count_timestamp"]].astype(int)
        else:
            count_timestamp = self.timestamps.copy()
            count_timestamp["count_timestamp"] = 1
            self.count_timestamp = count_timestamp.drop(columns = "timestamp").set_index("time_index")
        # va millor aixì per importar



    def Input_PV(self,df_PV_curbe,df_PV_inversion):
        """Function to upload all the photovoltaic information of a energy comunity.

            Parameters:
                    df_PV_curbe (pandas.Dataframe): Timeseries of generation or forecast
                    df_PV_inversion (pandas.Dataframe): Basic information of the photovoltaic panels and economic aportation of each participant of the energy comunity.
        """
        self.PV = df_PV_curbe.id_PV.nunique()
        self.PV_info = pd.DataFrame(data=df_PV_curbe.id_PV.unique(),columns=["id_PV"]).reset_index().rename(columns={"index":"PV_index"})        
        self.P_PV = pd.pivot_table(pd.merge(pd.merge(df_PV_curbe,self.PV_info,on="id_PV"),self.timestamps,on="timestamp").drop(columns=["id_PV","timestamp"]),values="P",index=["time_index"],columns="PV_index")
        self.Inv_PV = pd.pivot_table(pd.merge(pd.merge(df_PV_inversion,self.PV_info,on="id_PV"),self.clients_info[["i","id"]],on= "id").drop(columns=["id_PV","id"]),values="Inversion",index=["i"],columns="PV_index")
        
        self.create_CP(self.Inv_PV.reset_index(),pd.merge(df_PV_inversion.loc[:,df_PV_inversion.columns.isin(["id_PV","CP","CP_uses_CP"])],self.PV_info[["PV_index","id_PV"]],on= "id_PV"),type_info= "PV")

        if self.P_PV.isna().any().any():
            na_in_PV = self.PV_info.id_PV[self.PV_info.PV_index.isin(self.P_PV.isna().index[self.P_PV.isna().any()])]
            raise Exception("There are NaN in PV curbe {}".format(', '.join(str(x) for x in na_in_PV)))

        if self.Inv_PV.isna().any().any():
            na_in_invPV = self.PV_info.id_PV[self.PV_info.PV_index.isin(self.Inv_PV.isna().index[self.Inv_PV.isna().any()])]
            raise Exception("There are NaN in PV Inversion {}".format(', '.join(str(x) for x in na_in_invPV) ))



    def Input_Bateries(self,df_Bat_characteristics,df_Bat_inversion):
        """Function to upload all the battery information of a energy comunity.

            Parameters:
                    df_Bat_characteristics (pandas.Dataframe): Basic information of the Batery
                    df_Bat_inversion (pandas.Dataframe): Economic aportation of each participant of the energy comunity.
        """
        self.Bat = df_Bat_characteristics.id_Bat.nunique()
        self.Bat_info = df_Bat_characteristics.drop("CP", axis=1).reset_index().rename(columns={"index":"Bat_index"})  
        self.Inv_Bat = pd.pivot_table(pd.merge(pd.merge(df_Bat_inversion,self.Bat_info,on="id_Bat"),self.clients_info[["i","id"]],on= "id").drop(columns=["id_Bat","id"]),values="Inversion",index=["i"],columns="Bat_index")
        
        self.create_CP(self.Inv_Bat,pd.merge(df_Bat_characteristics.loc[:,df_Bat_characteristics.columns.isin(["id_Bat","CP","CP_uses_CP"])],self.Bat_info[["Bat_index","id_Bat"]],on= "id_Bat"),type_info= "Bat")

        if not "EBat_end" in self.Bat_info.keys():
            self.Bat_info["EBat_end"] = self.Bat_info["EBat_0"]

        if self.Inv_Bat.isna().any().any():
            na_in_invInv_Bat = self.Bat_info.id_Bat[self.Bat_info.Bat_index.isin(self.Inv_Bat.isna().index[self.Inv_Bat.isna().any()])]
            raise Exception("There are NaN in Battery Inversion {}".format(', '.join(str(x) for x in na_in_invInv_Bat) ))


    def Input_sharing_Factors_CP(self,df_Sharing,df_Sharing_Between_CP = None):
        """Function to upload all the sharing factors of a energy comunity, for the structures where this information is defines a priori.

            Parameters:
                    df_Sharing (pandas.Dataframe): Sharing factor of each conection point where the energy sources are conected to the different users.
                    df_Sharing_Between_CP (pandas.Dataframe): Sharing factor of each conection point where the energy sources are conected to other conection points with other energy resources.
        """
        df_CP_names = pd.DataFrame.from_dict(self.list_CP["names"], orient='index').reset_index().rename(columns={"index":"CP",0:"CP_id"})
        #pd.merge(pd.merge(df_Sharing,df_CP_names,on="CP"),self.timestamps,on="timestamp").drop(columns=["CP","timestamp"]).rename(columns={"CP_id":"CP"}),values="SF",index=["Bat_index","time_index"],columns="i"
        self.SF = pd.pivot_table(pd.merge(pd.merge(pd.merge(df_Sharing,df_CP_names,on="CP"),self.clients_info[["i","id"]],on= "id"),self.timestamps,on="timestamp").drop(columns=["CP","id","timestamp"]),values="SF",index=["CP_id","time_index"],columns="i")
        
        if self.SF.isna().any().any():
            na_in_CP = df_CP_names.CP[df_CP_names.CP_id.isin(self.SF.isna().any().index[self.SF.isna().any()])]
            raise Exception("There are NaN in {} Sharing Factors ".format(', '.join(str(x) for x in na_in_CP) ))
        
        elif len(self.SF.index)!= len(df_CP_names)*len(self.timestamps):
            if len(df_Sharing.CP.unique()) != len(df_CP_names):
                not_found_CP = [CP for CP in df_CP_names.CP if not CP in df_Sharing.CP.unique()]
                raise Exception("The Sharing Factors for CP {} weren't introduced".format(', '.join(str(x) for x in not_found_CP)))
            else:
                not_CP_full_length = []
                for CP in df_CP_names.CP_id:
                    if len(self.SF.reset_index()[self.SF.reset_index()["CP_id"] == CP]) != len(self.timestamps):
                        not_CP_full_length.append(CP)
                raise Exception("The not all the points in time Sharing Factors for CP {} were introduced".format(', '.join(str(x) for x in df_CP_names.set_index("CP_id").CP[not_CP_full_length])))

        if isinstance(df_Sharing_Between_CP, pd.DataFrame):
            self.df_Sharing_Between_CP_id = pd.merge(pd.merge(pd.merge(df_Sharing_Between_CP,df_CP_names,on="CP"),df_CP_names.rename(columns={"CP_id":"CP_id2","CP":"CP2"}),left_on="CP_where_energy_is_generated",right_on="CP2"),self.timestamps,on="timestamp").drop(columns=["CP","CP2","timestamp","CP_where_energy_is_generated"])
            SF_check = pd.merge(pd.pivot_table(self.df_Sharing_Between_CP_id.rename(columns={"CP_id":"i","CP_id2":"CP_id"}),values="SF",index=["CP_id","time_index"],columns="i"),self.SF,left_index=True, right_index=True,how="outer").fillna(0)
        elif len(df_CP_names)==1:
            self.df_Sharing_Between_CP_id = self.timestamps.loc[:,["time_index"]]
            self.df_Sharing_Between_CP_id["CP_id"] = 0
            self.df_Sharing_Between_CP_id["CP_id2"] = 0
            self.df_Sharing_Between_CP_id["SF"] = 0
            SF_check = pd.merge(pd.pivot_table(self.df_Sharing_Between_CP_id.rename(columns={"CP_id":"i","CP_id2":"CP_id"}),values="SF",index=["CP_id","time_index"],columns="i"),self.SF,left_index=True, right_index=True,how="outer").fillna(0)
        else:
            SF_check = self.SF

        if (SF_check.sum(1)!=1).any():# falta implementar
            SH_CP_not1 = pd.merge(pd.merge(pd.DataFrame(SF_check.sum(1)[(SF_check.sum(1)!=1)]).reset_index(),self.timestamps,on="time_index"),df_CP_names,on="CP_id")
            ErrorText = ""
            for index,i in SH_CP_not1.iterrows():
                ErrorText += "There Sharing Factors of CP {} doesn't add up to 1 in timestamp {} \n ".format(i["CP"],i["timestamp"])
            raise Exception(ErrorText)
        elif (SF_check!=SF_check.round(4)).any().any():
            SH_time_dec = pd.merge(pd.merge(pd.DataFrame(SF_check[((SF_check!=SF_check.round(4))).any(axis=1)]).reset_index(),self.timestamps,on="time_index"),df_CP_names,on="CP_id")
            ErrorText = ""
            for index,i in SH_time_dec.iterrows():
                ErrorText += "The format of Sharing Factors of Battery {} in timestamp {} doesn't fit Spanish regulation \n ".format(i["CP"],i["timestamp"])
            raise Exception(ErrorText)


    def create_CP(self,Inv,element_CP,type_info:str= "PV"):
        """Creates the input structure of the energy community for the energy resource type desired

            Parameters:
                    Inv (pandas.Dataframe): Economic aportation of each participant of the energy comunity, and therefore information of the clients that use that energy resource.
                    element_CP (pandas.Dataframe): Information of the location of each energy resource and dependace between conection points.
                    type_info (str): PV or Bat to indicate which element is beeing included.
        """
        #type_info= "Bat"
        #Inv = self.Inv_PV.reset_index()
        #Inv = self.Inv_Bat
        #element_CP = pd.merge(df_PV_inversion.loc[:,df_PV_inversion.columns.isin(["id_PV","CP","CP_uses_CP"])],self.PV_info[["PV_index","id_PV"]],on= "id_PV")
        #element_CP = pd.merge(df_Bat_characteristics.loc[:,df_Bat_characteristics.columns.isin(["id_Bat","CP","CP_uses_CP"])],self.Bat_info[["Bat_index","id_Bat"]],on= "id_Bat")
        for new_cp in pd.unique(element_CP.CP):
            if not new_cp in self.list_CP.keys():
                self.list_CP[new_cp]={"Bat":[],"PV":[],"I":[],"CP_uses_CP":[]}
                if len(self.list_CP["names"]) == 0:
                    self.list_CP["names"][new_cp] = 0
                else:
                    self.list_CP["names"][new_cp] = max([v for k,v in self.list_CP["names"].items()])+1
                if "CP_uses_CP" in element_CP.columns:
                    if not element_CP.loc[element_CP.CP == new_cp]["CP_uses_CP"].empty:
                        CP_uses_CP=[self.list_CP["names"][i] for i in element_CP.CP_uses_CP.loc[element_CP.CP == new_cp].to_list()[0]]
                        self.list_CP[new_cp]["CP_uses_CP"] = CP_uses_CP
        for i,element in element_CP.reset_index().iterrows():
            if not element[type_info+"_index"] in self.list_CP[element["CP"]][type_info]:
                self.list_CP[element["CP"]][type_info].append(element[type_info+"_index"])
        for i,consumer in Inv.reset_index().iterrows():
            for cp,item in self.list_CP.items():
                if cp != "names":
                    for element in item[type_info]:
                        if consumer[element] != 0:
                            if not int(consumer.i) in self.list_CP[cp]["I"]:
                                self.list_CP[cp]["I"].append(int(consumer.i))
        self.CP = len(self.list_CP["names"])

       

            

    def Declarar_parametres_basics(self):
        """Declaration of the basic parameters used in the optimitzation."""
        self.get_data_ready()
        self.model = ConcreteModel()#AbstractModel()
        # Define sets
        self.model.T = RangeSet(0,len(self.timestamps)-1)
        self.model.I = RangeSet(0,self.I-1)
        self.model.CP = RangeSet(0,self.CP-1)
        self.model.At = Param(default = 1)
        #if hasattr(self,"freq_SF"):
        #    self.Define_parameters_variables("freq" ,Var_or_Par="Par")
            #self.model.freq = Param(self.model.I,initialize=self.freq_SF.set_index("i").to_dict()["freq"],default=self.freq_SF.set_index("i").to_dict()["freq"])
        #else:
        #    self.model.freq = Param(self.model.I,default=1)


        new_Par =["T","I","At","CP"]
        if self.Bat > 0:
            self.model.Bat = RangeSet(0,self.Bat-1)
            new_Par.append("Bat")
        if self.PV > 0:
            self.model.PV = RangeSet(0,self.PV-1)
            new_Par.append("PV")
        for i in new_Par:
            self.Parameters.append(i)

    
    def Define_parameters_variables(self,name:str ,Var_or_Par:str="Var",domain:str="NonNegativeReals",bound = None,initialize=1):
        """Declaration of the variables and parameters used in the optimitzation.

            Parameters:
                    name (str): Name of the parameter or variable.
                    Var_or_Par (str): Var or Par if it's a variable or a parameter
                    is_NonNegativeReals (bool): if True is a NonNegativeReals if False it's a Real
        """
        self.list_dependence_Params_and_Variables={
            "P_Consumed":["I","T"],
            "Ecost":["I","T"],
            "Ecost_sell":["I","T"],
            "P_PV":["T","PV"],
            "SF":["I","T","CP"],
            "Inv_PV":["I","PV"],
            "EBat_max":["Bat"],
            "EBat_min":["Bat"],
            "PBat_max":["Bat"],
            "Inv_Bat":["I","Bat"],
            "EBat_0":["Bat"],
            "EBat_end":["Bat"],
            "nmax":["Bat"],
            "Cost":["I"],
            "P_Consumed_bill":["I","T"],
            "P_Injected_bill":["I","T"],
            "PBat_ch":["T","Bat"],
            "PBat_dch":["T","Bat"],
            "EBat":["T","Bat"],
            "Payback_CTE_PV":["PV"],
            "Payback_CTE_Bat":["Bat"],
            "Payback_PV":["I","PV"],
            "Payback_Bat":["I","Bat"],
            "Payback":["I"],
            "I_uses_CP":["I","CP"],
            "is_PV_in_CP":["PV","CP"],
            "is_Bat_in_CP":["Bat","CP"],
            "energy_CP":["T","CP"],
            "energy_CP_consumed":["T","CP"],
            "energy_CP_injected":["T","CP"],
            "CP_uses_CP":["CP","CP"],
            "SF_CP":["T","CP","CP"],
            "E_shared_CP":["T","CP","CP"],
            "E_shared":["I","T","CP"],
            "freq":["I"],
            "mean_self_consumption":[],
            "Charge":["T","Bat"],
            "Bat_operation":["T","Bat"],
            "mean_abs_ReturnInversion":["I"],
            "count_timestamp":["T"]
        }
        if Var_or_Par == "Par":
            setattr(self.model,name,Param(*[getattr(self.model,i) for i in self.list_dependence_Params_and_Variables[name]],default=self.data[None][name]))
            self.Parameters.append(name)
        elif Var_or_Par == "Var":
            if domain == "NonNegativeReals":
                setattr(self.model,name,Var(*[getattr(self.model,i) for i in self.list_dependence_Params_and_Variables[name]],domain=NonNegativeReals,initialize=initialize,bounds = bound))
            elif domain == "Real":
                setattr(self.model,name,Var(*[getattr(self.model,i) for i in self.list_dependence_Params_and_Variables[name]],domain=Reals,initialize=initialize,bounds = bound))
            elif domain == "Binary":
                setattr(self.model,name,Var(*[getattr(self.model,i) for i in self.list_dependence_Params_and_Variables[name]],domain=Binary,initialize=initialize,bounds = bound))
            elif domain == "Integers":
                setattr(self.model,name,Var(*[getattr(self.model,i) for i in self.list_dependence_Params_and_Variables[name]],domain=Integers,initialize=initialize,bounds = bound))
            self.Variables.append(name)
        else:
            raise Exception("No Var or Par")

    def search_and_add_Par_Var(self,Parameters,Variables):
        """For a list of Parameters and Variables cheks if they already exist and if not it includes them
        
            Parameters:
                    Parameters (list of str): Names of the parameters to check and add.
                    Var_or_Par (list of str): Names of the Variables to check and add.
        """
        Variables = list(set(Variables) - set(Variables).intersection(set(self.Parameters)))
        Parameters = list(set(Parameters) - set(Parameters).intersection(set(self.Variables)))
        for Param_name in set(Parameters) - set(self.Parameters):
            self.Define_parameters_variables(Param_name,"Par")

        for Var_name in set(Variables) - set(self.Variables):
            self.Define_parameters_variables(Var_name,"Var")
