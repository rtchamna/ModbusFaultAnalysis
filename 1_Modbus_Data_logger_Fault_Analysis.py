#!/usr/bin/env python
# coding: utf-8

# # Import Libraries

# In[3]:
# map{reg: Alarm}
# Find the most comment Alarm
# Can we take any safe action for the Alarm
# Implement Action
# Current > 100 and < -100
# Combine everything in a Master File
# Histogram of type of Alarm 

 


import pandas as pd
import numpy as np
import fileinput
from collections import Counter
import os
import sys
from itertools import groupby
from csv import writer

import matplotlib.pyplot as plt

# Using plotly.express
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time


# # Data Preprocessing

# ## Define Functions to Import and Transform the Data

# In[4]:

# Fault_Type = "Alarms"

Fault_Type =  sys.argv[-1]
# print (Fault_Type)

# kkkkkkkkkkkkkkkkkkkkkkkkkk

dict_fault_type = {"Warnings":[2283, 2298], "Alarms":[2299, 2314], "Faults":[2315, 2342], "User_Clear_Faults":[2343, 2370]}


def from_text_to_csv(file_path):
    print('converting txt to csv')
    now = time.time()
    df = pd.read_csv(file_path, sep='\t', skiprows=12).reset_index()
    df.columns = [*df.columns[1:], None]
    print(f'converting txt to csv. time spent = {int(time.time() - now)}s')
    return df

    
def transforming_and_saving_data_to_csv(df,file_path):
    
    
    import time 
    
    start_time = time.time()
    
    lenght_extension = 4
    filename_no_extension = file_path[0:len(file_path)-lenght_extension]
    
    head_line_number = 12

    df_dated = df.iloc[head_line_number+1:,:-1]

    df_dated.to_csv(f"{filename_no_extension}.csv")
    
    end_time = time.time()

    time_taken = end_time-start_time

    

    print("Execution time in seconds: ",time_taken)
    
    return df_dated

# In[ ]:





# file_path_ = "bcb-modbus-Harmony-2022-06-29-04-00-01.txt"
# file_path_ = "bcb-modbus-Harmony-2022-10-17-04-00-01.txt"

file_path_ = sys.argv[1]
Results_folder = sys.argv[2]
Results_Split_folder = sys.argv[3]
NaN_folder = sys.argv[4]


# print(NaN_folder)
# kkkkkkkkkkkkkkkkkkkkkkkkkk
# C:\Users\Rtchamna\Downloads\bcb_modbus_Harmony\NaN_folder\C:\Users\Rtchamna\Downloads\bcb_modbus_Harmony'

file_name_no_ext = os.path.splitext(file_path_)[0]

df = from_text_to_csv(file_path_)


# ## Saving the Transformed Csv
# Saving is optional, NOT necessary. Took about: **2 min:05 s** for a **775 MB** file 
# 

# In[7]:


# df_transformed = transforming_and_saving_data_to_csv(df,file_path_)


# In[8]:


# df = df_transformed


# In[25]:


# # mask = df.isnull().values.any()
# try:

    # os.mkdir("Results_Split_folder")
    # os.mkdir("Results_folder")
    # os.mkdir("NaN_folder")
    
# except Exception as ex:
    # print("folder already exists!",ex)
    
pd.options.mode.chained_assignment = None  # default='warn'

# Results_Split_folder = os.getcwd()+"\\Results_Split_folder\\"  
# Results_folder = os.getcwd()+"\\Results_folder\\"  
# NaN_folder = os.getcwd()+"\\NaN_folder\\" 


file_name_no_ext = os.path.basename(file_name_no_ext)

df_isna = df[df.isna().any(axis=1)]
df_isna.to_csv(os.path.join(NaN_folder, f"{file_name_no_ext}_NAN.csv"))

# In[27]:


df_no_nan = df.dropna()


# ## Transform 'Numeric' Strings to Real Numeric
# This process takes around **2 min**

# In[28]:


# The data are seen as strings, for example '3' we need to transform them as numeric
# print(df["87"][0])

start_time = time.time()

numeric_columns = [i for i in df.columns if str(i).isnumeric()]
temp1 = df_no_nan[['Count',  'Date',  'Time']]
temp2 = df_no_nan[numeric_columns].astype(int)
temp3 = df_no_nan[[None]]
df = pd.concat([temp1, temp2, temp3], axis=1)

# GET Non Zeros-Current 

df = df[(df["169"]>100) | (df["169"]<-100)]

end_time = time.time()

time_taken = end_time-start_time

print("Execution time in seconds: ",time_taken)

# print(df["87"][0])


# In[ ]:





# In[29]:


cwd = os.getcwd()
cwd 


# # Begining of the Program

# ## Functions Definitions

# In[30]:


# file_name = "bcb-modbus-Harmony-2022-06-29-04-00-01.csv"
# file_name = "bcb-modbus-Harmony-2022-10-17-04-00-01.csv"

# df = pd.read_csv(file_name)
# display(df.head())
# df = df.reset_index(drop=True)
# df.head()


# In[31]:


# try:

#     os.mkdir("Results_Split_folder")
#     os.mkdir("Results_folder")
# except Exception as ex:
#     print("folder already exists!",ex)
# pd.options.mode.chained_assignment = None  # default='warn'


# In[32]:


# columns_of_interes = [2,4,7,9]
# data_key = df.iloc[:,columns_of_interes[0]]

# values_indexes = columns_of_interes[1:]
# print(values_indexes)

# for i in values_indexes:
    # print(i)

    # globals()[f"data_val{i}"] = df.iloc[:,i]
# #     data_curr = data.iloc[:,columns_of_interest[2]]
    # tt = (globals()[f"data_val{i}"] for i in values_indexes  )
# #     tuple_from_dict = tuple(zip(data_key,data_val,data_cur

# In[ ]:


# df.columns.get_loc("Date")


# In[ ]:


# data_list [[2112, 2112, 2112, 2112, 2112], [366, 366, 359, 359, 328], [7869, 7869, 7868, 7868, 7866]]


# In[35]:


starting_column_index_of_interest = 169

date_idx = df.columns.get_loc("Date")
time_idx = df.columns.get_loc("Time")
current_idx = df.columns.get_loc("169")
voltage_idx = df.columns.get_loc("170")

columns_of_interest = df.columns.get_loc("2317")
# register_number_idx = df.columns.get_loc("171") # This will vary

start_index = df.columns.get_loc(f"{starting_column_index_of_interest}")

# # Data_of_interest["datetime"] = Data_of_interest["Date"]+" "+Data_of_interest["Time"]
# # Data_of_interest = Data_of_interest[["datetime",column_label,column_current]]
    
def data_grouping(data, data_subset = [time_idx,columns_of_interest,current_idx,voltage_idx]):
    
    """
    This function is used as follows: 
    
    - If the input is a List, the output is a dictionary of the indexes and values where the values of 
    the list change. In this case you dont need to add the columns_of_interest variable
    
    - If the input is a Dictionary, then the output will be a dictionary of items where the values of 
    the dictionary change. In this case you dont need to add the columns_of_interest variable
    
    - If the input is a DataFrame, then the output will be a list of the group of values of the columns of interest 
    In this case the columns_of_interest variable Must be the second element of the subset list 
    data frame you are interested in. The fist element is the key, the second element is the column you want to
    group by
    """
    
    if type(data) == list: # isinstance(data,list)
        change_list = [(i,data[i]) for i in range(1,len(data)) if data[i]!= data[i-1] ]
        Flag = constant_value_sign(data,change_list)
        
    elif type(data) == dict: # isinstance(data,dict)
        tuple_from_dict = tuple(zip(data.keys(),data.values()))
        change_list = [(val[0],val[1]) for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
                       tuple_from_dict[indx-1][1] ]
        
        Flag = constant_value_sign(data,change_list)
        
    elif isinstance(data, pd.DataFrame):

        data_key = data.iloc[:,data_subset[0]]
        
#         print(data_key)
        
        data_list = []
        for i in data_subset:
            
           

            val = data.iloc[:,i]           
            
            data_list.append(list(val))
            
#         print("data_list", data_list)
        tuple_from_dict = tuple(zip(*data_list))
        
#         print("tuple_from_dict",len(tuple_from_dict))
        

#         tuple_from_dict = tuple(zip(data_key,data_val,data_curr))
        change_list = [val for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
                       tuple_from_dict[indx-1][1] ]
        Flag = constant_value_sign(data,change_list)
    
    else:
        print("Please enter either a list a dictionary or a Data Frame...")
    
    return change_list, Flag



def constant_value_sign(data,change_list):
    
    """
    This function will take a list, a dictionary, or a dataframe as input, 
    and tell you if all the values are either positive, all negatives, or zeros, or mixed values
    
    """
    
    columns_label = data.columns[1]

    if type(data) == list:
        change_list = [(i,data[i]) for i in range(1,len(data)) if data[i]!= data[i-1] ]
        
        if len(change_list)== 0:
            if data[0] < 0:
                print(f"{columns_label}: All Values are Negative...")
                Flag = "All_Negative"
            elif data[0] > 0:
                print(f"{columns_label}: All Values are Positive...")
                Flag = "All_Positive"
            else:
                print(f"{columns_label}: All Values are Zero...")
                Flag = "All_Zero"
        else:
            Flag = "Mixed_Values"
    elif type(data) == dict: # isinstance(data,dict)
        
        tuple_from_dict = tuple(zip(data.keys(),data.values()))
        change_list = [(val[0],val[1]) for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
                       tuple_from_dict[indx-1][1] ]
        
        if len(change_list)== 0:
            if list(ddd.values())[0] < 0:
                print(f"{columns_label}: All Values are Negative...")
                Flag = "All_Negative"
            elif list(ddd.values())[0] > 0:
                print(f"{columns_label}: All Values are Positive...")
                Flag = "All_Positive"
            else:
                print(f"{columns_label}: All Values are Zero...")
                Flag = "All_Zero"
        else:
            Flag = "Mixed_Values"
            
    elif isinstance(data, pd.DataFrame):
        
        data_key = data.iloc[:,0] 
        data_val = data.iloc[:,1]
        data_curr = data.iloc[:,-1]
        

        tuple_from_dict = tuple(zip(data_key,data_val,data_curr))
        change_list = [val for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
                       tuple_from_dict[indx-1][1] ]

        
        
        if len(change_list)== 0 and len(data) != 0:

                    if data.reset_index(drop=True).iloc[:,1][0] < 0:
                        print(f"{columns_label}: All Values are Negative...")
                        Flag = "All_Negative"
                    elif data.reset_index(drop=True).iloc[:,1][0] > 0:
                        print(f"{columns_label}: All Values are Positive...")
                        Flag = "All_Positive"
                    else:
                        print(f"{columns_label}: All Values are Zero...")
                        Flag = "All_Zero"
        elif len(change_list)== 0 and len(data) == 0:
            Flag = "Empty_Data"

        else:
            Flag = "Mixed_Values"


            
    return Flag

            
            
    
                
def index_value_change(data):
    
    """
    This function is used as follows: 
    
    - If the input is a List, the output is a dictionary of the indexes and values where the values of 
    the list change
    
    - If the input is a Dictionary, then the output will be a dictionary of items where the values of 
    the dictionary change
    
    - If the input is a DataFrame, then the output will be a dictionary of values where the values of the 
    2nd column change
    """
    
    if type(data) == list: # isinstance(data,list)
        change_list = [(i,data[i]) for i in range(1,len(data)) if data[i]!= data[i-1] ]
        
        Flag = constant_value_sign(data,change_list)
        
    elif type(data) == dict: # isinstance(data,dict)
        tuple_from_dict = tuple(zip(data.keys(),data.values()))
        change_list = [(val[0],val[1]) for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
                       tuple_from_dict[indx-1][1] ]
        
        Flag = constant_value_sign(data,change_list)

        
    elif isinstance(data, pd.DataFrame):

        data_key = data.iloc[:,0] 
        data_val = data.iloc[:,1]
        data_curr = data.iloc[:,-1]
        

        tuple_from_dict = tuple(zip(data_key,data_val,data_curr))
        change_list = [val for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
                       tuple_from_dict[indx-1][1] ]

        
        Flag = constant_value_sign(data,change_list)
        
        
    else:
        print("Please enter either a list a dictionary or a Data Frame...")
    
    return change_list, Flag


def index_value_change_sign(data):
    
    """
    This function is used as follows: 
    
    - If the input is a List, the output is a dictionary of the indexes and values where the values of 
    the list change sign
    
    - If the input is a Dictionary, then the output will be a dictionary of items where the values of 
    the dictionary change sign
    
    - If the input is a DataFrame, then the output will be a dictionary of values where the values of the 
    2nd column change sign
    """
    
    if type(data) == list: # isinstance(data,list)
        
#         arr = [3,3,3,3,3,3,0,0,3,6,6,6,1,0,0,0,0,0,-1,-5,-5]

        tuple_arr_pos_neg_zero = [(i,1) if data[i]>0 else (i,-1) if data[i]<0 else (i,0) for i in range(len(data))]
        dict_tuple_arr_pos_neg_zero = dict(tuple_arr_pos_neg_zero)

        tuple_from_dict = tuple(zip(dict_tuple_arr_pos_neg_zero.keys(),dict_tuple_arr_pos_neg_zero.values()))
        change_list = [(val[0],val[1]) for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
                               tuple_from_dict[indx-1][1] ]
        change_list  = [{i[0]:data[i[0]]} for i in change_list]
        
        Flag = constant_value_sign(data,change_list)
    
    elif type(data) == dict: # isinstance(data,dict)
        
        tuple_arr_pos_neg_zero = [(k,1) if data[k]>0 else (k,-1) if data[k]<0 else (k,0)  for k,v in data.items()]

        # tuple_arr_pos_neg_zero = [(i,1) if arr[i]>0 else (i,-1) if arr[i]<0 else (i,0) for i in range(len(arr))]
        dict_tuple_arr_pos_neg_zero = dict(tuple_arr_pos_neg_zero)
        
        tuple_from_dict = tuple(zip(dict_tuple_arr_pos_neg_zero.keys(),dict_tuple_arr_pos_neg_zero.values()))
        change_list = [(val[0],val[1]) for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
                               tuple_from_dict[indx-1][1] ]
        change_list  = [(i[0],data[i[0]]) for i in change_list]
        
        Flag = constant_value_sign(data,change_list)
        
    elif isinstance(data, pd.DataFrame):

#         data_key = data.iloc[:,0] 
#         data_val = data.iloc[:,1]
#         tuple_from_dict = tuple(zip(data_key,data_val))

        data_curr = data.iloc[:,-1]
    
        data_key = Data_of_interest.iloc[:,0] 
        zp = zip(list(Data_of_interest.iloc[:,1]),list(data_curr))
        data_val = tuple(zp)
        
        

        tuple_from_dict = tuple(zip(data_key,data_val))
#         tuple_from_dict_plus_current = tuple(zip(data_key,data_val,data_curr))
        data_dict = dict(tuple_from_dict)
      

        tuple_arr_pos_neg_zero = [(k,1) if data_dict[k][0]>0 else (k,-1) if data_dict[k][0]<0 else (k,0)  for k,v in data_dict.items()]

        # tuple_arr_pos_neg_zero = [(i,1) if arr[i]>0 else (i,-1) if arr[i]<0 else (i,0) for i in range(len(arr))]
        dict_tuple_arr_pos_neg_zero = dict(tuple_arr_pos_neg_zero)

        tuple_from_dict = tuple(zip(dict_tuple_arr_pos_neg_zero.keys(),dict_tuple_arr_pos_neg_zero.values()))
        
#         change_list = [(val[0],val[1]) for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
#                                tuple_from_dict[indx-1][1] ]
        
        change_list = [val for indx, val in enumerate(tuple_from_dict) if indx>0 and  tuple_from_dict[indx][1] !=  
                       tuple_from_dict[indx-1][1] ]



        
        change_list = [(i[0],data_dict[i[0]]) for i in change_list]
        
        Flag = constant_value_sign(data,change_list)

        
    else:
        print("Please enter either a list a dictionary or a Data Frame...")
        
    return change_list, Flag

def insert_first_row(list_, dataframe):
    # INSERT the first Row to the group
    
    # INSERT the first Row to the group
    
    if len(dataframe) != 0:

        data_key = dataframe.iloc[:,0] 
        data_val = dataframe.iloc[:,1] 
        data_curr = dataframe.iloc[:,2]
        data_volt = dataframe.iloc[:,3]
#         [('6/29/2022 04:05:47', 0, 269, 7873),

        tuple_from_dict = tuple(zip(data_key,data_val,data_curr,data_volt))  

        list_.insert(0,tuple_from_dict[0])
        return list_ 
    else:
        return list_
    
def list_of_tuples_to_dataframe(data,column_label, data_labels = ["datetime", "Register","Current" ]):
    first = [i[0] for i in data]
    second = [i[1] for i in data]
    third = [i[2] for i in data]

    data_df = pd.DataFrame({data_labels[0] : first, data_labels[1]+ f": {column_label}" : second, data_labels[2]: third})
#     data_df.to_csv(Results_Split_folder+'Group_Non_Zeros_Reduced.csv', mode='a', index=False, header=True)
    
    return data_df

def list_of_tuples_to_dataframe_(data,column_label, data_labels = ["datetime", "Register","Current","Voltage"]):
    first = [i[0] for i in data]
    second = [i[1] for i in data]
    third = [i[2] for i in data]
    fourth = [i[3] for i in data]

    data_df = pd.DataFrame({data_labels[0] : first, data_labels[1]+ f": {column_label}" : second, 
                            data_labels[2]: third, data_labels[3]: fourth})
#     data_df.to_csv(Results_Split_folder+'Group_Non_Zeros_Reduced.csv', mode='a', index=False, header=True)
    
    return data_df


# In[36]:


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
        csv_writer.writerows


# In[ ]:





# In[ ]:





# In[37]:

# #Warning Bitfield (0-15)	402283	402299
		# 0
# Alarm Bitfield (0-15)	402299	402315
		# 0
# Fault Bitfield (0-27)	402315	402343
		# 0
# User Clear Fault Bitfield (0-27)	402343	402371
		# 0
# Fixed Block	402371	402443


# starting_column_index_of_interest = 2283  # Warning
# ending_column_index_of_interest = 2298 # Warning

# starting_column_index_of_interest = 2299  # Alarm
# ending_column_index_of_interest = 2314 # Alarm

# starting_column_index_of_interest = 2315 # Fault
# ending_column_index_of_interest = 2342   # Fault


# starting_column_index_of_interest = 2343  # User Clear Fault
# ending_column_index_of_interest = 2370 # User Clear Fault


starting_column_index_of_interest = dict_fault_type[Fault_Type][0] 
ending_column_index_of_interest   = dict_fault_type[Fault_Type][1] 





date_idx = df.columns.get_loc("Date")
time_idx = df.columns.get_loc("Time")
current_idx = df.columns.get_loc("169")
voltage_idx = df.columns.get_loc("170")

start_index = df.columns.get_loc(f"{starting_column_index_of_interest}")
end_index = df.columns.get_loc(f"{ending_column_index_of_interest}")



for ii in range(start_index, end_index+1):
    
    column_label = df.columns[ii]
    
        
    #     selected_columns = np.r_[date_idx,time_idx, ii]
    
    
    #     start_index = df.columns.get_loc(f"{2317}")
    # selected_columns = np.r_[date_idx,time_idx, start_index]
    selected_columns = [date_idx,time_idx, ii,current_idx,voltage_idx]

    # selected_columns
    # df
    Data_of_interest = df.iloc[:,selected_columns]
    column_current = Data_of_interest.columns[-1]
    
    Data_of_interest["datetime"] = Data_of_interest["Date"]+" "+Data_of_interest["Time"]
        
    Data_of_interest = Data_of_interest.drop(["Date","Time"],axis=True)
    # data_col = list(Data_of_interest.columns)
    # Move the ending column to the first position 
    Data_of_interest.insert(0, 'datetime', Data_of_interest.pop('datetime'))

    
#     Data_of_interest = Data_of_interest[["datetime",column_label,column_current]]

    # Rename the columns 
    
    Data_of_interest.columns = ["datetime", f"Reg: {column_label}", "Current", "Voltage"] 
#     data_grouping(Data_of_interest, data_subset = [0,1,2,3])

    #     Data_of_interest = df.iloc[:,selected_columns]

    # column_of_interest = [abs(i) for i in Data_of_interest_zero.iloc[:,2]]
    series_of_interest = Data_of_interest.iloc[:,1]
    
    # Get Only Valid Current 
    
    # Data_of_interest = Data_of_interest[(Data_of_interest["Current"]>100) | (Data_of_interest["Current"]<-100)]
    
    #  Transform the string va
    
#     a = np.array(list(map(lambda x: int(x), series_of_interest)))

    
    column_of_interest = [i for i in series_of_interest]
    # column_of_interest = np.nansum(np.array(column_of_interest))


    #   Data_of_interest_zero
    #         Data_of_interest_zero.to_csv(f"Data_of_interest_zero{i}.csv")

    # zeros_indexes is a list of indexed where the data is zero
    zeros_indexes = np.where(series_of_interest == 0)[0]
    # non_zeros_indexes is a list of indexed where the data is not zero
    non_zeros_indexes = np.where(series_of_interest != 0)[0]
    positive_indexes = np.where(series_of_interest > 0)[0]
    negative_indexes = np.where(series_of_interest < 0)[0]

    #Dictionary of the count of each element in the list
    count_zeros_ = Counter(zeros_indexes)
    count_non_zeros_ = Counter(non_zeros_indexes)
    count_positive_ = Counter(positive_indexes)
    count_negative_ = Counter(negative_indexes)
    
    zeros_indexes_set = [i for i in count_zeros_.keys() ]
    non_zeros_indexes_set = [i for i in count_non_zeros_.keys() ]
    
    positive_indexes_set = [i for i in count_positive_.keys() ]
    negative_indexes_set = [i for i in count_negative_.keys() ]
    
    #   zeros_indexes_set

    # if column_of_interest == 0:        

    #   append_list_as_row('Data_of_interest_zero_2.csv', ["0","0", "Everything was zero"])

    # else:


    Data_of_interest_zero = Data_of_interest.iloc[zeros_indexes_set, :]
    Data_of_interest_non_zero = Data_of_interest.iloc[non_zeros_indexes_set, :]
    Data_of_interest_positive = Data_of_interest.iloc[positive_indexes_set, :]
    Data_of_interest_negative = Data_of_interest.iloc[negative_indexes_set, :]
    
    
    #     Data_of_interest_zero.to_csv(f"Data_of_interest_zero_{ii}.csv")

    # Data_of_interest_zero.to_csv('Data_of_interest_zero_2.csv', mode='a', index=False, header=True)


    # Date_time[column_label] = column_of_interest

    column_of_interest_zero = [i for i in Data_of_interest_zero.iloc[:,1]]
    column_of_interest_non_zero = [i for i in Data_of_interest_non_zero.iloc[:,1]]
    column_of_interest_positive = [i for i in Data_of_interest_positive.iloc[:,1]]
    column_of_interest_negative = [i for i in Data_of_interest_negative.iloc[:,1]]

    groups = groupby(column_of_interest)
    result_ = [(label, sum(1 for _ in group)) for label, group in groups]

    data_ = [result_[i][0] for i in range(len(result_))]
    frequency_ = [result_[i][1] for i in range(len(result_))]

    result_split = pd.DataFrame()
    result_split[f"Data(ID: {column_label})"] = data_
    result_split["frequency"] = np.array(frequency_)


    # pd.DataFrame(np.array(result_),columns=["Condition","Frequency"]).to_csv("Vector_Decision.csv")
    result = pd.DataFrame(np.array(result_),columns=[f"Data(ID: {column_label})","Frequency"])


    ##############################################################################
    #
    ##############################################################################
    result_grp = result.groupby([f"Data(ID: {column_label})"]).sum().reset_index()
    result_grp_pct = result.groupby([f"Data(ID: {column_label})"]).sum().transform(lambda x: 100*x/x.sum()).reset_index()

    result_split.to_csv(os.path.join(Results_folder, "Frequency_count.csv"), mode='a', index=False, header=True)

    # append_list_as_row('Frequency_count_percentage.csv', [column_label])
    result_grp_pct.to_csv(os.path.join(Results_folder, "Frequency_count_percentage.csv"), mode='a', index=False, header=True)


    ##################################################################################################
    #                    NEW TECHNIQUE                                                               #
    ##################################################################################################
#     sol_values_change, Flag = index_value_change(Data_of_interest)
    
    sol_values_change, Flag = data_grouping(Data_of_interest, data_subset = [0,1,2,3])

    
#     sol_values_change_, Flag2 = data_grouping(Data_of_interest, data_subset = [0,1,2,3])
    
#     df_values_change_with_Voltage = list_of_tuples_to_dataframe_(sol_values_change_,column_label, 
#                                                         data_labels = ["datetime", "Register","Current","Voltage" ])
#     df_values_change_with_Voltage.to_csv(Results_folder+'Group_by_Value_Change_.csv', mode='a', index=False, header=True)    
        
        
    sol_sign_change, Flag = index_value_change_sign(Data_of_interest)
    
#     sol_values_change_non_zero_reduced = index_value_change(Data_of_interest_non_zero)[0]
#     sol_values_change_zero_reduced = index_value_change(Data_of_interest_zero)[0]
#     sol_values_change_positive_reduced = index_value_change(Data_of_interest_positive)[0]
#     sol_values_change_negative_reduced = index_value_change(Data_of_interest_negative)[0]

    sol_values_change_non_zero_reduced = data_grouping(Data_of_interest_non_zero,[0,1,2,3])[0]
    sol_values_change_zero_reduced = data_grouping(Data_of_interest_zero,[0,1,2,3])[0]
    sol_values_change_positive_reduced = data_grouping(Data_of_interest_positive,[0,1,2,3])[0]
    sol_values_change_negative_reduced = data_grouping(Data_of_interest_negative,[0,1,2,3])[0]



    
#     # INSERT the first Row to the group
#     data_key = Data_of_interest.iloc[:,0] 
#     data_val = Data_of_interest.iloc[:,1]    
#     tuple_from_dict = tuple(zip(data_key,data_val))
    
    sol_values_change = insert_first_row(sol_values_change,Data_of_interest)
    sol_sign_change = insert_first_row(sol_sign_change,Data_of_interest)
    
    sol_values_change_non_zero_reduced = insert_first_row(sol_values_change_non_zero_reduced,Data_of_interest_non_zero)
    sol_values_change_zero_reduced = insert_first_row(sol_values_change_zero_reduced,Data_of_interest_zero)
    sol_values_change_positive_reduced = insert_first_row(sol_values_change_positive_reduced,Data_of_interest_positive)
    sol_values_change_negative_reduced = insert_first_row(sol_values_change_negative_reduced,Data_of_interest_negative)

    

    
    # if Flag in ["All_Negative", "All_Positive", "All_Zero"]
    
#     print("Flag",Flag)

    if Flag == "Mixed_Values":

        

        # Data_of_interest_non_zero.to_csv(Results_folder+f'{file_name_no_ext}_{Fault_Type}Data.csv', mode='a', index=False, header=True)
        Data_of_interest_non_zero.to_csv(os.path.join(Results_folder, f'{Fault_Type}Data(Master).csv'), mode='a', index=False, header=True)
        Data_of_interest_non_zero.to_csv(os.path.join(Results_Split_folder, f'{file_name_no_ext}_1_{Fault_Type}Data_{column_label}.csv'), mode='a', index=False, header=True)

        
        
        df_values_change = list_of_tuples_to_dataframe_(sol_values_change,column_label, 
                                                       data_labels = ["datetime", "Register","Current","Voltage" ])
        df_values_change.to_csv(os.path.join(Results_folder, f'{file_name_no_ext}_Group_by_Value_Change.csv'), mode='a', index=False, header=True)    
        df_values_change.to_csv(os.path.join(Results_Split_folder, f'{file_name_no_ext}_Group_by_Value_Change{column_label}.csv'), mode='a', index=False, header=True)    

#         df_sign_change = list_of_tuples_to_dataframe(sol_sign_change,column_label, data_labels = ["datetime", "Register","Current" ])
#         df_sign_change.to_csv(Results_folder+'Group_by_Sign_Change.csv', mode='a', index=False, header=True)    

        
        df_values_change_non_zero_reduced = list_of_tuples_to_dataframe_(sol_values_change,column_label, 
                                                                         data_labels = ["datetime", "Register","Current","Voltage" ])
        df_values_change_non_zero_reduced.to_csv(os.path.join(Results_folder, f'{file_name_no_ext}_2_{Fault_Type}Data_Grouped.csv'), mode='a', index=False, header=True)    
        
        df_values_change_positive_reduced = list_of_tuples_to_dataframe_(sol_values_change_positive_reduced,column_label, 
                                                                         data_labels = ["datetime", "Register","Current","Voltage" ])
        df_values_change_positive_reduced.to_csv(os.path.join(Results_folder, f'{file_name_no_ext}_Alarm_Positives.csv'), mode='a', index=False, header=True)    

        df_values_change_negative_reduced = list_of_tuples_to_dataframe_(sol_values_change_negative_reduced,column_label, 
                                                                         data_labels = ["datetime", "Register","Current","Voltage"  ])
        df_values_change_negative_reduced.to_csv(os.path.join(Results_folder, f'{file_name_no_ext}_Alarm_Negatives.csv'), mode='a', index=False, header=True)    


    if Flag == "All_Negative":
        grouped_df_values_all_constant = pd.DataFrame({"" : [""], f"Register: {column_label}" : ["All Negative"]})
#         grouped_df_values_all_constant.to_csv(Results_folder+'Group_Positives.csv', mode='a', index=False, header=True)    
        grouped_df_values_all_constant.to_csv(os.path.join(Results_folder, f'{file_name_no_ext}_Alarm_All_Negatives.csv'), mode='a', index=False, header=True)    

    if Flag == "All_Positive":
        grouped_df_values_all_constant = pd.DataFrame({"" : [""], f"Register: {column_label}" : ["All Positive"]})
        grouped_df_values_all_constant.to_csv(os.path.join(Results_folder, f'{file_name_no_ext}_Alarm_All_Positives.csv'), mode='a', index=False, header=True)    

    if Flag == "All_Zero":
        grouped_df_values_all_constant = pd.DataFrame({"" : [""], f"Register: {column_label}" : ["All Zeros"]})
        grouped_df_values_all_constant.to_csv(os.path.join(Results_folder, f'{file_name_no_ext}_HealtyData.csv'), mode='a', index=False, header=True)    





