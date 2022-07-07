import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
a = pd.read_csv(r'BCHAIN-MKPRU.txt')
f = np.array(a)

bit_price = f[:1825]
sumvalue_end=[]

bit_num = []
value = []
sumvalue = []
valuefirst = 1000
bitnum_new = random.uniform(0, 1)
bitnum_new = round(bitnum_new,1)
bit_num.append(bitnum_new)
value.append(valuefirst)
Flag = 1

for i in range(1824):
    value_new = value[i]-bitnum_new*bit_price[i][1] - Flag* 0.01*bitnum_new*bit_price[i][1]
    value.append(value_new)
    sum_value = value_new + sum(bit_num) * bit_price[i][1]
    sumvalue.append(sum_value)
    bitnum_new = random.uniform(-1*sum(bit_num), value_new//bit_price[i+1][1])
    bitnum_new = round(bitnum_new, 1)
    if bitnum_new < 0:
        Flag = -1
    else:
        Flag = 1
    bit_num.append(bitnum_new)
    # sumvalue_end.append(sumvalue[1823])

plt.plot(sumvalue)
# plt.scatter(np.arange(300), sumvalue_end,marker='o',  c='green',cmap='Oranges')
plt.show()
