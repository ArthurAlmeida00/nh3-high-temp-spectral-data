import numpy as np                    # NumPy: leitura/organização numérica (vetores/matrizes)
import matplotlib.pyplot as plt       # Matplotlib: criação de gráficos
from matplotlib.ticker import MultipleLocator  # Controle do espaçamento dos *ticks* (marcas de eixo)
#CODIGO USADO PARA FAZER UM GRAFICO COM O BANCO DE DADOS EXOMOL
# Caminho do arquivo de dados (.xsec) com número de onda (cm^-1) e seção de choque (cm^2/molecule)
arq = r'C:'

# Leitura do arquivo como matriz float; coluna 0 = número de onda; coluna 1 = seção de choque
data = np.loadtxt(arq, dtype=float)
x, y = data[:,0], data[:,1]

# Criação da figura e do eixo principal (ax1) com tamanho apropriado para publicação
fig, ax1 = plt.subplots(figsize=(8, 4.5))

# Curva do espectro (linha azul fina)
ax1.plot(x, y, color='#0072B2', linewidth=1.0, label='T = 1200 K')

# Escala logarítmica no eixo Y (seção de choque varia em muitas ordens de grandeza)
ax1.set_yscale('log')

# Limites do eixo X em número de onda: evita 0 (divisão por zero no eixo superior) e exibe até 12000 cm^-1
ax1.set_xlim(50, 12100)

# Rótulos dos eixos com notação científica apropriada
ax1.set_xlabel(r'Wavenumber (cm$^{-1}$)', fontsize=13)
ax1.set_ylabel(r'Cross-section (cm$^{2}$/molecule)', fontsize=13)

# Estilo dos *ticks*: voltados para dentro, tamanho consistente; remove poluição visual
ax1.tick_params(axis='both', direction='in', length=5, width=0.8, labelsize=11)

# Remoção das bordas superior e direita (estética típica de artigos)
for s in ['top', 'right']:
    ax1.spines[s].set_visible(False)

# ------------------- Eixo superior (comprimento de onda em micrômetros) -------------------

# Transformações entre número de onda (cm^-1) e comprimento de onda (µm)
def num_to_lambda(v): return 1e4 / v   # cm^-1 -> µm
def lambda_to_num(l): return 1e4 / l   # µm -> cm^-1

# Criação do eixo secundário no topo, acoplado ao eixo X principal via transformações acima
secax = ax1.secondary_xaxis('top', functions=(num_to_lambda, lambda_to_num))

# Rótulo do eixo superior
secax.set_xlabel(r'Wavelength ($\mu$m)', fontsize=13)

# Marcas específicas desejadas em µm (de 100 até ~0,833 µm) e rótulos sem zeros desnecessários
lambda_ticks = [100, 10, 5, 4, 3, 2.5, 2, 1.5, 1.25, 1, 0.833]
secax.set_xticks(lambda_ticks)
secax.set_xticklabels([f'{t:g}' for t in lambda_ticks])  # formatação compacta (100, 10, 2.5, 0.833, ...)
secax.tick_params(axis='x', labelrotation=0, labelsize=11)

# ------------------- Grid e espaçamento das marcas -------------------

# Define espaçamento das marcas principais do eixo X a cada 2000 cm^-1 (menos linhas de grade)
ax1.xaxis.set_major_locator(MultipleLocator(2000))

# Grade principal sutil (tracejada, fina, semi-transparente) para leitura sem poluir
ax1.grid(which='major', color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

# Fundo branco do painel do gráfico
ax1.set_facecolor('white')

# Legenda sem moldura, no canto superior direito
plt.legend(frameon=False, fontsize=11, loc='upper right')

# Ajuste automático de margens para evitar sobreposição de textos
plt.tight_layout()
plt.show()
