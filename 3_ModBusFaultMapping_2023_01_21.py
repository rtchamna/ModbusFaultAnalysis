#!/usr/bin/env python
# coding: utf-8

# # Dataset Importing

# In[11]:


import pandas as pd 
import os, sys 

# Fault_Type = "Alarms"
Fault_Type =  sys.argv[-1]

print(Fault_Type)

dict_fault_type = {"Warnings":[2283, 2298], "Alarms":[2299, 2314], "Faults":[2315, 2342], "User_Clear_Faults":[2343, 2370]}


# Alarm: 2299 – 2314
# Fault: 2315-2342

begin_alarm = dict_fault_type[Fault_Type][0] 
end_alarm   = dict_fault_type[Fault_Type][1] 

# print(begin_alarm)
# print(end_alarm)

# begin_alarm = 2299
# end_alarm = 2314


cwd = os.getcwd()
# print("cwd:",cwd)

os.chdir(cwd+"\\Results_folder\\")
# path = r"C:\Users\Rtchamna\Downloads\bcb_modbus_Harmony\Results_folder\AlarmsData(Master)_backup.xlsx"

file = f"Modbus_{Fault_Type}_Combined.csv"


# Import the Alarms Dated Dataset
# df = pd.read_csv("C:/Users/Rtchamna/Downloads/bcb_modbus_Harmony/Modbus_Alarm_Combined.csv")
df = pd.read_csv(file)



cwd = sys.argv[1]
os.chdir(cwd)

# Import the Bit Alarm Map Table
# AlarmMap = pd.read_excel(r"C:\Users\Rtchamna\OneDrive - EOS ENERGY STORAGE\ModbusDataAnalysis_Fault_Parser.xlsx",sheet_name="AlarmMap",header=None)

AlarmMap = pd.read_excel(r"ModbusDataAnalysis_Fault_Parser.xlsx", sheet_name = f"{Fault_Type}Map",header=None)

AlarmMap = AlarmMap.dropna()
AlarmMap.columns = ["Alarm_Name","Bit_Range"]


# # Creating Alarm Dictionary Map



def clean_alarm_map(col):
    
    name = col[0]
    bit = col[1]
    
#     print(name,bit)
    
    name = name.split(":")[1]
    bit = bit.split(" ")[1]
    
    return name.strip(), bit.strip()


alarm_map_series =  AlarmMap.apply(clean_alarm_map,axis=1)
alarm_map_list_of_tuples = list(alarm_map_series)
dict_alarm_map = {i[1]:i[0] for i in alarm_map_list_of_tuples}

# alarm_map_list_of_tuples
# dict_alarm_map 


# In[14]:


N = len(dict_alarm_map.keys())
range_list_vect = []
for i in range(N):

    range_str = list(dict_alarm_map.keys())[i].split("-")

    if len(range_str) == 2:

        from_bit = int(range_str[0])
        to_bit = int(range_str[1])

        range_list = [i for i in range(from_bit,to_bit+1)]
        
    elif len(range_str) == 1:

        from_bit = to_bit = int(range_str[0])
        range_list = [i for i in range(from_bit,to_bit+1)]

    range_list_vect.append((range_list,alarm_map_list_of_tuples[i][0]))


alarm_extended_dict = {}

for k in range(len(range_list_vect)):

    range_ = range_list_vect[k][0]
    alarm = range_list_vect[k][1]
    
#     print("range_",len(range_))

    if len(range_) == 12:
        dd = {i:alarm+f" S_{range_.index(i)+1}" for i in range_}
        alarm_extended_dict.update(dd)
    else:
        dd = {i:alarm for i in range_}
        alarm_extended_dict.update(dd)
        
    


# alarm_extended_dict   


# # Integer to Binary (Optional)

# In[ ]:





# In[15]:


def int_to_binary(x): 
    
    if x>0:
        return f'b{x:016b}'
    else:
        x = 2**16 + x 
        return f'b{x:016b}' 
    
df["Register Binary"] = df["Register Value"].apply(int_to_binary)


# # Zip (Register, Value)

# In[16]:


def reg_and_val(col):
    reg_val = col[2]
    reg_label = col[5]
    
    reg = reg_label.split(":")[1]
#     val = reg_val 
    return reg.strip(),reg_val


df["Register_and_Value"] = df.apply(reg_and_val,axis=1)

# print(df)
# # Find Alarms Bit Position

# In[17]:



# def Alarmsbits(val = 2048):
#     s = f'{val:016b}'
    
#     dd = {i:s[-i-1] for i in range(16)}

#     res = [i for i in dd if int(dd[i])!=0]
#     return res 

# def Alarmsbits_reg(reg_val):
    
    # reg = int(reg_val[0])
    # val = reg_val[1]
    
    # if val < 0:
         # val = 2**16 + val
    
    # dict_reg = {i:16*(i-2315) for i in range(2315,2343)}
# #     dict_reg
    
    # s = f'{val:016b}'
    
    # dd = {i:s[-i-1] for i in range(16)}
    # try: 
        # res = [i + dict_reg[reg] for i in dd if int(dd[i])!=0]
        # return res 
    # except (Exception) as exp:
        # pass 
# #         print(f" Make sure the register {reg} is in the range...")



# begin_alarm = dict_fault_type[Fault_Type][0] 
# end_alarm   = dict_fault_type[Fault_Type][1] 

def Alarmsbits_reg(reg_val):
    
    reg = int(reg_val[0])
    val = reg_val[1]
    
    if val < 0:
         val = 2**16 + val
    
    dict_reg = {i:16*(i-begin_alarm) for i in range(begin_alarm,end_alarm+1)}
#     dict_reg
    
    s = f'{val:016b}'
    
    dd = {i:s[-i-1] for i in range(16)}
    try: 
        res = [i + dict_reg[reg] for i in dd if int(dd[i])!=0]
        return res 
    except (Exception) as exp:
        pass 
        

# df["Register_and_Value"][0]
df[f"{Fault_Type}_Bit_Position"] = df["Register_and_Value"].apply(Alarmsbits_reg)

print(df.head()) 


# # Find Alarms Name From Bit Position

# In[18]:

df["Register_and_Value"].to_csv("Register_and_Value.csv")
# set([ alarm_extended_dict[i] for i in aa])

df[f"Type of {Fault_Type}"] = df[f"{Fault_Type}_Bit_Position"].apply(lambda x: sorted(list(set([alarm_extended_dict[i] for i in x]))))

# df["Type of Alarm"][0]


# # String Compression

# In[19]:


import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# my_list = ["x S1","x S2","z S2","t S2"]
# Expected_result = ["d1(x,y)","d2(z,t)"]



def str_compress(my_list):

    # df["Type of Alarm"]
    df_ = pd.DataFrame(my_list,columns=["col1"])

    df2 = df_["col1"].str.split(" S_",expand = True)
#     display(df2)
    if len(df2.columns) > 1:

        df2.columns = ["col1","col2"]
#         display(df2)
        # apply(lambda x: x.split(" ",expand = True))
        grp = df2.groupby(["col1"])

        result = []
        for grp_name, data in grp:
            if None not in list(data["col2"]):
                
              data_col2_list = list(data["col2"])
              data_col2_list = [int(i) for i in data_col2_list]
              data_col2_list = sorted(data_col2_list)
              data_col2_list = [str(i) for i in data_col2_list]
#               print(data_col2_list)
                
              res =  grp_name +" String (" + ",".join(data_col2_list) + ")"
              result.append(res)
              return result
            else:
              res =  grp_name
              result.append(res)
                
        return result
    else:
        return my_list


# {'Block Contactor Open Failure', 'Module Over Soc S2', 'Module Over Soc S9', 'Module Over Soc S11'}
# {'String Module Communications Failure Reading S1', 'String Module Communications Failure Reading S3'}


# In[43]:


df[f"Type_of {Fault_Type}_Compressed"] = df[f"Type of {Fault_Type}"].apply(str_compress)


# # From List to String

# In[40]:


aa = "Module Over Temperature String (5,9); OK Great;"
aa[:-1]


# In[49]:


aa = ['Module Over Temperature String (5,9)',"OK Great"]

def from_list_to_string(list_):

    s = ""
    for i in list_:
        s+=i+"; " 
    return s.strip()[:-1]

df[f"Type_of {Fault_Type}_Compressed_2"] = df[f"Type_of {Fault_Type}_Compressed"].apply(from_list_to_string)
df[f"Type_of {Fault_Type}_Compressed_2"]


# In[62]:


aa = "String is not a String great"
aa = "Module Over Temperature String (5,9)"
aa.count("String")
aa.split("String")[0].strip()


# # Groupe Alarm Type

# In[64]:


def grp_alarm_type(x):
    if x.strip().lower().count("string") >1:
        return "String".join(x.split("String")[:2])
    else:
        return x.split("String")[0].strip()
#     else 
        
df[f"Type_of {Fault_Type}_Grouped"] = df[f"Type_of {Fault_Type}_Compressed_2"].apply(grp_alarm_type)

# df[f"Type_of {Fault_Type}_Grouped"]


# In[65]:


# df.columns


# # Save the result

# In[70]:


columns_of_interrest = ["datetime",'Current', 'Voltage',"Register Label","Register_and_Value",
                        f"{Fault_Type}_Bit_Position",f"Type_of {Fault_Type}_Compressed_2",f"Type_of {Fault_Type}_Grouped"]


# In[74]:

os.chdir(cwd+"\\Results_folder\\")

df[columns_of_interrest].to_csv(f"Result_Modbus_{Fault_Type}Analysis.csv")


# In[ ]:





# In[ ]:





# In[ ]:




