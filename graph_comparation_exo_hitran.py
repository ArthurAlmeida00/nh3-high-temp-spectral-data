import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ===================== CONFIGURAÇÕES GERAIS =====================
#CODIGO FEITO PARA COMPARAR LINHAS ESPECTRAIS CROSSSECTION DO EXOMOL E HITRAN

# --- HITRAN (κ -> σ) ---
FILE_KAPPA_300 = r'D:'  # κ(ν) a 300 K
UNIT = "cm^-1"          # "cm^-1"  ou  "cm^-1 amagat^-1"
T_K = 300.0             # temperatura do arquivo HITRAN (K)
P_BAR = 1.0             # pressão (bar)
Y_ABS = 1.0             # fração molar do absorvedor (NH3)

NU_START, NU_STOP, NU_STEP = 50.0, 10000.0, 0.01  # malha fixa do HITRAN

# --- ExoMol (σ já em cm²/molécula) ---
FILE_EXOMOL_300 = r'C:'

# Constante de Loschmidt a 296 K e 1 atm (moléculas/cm³)
N0_296 = 2.479e19

def number_density(p_bar: float, T: float) -> float:
    """Retorna N [moléculas/cm³] dado p em bar e T em K."""
    p_atm = p_bar / 1.01325  # 1 bar ≈ 0.986923 atm
    return N0_296 * p_atm * (296.0 / T)

def hitran_to_sigma(kappa: np.ndarray, T: float, p_bar: float, Y: float, unit: str) -> np.ndarray:
    """Converte kappa(HITRAN) → seção de choque σ [cm²/molécula]."""
    if unit == "cm^-1 amagat^-1":
        return kappa / (N0_296 * Y)
    elif unit == "cm^-1":
        N = number_density(p_bar, T)
        return kappa / (N * Y)
    else:
        raise ValueError("UNIT deve ser 'cm^-1' ou 'cm^-1 amagat^-1'.")

# ===================== LEITURA HITRAN 300 K =====================

kappa = np.loadtxt(FILE_KAPPA_300, dtype=float)                   
nu_hit = np.arange(NU_START, NU_STOP + NU_STEP/2, NU_STEP)

n = min(len(nu_hit), len(kappa))
nu_hit, kappa = nu_hit[:n], kappa[:n]

sigma_hit = hitran_to_sigma(kappa, T_K, P_BAR, Y_ABS, UNIT)

# ===================== LEITURA EXOMOL 300 K =====================

data_exo = np.loadtxt(FILE_EXOMOL_300, dtype=float)
nu_exo, sigma_exo = data_exo[:, 0], data_exo[:, 1]

# ========================= PLOT COMPARATIVO =========================

fig, ax1 = plt.subplots(figsize=(8, 4.5))

# ExoMol (azul)
ax1.plot(nu_exo, sigma_exo, color='#0072B2', lw=1.0,
         label='ExoMol / CoYuTe, 300 K, 1 bar')

# HITRAN (laranja)
ax1.plot(nu_hit, sigma_hit, color='#D55E00', lw=1.0,
         label='HITRAN, 300 K, 1 bar')

ax1.set_yscale('log')
ax1.set_xlim(50, 10000)

ax1.set_xlabel(r'Wavenumber (cm$^{-1}$)', fontsize=13)
ax1.set_ylabel(r'Cross-section (cm$^{2}$/molecule)', fontsize=13)

ax1.tick_params(axis='both', direction='in', length=5, width=0.8, labelsize=11)
for s in ['top', 'right']:
    ax1.spines[s].set_visible(False)

# ---- eixo superior em µm ----
def num_to_lambda(v): return 1e4 / v
def lambda_to_num(l): return 1e4 / l

secax = ax1.secondary_xaxis('top', functions=(num_to_lambda, lambda_to_num))
secax.set_xlabel(r'Wavelength ($\mu$m)', fontsize=13)

lambda_ticks = [100, 10, 5, 4, 3, 2.5, 2, 1.5, 1.25, 1, 0.833]
secax.set_xticks(lambda_ticks)
secax.set_xticklabels([f'{t:g}' for t in lambda_ticks])
secax.tick_params(axis='x', labelsize=11)

ax1.xaxis.set_major_locator(MultipleLocator(2000))
ax1.grid(which='major', color='gray', linestyle='--', linewidth=0.4, alpha=0.3)
ax1.set_facecolor('white')

plt.legend(frameon=False, fontsize=11, loc='upper right')
plt.tight_layout()
plt.show()
