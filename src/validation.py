import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Validation:
    def __init__(self):
        self.df_val = None
        self.disaggregated_CP = None
        self.clients_info = None
        self.pv_cp = None
        self.df_pv_curve_val = None
        self.list_CP = None
        self.PV_info = None
        self.Energy_by_CP = None
        self.df_inv = None
        self.df_inv_by_CP = None
        self.Inv_PV = None
        self.At = None
        self.df_sharing_val = None
        self.df_consumption_price_val = None

    def input_consumption_price_validation(self,df_consumption_val,df_price_val):
        df_val = pd.merge(df_consumption_val,self.clients_info,on="id")
    
        df_val = pd.merge(df_val,df_price_val.rename(columns={"price":"price_buy","id_price":"price"}), how="left",on=["Timestamp","price"])
        df_val = pd.merge(df_val,df_price_val.rename(columns={"price":"price_s","id_price":"price_sell"}), how="left",on=["Timestamp","price_sell"])
        self.df_consumption_price_val= df_val
    
    def input_pv_val(self,df_pv_curve_val):
        pv_cp = []
        for k,v in self.list_CP.items():
            if k != "names":
                for pv in v["PV"]:
                    pv_cp.append({"CP":{v:k for k,v in self.list_CP["names"].items()}[pv],"PV_index":pv,})
        pv_cp = pd.DataFrame.from_records(pv_cp)
        self.pv_cp = pv_cp.copy()
        pv_cp = pd.merge(self.PV_info,pv_cp,on="PV_index")
        df_pv_curve_val = pd.merge(df_pv_curve_val,pv_cp,on="id_PV")
        df_pv_curve_val.drop(columns=["PV_index"],inplace=True)
        self.df_pv_curve_val = df_pv_curve_val
        return df_pv_curve_val

    def input_bat_val(self):
        raise Exception("Not implemented yet")

    def input_sf_val(self,df_sharing):
        if len(df_sharing.index.names)!=3:
            df_sharing.set_index(['id', 'timestamp', 'CP'],inplace=True)
        self.df_sharing_val = df_sharing


    def get_cp_energy_val(self,plot = False):
        df=pd.DataFrame()
        df_inv=pd.DataFrame()
        if hasattr(self,"df_pv_curve_val"):
            df_pv_curve_val_ = self.df_pv_curve_val.copy()
            df_pv_curve_val_.rename(columns={"P":"Energy"},inplace=True)
            df_pv_curve_val_["id"]="PV_" + df_pv_curve_val_["id_PV"]
            df = pd.concat([df,df_pv_curve_val_.drop(columns="id_PV")])
            inv_pv_ = pd.melt(self.Inv_PV,var_name="PV_index").reset_index(names="i")
            inv_pv_ = pd.merge(inv_pv_, self.clients_info, on="i")
            inv_pv_ = pd.merge(self.PV_info, inv_pv_, on="PV_index")
            inv_pv_ = pd.merge(self.pv_cp, inv_pv_, on="PV_index")
            inv_pv_ = inv_pv_.loc[:,["id_PV","id","CP","value"]]
            inv_pv_["id_resource"]="PV_"+inv_pv_["id_PV"]
            df_inv = pd.concat([df_inv,inv_pv_])
        if hasattr(self, "df_bat_curve_val"):
            print("To Implement")
            ## implement battery inversion
        self.disaggregated_CP =  df.pivot_table(index=["CP","timestamp_validation","Timestamp"],columns="id",values="Energy").reset_index()
        self.Energy_by_CP = df.drop(columns="id").groupby(["CP","timestamp_validation","Timestamp"]).sum().reset_index()
        self.df_inv = df_inv.pivot_table(index=["CP","id"],columns="id_resource",values="value").reset_index()
        self.df_inv_by_CP = df_inv.drop(columns=["id_resource","id_PV"]).groupby(["CP","id"]).sum()
        ## The interaction between the different CP should also be implemented
        ##self.plot_results_sharing_factors(plot=False,SF_required = "CP")
        if plot:
            for cp in self.disaggregated_CP.CP.unique():
                df_plot = self.disaggregated_CP.loc[self.disaggregated_CP.CP == cp].copy()
                df_plot.drop(columns=["timestamp_validation","CP"]).set_index("Timestamp").sort_index().plot(title=f"{cp} Generation")
        return self.Energy_by_CP,self.df_inv_by_CP

    def energy_balance_client_val(self):
        if hasattr(self,"df_sharing_val"):
            df_sf = self.df_sharing_val
        else:
            df_sf = self.plot_results_sharing_factors(plot=False)
        df_sf.reset_index(inplace=True)
        df_sf.rename(columns={"timestamp":"timestamp_validation"}, inplace=True)
        if hasattr(self,"Energy_by_CP"):
            df_cp = self.Energy_by_CP.copy()
            df_inv = self.df_inv.copy()
        else:
            df_cp,df_inv = self.get_cp_energy_val(plot=False)
            #df_cp,df_inv = get_CP_energy(self, plot=False)
        df_val = self.df_consumption_price_val.copy()
        df_cp =  pd.merge(df_sf,df_cp,on=["timestamp_validation","CP"],how="outer")
        df_cp["Energy_Allocated"] = df_cp["SF"] * df_cp["Energy"]
        df_cp["CP"] = "Energy_Allocated_"+df_cp["CP"]
        #df_cp.set_index(["id","Timestamp"]).sort_index()
        df_cp = df_cp.pivot_table(index=["id","Timestamp"],columns="CP",values="Energy_Allocated").reset_index()
        df_val = pd.merge(df_cp,df_val, on = ["Timestamp","id"])
        df_val["Total_Energy_Allocated"] = df_val.filter(like='Energy_Allocated_').sum(axis=1)
        df_val["Final_Consumption"] = df_val["consumption"] - df_val["Total_Energy_Allocated"]
        df_val["Original_Cost"] = np.where(df_val.consumption>0,df_val.consumption*df_val.price_buy,df_val.consumption*df_val.price_s)
        df_val["Final_Cost"] = np.where(df_val.Final_Consumption > 0, df_val.Final_Consumption * df_val.price_buy,
                                           df_val.Final_Consumption * df_val.price_s)
        df_val["savings"] = df_val["Original_Cost"] - df_val["Final_Cost"]
        df_val["Surplus"] = np.where(df_val.Final_Consumption >= 0, 0,-1*df_val.Final_Consumption)

        df_inv.reset_index(inplace=True)
        df_inv["CP"] = "Inversion_"+df_inv["CP"]
        df_inv = df_inv.groupby(["id","CP"]).sum().sum(axis=1).reset_index().rename(columns={0:"value"}).pivot_table(index=["id"],columns="CP",values="value")

        df_val_summary = df_val.drop(columns="Timestamp").groupby("id").sum()
        df_val_summary = pd.merge(df_inv,df_val_summary,on="id",how="outer")
        df_val_summary["Total_Inversion"] = df_val_summary.filter(like='Inversion_').sum(axis=1)

        number_of_points2year=len(df_val.Timestamp.unique()) * self.At/(24*365)
        df_val_summary["ROI_yearly"] = df_val_summary["Total_Inversion"]/(df_val_summary["savings"]/number_of_points2year)
        self.df_val = df_val
        self.df_val_summary = df_val_summary
        return df_val,df_val_summary


    def self_consumption_rate_val(self,plot= False):
        if hasattr(self,"df_val"):
            df_val = self.df_val.copy()
        else:
            _,df_val = self.energy_balance_client()
        df_val["self_consumption_rate_instantly"] = df_val["Total_Energy_Allocated"]/  df_val["consumption"]
        df_self_consumption_rate = df_val.loc[:,["id","Timestamp","self_consumption_rate_instantly"]]#pd.pivot_table(df_val,values="self_consumption_rate_instantly",index=["Timestamp","id"],columns="CP")
        df_self_consumption_rate.set_index(["id","Timestamp"],inplace=True)
        first = True
        res_df = pd.DataFrame()
        for i in df_self_consumption_rate.columns:
            division = 0.1
            binsize = np.arange(-1, (2 + division) / division) * division
            binsize = np.append(binsize, float("inf"))
            bins = pd.cut(df_self_consumption_rate[i], bins=binsize, labels=[float(round(i, 2)) for i in binsize][1:],right=True)
            if first:
                first = False
                res_df = df_self_consumption_rate[[i]].groupby(bins, observed=True).agg("count")/len(df_self_consumption_rate)
            else:
                res_df = pd.concat([res_df, df_self_consumption_rate[[i]].groupby(bins, observed=True).agg("count") / len(df_self_consumption_rate)],axis=1)
        if plot:
            ax = res_df.plot()
            ax.vlines(x=(1 / division), ymin=0, ymax=res_df.max().values[0], color='b', linestyle='--', lw=2)
            return True
        else:
            mean_grater0 = df_self_consumption_rate.loc[(df_self_consumption_rate.self_consumption_rate_instantly > 0) & (
                        df_self_consumption_rate.self_consumption_rate_instantly < float("inf"))].mean().values[0]
            mean = df_self_consumption_rate.loc[
                        df_self_consumption_rate.self_consumption_rate_instantly < float("inf")].mean().values[0]

            return res_df, mean, mean_grater0


    def summary_overall_val(self,plot= False,profit=True):
        df_val = self.df_val.copy()#.columns
        list_df = []
        list_df.append(df_val.loc[:,["Timestamp","consumption","Final_Consumption"]].groupby(["Timestamp"]).agg("sum").rename(columns= {"Final_Consumption":"Billed","consumption":"Consumption"}))
        list_df.append(df_val.loc[:,["Timestamp","price_s","price_buy"]].groupby(["Timestamp"]).agg("mean"))
        columns_to_join = ["Billed","Consumption"]
        if hasattr(self,"df_pv_curve_val"):
            df_pv_curve_val_ = self.df_pv_curve_val.copy()
            df_pv_curve_val_.rename(columns={"P":"Energy"},inplace=True)
            list_df.append(df_pv_curve_val_.drop(columns=["CP","timestamp_validation","id_PV"]).groupby("Timestamp").agg("sum").rename(columns={"Energy":"PV"}))
            columns_to_join.append("PV")

        columns_to_plot_cost = []
        df = pd.concat(list_df,axis=1,sort=False)
        for column in columns_to_join:
            if column == "PV":
                df["Consumption_"+ column] = df["Consumption"]-df[column]
                column2 = "Consumption_"+ column
            elif column == "Battery":
                df["Consumption_"+ column] = df["Consumption"]-df[column]
                column2 = "Consumption_"+ column
            else:
                column2 = column
            df["Cost_"+ column] = np.where(df.loc[:,column2] > 0, df.loc[:,column2]*df.price_buy, df.loc[:,column2]*df.price_s)
            columns_to_plot_cost.append("Cost_"+ column)
        if plot:
            if profit:
                fig, axs = plt.subplots(3, 1)
                df.loc[:, columns_to_join].plot(title="EC Energy Flow", ax=axs.flatten()[0])
                df.loc[:, columns_to_plot_cost].plot(title="EC Energy Cost", ax=axs.flatten()[1])
                df.loc[:, columns_to_plot_cost].cumsum().plot(title="EC Energy Cost", ax=axs.flatten()[2])
            else:
                df.loc[:, columns_to_join].plot(title="EC Energy Flow")
            # plt.show()
        else:
            return df



#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)