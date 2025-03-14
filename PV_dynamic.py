from pyomo.environ import ConcreteModel, Var, Objective, Constraint, NonNegativeReals, minimize, SolverFactory
import matplotlib.pyplot as plt

# Data / Parameters
load = [99,93, 88, 87, 87, 88, 109, 127, 140, 142, 142, 140, 140, 140, 137, 139, 146, 148, 148, 142, 134, 123, 108, 93]
lf_pv = [0.00E+00, 0.00E+00, 0.00E+00, 0.00E+00, 9.80E-04, 2.47E-02, 9.51E-02, 1.50E-01, 2.29E-01, 2.98E-01, 3.52E-01, 4.15E-01, 4.58E-01, 3.73E-01, 2.60E-01, 2.19E-01, 1.99E-01, 8.80E-02, 7.03E-02, 3.90E-02, 9.92E-03, 1.39E-06, 0.00E+00, 0.00E+00]
timestep = len(load)
c_pv = 2500
c_batt = 1000
eff_batt_in = 0.95
eff_batt_out = 0.95
chargetime = 4  # hours to charge fully the battery

# Model
model = ConcreteModel()

# Define model variables
model.pv = Var( domain=NonNegativeReals)
model.E_pv = Var(range(timestep), domain=NonNegativeReals)
model.batt_max = Var( domain=NonNegativeReals)
model.batt = Var(range(timestep), domain=NonNegativeReals)
model.batt_in = Var(range(timestep), domain=NonNegativeReals)
model.batt_out = Var(range(timestep), domain=NonNegativeReals)

# Define the constraints


def power_balance(model, t):
    return model.E_pv[t] + model.batt_in[t]- model.batt_out[t] == load[t] 
model.power_balance = Constraint(range(timestep), rule=power_balance)

def pv_production(model, t):
    return model.E_pv[t] == model.pv*lf_pv[t]
model.pv_production = Constraint(range(timestep), rule=pv_production)

def battery_charge_rate (model, t):
    if model.E_pv[t] - load[t] < 0:
        model.batt_in[t] = model.E_pv[t] - load[t]
    else:
        model.batt_in[t] = 0
    return model.batt_in[t] <= model.batt_max / chargetime
model.battery_charge_rate = Constraint(range(timestep), rule=battery_charge_rate)

def battery_discharge_rate (model, t):
    if load[t] - model.E_pv[t] > 0:
        model.batt_out[t] = load[t] - model.E_pv[t]
    else:
        model.batt_out[t] = 0
    return model.batt_out[t] <= model.batt_max / chargetime
model.battery_discharge_rate = Constraint(range(timestep), rule=battery_discharge_rate)

def battery_balance(model, t):
    if t == 0:
        return model.batt[t] == model.batt_in[t]*eff_batt_in - model.batt_out[t]/eff_batt_out
    else:
        return model.batt[t] == model.batt[t-1] + model.batt_in[t]*eff_batt_in - model.batt_out[t]/eff_batt_out
model.battery_balance = Constraint(range(timestep), rule=battery_balance)



# Define the objective functions
def obj_rule(model):
    return model.pv*c_pv + model.batt_max*c_batt
model.obj = Objective(rule=obj_rule, sense=minimize)


# Specify the path towards your solver (gurobi) file
solver = SolverFactory('gurobi')
solver.solve(model)

# Results - Print the optimal PV size and optimal battery capacity
##########################################
############ CODE TO ADD HERE ############
##########################################


# Plotting - Generate a graph showing the evolution of (i) the load, 
# (ii) the PV production and, (iii) the soc of the battery
##########################################
############ CODE TO ADD HERE ############
##########################################