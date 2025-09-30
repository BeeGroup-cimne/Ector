from pyomo.environ import *    

class Cost_Function:
    def Cost_Function_cost(self):
        def cost_rule(model):
            return sum(model.Cost[i] for i in model.I)
        self.model.obj = Objective(rule=cost_rule)
    

    def Cost_Function_squared_cost(self):
        def cost_rule(model):
            return sum(model.Cost[i]*model.Cost[i] for i in model.I)
        self.model.obj = Objective(rule=cost_rule)

    def Cost_Function_Cost_bat_operation(self):
        def cost_rule(model):
            return sum(model.Cost[i] for i in model.I)+sum(sum((model.PBat_ch[t,bat]+model.PBat_dch[t,bat])*model.At for t in model.T)/(2*model.EBat_max[bat])for bat in model.Bat)
        self.model.obj = Objective(rule=cost_rule)

    def Cost_Function_squared_Cost_bat_operation(self):
        def cost_rule(model):
            return sum(model.Cost[i]*model.Cost[i] for i in model.I)+0.001*sum(sum((model.PBat_ch[t,bat]+model.PBat_dch[t,bat])*model.At for t in model.T)/(2*model.EBat_max[bat])for bat in model.Bat)
        self.model.obj = Objective(rule=cost_rule)
    
    def Pareto_Cost_self_consumption(self,delta):
        def cost_rule(model):
            return (1-delta)*sum(model.Cost[i] for i in model.I)+delta*model.mean_self_consumption
        self.model.obj = Objective(rule=cost_rule)

    def Ob_self_consumption(self):
        def cost_rule(model):
            return model.mean_self_consumption
        self.model.obj = Objective(rule=cost_rule)
    
    def Cost_Function_cost_selfconsumption(self):
        def cost_rule(model):
            return sum(model.Cost[i] for i in model.I)+0.001*sum(sum((sum(model.I_uses_CP[i,cp]*model.SF[i,int((t-(t % model.freq[i]))/model.freq[i]),cp]*self.get_energy_CP(model,t)[cp] for cp in model.CP))/ (model.P_Consumed[i,t]+10**-3)for i in model.I)for t in model.T)
        self.model.obj = Objective(rule=cost_rule)

    def cost_rule_mean_abs_ReturnInversion(self):

        Parameters=["I","T"]
        Variables=["mean_abs_ReturnInversion","Payback"]
        self.search_and_add_Par_Var(Parameters,Variables)

        def mean_abs_ReturnInversion_pos_funct(model,i):
            return model.mean_abs_ReturnInversion[i] >= sum(model.Payback[ii] for ii in model.I)/len(model.I)-model.Payback[i]
        self.model.mean_abs_ReturnInversion_pos_funct = Constraint(self.model.I,rule=mean_abs_ReturnInversion_pos_funct)

        def mean_abs_ReturnInversion_neg_funct(model,i):
            return model.mean_abs_ReturnInversion[i] >= -1*(sum(model.Payback[ii] for ii in model.I)/len(model.I)-model.Payback[i])
        self.model.mean_abs_ReturnInversion_neg_funct = Constraint(self.model.I,rule=mean_abs_ReturnInversion_neg_funct)

        def cost_rule_mean_abs_ReturnInversion(model):
            return sum(model.mean_abs_ReturnInversion[i] for i in model.I)
        self.model.obj = Objective(rule=cost_rule_mean_abs_ReturnInversion)
