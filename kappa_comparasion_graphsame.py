import numpy as np
import matplotlib.pyplot as plt

# ===================== ARQUIVOS =====================
FILE_KAPPA_HIT = r'D:'
FILE_KAPPA_EXO = r'C:'

# ===================== MALHA DO HITRAN =====================
NU_START, NU_STOP, NU_STEP = 50.0, 10000.0, 0.01

# ===================== LEITURA HITRAN =====================
kappa_hit = np.loadtxt(FILE_KAPPA_HIT)
nu_hit = np.arange(NU_START, NU_STOP + NU_STEP/2, NU_STEP)

n = min(len(kappa_hit), len(nu_hit))
kappa_hit = kappa_hit[:n]
nu_hit = nu_hit[:n]

# ===================== LEITURA EXOMOL =====================
data_exo = np.loadtxt(FILE_KAPPA_EXO)
nu_exo = data_exo[:, 0]
kappa_exo = data_exo[:, 1]

mask = (nu_exo >= NU_START) & (nu_exo <= NU_STOP)
nu_exo = nu_exo[mask]
kappa_exo = kappa_exo[mask]

# ===================== FIGURA: EIXO EM CIMA + EIXO EM BAIXO =====================

fig = plt.figure(figsize=(9, 6))

# HITRAN (em cima)
ax_top = fig.add_subplot(2, 1, 1)
ax_top.plot(nu_hit, kappa_hit, color='purple', lw=0.7)
ax_top.set_ylabel(r'$\kappa_{\rm HITRAN}$ (cm$^{-1}$)', fontsize=12)
ax_top.set_xlim(NU_START, NU_STOP)
ax_top.grid(True, linestyle='--', linewidth=0.4, alpha=0.4)
ax_top.tick_params(axis='x', labelbottom=False)

# ExoMol (em baixo)
ax_bottom = fig.add_subplot(2, 1, 2, sharex=ax_top)
ax_bottom.plot(nu_exo, kappa_exo, color='red', lw=0.7)
ax_bottom.set_xlabel(r'Wavenumber, $\eta$ (cm$^{-1}$)', fontsize=12)
ax_bottom.set_ylabel(r'$\kappa_{\rm ExoMol}$ (cm$^{-1}$)', fontsize=12)
ax_bottom.grid(True, linestyle='--', linewidth=0.4, alpha=0.4)

plt.tight_layout()
plt.show()
