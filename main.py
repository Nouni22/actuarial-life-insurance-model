import pandas as pd
import numpy as np
import numpy_financial as npf

np.random.seed(42)

n = 100

portfolio = pd.DataFrame({
    "age": np.random.randint(25, 70, n),
    "prime": np.random.uniform(5000, 50000, n),
    "duration": np.random.randint(5, 20, n),
    "interest_rate": np.random.uniform(0.01, 0.04, n)
})

print(portfolio.head())


def simulate_cashflows(row):
    cashflows = []
    
    for t in range(int(row["duration"])):
        
        # Prime payée au début
        premium = row["prime"] if t == 0 else 0
        
        # Prestations (ex: coût assurance)
        benefit = -row["prime"] * 0.02 * t
        
        # Rachat aléatoire (10% de probabilité)
        surrender = -row["prime"] * 0.5 if np.random.rand() < 0.1 else 0
        
        cashflows.append(premium + benefit + surrender)
    
    return cashflows

portfolio["cashflows"] = portfolio.apply(simulate_cashflows, axis=1)

print(portfolio[["age", "cashflows"]].head())



#Ajouter la fonction NPV

def npv(cashflows, rate):
    return sum(cf / (1 + rate)**t for t, cf in enumerate(cashflows))

#Calculer la valeur du portefeuille
portfolio["npv"] = portfolio.apply(
    lambda row: npv(row["cashflows"], row["interest_rate"]),
    axis=1
)

print(portfolio[["npv"]].head())


#Fonction IRR

def compute_irr(cashflows):
    try:
        return npf.irr(cashflows)
    except:
        return None
    
#Calcul IRR

portfolio["irr"] = portfolio["cashflows"].apply(compute_irr)

print(portfolio[["irr"]].head())

print("IRR moyen :", portfolio["irr"].mean())  #vision globale


#Simulation choc de taux

def shock_npv(row, shock):
    new_rate = row["interest_rate"] + shock
    return npv(row["cashflows"], new_rate)

portfolio["npv_up"] = portfolio.apply(lambda r: shock_npv(r, 0.01), axis=1)
portfolio["npv_down"] = portfolio.apply(lambda r: shock_npv(r, -0.01), axis=1)

print(portfolio[["npv", "npv_up", "npv_down"]].head())

#Calcul des pertes
portfolio["loss_up"] = portfolio["npv"] - portfolio["npv_up"]
portfolio["loss_down"] = portfolio["npv"] - portfolio["npv_down"]

#Calcul SCR
SCR = max(
    portfolio["loss_up"].mean(),
    portfolio["loss_down"].mean()
)

print("SCR simplifié :", SCR)