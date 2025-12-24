import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ===================== ARQUIVO EXOMOL =====================
arq = r'C:'

# ===================== LEITURA DOS DADOS =====================
data = np.loadtxt(arq, dtype=float)
x, y = data[:,0], data[:,1]

# ===================== FIGURA E EIXO PRINCIPAL =====================
fig, ax1 = plt.subplots(figsize=(8, 4.5))

ax1.plot(
    x, y,
    color='#0072B2', linewidth=1.0,
    label='ExoMol / CoYuTe, 1200 K'
)

ax1.set_yscale('log')
ax1.set_xlim(50, 12100)

# ===================== RÓTULOS (TRADUZIDOS + FONTE MAIOR) =====================
ax1.set_xlabel('Número de onda (cm$^{-1}$)', fontsize=18)
ax1.set_ylabel('Seção transversal de absorção (cm$^{2}$/molécula)', fontsize=18)

# ===================== TICKS MAIORES =====================
ax1.tick_params(axis='both', direction='in',
                length=5, width=0.8, labelsize=16)

for s in ['top', 'right']:
    ax1.spines[s].set_visible(False)

# ===================== EIXO SUPERIOR EM µm =====================
def num_to_lambda(v):
    return 1e4 / v

def lambda_to_num(l):
    return 1e4 / l

secax = ax1.secondary_xaxis('top', functions=(num_to_lambda, lambda_to_num))
secax.set_xlabel('Comprimento de onda ($\\mu$m)', fontsize=18)

lambda_ticks = [100, 10, 5, 4, 3, 2.5, 2, 1.5, 1.25, 1, 0.833]
secax.set_xticks(lambda_ticks)
secax.set_xticklabels([f'{t:g}' for t in lambda_ticks])
secax.tick_params(axis='x', labelsize=16)

# ===================== GRID =====================
ax1.xaxis.set_major_locator(MultipleLocator(2000))
ax1.grid(which='major', color='gray', linestyle='--',
         linewidth=0.4, alpha=0.3)

ax1.set_facecolor('white')

# ===================== LEGENDA MAIOR =====================
plt.legend(frameon=False, fontsize=16, loc='upper right')

plt.tight_layout()
plt.show()
