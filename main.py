import pandas as pd
import numpy as np

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