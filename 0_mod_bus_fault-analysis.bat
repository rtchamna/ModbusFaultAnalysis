echo off


echo.
echo  BEGINNING TIME: %time%
echo.


REM call C:\Users\tcham\Anaconda3\Scripts\activate.bat
call C:\ProgramData\Anaconda3\Scripts\activate.bat



:::::::::::::::::::::::::::::::::
:: DATE VALUES

:: Automatically Set the date
for /F "tokens=2" %%i in ('date /t') do set mydate=%%i
set mytime=%time%

:: Manually Set the date: Must be on the forme mm/dd/yyyy
:: Comment this line out if you ant to input date manually

REM There where data this date:06/16/2022
REM There where no data this date:06/20/2022

REM set mydate=06/16/2022
REM set mydate=06/24/2022




echo Current date is %mydate%
echo Current time is %mytime%


::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::                                  DATA COLLECTION FROM SOURCE                          :
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
REM md Graph_Directory

REM md is used to create a directory. 
md Results_Split_folder
md Results_folder
md NaN_folder

REM echo "%cd%"
REM No need to change this line. The Graph_Directory will me created in your working directory. For some reason, the path must end with antislilash (\) for it to work.
set Results_Split_fold="%cd%"\Results_Split_folder\

set Results_fold="%cd%"\Results_folder\
set NaN_fold="%cd%"\NaN_folder\

set Fault_Type=Alarms
set Fault_Type=Warnings
set Fault_Type=Faults
REM set Fault_Type=User_Clear_Faults




REM echo is used to display/print something on the screen. when you end echo with a dot(.) it prints nothing/blank
echo.
REM echo is used to display/print something on the screen
echo "WORKING ON IT..."
echo.

REM DO NOT FORGET THE Quote "" arround the file directory in the case your directorty contains a space: "%cd%", "%%f"
for  %%f in ("%cd%"\*.txt) do ( 

echo %%f

:: python is used to run the python script. Here, the python script takes the variable csv_file as argument. 
:: Notice that to call a variable, we enclose it in % %
python "%cd%"\1_Modbus_Data_logger_Fault_Analysis.py "%%f" %Results_fold% %Results_Split_fold% %NaN_fold% %mydate% %Fault_Type%

)


python "%cd%"\2_Modbus_Data_logger_Fault_Analysis_Post_Processing.py %Fault_Type%

python "%cd%"\3_ModBusFaultMapping_2023_01_21.py "%cd%" %Fault_Type%


echo.
echo " I am done ..." 

REM echo Yaa2 maf1 laha > testTchamna.txt
date /t
echo.
echo  END TIME: %time%

@pause
pause