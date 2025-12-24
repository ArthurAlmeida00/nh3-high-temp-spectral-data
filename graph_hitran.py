# === HITRAN → seção de choque (cm²/molécula) e gráfico no mesmo padrão do ExoMol ===
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# --------------------- CONFIGURAÇÃO (editar) ---------------------
FILE_KAPPA = r'D:'  # 1 coluna: kappa
UNIT = "cm^-1"                 # "cm^-1"  ou  "cm^-1 amagat^-1"
T_K = 300.0                    # K   (do nome do arquivo)
P_BAR = 1.0                    # bar (do nome do arquivo)
Y_ABS = 1.0                    # fração molar do absorvedor (ex.: NH3). Se diluente=0.2 → Y_ABS=0.8

NU_START, NU_STOP, NU_STEP = 50.0, 10000.0, 0.01  # malha fixa do HITRAN
# ---------------------------------------------------------------

# Constante de Loschmidt a 296 K e 1 atm (moléculas/cm³)
N0_296 = 2.479e19

def number_density(p_bar: float, T: float) -> float:
    """Retorna N [moléculas/cm³] dado p em bar e T em K."""
    p_atm = p_bar / 1.01325  # 1 bar ≈ 0,986923 atm
    return N0_296 * p_atm * (296.0 / T)

def hitran_to_sigma(kappa: np.ndarray, T: float, p_bar: float, Y: float, unit: str) -> np.ndarray:
    """Converte kappa(HITRAN) → seção de choque σ [cm²/molécula]."""
    if unit == "cm^-1 amagat^-1":
        # κ_amagat / (N0 * Y)  (independe de T e p)
        return kappa / (N0_296 * Y)
    elif unit == "cm^-1":
        # κ / (N(T,p) * Y)
        N = number_density(p_bar, T)
        return kappa / (N * Y)
    else:
        raise ValueError("UNIT deve ser 'cm^-1' ou 'cm^-1 amagat^-1'.")

# ---- leitura da coluna de κ e construção do eixo de número de onda ----
kappa = np.loadtxt(FILE_KAPPA, dtype=float)                  # κ(ν) em 1D
nu = np.arange(NU_START, NU_STOP + NU_STEP/2, NU_STEP)       # ν̃ [cm^-1]

# alinhamento de comprimentos (caso difira por 1 amostra)
n = min(len(nu), len(kappa))
nu, kappa = nu[:n], kappa[:n]

# ---- conversão para σ(ν) em cm²/molécula ----
sigma = hitran_to_sigma(kappa, T_K, P_BAR, Y_ABS, UNIT)

# ========================= PLOT =========================
fig, ax1 = plt.subplots(figsize=(8, 4.5))

ax1.plot(nu, sigma, color='#0072B2', lw=1.0,
         label=f' T {int(T_K)} K, {P_BAR:g} bar ')

ax1.set_yscale('log')
ax1.set_xlim(50, 10000)
ax1.set_xlabel(r'Wavenumber (cm$^{-1}$)', fontsize=13)
ax1.set_ylabel(r'Cross-section (cm$^{2}$/molecule)', fontsize=13)
ax1.tick_params(axis='both', direction='in', length=5, width=0.8, labelsize=11)
for s in ['top', 'right']:
    ax1.spines[s].set_visible(False)

# eixo superior em µm (escala inversa)
def num_to_lambda(v): return 1e4 / v
def lambda_to_num(l): return 1e4 / l
secax = ax1.secondary_xaxis('top', functions=(num_to_lambda, lambda_to_num))
secax.set_xlabel(r'Wavelength ($\mu$m)', fontsize=13)
lambda_ticks = [100, 10, 5, 4, 3, 2.5, 2, 1.5, 1.25, 1, 0.833]
secax.set_xticks(lambda_ticks)
secax.set_xticklabels([f'{t:g}' for t in lambda_ticks])
secax.tick_params(axis='x', labelsize=11)

# grid mais espaçado
ax1.xaxis.set_major_locator(MultipleLocator(2000))
ax1.grid(which='major', color='gray', linestyle='--', linewidth=0.4, alpha=0.3)
ax1.set_facecolor('white')

plt.legend(frameon=False, fontsize=11, loc='upper right')
plt.tight_layout()
plt.show()

