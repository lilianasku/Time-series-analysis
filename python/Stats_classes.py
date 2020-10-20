#Stats functions and classes

import sys
import numpy as np
import pandas as pd

#functon for creating n_samples list of bootstraps
def create_bootstraps(data_list, n_samples=1):
    assert len(data_list)!=0, 'Empty list'
    bs_list=[]
    for number in range(n_samples):
        bs=np.random.choice(data_list, size=len(data_list))
        bs_list.append(bs)
    yield bs_list

def main():
   l=[2,4,7,8]
   results=list(create_bootstraps(l,3))

if __name__=="__main__":
    main()
