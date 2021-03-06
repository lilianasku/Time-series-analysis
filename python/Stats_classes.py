#Stats functions

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#n_samples
def create_bootstraps(data_list, n_samples = 1):
    bs_list = []
    for number in range(n_samples):
        bs = np.random.choice(data_list, size = len(data_list))
        bs_list.append(bs)
    yield bs_list

#one bootstrap replica
def create_one_bootstrap(data_list, function):
    bs = np.random.choice(data_list, size = len(data_list))
    return function(bs)

#empirical cumulative distribution (ecdf)
def calculate_ecdf(data_list):
    n = len(data_list)
    x = np.sort(data_list)
    y = np.arange(1,len(x)+1)/n
    return x,y

def plot_ecdf(x,y):
    plt.plot(x,y,marker = '.', linestyle = 'none')
    plt.xlabel('x_variable')
    plt.ylabel('ECDF')
    plt.title('Empirical cumulative distribution')
    plt.show()

def overplot_percentile(x,y):
    percentile = np.array ([2.5, 25, 50, 75])
    per = np.percentile(x, percentile)
    plt.plot(x,y, marker = '.', linestyle = 'none')
    plt.plot(per, percentile/100, marker = 'D', color = 'red', linestyle = 'none')
    plt.xlabel('xaxis')
    plt.ylabel('ECDF')
    plt.title('Empirical cumulative distribution')
    plt.show()

def main():
    test_list = [2,4,7,8]
    assert len(test_list) != 0, 'Empty list'

    results = list(create_bootstraps(test_list,3))
    result = create_one_bootstrap(test_list,np.mean)

    x,y = calculate_ecdf(test_list)
    print(result)
    print(x,y)
    overplot_percentile(x,y)

if __name__=="__main__":
    main()
