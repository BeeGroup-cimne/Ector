

class standard_cases:
    def Std_Batery_Optimitzation(self,
                                 df_clients,
                                 df_consumption,
                                 df_price,
                                 df_PV_curbe,
                                 df_PV_inversion,
                                 df_Bat_characteristics,
                                 df_Bat_inversion,
                                 df_Sharing):
        self.Input_clients(df_clients,df_consumption,df_price)
        self.Input_PV(df_PV_curbe,df_PV_inversion)
        self.Input_Bateries(df_Bat_characteristics,df_Bat_inversion)
        self.Input_sharing_Factors_CP(df_Sharing)
        self.get_data_ready()

        self.Declarar_parametres_basics()
        self.constrain_Battery_limits()
        self.constrain_Bat_degradation()
        self.constrain_P_Balance()
        self.constrain_cost()
        self.constrain_energy_in_CP(SF_Par = True)
        self.constrain_LP_required_charge_to_clients()

        self.Cost_Function_cost()

        a,b = self.solver('gurobi')

        results = self.pyomo_to_df()
        return self,results
    
    def Std_sharing_factors(self,
                                 df_clients,
                                 df_consumption,
                                 df_price,
                                 df_PV_curbe,
                                 df_PV_inversion):
        
        self.Input_clients(df_clients,df_consumption,df_price)
        self.Input_PV(df_PV_curbe,df_PV_inversion)

        self.Declarar_parametres_basics()
        self.constrain_P_Balance()
        self.constrain_cost()
        self.constrain_LP_required_charge_to_clients()
        self.constrain_sharing_factors()
        #self.constrain_Payback_general()

        #self.constrain_max_energy_allocated(0.4)
        #self.constrain_max_instanteneos_self_consumption(1)

        self.Cost_Function_cost()
        #self.Cost_Function_cost_selfconsumption()
        #EC.Constrains_on_the_temporal_sharing_coeficients()


        self.get_data_ready()
        a,b = self.solver('glpk')

        results = self.pyomo_to_df()

        return self,results
    
    def Std_sharing_factors_2(self,
                                 df_clients,
                                 df_consumption,
                                 df_price,
                                 df_PV_curbe,
                                 df_PV_inversion):
        
        self.Input_clients(df_clients,df_consumption,df_price)
        self.Input_PV(df_PV_curbe,df_PV_inversion)

        self.Declarar_parametres_basics()
        self.constrain_P_Balance()
        self.constrain_cost()
        self.constrain_LP_required_charge_to_clients()
        self.constrain_sharing_factors()
        #self.constrain_Payback_general()

        #self.constrain_max_energy_allocated(0.4)
        #self.constrain_max_instanteneos_self_consumption(1)

        self.Cost_Function_cost()
        #self.Cost_Function_cost_selfconsumption()
        #EC.Constrains_on_the_temporal_sharing_coeficients()


        self.get_data_ready()
        a,b = self.solver('glpk')

        results = self.pyomo_to_df()

        return self,results
    def Std_sharing_factors_cost_fix(self,
                                 df_clients,
                                 df_consumption,
                                 df_price,
                                 df_PV_curbe,
                                 df_PV_inversion,
                                 cost):
        
        self.Input_clients(df_clients,df_consumption,df_price)
        self.Input_PV(df_PV_curbe,df_PV_inversion)

        self.Declarar_parametres_basics()
        self.constrain_P_Balance()
        self.constrain_cost()
        self.constrain_fix_cost(cost)
        self.constrain_LP_required_charge_to_clients()
        self.constrain_sharing_factors()
        
        self.constrain_Payback_general()
        self.model.same_Payback_fix.deactivate()
        self.model.P_Utilized_limitation1.deactivate()
        
        self.cost_rule_mean_abs_ReturnInversion()

        self.get_data_ready()
        a,b = self.solver('glpk')

        results = self.pyomo_to_df()

        return self,results
    

    def Std_sharing_factors_Batery(self,
                                 df_clients,
                                 df_consumption,
                                 df_price,
                                 df_PV_curbe,
                                 df_PV_inversion,
                                 df_Bat_characteristics,
                                 df_Bat_inversion):
        
        self.Input_clients(df_clients.reset_index(drop=True),
                        df_consumption,
                        df_price)
        self.Input_PV(df_PV_curbe,df_PV_inversion)
        self.Input_Bateries(df_Bat_characteristics,df_Bat_inversion)


        self.Declarar_parametres_basics()
        self.constrain_P_Balance(SF_Par=False)
        self.constrain_sharing_factors()
        self.constrain_cost()
        self.constrain_Battery_limits()
        self.constrain_Bat_degradation()
        #self.constrain_energy_in_CP()
        #Falta tornar a pensar aixo
        #EC.constrain_Payback_by_element(element="Bat")#optional to fix the Payback of the Bat between all the users
        self.Constrains_on_the_temporal_sharing_coeficients()


        self.constrain_Payback_general()


        #EC.Cost_Function_cost()
        self.Cost_Function_squared_cost()
        self.get_data_ready()
        a,b = self.solver('glpk')

        # Extract data
        results = self.pyomo_to_df()

        return self,results
    
    def Std_EC_Batery_with_already_SF(self,
                                   df_clients,
                                   df_consumption,
                                   df_price,
                                   df_PV_curbe,
                                   df_PV_inversion,
                                   df_Bat_characteristics,
                                   df_Bat_inversion,
                                   df_Sharing,
                                   df_Sharing_Between_CP = None):

        self.Input_clients(df_clients.reset_index(drop=True),
                    df_consumption,
                    df_price)
        self.Input_PV(df_PV_curbe,df_PV_inversion)
        self.Input_Bateries(df_Bat_characteristics,df_Bat_inversion)
        self.Input_sharing_Factors_CP(df_Sharing,df_Sharing_Between_CP)


        self.Declarar_parametres_basics()
        self.constrain_Battery_limits()
        self.constrain_Bat_degradation()
        self.constrain_P_Balance()
        self.constrain_cost()
        self.constrain_energy_in_CP(SF_Par = True)
        self.constrain_LP_required_charge_to_clients()
        #Falta tornar a pensar aixo
        #EC.constrain_Payback_by_element(element="Bat")#optional to fix the Payback of the Bat between all the users

        self.constrain_Payback_general()

        #EC.Cost_Function_cost()
        self.Cost_Function_squared_cost()
        self.get_data_ready()
        a,b = self.solver('gurobi')

        # Extract data
        results = self.pyomo_to_df()

        return self,results