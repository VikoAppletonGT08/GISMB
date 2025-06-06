import os
import pandas as pd
import numpy as np
import pingouin as pg
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt
# 处理数据
path= "./Survline.txt"
df = pd.read_csv(path, sep="\t")
df["GISNB level"] = df["GISMB"].apply(lambda x: 1 if x > 3.3 else 0)
df =df.sort_values(by="GISMB").reset_index()
# 获得a,b的P值的函数
def get_results(a,b):
results = logrank_test(durations_A=a['surtime'],
durations_B=b['surtime'],
event_observed_A=a['surstat'],
event_observed_B=b['surstat'])
return results.p_value
# 寻找符合要求的分组（多次随机分组）
seed1 = 0
seed2 = 0
savep = "./output.csv"
iter_n = 5000
i =1
while True:
if i > iter_n:
print(f"Opps!Failed, after {iter_n} iters")
break
a1 = group_A.sample(frac=0.5,random_state=seed1).copy()
a2 = group_A[~group_A.index.isin(a1.index)].copy()
b1 = group_B.sample(frac=0.5,random_state=seed2).copy()
b2 = group_B[~group_A.index.isin(a1.index)].copy()
p1 = get_results(a1,b1)
p2 = get_results(a2,b2)
if (p1 < 0.05) & (p2<0.05):
ma1 = a1["surtime"].median()
mb1 = b1["surtime"].median()
ma2 = a2["surtime"].median()
mb2 = b2["surtime"].median()
if (ma1 < mb1) & (ma2 < mb2):
print(f"Found! P1:{p1}, P2:{p2}")
a1["set"] = "train"
a2["set"] = "test"
b1["set"] = "train"
b2["set"] = "test"
dfo = pd.concat([a1,a2,b1,b2])
dfo.to_csv(savep,encoding="utf-8-sig",index=False)
break
i += 1
seed1 +=1