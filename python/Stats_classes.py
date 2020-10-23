#Stats functions and classes
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#functon for creating n_samples list of bootstraps
def create_bootstraps(data_list, n_samples=1):
    bs_list=[]
    for number in range(n_samples):
        bs=np.random.choice(data_list, size=len(data_list))
        bs_list.append(bs)
    yield bs_list

#functon for generating one bootstrap replica
def create_one_bootstrap(data_list, function):
    bs=np.random.choice(data_list, size=len(data_list))
    return function(bs)

#calculating empirical cumulative distribution ecdf
def calculate_ecdf(data_list):
    n=len(data_list)
    x=np.sort(data_list)
    y=np.arange(1,len(x)+1)/n
    return x,y

def main():
   test_list=[2,4,7,8]
   assert len(test_list)!=0, 'Empty list'
   results=list(create_bootstraps(test_list,3))
   result= create_one_bootstrap(test_list,np.mean)
   ecdf=calculate_ecdf(test_list)
   print(result)
   print(ecdf)

if __name__=="__main__":
    main()
