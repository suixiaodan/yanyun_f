import numpy as np
import pandas as pd
import scipy.io as scio
from scipy.stats import pearsonr
import math
import os
import glob

def getonedata(filename):#convert one csv file into a datalist
    data = pd.read_csv(filename)
    data = data.drop('Unnamed: 0',axis=1)
    data = pd.DataFrame(data)
    data = np.array(data)
    where_are_inf = np.isinf(data)
    data[where_are_inf] = 100
    where_are_nan = np.isnan(data)
    data[where_are_nan] = 0
    data = (np.tril(data,-1))
    data = data.reshape((13456))
    return data

if __name__ == '__main__':

    subInfo = pd.read_excel('/neurolab/Data/ADNI_ROISignal/fmri_adni2_sort_new.xlsx')
    subInfo = subInfo[['Subject','dataName','Grouping','Sex','Age','DXCONV']]
    #subInfo = subInfo.drop_duplicates(subset=['Subject'], keep='first')
    # subInfo = subInfo[subInfo.Grouping.isin([1,5])]
    subData = np.zeros((13457))
    flist = glob.glob('*.csv')
    for item in subInfo['dataName']:
        item_new = item.replace("'","")
        subInfo['dataName'] = subInfo['dataName'].replace(item,item_new)
        filename = str('ROISignals_%s.csv'%item_new)
        # if subInfo['DXCONV']
        if filename in flist:
            if subInfo[subInfo['dataName'] == item_new]['DXCONV'].values < 4:
                print filename
                data = getonedata(filename)
                data = np.r_[np.array([str(item_new)]), data]
                subData = np.c_[subData,data]

    subData = subData.T
    subData = pd.DataFrame(subData)
    subData.rename(columns={0: 'dataName'}, inplace=True)
    df_data = pd.merge(subInfo, subData, how='inner', on=['dataName'])

    # df_data.to_csv('ADData.csv')

    df_data_nodup = df_data.drop_duplicates(subset=['Subject'], keep='first')
    df_data_nodup.to_csv('ADData_NoDup.csv')
    # df_data_res = df_data.append(df_data_nodup).drop_duplicates(subset=['dataName'], keep=False)

    ###test Riemann Kernel PCA on dataset
    from FeatureSelector import RiemannKernelPCA
    X = np.array(df)
    X = X[:,5:13461]
    kpca = RiemannKernelPCA.kpca(X,redu_dim=190)





    a = 1
