# ================================================================
# Conversão ExoMol: σ[cm²/molécula] → κ[cm⁻¹]
# A partir da relação: kappa = N(T,p) * Y_abs * sigma
# ================================================================

import numpy as np

# --------------------- CONFIGURAÇÕES (editar) ---------------------
FILE_XSEC = r"C:"     # entrada: nu, sigma
FILE_OUT  = r"C:"    # saída: nu, kappa

T_K   = 1200.0   # Temperatura [K]
P_BAR = 1.0     # Pressão total [bar]
Y_ABS = 1.0     # Fração molar do absorvedor (ex.: NH3 = 1.0 se gás puro)
# -----------------------------------------------------------------

# Constante de Loschmidt a 296 K e 1 atm [moléculas/cm³]
N0_296 = 2.479e19

def number_density(p_bar: float, T: float) -> float:
    """
    Retorna N(T,p) em [moléculas/cm³] a partir de:
    - p em bar
    - T em K
    usando N0_296 como referência (296 K, 1 atm).
    """
    p_atm = p_bar / 1.01325  # conversão aproximada bar → atm
    return N0_296 * p_atm * (296.0 / T)

# ===================== LEITURA DO ARQUIVO XSEC =====================

# Espera-se: coluna 0 = nu [cm^-1], coluna 1 = sigma [cm²/molécula]
data = np.loadtxt(FILE_XSEC)
nu = data[:, 0]
sigma = data[:, 1]

# ===================== CÁLCULO DE κ(ν̃) =====================

N = number_density(P_BAR, T_K)       # [moléculas/cm³]
kappa = N * Y_ABS * sigma            # κ em [cm⁻¹]

# ===================== GRAVAÇÃO DO ARQUIVO DE SAÍDA =====================

out = np.column_stack([nu, kappa])
np.savetxt(
    FILE_OUT,
    out,
    fmt="%.8e",
    header="nu(cm^-1)    kappa(cm^-1)"
)

print("Conversão concluída.")
print(f"Arquivo gerado: {FILE_OUT}")
