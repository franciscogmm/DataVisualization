import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn_pandas import DataFrameMapper

def na_handling(data, arg):
    '''
    
    select whether to delete, interpolation to handle rows with NAs
    
    '''
    if arg == 1:
        data_nona = data.dropna()
        if (len(data_nona.index) == len(data.index)):
            pass
        else:
            print 'Rows: From ' + str(len(data.index)) + ' to ' + str(len(data_nona.index))
    elif arg == 2:
        data_nona = data.interpolate()
        # if time series, method='quadratic'
        # if values approximating a cumulative distribution function, method = 'pchip'
        # if goal of smooth plotting, method='akima'
        data_nona = data_nona.dropna() #drop all rows that were not imputed
        print 'Remaining decreased to ' + str(len(data_nona.index)) + ' from ' + str(len(data.index))
    else:
        print 'arg = 1 or 2'
        print 'call function again'
    return data_nona

def get_numerical_columns(dataset_input):
    return list(dataset_input.select_dtypes(include=['float32', 'float64', 'int32', 'int64']).columns)

def get_categorical_columns(dataset_input):
    return list(dataset_input.select_dtypes(include=['O']).columns)

def preprocess_cat(dataset_input):
    dataset_input = remove_inc_variables(dataset_input, 0.1)
    dataset_input = na_handling(dataset_input, 1)
    categories =  get_categorical_columns(dataset_input)
    numbers = get_numerical_columns(dataset_input)

    mapper = DataFrameMapper(
            [(category, preprocessing.LabelEncoder()) for category in categories] +
            [(number, None) for number in numbers], df_out = True)
    
    transformedData = mapper.fit_transform(dataset_input)
    dummified = pd.get_dummies(transformedData, columns = categories)
    #print list(dummified.columns)
    drops = []
    for i in categories:
        dummy_i = [col for col in dummified.columns if i in col]
        #print "Dummify Variable - ",i, dummy_i
        #drop the 1st of the list
        drops.append(dummy_i[0])
    #print drops
    dataset_input2 = dummified.drop(drops, axis = 1)
    return dataset_input2, mapper, numbers

def preprocess_num(dataset_input, num_cols):

    numbers = num_cols
    categories = [col for col in list(dataset_input.columns) if col not in numbers][1:]
    means_dict = {}
    std_dict = {}
    
    #save means and std of fit
    for i in numbers:
        means_dict[i] = dataset_input.ix[:,i].mean()
        std_dict[i] = dataset_input.ix[:,i].std(ddof=0)
    
    mapper = DataFrameMapper(
            [(category, None) for category in categories] +
            [(number, preprocessing.StandardScaler()) for number in numbers], df_out = True)
    
    transformedData = mapper.fit_transform(dataset_input)
    return transformedData, mapper, means_dict, std_dict

def remove_inc_variables(data, pct):
    '''
    
    Check Missing Values - col wise, then row-wise
    if missing values per column is greater than 10% of total row count, remove
    
    '''
    col_to_keep = []
    starting = len(data.columns)
    for i in range(len(data.columns)):
        if (float(data.iloc[:,i].isnull().sum().tolist()) / float(len(data.index))) > pct:
            print str(data.iloc[:,i].name) + " Removing | NAs: " + str(round(float(data.iloc[:,i].isnull().sum().tolist()) / float(len(data.index)),2))
        else:
            col_to_keep.append(i)
    data_nona = data.iloc[:,col_to_keep]
    ending = len(data_nona.columns)
    print "Variables: From %d to %d" % (starting, ending)
    return data_nona