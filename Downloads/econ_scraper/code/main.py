import pandas as pd
from aer import getAER
from qje_restud import getQJE, getREStud
from jpe import getJPE
from ecta import getECTA

aerDf = getAER()
qjeDF = getQJE(1985, 2018)
jpeDF = getJPE(1988, 2018)
ectaDF = getECTA(1999, 2018)
restudDF = getREStud(1985, 2018)
top5DF = pd.concat([aerDF, qjeDF, jpeDF, ectaDF, restudDF], ignore_index=True)
top5DF.to_csv('../data/top5.csv')
