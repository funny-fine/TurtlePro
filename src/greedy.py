import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, date, timedelta
a = pd.read_csv(r'BCHAIN-MKPRU.txt')
bitcoin_date = np.array(a['Date'])
bitcoin_value = np.array(a['Value'])

aa = pd.read_csv(r'LBMA-GOLD21.txt')
gold_date = np.array(aa['Date'])
gold_value = np.array(aa['USD (PM)'])
sumdiff=0


for i in range(1266):
    a = gold_date[i]
    b = a.split('/')
    gold_date[i] = '20' + b[2] + '-' + b[0] + '-' + b[1]
for i in range(1265):
    t1 = datetime.strptime(gold_date[i], "%Y-%m-%d")
    t2 = datetime.strptime(gold_date[i+1], "%Y-%m-%d")
    if int(str(t2-t1)[0]) != 1:
        diff = int(str(t2-t1)[0])
        for j in range(1, diff):
            gold_value = np.insert(gold_value, i+j+sumdiff, gold_value[i+sumdiff])
        sumdiff += diff - 1


firstvalue=1000
bit_num = []
gold_num = []
value = []
value.append(firstvalue)
sumvalue = []
Flag1 = 0
Flag2 = 0
bitnum_new = 0
goldnum_new = 0

for i in range(1825):


    if bitcoin_value[i + 1] - bitcoin_value[i]<0:
        bitnum_new = -sum(bit_num)
        if 0.02 * bitnum_new * bitcoin_value[i] > bitnum_new*(bitcoin_value[i+1] - bitcoin_value[i]):
            bit_num.append(-sum(bit_num))
            print(0)
            if bitnum_new<0:
                Flag1=-1
        else:
            bitnum_new = 0
            bit_num.append(0)
            Flag1 = 0

    if gold_value[i + 1] - gold_value[i]<0:
        goldnum_new = -sum(gold_num)
        if 0.01 * goldnum_new * gold_value[i] > goldnum_new * (gold_value[i] - gold_value[i+1]):
            gold_num.append(-sum(gold_num))
            print(0)
            if goldnum_new < 0:
                Flag2 = -1
        else:
            goldnum_new= 0
            gold_num.append(0)
            Flag2 = 0

    if bitcoin_value[i + 1] - bitcoin_value[i] > 0:

        if bitcoin_value[i+1] - bitcoin_value[i] > gold_value[i+1] - gold_value[i] and (gold_value[i+1] - gold_value[i])>=0:
            bitnum_new = round(value_new / bitcoin_value[i],1)
            if 0.02 * bitnum_new * bitcoin_value[i] < bitnum_new*(bitcoin_value[i + 1] - bitcoin_value[i]):
                bit_num.append(bitnum_new)
                if bitnum_new > 0:
                    Flag1 = 1
            else:
                bitnum_new = 0
                bit_num.append(0)
                Flag1 = 0
            goldnum_new = 0
            gold_num.append(0)
            Flag2=0

        if bitcoin_value[i+1] - bitcoin_value[i] < gold_value[i+1] - gold_value[i]:
            goldnum_new = round(value_new / gold_value[i],1)
            if 0.01 * goldnum_new * gold_value[i] <goldnum_new*(gold_value[i + 1] - gold_value[i]):
                gold_num.append(goldnum_new)
                if goldnum_new > 0:
                    Flag2 = 1
            else:
                goldnum_new = 0
                gold_num.append(0)
                Flag2 = 0
            bitnum_new = 0
            bit_num.append(0)
            Flag1 = 0

        if (gold_value[i+1] - gold_value[i])<0:
            bitnum_new = round(value_new / bitcoin_value[i],1)
            if 0.02 * bitnum_new * bitcoin_value[i] < bitnum_new*(bitcoin_value[i + 1] - bitcoin_value[i]):
                bit_num.append(bitnum_new)
                if bitnum_new > 0:
                    Flag1 = 1
            else:
                bitnum_new= 0
                bit_num.append(0)
                Flag1 = 0

    if gold_value[i+1] - gold_value[i] > 0:
        if (bitcoin_value[i+1] - bitcoin_value[i])<0:
            goldnum_new = round(value_new / gold_value[i],1)
            if 0.01 * goldnum_new * gold_value[i] < goldnum_new*(gold_value[i + 1] - gold_value[i]):
                gold_num.append(goldnum_new)
                if goldnum_new > 0:
                    Flag2 = 1
            else:
                goldnum_new = 0
                gold_num.append(0)
                Flag2 = 0
    value_new = round(value[i] - bitnum_new * bitcoin_value[i] - goldnum_new * gold_value[i] - Flag1 * 0.02 * bitnum_new * bitcoin_value[i] - Flag2 * 0.01 * goldnum_new * gold_value[i],2)
    value.append(value_new)
    sum_value = round(value_new + sum(bit_num) * bitcoin_value[i] + sum(gold_num) * gold_value[i],2)
    sumvalue.append(sum_value)
print(sumvalue)
print(len(value))

plt.plot(sumvalue)
plt.show()


