import pandas as pd 
import os, sys

# Fault_Type = "Alarms"
Fault_Type =  sys.argv[-1]


dict_fault_type = {"Warnings":[2283, 2298], "Alarms":[2299, 2314], "Faults":[2315, 2342], "User_Clear_Faults":[2343, 2370]}


cwd = os.getcwd()
# print("cwd:",cwd)

os.chdir(cwd+"\\Results_folder\\")
# path = r"C:\Users\Rtchamna\Downloads\bcb_modbus_Harmony\Results_folder\AlarmData(Master)_backup.xlsx"

file = f"{Fault_Type}Data(Master).csv"

##############################################################

# df_original = pd.read_excel(path, date_parser="datetime",header=None)
df_original = pd.read_csv(file, date_parser="datetime",header=None)


# df_original2 = pd.read_excel(path, skiprows=4, usecols= range(0,4), header=None)

df_original.columns=["datetime","Register Value","Current","Voltage"]

mask_datetime = df_original["datetime"] == "datetime"

df_original['Register Label'] = df_original["Register Value"].where(mask_datetime).ffill()

new_df = df_original[~mask_datetime]

new_df.to_csv(f"Modbus_{Fault_Type}_Combined.csv")

new_df

