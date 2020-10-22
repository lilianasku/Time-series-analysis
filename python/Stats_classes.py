#Stats functions and classes
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#functon for creating n_samples list of bootstraps
def create_bootstraps(data_list, n_samples=1):
    assert len(data_list)!=0, 'Empty list'
    bs_list=[]
    for number in range(n_samples):
        bs=np.random.choice(data_list, size=len(data_list))
        bs_list.append(bs)
    yield bs_list

#functon for generating one bootstrap replica
def create_one_bootstrap(data_list, function):
    assert len(data_list)!=0, 'Empty list'
    bs=np.random.choice(data_list, size=len(data_list))
    return function(bs)

#calculating empirical cumulative distribution ecdf
def calculate_ecdf(data):
    n=len(data)
    x=np.sort(data)
    y=np.arange(1,len(x)+1)/n
    return x,y

def main():
   l=[2,4,7,8]
   results=list(create_bootstraps(l,3))
   result= create_one_bootstrap(l,np.mean)
   print(result)


if __name__=="__main__":
    main()
