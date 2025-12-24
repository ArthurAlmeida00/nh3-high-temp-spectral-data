import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from io import StringIO

#Codigo gerado para realizar b_js polinomios do WSGG
# ===================== DADOS =====================
# Copie exatamente como está abaixo
data_txt = """
0,210462755  0,271103345  0,354155469  0,124222744  400  160000  64000000  25600000000,00
0,183476709  0,224688447  0,396635437  0,138032536  500  250000  125000000  62500000000,00
0,148745343  0,199171592  0,399167518  0,196054958  600  360000  216000000  129600000000,00
0,1171641    0,209508803  0,378652289  0,25157361   700  490000  343000000  240100000000,00
0,09178145   0,250637209  0,345180936  0,285689262  800  640000  512000000  409600000000,00
0,072014913  0,308406497  0,306348725  0,298844792  900  810000  729000000  656100000000,00
0,056540828  0,368531637  0,2672402    0,299733229  1000 1000000 1000000000 1000000000000,00
0,044322146  0,421420748  0,230410656  0,296696477  1100 1210000 1331000000 1464100000000,00
0,034644192  0,462014569  0,196886292  0,295448117  1200 1440000 1728000000 2073600000000,00
"""

# ===================== LEITURA DOS DADOS =====================
# decimal=',' → interpreta vírgula como separador decimal
# sep=r'\s+' → separador = qualquer quantidade de espaços/tab
df = pd.read_csv(StringIO(data_txt), 
                 sep=r'\s+', 
                 header=None, 
                 decimal=',')

df.columns = ['Y1', 'Y2', 'Y3', 'Y4', 'T', 'T2', 'T3', 'T4']

# ===================== REGRESSÕES MÚLTIPLAS =====================
# Variáveis independentes (preditoras)
X = df[['T', 'T2', 'T3', 'T4']]
X = sm.add_constant(X)  # adiciona termo constante (intercepto)

resultados = {}

for y in ['Y1', 'Y2', 'Y3', 'Y4']:
    modelo = sm.OLS(df[y], X)
    ajuste = modelo.fit()
    resultados[y] = ajuste
    
    print(f"\n==============================")
    print(f"      MODELO PARA {y}")
    print(f"==============================")
    print(ajuste.summary())

# ===================== GRÁFICO OBSERVADO x AJUSTADO =====================
for y in ['Y1', 'Y2', 'Y3', 'Y4']:
    ajuste = resultados[y]
    y_obs = df[y]
    y_pred = ajuste.fittedvalues
    
    plt.figure()
    plt.plot(df['T'], y_obs, 'o', label='Observado')
    plt.plot(df['T'], y_pred, '-s', label='Ajustado')
    plt.xlabel('Temperatura [K]')
    plt.ylabel(y)
    plt.title(f'Regressão múltipla para {y} em função de T, T², T³, T⁴')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
