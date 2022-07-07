import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, date, timedelta
import talib
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

bit01 = []
gold01 = []
for i in range(1825):
    if bitcoin_value[i + 1] - bitcoin_value[i] < 0:
        bit01.append(0)
    if bitcoin_value[i + 1] - bitcoin_value[i] > 0:
        bit01.append(1)
    if gold_value[i + 1] - gold_value[i] < 0:
        gold01.append(0)
    if gold_value[i + 1] - gold_value[i] > 0:
        gold01.append(1)



x = 10
ATR = 1
beta = 1
d = 1
y = 1
z = 1
m = 0.5
k = 5
n = 0.1
t1 = 1
t2 = 1
firstvalue=1000
bit_num = []
gold_num = []
value = []
value.append(firstvalue)
sumvalue = []
Flag1 = 0 #
Flag2 = 0 #
valuenew_bit = 0
valuenew_gold = 0
last_price_bit = 0
last_price_gold = 0  #
pingcangtiaojian1 = 0
pingcangtiaojian2 = 0

def one_unit(x, atr, sumvalue):
    if atr > 40:
        one_u = 10*x*0.01*sumvalue/atr
    elif atr > 100:
        one_u = 40 * x * 0.01 * sumvalue / atr
    else:
        one_u = x * 0.01 * sumvalue / atr
    return one_u


def get_atr(high, low, close):
    atr_array=[]
    for i in range(20):
        atr_array.append(max(abs(high[i]-low[i]),abs(high[i]-close[i]),abs(low[i]-close[i])))

    atr = np.mean(atr_array)
    return atr


def get_high_low_close_bit(time):
    close=[]
    high=[]
    low=[]
    for i in range(20,0,-1):
        close.append(bitcoin_value[time-i])
        high.append(max(max(bitcoin_value[time-i-10:time-i]), max(bitcoin_value[time-i:time-i+5])))
        low.append(min(min(bitcoin_value[time - i - 10:time - i]), min(bitcoin_value[time - i:time - i + 5])))
    high = np.array(high)
    low = np.array(low)
    close = np.array(close)
    return high,low,close


def get_high_low_close_gold(time):
    close=[]
    high=[]
    low=[]
    for i in range(20,0,-1):
        close.append(gold_value[time-i])
        high.append(max(max(gold_value[time-i-10:time-i]), max(gold_value[time-i:time-i+5])))
        low.append(min(min(gold_value[time - i - 10:time - i]), min(gold_value[time - i:time - i + 5])))
    high = np.array(high)
    low = np.array(low)
    close = np.array(close)
    return high,low,close


def jiacang_bit(sumvalue, price, high, low, close):
    last_price_bit = price
    bitnum_new = one_unit(x, get_atr(high, low, close), sumvalue)/price
    bit_num.append(bitnum_new)

    valuenew_bit = bitnum_new*price + 0.02 * bitnum_new * price
    print(bitnum_new * price)
    return last_price_bit, valuenew_bit


def jiacang_gold(sumvalue, price, high, low, close):
    last_price_gold = price
    goldnum_new = one_unit(x, get_atr(high, low, close), sumvalue)/price
    gold_num.append(goldnum_new)


    valuenew_gold = goldnum_new*price + 0.01 * goldnum_new * price

    return last_price_gold, valuenew_gold


def zhisun_bit(sumvalue, price, high, low, close):
    last_price_bit = price
    bitnum_new = one_unit(x, get_atr(high, low, close),sumvalue)/price
    bit_num.append(-bitnum_new)

    valuenew_bit = -bitnum_new * price + 0.02 * bitnum_new * price
    print(bitnum_new * price)
    return last_price_bit, valuenew_bit


def zhisun_gold(sumvalue, price, high, low, close):
    last_price_gold = price
    goldnum_new = one_unit(x, get_atr(high, low, close),sumvalue)/price
    gold_num.append(-goldnum_new)

    valuenew_gold = -goldnum_new*price + 0.01 * goldnum_new * price

    return last_price_gold, valuenew_gold


def pingcang_bit(price):
    last_price_bit = price
    bitnum_new = sum(bit_num)
    bit_num.append(-bitnum_new)

    valuenew_bit = -bitnum_new * price + 0.02 * bitnum_new * price
    return last_price_bit, valuenew_bit


def pingcang_gold(price):
    last_price_gold = price
    goldnum_new = sum(gold_num)
    gold_num.append(-goldnum_new)

    valuenew_gold = -goldnum_new * price + 0.02 * goldnum_new * price
    return last_price_gold, valuenew_gold


for i in range(30, 1825):

    if Flag1 == 0 and bitcoin_value[i] > max(bitcoin_value[i-20:i]):
        high_bit, low_bit, close_bit = get_high_low_close_bit(i)

        last_price_bit, valuenew_bit = jiacang_bit(sum_value, bitcoin_value[i], high_bit, low_bit, close_bit)
        Flag1 = 1
    if Flag2 == 0 and gold_value[i] > max(gold_value[i - 20:i]):
        high_gold, low_gold, close_gold = get_high_low_close_gold(i)

        last_price_gold, valuenew_gold = jiacang_gold(sum_value, gold_value[i], high_gold, low_gold, close_gold)
        Flag2 = 1

    if Flag1 == 1:
        high_bit, low_bit, close_bit = get_high_low_close_bit(i)

        if (bitcoin_value[i] - last_price_bit) > 0.01*get_atr(high_bit, low_bit, close_bit) or \
                (last_price_bit-bitcoin_value[i])>10*get_atr(high_bit, low_bit, close_bit):


            last_price_bit, valuenew_bit = jiacang_bit(sum_value, bitcoin_value[i], high_bit, low_bit, close_bit)

        elif (last_price_bit - bitcoin_value[i]) > 0.3*get_atr(high_bit, low_bit, close_bit) :

            last_price_bit, valuenew_bit = zhisun_bit(sum_value,bitcoin_value[i], high_bit, low_bit,close_bit)

        elif sum(bit01[i-4:i+1]) == 0:

            for j in range(i-4, i+1):
                if (bitcoin_value[j]-bitcoin_value[j-1]) >= -0.1*get_atr(high_bit, low_bit, close_bit):
                    pingcangtiaojian1 += 1

            if pingcangtiaojian1 == k:
                last_price_bit, valuenew_bit = pingcang_bit(bitcoin_value[i])
                Flag1 = 0

            else:
                bit_num.append(0)
                valuenew_bit = 0

        else:
            bit_num.append(0)
            valuenew_bit = 0


    if Flag2 == 1:
        high_gold, low_gold, close_gold = get_high_low_close_gold(i)

        if (gold_value[i] - last_price_gold) > 1*get_atr(high_gold, low_gold, close_gold):

            last_price_gold, valuenew_gold = jiacang_gold(value_new, gold_value[i], high_gold, low_gold, close_gold)

        elif (last_price_gold - gold_value[i]) > 20*get_atr(high_gold, low_gold, close_gold):
            last_price_gold, valuenew_gold = zhisun_gold(value_new,gold_value[i], high_gold, low_gold,close_gold)

        elif sum(gold01[i-4: i+1]) == 0:
            for j in range(i - 4, i + 1):
                if (gold_value[j] - gold_value[j - 1]) >= n * get_atr(high_gold, low_gold, close_gold):
                    pingcangtiaojian2 += 1

            if pingcangtiaojian2 == k:
                last_price_gold, valuenew_gold = pingcang_gold(gold_value[i])
                Flag2 = 0

            else:
                gold_num.append(0)
                valuenew_gold = 0


        else:
            gold_num.append(0)
            valuenew_gold = 0

    value_new = value[i-30]-valuenew_bit-valuenew_gold

    value.append(value_new)
    sum_value = value_new + sum(bit_num) * bitcoin_value[i] + sum(gold_num) * gold_value[i]
    sumvalue.append(sum_value)
    pingcangtiaojian1 = 0
    pingcangtiaojian2 = 0
print(sumvalue)



plt.plot(sumvalue[0:1770])
# plt.plot(gold_num)
plt.show()

