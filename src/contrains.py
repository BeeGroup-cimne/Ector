from pyomo.environ import *
import pandas as pd

class constrains:
    def sharing_factors_disc(self,i,t,counting=False):
        """Returns the time index for the sharing factors depending on the frequency defined for each consumer."""
        if not hasattr(self,"freq_SF"):
            return t
        row = self.freq_SF[self.freq_SF["i"]==i]
        if counting:
            t=len(self.timestamps)-1
        if row.empty:
            return t
        elif "type_freq" not in row.columns or row.type_freq.values[0]=="contiguous":
            return int(((t-(t % row.freq))/row.freq).iloc[0])
        elif row.type_freq.values[0]=="Daily":
            return int(((t%(24/self.At) - (t%(24/self.At)% row.freq))/row.freq).iloc[0])#int(t % (24/self.At))
        elif row.type_freq.values[0]=="WeekdayDaily":
            if t > (24/self.At)*5:
                return int((((t%(24/self.At) - (t%(24/self.At)% row.freq))/row.freq)+((24/self.At-((24/self.At)%row.freq)+row.freq)/row.freq)).iloc[0])#int(t % (24/self.At))+(24/self.At)
            else:
                return int(((t%(24/self.At) - (t%(24/self.At)% row.freq))/row.freq).iloc[0])#int(t % (24/self.At))

    def constrain_sharing_factors(self): 
        """Builds the coinstrain to make the summatory of all sharing factors to one,Sharing_Factors."""
        if self.mode == "Eallocation":
            Parameters =["I","T","CP","I_uses_CP","CP_uses_CP"] 
            Variables = ["E_shared","E_shared_CP"]
            def Solar_energy_shared(model,t,cp):          
                if self.PV > 0 and self.Bat == 0:
                    Parameters.append("PV")
                    Parameters.append("is_PV_in_CP")
                    Parameters.append("P_PV")
                    self.search_and_add_Par_Var(Parameters,Variables)
                    return sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)\
                        + sum(model.CP_uses_CP[cp,cp2]*model.E_shared_CP[t,cp,cp2] for cp2 in model.CP if cp2 != cp) \
                        ==  \
                        sum(model.I_uses_CP[i,cp]*model.E_shared[i,t,cp] for i in model.I)\
                        + sum(model.CP_uses_CP[cp2,cp]*model.E_shared_CP[t,cp2,cp] for cp2 in model.CP if cp2 != cp)
                
                elif self.PV == 0 and self.Bat > 0:
                    Parameters.append("Bat")
                    Parameters.append("is_Bat_in_CP")
                    Variables.append("PBat_ch")
                    Variables.append("PBat_dch")
                    self.search_and_add_Par_Var(Parameters,Variables)
                    return sum(model.CP_uses_CP[cp,cp2]*model.E_shared_CP[t,cp,cp2] for cp2 in model.CP if cp2 != cp)\
                        + sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat) \
                        - sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat)\
                        ==  \
                        sum(model.I_uses_CP[i,cp]*model.E_shared[i,t,cp] for i in model.I)\
                        + sum(model.CP_uses_CP[cp2,cp]*model.E_shared_CP[t,cp2,cp] for cp2 in model.CP if cp2 != cp) # if cp2 != cp2#invertit Cp2 i Cp, perque aquí busquem a quins CP2 injecta cp
            
                elif self.PV > 0 and self.Bat > 0:
                    Parameters.append("Bat")
                    Parameters.append("is_Bat_in_CP")
                    Variables.append("PBat_ch")
                    Variables.append("PBat_dch")
                    Parameters.append("PV")
                    Parameters.append("is_PV_in_CP")
                    Parameters.append("P_PV")
                    self.search_and_add_Par_Var(Parameters,Variables)
                    return sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)\
                        + sum(model.CP_uses_CP[cp,cp2]*model.E_shared_CP[t,cp,cp2] for cp2 in model.CP if cp2 != cp)\
                        + sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat) \
                        - sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat)\
                        ==  \
                        sum(model.I_uses_CP[i,cp]*model.E_shared[i,t,cp] for i in model.I)\
                        + sum(model.CP_uses_CP[cp2,cp]*model.E_shared_CP[t,cp2,cp] for cp2 in model.CP if cp2 != cp) 
                        # Solar + E_imported + P_bat_discharge - P_bat_charge  = E_shared + E_Exported

                        # if cp2 != cp2#invertit Cp2 i Cp, perque aquí busquem a quins CP2 injecta cp
            self.model.Solar_energy_shared = Constraint(self.model.T,self.model.CP,rule=Solar_energy_shared)
        elif self.mode == "SF":
            Parameters =["I","T","CP","I_uses_CP","CP_uses_CP"] 
            Variables = ["SF","SF_CP"]
            self.search_and_add_Par_Var(Parameters,Variables)
            def Sharing_Factors(model,t,cp):
                return 1 ==  sum(model.I_uses_CP[i,cp]*model.SF[i,self.sharing_factors_disc(i,t),cp] for i in model.I) + sum(model.CP_uses_CP[cp2,cp]*model.SF_CP[t,cp2,cp] for cp2 in model.CP if cp2 != cp) # if cp2 != cp2#invertit Cp2 i Cp, perque aquí busquem a quins CP2 injecta cp
            self.model.Sharing_Factors = Constraint(self.model.T,self.model.CP,rule=Sharing_Factors)
            #LIMITING REDUNDANT CONSTRAINS      
            for CP in self.model.CP:
                deactivated = []
                for t in self.model.T:
                    if t in deactivated:
                        continue
                    for tt in self.model.T:
                        if tt > t and tt not in deactivated:
                            if self.model.Sharing_Factors[(t,CP)].expr.to_string() == self.model.Sharing_Factors[(tt,CP)].expr.to_string():
                                self.model.Sharing_Factors[(tt,CP)].deactivate()
                                deactivated.append(tt)

            
    def constrain_max_energy_allocated(self,percentage):
        if self.mode == "Eallocation":
            Parameters =["I","T","CP","I_uses_CP","CP_uses_CP"] 
            Variables = ["E_shared","E_shared_CP"]
            if self.Bat>0:
                Parameters.append("Bat")
                Parameters.append("is_Bat_in_CP")
                Variables.append("PBat_ch")
                Variables.append("PBat_dch")
            if self.PV>0:
                Parameters.append("PV")
                Parameters.append("is_PV_in_CP")
                Parameters.append("P_PV")
            self.search_and_add_Par_Var(Parameters,Variables)
            def Solar_energy_shared2(model,i,t,cp): 
                aux = 0
                if self.PV > 0:
                    aux = aux + sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)
                if self.Bat > 0:
                    aux = aux + sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat) \
                    - sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat)
                return (aux\
                    + sum(model.CP_uses_CP[cp,cp2]*model.E_shared_CP[t,cp,cp2] for cp2 in model.CP if cp2 != cp))\
                    >=  \
                    (model.I_uses_CP[i,cp]*model.E_shared[i,t,cp] )/percentage
                #return (sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)\
                #    + sum(model.CP_uses_CP[cp,cp2]*model.E_shared_CP[t,cp,cp2] for cp2 in model.CP if cp2 != cp)\
                #    + sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat) \
                #    - sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat))\
                #    >=  \
                #    (model.I_uses_CP[i,cp]*model.E_shared[i,t,cp] )/percentage
                #    # Solar + E_imported + P_bat_discharge - P_bat_charge  = E_shared + E_Exported
                #
                #        # if cp2 != cp2#invertit Cp2 i Cp, perque aquí busquem a quins CP2 injecta
        elif self.mode == "SF":
            def Solar_energy_shared2(model,i,t,cp): 
                return percentage>= model.SF[i,self.sharing_factors_disc(i,t),cp]
        self.model.Solar_energy_shared2 = Constraint(self.model.I,self.model.T,self.model.CP,rule=Solar_energy_shared2)

    
    def constrain_max_instanteneos_self_consumption(self,percentage):
        if self.mode == "Eallocation":  
            Parameters =["I","T","CP","P_Consumed"] 
            Variables = ["E_shared"]
            self.search_and_add_Par_Var(Parameters,Variables)
            def max_instanteneos_self_consumption(model,i,t): 
                return percentage >= (sum(model.E_shared[i,t,cp] for cp in model.CP))/(model.P_Consumed[i,t]+10**-3)
                    # Solar + E_imported + P_bat_discharge - P_bat_charge  = E_shared + E_Exported

                        # if cp2 != cp2#invertit Cp2 i Cp, perque aquí busquem a quins CP2 injecta
            self.model.max_instanteneos_self_consumption = Constraint(self.model.I,self.model.T,rule=max_instanteneos_self_consumption)
        elif self.mode == "SF":
            Parameters =["I","T","CP","P_Consumed","I_uses_CP"] 
            Variables = []
            Parameters.append("CP_uses_CP")
            if self.SF_Par:
                Parameters.append("SF")
                Parameters.append("SF_CP")
            else:
                Variables.append("SF")
                Variables.append("SF_CP")
                
            if self.Bat > 0:
                Parameters.append("Bat")
                Parameters.append("is_Bat_in_CP")
                Variables.append("PBat_ch")
                Variables.append("PBat_dch")
            if self.PV > 0:
                Parameters.append("PV")
                Parameters.append("is_PV_in_CP")
                Parameters.append("P_PV")
            self.search_and_add_Par_Var(Parameters,Variables)
            def max_instanteneos_self_consumption(model,i,t): 
                energy_CP = self.get_energy_CP(model,t)
                return percentage >= (sum(model.I_uses_CP[i,cp]*model.SF[i,self.sharing_factors_disc(i,t),cp]*energy_CP[cp] for cp in model.CP))/ (model.P_Consumed[i,t]+10**-3)
                    # Solar + E_imported + P_bat_discharge - P_bat_charge  = E_shared + E_Exported

                        # if cp2 != cp2#invertit Cp2 i Cp, perque aquí busquem a quins CP2 injecta
            self.model.max_instanteneos_self_consumption = Constraint(self.model.I,self.model.T,rule=max_instanteneos_self_consumption)
    
    def constrain_def_instanteneos_self_consumption(self):
        if self.mode == "Eallocation":  
            Parameters =["I","T","CP","P_Consumed"] 
            Variables = ["E_shared","mean_self_consumption"]
            self.search_and_add_Par_Var(Parameters,Variables)
            def def_instanteneos_self_consumption(model): 
                return model.mean_self_consumption == sum(sum(sum(model.E_shared[i,t,cp] for cp in model.CP)/(model.P_Consumed[i,t]+10**-3)for t in model.T)/len(model.T)for i in model.I)/len(model.I)
            self.model.def_instanteneos_self_consumption = Constraint(rule=def_instanteneos_self_consumption) 
        elif self.mode == "SF":
            Parameters =["I","T","CP","P_Consumed","I_uses_CP"] 
            Variables = ["SF","mean_self_consumption"]
            Parameters.append("CP_uses_CP")
            if self.SF_Par:
                Parameters.append("SF")
                Parameters.append("SF_CP")
            else:
                Variables.append("SF")
                Variables.append("SF_CP")
                
            if self.Bat > 0:
                Parameters.append("Bat")
                Parameters.append("is_Bat_in_CP")
                Variables.append("PBat_ch")
                Variables.append("PBat_dch")
            if self.PV > 0:
                Parameters.append("PV")
                Parameters.append("is_PV_in_CP")
                Parameters.append("P_PV")
            self.search_and_add_Par_Var(Parameters,Variables)
            def def_instanteneos_self_consumption(model): 
                energy_CP = {}
                for t in model.T:
                    energy_CP[t] = self.get_energy_CP(model,t)
                return model.mean_self_consumption == sum(sum(sum(model.I_uses_CP[i,cp]*model.SF[i,self.sharing_factors_disc(i,t),cp]*energy_CP[t][cp] for cp in model.CP)/\
                                     (model.P_Consumed[i,t]+10**-3)for t in model.T)/len(model.T)for i in model.I)/len(model.I)
            self.model.def_instanteneos_self_consumption = Constraint(rule=def_instanteneos_self_consumption) 


    
    def fix_Var_required(self,instance):
        """Fixes the Varianbles that are not required to change to a default value. 
            Specificly fixes the sharing factors that are not required to 0.
        
            Parameters:
                    instance (pyomo.instance): instance being build.
        """
        if "SF" in self.Variables and self.I <= 1:
            for cp,cp_internal in self.list_CP["names"].items():
                for i in self.model.I:
                    if not i in self.list_CP[cp]["I"]:
                        for t in self.model.T:
                            instance.SF[i,t,cp].fix(0)
            for cp in self.model.CP:
                for i in self.model.I:
                    max_SF_t = self.sharing_factors_disc(i,0,counting=True)
                    for t in self.model.T:
                        if t > max_SF_t:
                            self.model.SF[i,t,cp].fix(0)
        if "SF_CP" in self.Variables and self.CP <= 1:
            for cp,cp_internal in self.list_CP["names"].items():
                for cp2 in self.model.CP:
                    if not cp2 in self.list_CP[cp]["CP_uses_CP"]:
                        for t in self.model.T:
                            #print(t,cp2,cp_internal)
                            instance.SF_CP[t,cp_internal,cp2].fix(0)
        if "E_shared" in self.Variables and self.I <= 1:
            for cp,cp_internal in self.list_CP["names"].items():
                for cp2 in self.model.CP:
                    if not cp2 in self.list_CP[cp]["I"]:
                        for t in self.model.T:
                            print(t,cp2,cp_internal)
                            instance.E_shared[t,cp_internal,cp2].fix(0)
        if "E_shared_CP" in self.Variables and self.CP <= 1:
            for cp,cp_internal in self.list_CP["names"].items():
                for cp2 in self.model.CP:
                    if not cp2 in self.list_CP[cp]["CP_uses_CP"]:
                        for t in self.model.T:
                            #print(t,cp2,cp_internal)
                            instance.E_shared_CP[t,cp_internal,cp2].fix(0)
        return instance
###### PENDENT D'eliminar
    #def get_energy_for_consumer(self,model,t):
    #    executed = []
    #    energy_CP = {}
    #    data_matrix_CP = self.create_CP_matrix()["CP_uses_CP"]
#
    #    for iter in range(5):
    #        execute = []
    #        for CP in self.model.CP:
    #            if CP in executed:
    #                break
    #            if 0 == sum(data_matrix_CP[CP,CP2] for CP2 in self.model.CP):
    #                execute.append(CP)
    #                for CP2 in self.model.CP:
    #                    data_matrix_CP[CP2,CP] = 0
    #        for cp in execute:
    #            for i in model.I:
    #                energy_CP[i,cp] = 0
    #                if self.PV > 0 and self.Bat == 0:
    #                    energy_CP[i,cp] = sum(model.I_uses_CP[i,cp]*model.Solar_shared[i,int((t-(t % model.freq[i]))/model.freq[i]),cp] for pv in model.PV) #invertit Cp2 i Cp, perque aquí busquem de quins CP2 consumeix cp 
#
    #                elif self.PV == 0 and self.Bat > 0:
    #                    energy_CP[i,cp] = sum(model.I_uses_CP[i,cp]*model.PBat_dch[i,int((t-(t % model.freq[i]))/model.freq[i]),cp]  for bat in model.Bat)
    #                                    
    #                elif self.PV > 0 and self.Bat > 0:
    #                    energy_CP[cp] = sum(model.I_uses_CP[i,cp]*model.Solar_shared[i,int((t-(t % model.freq[i]))/model.freq[i]),cp] for pv in model.PV) \
    #                                    +  sum(model.I_uses_CP[i,cp]*model.PBat_dch[i,int((t-(t % model.freq[i]))/model.freq[i]),cp] for bat in model.Bat)\
    #                                    - sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat)\
    #                                    + sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat)\
    #                                    + sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)\
    #                                    + sum(model.CP_uses_CP[cp,cp2]*model.SF_CP[t,cp,cp2]*model.energy_CP[cp2] for cp2 in model.CP if cp2 != cp)
    #            #print(energy_CP[cp])
    #    return energy_CP
    

    def get_energy_CP(self,model,t):
        executed = []
        energy_CP = {}
        data_matrix_CP = self.create_CP_matrix()["CP_uses_CP"]

        for i in range(5):
            execute = []
            for CP in self.model.CP:
                if CP in executed:
                    break
                if 0 == sum(data_matrix_CP[CP,CP2] for CP2 in self.model.CP):
                    execute.append(CP)
                    for CP2 in self.model.CP:
                        data_matrix_CP[CP2,CP] = 0
            for cp in execute:
                energy_CP[cp] = 0
                if self.PV > 0 and self.Bat == 0:
                    energy_CP[cp] = sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)\
                                    + sum(model.CP_uses_CP[cp,cp2]*energy_CP[cp2] for cp2 in model.CP if (cp2 != cp and model.CP_uses_CP[cp,cp2] ==1)) #invertit Cp2 i Cp, perque aquí busquem de quins CP2 consumeix cp 
                elif self.PV == 0 and self.Bat > 0:
                    energy_CP[cp] = -sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat)\
                                    + sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat)\
                                    + sum(model.CP_uses_CP[cp,cp2]*energy_CP[cp2] for cp2 in model.CP if (cp2 != cp and model.CP_uses_CP[cp,cp2] ==1))
                elif self.PV > 0 and self.Bat > 0:
                    energy_CP[cp] = -sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat)\
                                    + sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat)\
                                    + sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)\
                                    + sum(model.CP_uses_CP[cp,cp2]*energy_CP[cp2] for cp2 in model.CP if (cp2 != cp and model.CP_uses_CP[cp,cp2] ==1))
                #print(energy_CP[cp])
        return energy_CP

    def get_energy_CP_consumed(self,model,t):
        executed = []
        energy_CP_consumed = {}
        data_matrix_CP = self.create_CP_matrix()["CP_uses_CP"]

        for i in range(5):
            execute = []
            for CP in self.model.CP:
                if CP in executed:
                    break
                if 0 == sum(data_matrix_CP[CP,CP2] for CP2 in self.model.CP):
                    execute.append(CP)
                    for CP2 in self.model.CP:
                        data_matrix_CP[CP2,CP] = 0
            for cp in execute:
                energy_CP_consumed[cp] = 0
                if self.PV > 0 and self.Bat == 0:
                    energy_CP_consumed[cp] = 0
                elif self.PV == 0 and self.Bat > 0:
                    energy_CP_consumed[cp] == sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat)
                elif self.PV > 0 and self.Bat > 0:
                    energy_CP_consumed[cp] = sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat)
            #print(energy_CP[cp])
        return energy_CP_consumed
    
    def get_energy_CP_injected(self,model,t):
        executed = []
        energy_CP_injected = {}
        data_matrix_CP = self.create_CP_matrix()["CP_uses_CP"]
        energy_CP = self.get_energy_CP(model,t)

        for i in range(5):
            execute = []
            for CP in self.model.CP:
                if CP in executed:
                    break
                if 0 == sum(data_matrix_CP[CP,CP2] for CP2 in self.model.CP):
                    execute.append(CP)
                    for CP2 in self.model.CP:
                        data_matrix_CP[CP2,CP] = 0
            for cp in execute:
                energy_CP_injected[cp] = 0
                if self.PV > 0 and self.Bat == 0:
                    energy_CP_injected[cp] = sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)\
                                + sum(model.CP_uses_CP[cp,cp2]*model.SF_CP[t,cp,cp2]*energy_CP[cp2] for cp2 in model.CP if (cp2 != cp and model.CP_uses_CP[cp,cp2] ==1)) 
                elif self.PV == 0 and self.Bat > 0:
                    energy_CP_injected[cp] = sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat)\
                                + sum(model.CP_uses_CP[cp,cp2]*model.SF_CP[t,cp,cp2]*energy_CP[cp2] for cp2 in model.CP if (cp2 != cp and model.CP_uses_CP[cp,cp2] ==1)) 
                elif self.PV > 0 and self.Bat > 0:
                    energy_CP_injected[cp] = sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat)\
                                + sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)\
                                + sum(model.CP_uses_CP[cp,cp2]*model.SF_CP[t,cp,cp2]*energy_CP[cp2] for cp2 in model.CP if (cp2 != cp and model.CP_uses_CP[cp,cp2] ==1))
            #print(energy_CP[cp])
        return energy_CP_injected

    def constrain_P_Balance(self):
        """Builds a constrain to define the energy in each consumer of the EC, P_Balance. It separates the consumption and the injection. 

            Parameters:
                    SF_Par (bool): indicates if the sharing factors are a variable,False, or a parameter, True
        """
        Parameters =["I","T","CP","P_Consumed","I_uses_CP"] 
        Variables = ["P_Consumed_bill","P_Injected_bill"]
        
        if self.mode == "Eallocation":
            Variables.append("E_shared_CP")
            Variables.append("E_shared")
            self.search_and_add_Par_Var(Parameters,Variables)
            def P_Balance(model,i,t):                
                return model.P_Consumed_bill[i,t]  - model.P_Injected_bill[i,t]  ==\
                    model.P_Consumed[i,t]- sum(model.I_uses_CP[i,cp]*model.E_shared[i,t,cp] for cp in model.CP)
            
        elif self.mode == "SF": 
            Parameters.append("CP_uses_CP")
            if self.SF_Par:
                Parameters.append("SF")
                Parameters.append("SF_CP")
            else:
                Variables.append("SF")
                Variables.append("SF_CP")
                
            if self.Bat > 0:
                Parameters.append("Bat")
                Parameters.append("is_Bat_in_CP")
                Variables.append("PBat_ch")
                Variables.append("PBat_dch")
            if self.PV > 0:
                Parameters.append("PV")
                Parameters.append("is_PV_in_CP")
                Parameters.append("P_PV")
            self.search_and_add_Par_Var(Parameters,Variables)
            def P_Balance(model,i,t):
                energy_CP = self.get_energy_CP(model,t)

                return model.P_Consumed_bill[i,t]  - model.P_Injected_bill[i,t]  ==  model.P_Consumed[i,t]\
                    - sum(model.I_uses_CP[i,cp]*model.SF[i,self.sharing_factors_disc(i,t),cp]*energy_CP[cp] for cp in model.CP)
            self.model.P_Balance = Constraint(self.model.I,self.model.T,rule=P_Balance)


    def constrain_cost(self):
        """Builds a constrain to calculate the cost in each consumer of the EC, const_cost. It is calculated for the whole period and it only can be positive."""
        Parameters =["I","T","At","Ecost","Ecost_sell","count_timestamp"] 
        Variables = ["P_Consumed_bill","P_Injected_bill","Cost"]
        self.search_and_add_Par_Var(Parameters,Variables)

        #limit the cost of the month to 0
        def const_cost(model,i):
            return model.Cost[i] == sum(((model.P_Consumed_bill[i,t]*model.At*model.Ecost[i,t])-(model.P_Injected_bill[i,t]*model.At*model.Ecost_sell[i,t]))*model.count_timestamp[t] for t in model.T)
        self.model.const_cost = Constraint(self.model.I,rule=const_cost)
    
    def constrain_fix_cost(self,value):
        """Builds a constrain to calculate the cost in each consumer of the EC, const_cost. It is calculated for the whole period and it only can be positive."""
        Parameters =["I"] 
        Variables = ["Cost"]
        self.search_and_add_Par_Var(Parameters,Variables)

        #limit the cost of the month to 0
        def const_fix_cost(model):
            return value >= sum(model.Cost[i] for i in model.I)
        self.model.const_fix_cost = Constraint(rule=const_fix_cost)

    def constrain_LP_required_charge_to_clients(self):
        """Builds two constrains to define the energy in each consumer of the EC, P_Balance. It separates the consumption and the injection. 

            Parameters:
                    SF_Par (bool): indicates if the sharing factors are a variable,False, or a parameter, True
        """
        Parameters =["I","T","CP","I_uses_CP"] 
        Variables = ["P_Consumed_bill","P_Injected_bill"]#,"energy_CP_consumed","energy_CP_injected"]
        if self.SF_Par:
            Parameters.append("SF")
        elif self.mode == "Eallocation":#this use to be and else
            Variables.append("E_shared_CP")
            Variables.append("E_shared")
        self.search_and_add_Par_Var(Parameters,Variables)

        #It tended to consume more to compensate surplus what it's stupid, It buyed energy to sell it WTF.
        if self.mode == "SF":
            def P_Utilized_limitation1(model,i,t):
                energy_CP_consumed = self.get_energy_CP_consumed(model,t)
            
                return model.P_Consumed_bill[i,t] <= model.P_Consumed[i,t] + sum(model.I_uses_CP[i,cp]*model.SF[i,self.sharing_factors_disc(i,t),cp]*energy_CP_consumed[cp] for cp in model.CP)
            self.model.P_Utilized_limitation1 = Constraint(self.model.I,self.model.T,rule=P_Utilized_limitation1) #abans s'anulaven sóc tonto
            def P_Utilized_limitation(model,i,t):
                energy_CP_injected = self.get_energy_CP_injected(model,t)

                return model.P_Injected_bill[i,t] <= + sum(model.I_uses_CP[i,cp]*model.SF[i,self.sharing_factors_disc(i,t),cp]*energy_CP_injected[cp] for cp in model.CP)
            self.model.P_Utilized_limitation = Constraint(self.model.I,self.model.T,rule=P_Utilized_limitation)
        elif self.mode == "Eallocation":
            def P_Utilized_limitation1(model,i,t):           
                return model.P_Consumed_bill[i,t] <= model.P_Consumed[i,t]# - model.P_Consumed[i,t]
            self.model.P_Utilized_limitation1 = Constraint(self.model.I,self.model.T,rule=P_Utilized_limitation1) #abans s'anulaven sóc tonto
            
            if self.Bat > 0:
                self.search_and_add_Par_Var(["is_Bat_in_CP","is_PV_in_CP","P_PV"], [])
                def P_Utilized_limitation(model,i,t):           
                    return model.P_Injected_bill[i,t] <= sum(model.I_uses_CP[i,cp]*model.E_shared[i,t,cp] for cp in model.CP)# - model.P_Consumed[i,t]
                self.model.P_Utilized_limitation = Constraint(self.model.I,self.model.T,rule=P_Utilized_limitation) #abans s'anulaven sóc tonto
                def P_Bat_limitation_contradiction(model,cp,t):
                    return sum(model.is_Bat_in_CP[bat,cp]*model.PBat_ch[t,bat] for bat in model.Bat) <= \
                    + sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV)\
                    + sum(model.CP_uses_CP[cp,cp2]*model.E_shared_CP[t,cp,cp2] for cp2 in model.CP if cp2 != cp)#\
                    #+ sum(model.I_uses_CP[i,cp]*model.E_shared[i,t,cp]for i in model.I)
                self.model.P_Bat_limitation_contradiction = Constraint(self.model.CP,self.model.T,rule=P_Bat_limitation_contradiction)
                def P_Bat_limitation_contradiction2(model,cp,t):
                    return sum(model.is_Bat_in_CP[bat,cp]*model.PBat_dch[t,bat] for bat in model.Bat) <=  \
                    sum(model.I_uses_CP[i,cp]*model.E_shared[i,t,cp] for i in model.I)\
                    + sum(model.CP_uses_CP[cp2,cp]*model.E_shared_CP[t,cp2,cp] for cp2 in model.CP if cp2 != cp) 
                self.model.P_Bat_limitation_contradiction2 = Constraint(self.model.CP,self.model.T,rule=P_Bat_limitation_contradiction2)
                





    def Constrains_on_the_temporal_sharing_coeficients(self):
        """Limits how often a sharing factor can change value 

            Parameters:
                    SF_Par (bool): indicates if the sharing factors are a variable,False, or a parameter, True
        """
        #if hasattr(self,"freq_SF"):
        #    self.search_and_add_Par_Var(["freq"],["SF"])
        #
        #    #self.freq_SF = 
        #    def freq_SF(model,i,t):
        #        if t % model.freq[i] != 0 and t != 0:
        #            for cp in model.CP:
        #                return model.SF[i,t-1,cp] == model.SF[i,sharing_factors_disc(i,t),cp]
        #        return Constraint.Skip
        #    self.model.freq_SF = Constraint(self.model.I,self.model.T,rule=freq_SF)
        #if hasattr(self,"freq_SF"):
        #    self.search_and_add_Par_Var(["freq"],["SF"])
        #    #self.freq_SF = 
        #    def freq_SF(model,i,t):
        #        if t % model.freq[i] != 0 and t != 0:
        #            get_energy_CP = get_energy_CP(model,t)
        #            for cp in model.CP:
        #                return model.SF[i,t-1,cp] == model.E_shared[i,t,cp]/get_energy_CP
        #        return Constraint.Skip
        #    self.model.freq_SF = Constraint(self.model.I,self.model.T,rule=freq_SF)
        #model.E_shared[i,t,cp] for i in model.I)\
        #model.E_shared_CP[t,cp2,cp] 
        print(1)


    


    def constrain_Payback_general(self):
        Parameters = ["I_uses_CP","Ecost","P_Consumed"]
        Variables = ["Payback","Cost"]
        if self.Bat > 0:
            Parameters.append("Inv_Bat")
            Parameters.append("is_Bat_in_CP")
        if self.PV > 0:
            Parameters.append("Inv_PV")
            Parameters.append("is_PV_in_CP")
        
        self.search_and_add_Par_Var(Parameters,Variables)
        if self.PV > 0 and self.Bat == 0:
            def Payback_funct(model,i):
                return model.Payback[i] == (sum(model.Ecost[i,t]*model.P_Consumed[i,t]*model.count_timestamp[t] for t in model.T)-model.Cost[i])/sum(model.I_uses_CP[i,cp]*sum(model.is_PV_in_CP[pv,cp]*model.Inv_PV[i,pv] for pv in model.PV)for cp in model.CP)
        elif self.PV == 0 and self.Bat > 0:
            def Payback_funct(model,i):
                return model.Payback[i] == (sum(model.Ecost[i,t]*model.P_Consumed[i,t]*model.count_timestamp[t] for t in model.T)-model.Cost[i])/sum(model.I_uses_CP[i,cp]*sum(model.is_Bat_in_CP[bat,cp]*model.Inv_Bat[i,bat] for bat in model.Bat)for cp in model.CP)
        elif self.PV > 0 and self.Bat > 0:
            def Payback_funct(model,i):
                return model.Payback[i] == (sum(model.Ecost[i,t]*model.P_Consumed[i,t]*model.count_timestamp[t] for t in model.T)-model.Cost[i])/sum(model.I_uses_CP[i,cp]*(sum(model.is_Bat_in_CP[bat,cp]*model.Inv_Bat[i,bat] for bat in model.Bat)\
                    + sum(model.is_PV_in_CP[pv,cp]*model.Inv_PV[i,pv] for pv in model.PV))for cp in model.CP)
        self.model.Payback_funct = Constraint(self.model.I,rule=Payback_funct)

        def same_Payback_fix(model,i):
            if i >0:
                return model.Payback[i-1] == model.Payback[i] 
            return Constraint.Skip
        self.model.same_Payback_fix = Constraint(self.model.I,rule=same_Payback_fix)
       
    def constrain_Payback_by_element(self,element="Bat"):
        if element =="Bat" and self.Bat> 0:
            self.search_and_add_Par_Var(["Inv_Bat"],["Payback_Bat"])
            def Payback_Bat_funct(model,i,bat):
                return model.Payback_Bat[i,bat] == (sum(model.Ecost[i,t]*model.SF_Bat[i,t,bat]*model.PBat_dch[t,bat] for t in model.T))/sum(model.Inv_Bat[i,bat] for bat in model.Bat)
            self.model.Payback_Bat_funct = Constraint(self.model.I,self.model.Bat,rule=Payback_Bat_funct)

            def P_Balance_Bat_Q(model,i,bat):
                if i >0:
                    return model.Payback_Bat[i-1,bat] == model.Payback_Bat[i,bat] 
                return Constraint.Skip
            self.model.P_Balance_Bat_Q = Constraint(self.model.I,self.model.Bat,rule=P_Balance_Bat_Q)
    
    def constrain_Bat_degradation(self):
        Parameters =["Bat","T","nmax","EBat_max","At"] 
        Variables = ["EBat","PBat_ch","PBat_dch"]
        self.search_and_add_Par_Var(Parameters,Variables)

        def Bat_degradation(model,bat):
            return model.nmax[bat] >= sum((model.PBat_ch[t,bat]+model.PBat_dch[t,bat])*model.At for t in model.T)/(2*model.EBat_max[bat])
        self.model.Bat_degradation = Constraint(self.model.Bat,rule=Bat_degradation)
    

    def constrain_Battery_limits(self,margin_end=None):
        Parameters =["Bat","T","At","EBat_0","EBat_end","EBat_max","is_Bat_in_CP"]
        Variables = ["EBat","PBat_ch","PBat_dch"]
        i = 'PBat_max'
        def fb(model,t,bat):
            return (0,(pd.pivot_table(self.Bat_info,index=["Bat_index"],values= i)*self.At).to_dict()[i][bat])
        self.Define_parameters_variables("PBat_ch","Var",domain = "NonNegativeReals",bound = fb)
        self.Define_parameters_variables("PBat_dch","Var",domain = "NonNegativeReals",bound = fb)
        i = 'EBat_min'
        ii = 'EBat_max'
        def fb(model,t,bat):
            return ((pd.pivot_table(self.Bat_info,index=["Bat_index"],values= i)*self.At).to_dict()[i][bat],(pd.pivot_table(self.Bat_info,index=["Bat_index"],values= ii)*self.At).to_dict()[ii][bat])
        self.Define_parameters_variables("EBat","Var",domain = "NonNegativeReals",bound = fb,initialize=self.Bat_info["EBat_0"].values[0])
        self.search_and_add_Par_Var(Parameters,Variables)

        #def Battery_limits_min(model,t,bat):
        #    return model.EBat_min[bat] <= model.EBat[t,bat]
        #self.model.Energy_Bat_min = Constraint(self.model.T,self.model.Bat,rule=Battery_limits_min)
        #
        #def Battery_limits_max(model,t,bat):
        #    return model.EBat_max[bat] >= model.EBat[t,bat]
        #self.model.Energy_Bat_max = Constraint(self.model.T,self.model.Bat,rule=Battery_limits_max)

        #def Battery_limits_charge(model,t,bat):
        #    return model.PBat_max[bat]  >= model.PBat_ch[t,bat]#*model.Beta[t]
        #self.model.Power_Bat_charge = Constraint(self.model.T,self.model.Bat,rule=Battery_limits_charge)
        #
        #def Battery_limits_discharge(model,t,bat):
        #    return model.PBat_max[bat]  >= model.PBat_dch[t,bat]# for i in model.n)#*(1-model.Beta[t])
        #self.model.Power_Bat_discharge_limit = Constraint(self.model.T,self.model.Bat,rule=Battery_limits_discharge)

        def Battery_limits_charging(model,t,bat):
            if t>0:
                return model.EBat[t,bat] == model.EBat[t-1,bat] + model.PBat_ch[t,bat]*model.At - model.PBat_dch[t,bat]*model.At#sum( for i in model.n)i,
            return Constraint.Skip
        self.model.Energy_Bat_charging = Constraint(self.model.T,self.model.Bat,rule=Battery_limits_charging)

        def Battery_limits_charging0(model, t,bat):
            if t==0:
                return model.EBat[t,bat] == model.EBat_0[bat] + model.PBat_ch[t,bat]*model.At - model.PBat_dch[t,bat]*model.At# sum(for i in model.n),i
            return Constraint.Skip
        self.model.Energy0_Bat_charging = Constraint(self.model.T,self.model.Bat, rule=Battery_limits_charging0)
        if margin_end == None:
            def Battery_limits_chargingend(model, t,bat):
                if t==(len(model.T)-1):
                    return model.EBat[t,bat] == model.EBat_end[bat]
                return Constraint.Skip
            self.model.Batteryend_limits_charging = Constraint(self.model.T,self.model.Bat, rule=Battery_limits_chargingend)
        else:
            def Battery_limits_chargingend_min(model, t,bat):
                if t==(len(model.T)-1):
                    return model.EBat[t,bat] >= model.EBat_end[bat]-(margin_end*model.EBat_max[bat])
                return Constraint.Skip
            self.model.Battery_limits_chargingend_min = Constraint(self.model.T,self.model.Bat, rule=Battery_limits_chargingend_min)
            def Battery_limits_chargingend_max(model, t,bat):
                if t==(len(model.T)-1):
                    return model.EBat[t,bat] <= model.EBat_end[bat]+(margin_end*model.EBat_max[bat])
                return Constraint.Skip
            self.model.Battery_limits_chargingend_max = Constraint(self.model.T,self.model.Bat, rule=Battery_limits_chargingend_max)


    
    def fuzzy_logic_Battery(self,percentage_discharging_margin = 1, limitdischarge = True):
        Parameters =["Bat","T","EBat_min","EBat_max","PBat_max","At","EBat_0","EBat_end"] 
        Variables = ["EBat","PBat_ch","PBat_dch"]
        self.search_and_add_Par_Var(Parameters,Variables)
        self.Define_parameters_variables("Charge","Var",domain = "Binary")#,bound = (-1,1))

        
        def Battery_charging_value(model, t,bat):
            #relaxation to never surpas the power need to be cheked a posteriori
            return model.PBat_ch[t,bat] == (model.Charge[t,bat])*sum(sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV) for cp in model.CP if model.is_Bat_in_CP[bat,cp]==1)
        self.model.Battery_charging_value = Constraint(self.model.T,self.model.Bat, rule=Battery_charging_value)
        if limitdischarge:

            def Battery_discharging_value(model, t,bat):
                #relaxation to never surpas the power need to be cheked a posteriori
                return model.PBat_dch[t,bat] == (1-model.Charge[t,bat])*percentage_discharging_margin*(sum(sum(model.I_uses_CP[i,cp]* model.P_Consumed[i,t] for i in model.I) for cp in model.CP if model.is_Bat_in_CP[bat,cp]==1)-sum(sum(model.is_PV_in_CP[pv,cp]*model.P_PV[t,pv] for pv in model.PV) for cp in model.CP if model.is_Bat_in_CP[bat,cp]==1))
            self.model.Battery_discharging_value = Constraint(self.model.T,self.model.Bat, rule=Battery_discharging_value)
