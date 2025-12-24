import numpy as np
import matplotlib.pyplot as plt
#CODIGO PARA GERAR GRAFICO COM KAPPA
# ================= CONFIGURAÇÕES =================
FILE_KAPPA = r"C:"   # entrada: nu, kappa
TITLE = "Coeficiente de Absorção κ(ν̃)"
# ==================================================

# ---- leitura ----
data = np.loadtxt(FILE_KAPPA)
nu = data[:, 0]       # número de onda [cm^-1]
kappa = data[:, 1]    # coeficiente κ [cm^-1]

# ---- plot ----
plt.figure(figsize=(9, 4))
plt.plot(nu, kappa, linewidth=1.0)

plt.yscale("log")
plt.xlabel("Número de onda (cm⁻¹)", fontsize=12)
plt.ylabel("κ(ν̃)  [cm⁻¹]", fontsize=12)
plt.title(TITLE, fontsize=13)

plt.grid(True, which="both", linestyle="--", linewidth=0.4, alpha=0.6)
plt.tight_layout()
plt.show()
