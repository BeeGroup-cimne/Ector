import pandas as pd
from pyomo.environ import *
import pyomo.environ as pyo
import numpy as np

from ECTOR.src.Parameters import Parameters
from ECTOR.src.contrains import constrains
from ECTOR.src.cost_function import Cost_Function
from ECTOR.src.plotter import plotter
from ECTOR.src.standard_cases import standard_cases
from ECTOR.src.validation import Validation


class ECTOR(Parameters,constrains,Cost_Function,plotter,standard_cases,Validation):
    def __init__(self,mode,SF_Par,Abstract = False):
        self.mode = mode
        self.SF_Par = SF_Par
        self.I  = 1
        self.PV = 0
        self.Bat = 0
        self.CP = 0
        self.list_CP = {"names":{}}
        self.At = 1
        self.Parameters = []
        self.Variables = []
        if Abstract:
            self.model = AbstractModel()
        else:
            self.model = ConcreteModel()

    def solver(self,solver:str , name:str = None,seed: int = None):
        """Ends builfing the model and finds the solution.

            Parameters:
                    solver (str): Solver that is wanted to be used, i.e. gurobi
                    name (str): Name of the logfile to be saved
                    seed (int): Specific seed for the solver

            Returns:
                    instance (pyomo.instance): Instance of the problem with the results
                    results (list of pandas.Dataframes): List of the results formated
        """

        opt = SolverFactory(solver)#, solver_io="python")
        #opt.options['slog'] = 1
        #if(solver == "glpk"):
        #    opt.options['mipgap'] = 0.02
        #    opt.options['tmlim'] = 60*10
        #elif(solver == "gurobi"):
        #    opt.options["MIPGap"] = 0.02
            
        if seed != None:
            opt.options['seed'] = seed
        instance = self.model.create_instance(self.data)
        
        instance = self.fix_Var_required(instance)

        if name == None:
            results = opt.solve(instance, tee=True,report_timing = True)
        else:
            results = opt.solve(instance, tee=False ,report_timing = True, logfile=name)
        results.write()
        instance.solutions.load_from(results)
        
        print('done')
        self.instance,self.results=instance,results
        return instance,results

    def pyomo_to_df(self):
        """Rebuilds all the results in the pyomo format to the formating and the names in the input

            Returns:
                    results (list of pandas.Dataframes): List of the results formated
        """
        data_json = {}
        for v in self.instance.component_objects(pyo.Var,active=True):
            for index in v:
                if not v.name in data_json.keys():
                    data_json[v.name] = {}
                data_json[v.name][index] = pyo.value(v[index])

        for key in data_json.keys():
            for i in data_json[key].copy():
                if i == None:
                    data_json[key][1] = data_json[key][i]
                    data_json[key].pop(i)

        Dict_parameters ={key: self.list_dependence_Params_and_Variables[key] for key in data_json.keys()}

        unique_index_group = [list(value) for value in set(tuple(value) for key,value in Dict_parameters.items())]

        list_of_df = []
        for index_group in unique_index_group:
            #index_group = unique_index_group[0]
            keys_same_index_group = [k for k, v in Dict_parameters.items() if v == index_group]
            data_index_group = {key: data_json[key] for key in keys_same_index_group}
            df = pd.DataFrame(data_index_group)
            if pd.DataFrame(index_group).duplicated().any():
                df_index_group = pd.DataFrame(index_group)
                df_index_group[df_index_group.duplicated()] = df_index_group[df_index_group.duplicated()]+"2"
                df.index.names = [str(i) for i in df_index_group[0].values]
                index_group = [str(i) for i in df_index_group[0].values]
                index_new = []
            elif len(index_group) == 0:
                index_new = "index"
            else:
                df.index.names = index_group
                index_new = []
            df = df.reset_index()
            for index in index_group:
                if index == "I":
                    df  = pd.merge(df,self.clients_info[["i","id"]],left_on="I",right_on="i").drop(columns=["I","i"])
                    index_new.append("id")
                elif index == "T":
                    df  = pd.merge(df,self.timestamps,left_on="T",right_on="time_index").drop(columns=["T","time_index"])
                    index_new.append("timestamp")
                elif index == "PV":
                    df  = pd.merge(df,self.PV_info,left_on="PV",right_on="PV_index").drop(columns=["PV","PV_index"])
                    index_new.append("id_PV")
                elif index == "Bat":
                    df  = pd.merge(df,self.Bat_info[["Bat_index","id_Bat"]],left_on="Bat",right_on="Bat_index").drop(columns=["Bat","Bat_index"])
                    index_new.append("id_Bat")
                elif index == "CP":
                    df_CP_names = pd.DataFrame.from_dict(self.list_CP["names"], orient='index').reset_index().rename(columns={"index":"CP_name",0:"CP_id"})
                    df  = pd.merge(df,df_CP_names,left_on=index,right_on="CP_id").drop(columns=[index,"CP_id"]).rename(columns={"CP_name":"CP"})
                    index_new.append("CP")
                elif index == "CP2":
                    df_CP_names = pd.DataFrame.from_dict(self.list_CP["names"], orient='index').reset_index().rename(columns={"index":"CP_name",0:"CP_id"})
                    df  = pd.merge(df,df_CP_names,left_on=index,right_on="CP_id").drop(columns=[index,"CP_id"]).rename(columns={"CP_name":"CP_where_energy_is_generated"})
                    index_new.append("CP_where_energy_is_generated")

            df = df.set_index(index_new)
            list_of_df.append(df)
            self.list_df_results = list_of_df
        return list_of_df
    
    def create_CP_matrix(self):
        """Creates the structure of the matrix of where the different elements are inside the EC.

            Returns:
                    data_out (dict with DataFrames): Dictionaries with dataframes with the information of which element is inside each CP
        """
        data = {"PV":np.zeros([self.PV, self.CP]),"Bat":np.zeros([self.Bat, self.CP]),"I":np.zeros([self.I, self.CP]),"CP_uses_CP":np.zeros([self.CP, self.CP])}
        for k,cp in self.list_CP["names"].items():
            for element in self.list_CP[k].keys():
                for ii in self.list_CP[k][element]:
                    data[element][ii][cp] = 1
        data_out = {}
        data_out["I_uses_CP"] = pd.DataFrame(data["I"]).stack(level=0).to_dict()
        data_out["is_PV_in_CP"] = pd.DataFrame(data["PV"]).stack(level=0).to_dict()
        data_out["is_Bat_in_CP"] = pd.DataFrame(data["Bat"]).stack(level=0).to_dict()
        data_out["CP_uses_CP"] = pd.DataFrame(data["CP_uses_CP"]).T.stack(level=0).to_dict()
        to_pop=[]
        for k,v in data_out.items():
            if len(v.keys()) == 0:
                to_pop.append(k)
        for i in to_pop:
            data_out.pop(i)
        return data_out



    def get_data_ready(self):
        """Creates the structure of the data in the format required by pyomo
        """
        self.data = {None:{
            "At":{None:self.At}
        }}
        ### data from clients
        self.data[None]["P_Consumed"] = pd.pivot_table(self.P_Consumed.stack(level=0).reset_index(),index=["i","time_index"]).to_dict()[0]

        Ecost = pd.merge(pd.merge(self.id_price,self.Ecost.stack(level=0).rename("Price").reset_index(),on="price_index"),self.clients_info,right_on="price",left_on="id_price").drop(columns=["price_sell","id_price","price","price_index","id"])
        Ecost_sell = pd.merge(pd.merge(self.id_price,self.Ecost.stack(level=0).rename("Price").reset_index(),on="price_index"),self.clients_info,right_on="price_sell",left_on="id_price").drop(columns=["price_sell","id_price","price","price_index","id"])
        self.data[None]["Ecost"] = pd.pivot_table(Ecost,index=["i","time_index"]).to_dict()["Price"]
        self.data[None]["Ecost_sell"] = pd.pivot_table(Ecost_sell,index=["i","time_index"]).to_dict()["Price"]
        
        ### data PV
        if self.PV > 0:
            self.data[None]["P_PV"] = pd.pivot_table(self.P_PV.stack(level=0).reset_index(),index=["time_index","PV_index"]).to_dict()[0]
                      
            if not self.Inv_PV is None:
                self.data[None]["Inv_PV"] = pd.pivot_table(self.Inv_PV.stack(level=0).reset_index(),index=["i","PV_index"]).to_dict()[0]
        
        ### data Bat
        if self.Bat > 0:
            for i in  ['PBat_max', 'EBat_min', 'EBat_max', 'EBat_0','nmax', 'EBat_end']:
                if i in self.Bat_info.columns:
                    if i == "PBat_max":
                        self.data[None][i] =  (pd.pivot_table(self.Bat_info,index=["Bat_index"],values= i)*self.At).to_dict()[i]
                    elif i == "nmax":
                        self.data[None][i] =  (pd.pivot_table(self.Bat_info,index=["Bat_index"],values= i)*(self.At*len(self.timestamps)/24)).to_dict()[i]
                    else:
                        self.data[None][i] =  (pd.pivot_table(self.Bat_info,index=["Bat_index"],values= i)).to_dict()[i]      
            if not self.Inv_Bat is None:
                self.data[None]["Inv_Bat"] = pd.pivot_table(self.Inv_Bat.stack(level=0).reset_index(),index=["i","Bat_index"]).to_dict()[0]

        ### data Shating factors
        if hasattr(self,"SF"):
            self.data[None]["SF"] = pd.pivot_table(self.SF.stack(level=0).reset_index(),index=["i","time_index","CP_id"]).to_dict()[0]   
        if hasattr(self,"df_Sharing_Between_CP_id"):
            self.data[None]["SF_CP"] = self.df_Sharing_Between_CP_id.set_index(["time_index","CP_id","CP_id2"]).to_dict()["SF"]
            for cp,CP_id in self.list_CP["names"].items():
                for cp2,CP_id2 in self.list_CP["names"].items():
                    for time_index in self.timestamps.time_index:
                        if not (time_index,CP_id,CP_id2) in self.data[None]["SF_CP"].keys():
                            self.data[None]["SF_CP"][(time_index,CP_id,CP_id2)] = 0

        if hasattr(self,"count_timestamp"):
            self.data[None]["count_timestamp"] = self.count_timestamp.to_dict()["count_timestamp"]
        else:
            self.data[None]["count_timestamp"] = {time_index:1 for time_index in self.timestamps.time_index}
        
        ### data structure EC
        data_matrix_CP = self.create_CP_matrix()
        for k,v in data_matrix_CP.items():
            self.data[None][k] = v

        

