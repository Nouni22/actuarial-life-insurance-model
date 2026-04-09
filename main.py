 #print("J'apprends Python!")

#print(17 + 35 * 2) 

#nom = "NOUNI"
#prenom = "Aurore"
#age = 28
#print(f"Je m'appelle {prenom} et j'ai {age} ans")
#age = age + 10
#print(f"Je m'appelle {prenom} et j'ai {age} ans maintenant")


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