import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ==========================
# 1) DADOS (já convertidos)
# ==========================
T = np.array([400, 500, 600, 700, 800, 900, 1000, 1100, 1200], dtype=float)

# ==========================
# DADOS CORRIGIDOS
# ==========================

# S = 30 m
LBL_30  = np.array([0.958361577, 0.944575369, 0.945764245, 0.957258408,
                    0.969664939, 0.978224689, 0.981962636, 0.981440438,
                    0.977406643])

WSGG_30 = np.array([0.956563951, 0.939076975, 0.937804345, 0.950052957,
                    0.965514653, 0.977482735, 0.983889525, 0.984776294,
                    0.980953408])

# S = 10 m
LBL_10  = np.array([0.9232181,   0.899221221, 0.880513683, 0.878387688,
                    0.887063372, 0.898492561, 0.907209247, 0.910550868,
                    0.907729893])

WSGG_10 = np.array([0.922525416, 0.901269848, 0.884129097, 0.881187306,
                    0.88730763,  0.89566507,  0.901816667, 0.903523524,
                    0.900033956])


# S = 1 m
LBL_1  = np.array([0.736768574, 0.728738820, 0.689337163, 0.648819171,
                   0.615711025, 0.589812063, 0.568223816, 0.548085056,
                   0.527424848])

WSGG_1 = np.array([0.732625462, 0.722926708, 0.682667008, 0.642857002,
                   0.611557302, 0.5876946,   0.567810146, 0.548861345,
                   0.528904042])


# S = 0.1 m
LBL_01  = np.array([0.387220855, 0.377166052, 0.343432226, 0.304996935,
                    0.268982955, 0.237100098, 0.209243004, 0.184884430,
                    0.163491159])

WSGG_01 = np.array([0.384672655, 0.372207004, 0.337216301, 0.298444175,
                    0.262596331, 0.231178968, 0.203975795, 0.180357486,
                    0.159703304])


# ===========================================
# 2) FUNÇÃO PARA CALCULAR MÉTRICAS DE ERRO
# ===========================================
def calcular_erros(lbl, wsgg):
    """Retorna dicionário com erros ponto a ponto."""
    diff = wsgg - lbl                          # erro absoluto (diferença)
    rel = diff / lbl                           # erro relativo em relação ao LBL
    rel_sym = diff / ((np.abs(wsgg)+np.abs(lbl))/2)  # diferença relativa simétrica
    rmse = np.sqrt(np.mean(diff**2))
    mae = np.mean(np.abs(diff))
    max_abs = np.max(np.abs(diff))
    return {
        "diff": diff,
        "rel": rel,
        "rel_sym": rel_sym,
        "RMSE": rmse,
        "MAE": mae,
        "MAX_ABS": max_abs
    }

# ===========================================
# 3) CÁLCULO DOS ERROS PARA CADA PERCURSO
# ===========================================
erros_30 = calcular_erros(LBL_30, WSGG_30)
erros_10 = calcular_erros(LBL_10, WSGG_10)
erros_1  = calcular_erros(LBL_1,  WSGG_1)
erros_01 = calcular_erros(LBL_01, WSGG_01)

# ==========================
# 4) TABELA TEXTO NO TERMINAL
# ==========================
def imprimir_tabela(T, lbl, wsgg, erros, titulo):
    print("\n" + "="*70)
    print(titulo)
    print("="*70)
    print(f"{'T [K]':>6} | {'LBL':>10} | {'WSGG':>10} | {'Δ = WSGG-LBL':>13} | {'ERRO REL. %':>11}")
    print("-"*70)
    for Ti, li, wi, di, ri in zip(T, lbl, wsgg, erros["diff"], erros["rel"]):
        print(f"{Ti:6.0f} | {li:10.6f} | {wi:10.6f} | {di:13.6f} | {ri*100:11.3f}")

    print("-"*70)
    print(f"RMSE = {erros['RMSE']:.6e}")
    print(f"MAE  = {erros['MAE']:.6e}")
    print(f"MAX |Δ| = {erros['MAX_ABS']:.6e}")

imprimir_tabela(T, LBL_30, LBL_30 + erros_30["diff"], erros_30, "Percurso S = 30 m")
imprimir_tabela(T, LBL_10, LBL_10 + erros_10["diff"], erros_10, "Percurso S = 10 m")
imprimir_tabela(T, LBL_1,  LBL_1  + erros_1["diff"],  erros_1,  "Percurso S = 1 m")
imprimir_tabela(T, LBL_01, LBL_01 + erros_01["diff"], erros_01, "Percurso S = 0,1 m")

# ==========================
# 5) GRÁFICO DOS ERROS (CONFIGURAÇÃO PADRONIZADA)
# ==========================
fig, ax = plt.subplots(figsize=(8, 4.5))

ax.plot(T, erros_30["rel_sym"]*100, marker="o", label="S = 30 m")
ax.plot(T, erros_10["rel_sym"]*100, marker="s", label="S = 10 m")
ax.plot(T, erros_1["rel_sym"]*100,  marker="^", label="S = 1 m")
ax.plot(T, erros_01["rel_sym"]*100, marker="v", label="S = 0,1 m")

ax.axhline(0, linestyle="--", color="gray", linewidth=0.8)

ax.set_xlabel("Temperatura (K)", fontsize=18)
ax.set_ylabel("Erro relativo simétrico (%)", fontsize=18)
ax.set_title("Erro relativo simétrico (WSGG vs LBL)", fontsize=18)

ax.tick_params(axis='both', direction='in', length=5, width=0.8, labelsize=16)

ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.3)
ax.set_facecolor('white')

plt.legend(frameon=False, fontsize=16, loc='best')
plt.tight_layout()
plt.show()

# ==========================
# 6) GRÁFICO LBL vs WSGG (TODOS OS PERCURSOS, CONFIGURAÇÃO PADRONIZADA)
# ==========================
fig, ax = plt.subplots(figsize=(8, 4.5))

# --- S = 30 m ---
ax.plot(T, LBL_30,  marker="o", linestyle="-",  label="LBL 30 m")
ax.plot(T, WSGG_30, marker="o", linestyle="--", label="WSGG 30 m")

# --- S = 10 m ---
ax.plot(T, LBL_10,  marker="s", linestyle="-",  label="LBL 10 m")
ax.plot(T, WSGG_10, marker="s", linestyle="--", label="WSGG 10 m")

# --- S = 1 m ---
ax.plot(T, LBL_1,   marker="^", linestyle="-",  label="LBL 1 m")
ax.plot(T, WSGG_1,  marker="^", linestyle="--", label="WSGG 1 m")

# --- S = 0.1 m ---
ax.plot(T, LBL_01,   marker="v", linestyle="-",  label="LBL 0,1 m")
ax.plot(T, WSGG_01,  marker="v", linestyle="--", label="WSGG 0,1 m")

ax.set_xlabel("Temperatura (K)", fontsize=18)
ax.set_ylabel("Emitância", fontsize=18)
ax.set_title("Comparação entre as emitâncias LBL e WSGG", fontsize=18)

ax.tick_params(axis='both', direction='in', length=5, width=0.8, labelsize=16)

ax.set_ylim(0, 1)
ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.3)
ax.set_facecolor('white')

plt.legend(ncol=2, fontsize=16, frameon=False, loc='lower left')
plt.tight_layout()
plt.show()
