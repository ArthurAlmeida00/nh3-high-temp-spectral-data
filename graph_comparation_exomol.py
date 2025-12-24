import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
#CODIGO USADO PARA COMPARAR VISUALMENTE LINHAS ESPECTRAIS EM CROSS SECTION DA BASE DE DADOS EXOMOL
# ------------------------ Caminhos dos arquivos ------------------------
arq_1200 = r'C:'
arq_300  = r'C:'

# ------------------------ Leitura dos dados ----------------------------
data1200 = np.loadtxt(arq_1200, dtype=float)
data300  = np.loadtxt(arq_300, dtype=float)

x1200, y1200 = data1200[:,0], data1200[:,1]
x300,  y300  = data300[:,0],  data300[:,1]

# ------------------------ Figura e eixo principal ----------------------
fig, ax1 = plt.subplots(figsize=(8, 4.5))

# Curva T = 1200 K
ax1.plot(x1200, y1200, color='#0072B2', linewidth=1.0, label='T = 1200 K, 1 bar')

# Curva T = 300 K
ax1.plot(x300, y300, color='#D55E00', linewidth=1.0, label='T = 300 K, 1 bar')

# Escala log no eixo Y
ax1.set_yscale('log')

# Limites
ax1.set_xlim(50, 12100)

# Rótulos
ax1.set_xlabel(r'Wavenumber (cm$^{-1}$)', fontsize=13)
ax1.set_ylabel(r'Cross-section (cm$^{2}$/molecule)', fontsize=13)

# Ticks
ax1.tick_params(axis='both', direction='in', length=5, width=0.8, labelsize=11)

# Remover bordas superior/direita
for s in ['top', 'right']:
    ax1.spines[s].set_visible(False)

# ------------------------ Eixo secundário em μm ------------------------
def num_to_lambda(v): return 1e4 / v
def lambda_to_num(l): return 1e4 / l

secax = ax1.secondary_xaxis('top', functions=(num_to_lambda, lambda_to_num))
secax.set_xlabel(r'Wavelength ($\mu$m)', fontsize=13)

lambda_ticks = [100, 10, 5, 4, 3, 2.5, 2, 1.5, 1.25, 1, 0.833]
secax.set_xticks(lambda_ticks)
secax.set_xticklabels([f'{t:g}' for t in lambda_ticks])
secax.tick_params(axis='x', labelrotation=0, labelsize=11)

# ------------------------ Grid ------------------------
ax1.xaxis.set_major_locator(MultipleLocator(2000))
ax1.grid(which='major', color='gray', linestyle='--', linewidth=0.4, alpha=0.3)
ax1.set_facecolor('white')

# ------------------------ Legenda ------------------------
plt.legend(frameon=False, fontsize=11, loc='upper right')

plt.tight_layout()
plt.show()
