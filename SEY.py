import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 2000, 10000)
e_max = 500
nom = x/e_max
yeild_max = [4, 3.5, 3]
colors = ["#2B2F42","#EF233C","#8D99AE"]

for i, sy in enumerate(yeild_max):
    print(colors[i])
    cst = []
    for n in nom:
        if n <= 1:
            #y = yeild_max * (n * np.exp(1 - n))**0.56
            z = 0.5
            a = 1
            y = sy * ((2 * n ) / (1 + (n ** (1.85 * (2 * z / a)))))
            cst.append(y)
        if 1 < n <= 3.6:
            y = sy * (n * np.exp(1 - n))**0.25
            cst.append(y)
        if n > 3.6:
            y = sy* (1.125* n)**-0.65
            cst.append(y)
    plt.plot(x, cst, color=colors[i], label=f"SEY = {sy}")

plt.xlabel("Energy (eV)")
plt.ylabel("Yield")
plt.title("SEY vs energy of inpacting electrons")
plt.legend(fontsize=12)
plt.grid(True)
plt.xlim(0, 1500)
plt.show()