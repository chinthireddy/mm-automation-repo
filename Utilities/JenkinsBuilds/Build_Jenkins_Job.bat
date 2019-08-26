@echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime  ^| find "."') do set dt=%%a
set YYYY=%dt:~0,4%
set MM=%dt:~4,2%
set DD=%dt:~6,2%
set HH=%dt:~8,2%
set Min=%dt:~10,2%
set Sec=%dt:~12,2%
set timeStamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%
for /f "tokens=1,2,3,4 delims=;" %%a in (Properties.txt) do set jenkinsSrv=%%a &set userName=%%b & set passWord=%%c & set buildParams=%%d
set /p jobName= Enter the Name of the Jenkins job that you would like to build:
set /p timesToRun= Enter the number of times you would like to build the job '%jobName%':
echo Your build requests are processing...
for /l %%x in (1, 1, %timesToRun%) do java -jar jenkins-cli.jar -noCertificateCheck -s %jenkinsSrv% build %jobName% -s --username %userName% --password %passWord% %buildParams% >> %jobName%_RunLog_%timeStamp%.txt
echo All %timesToRun% job builds are now complete. You can review the results of the run in the log file %jobName%_RunLog.txt
ren %jobName%_RunLog_%timeStamp%.txt %jobName%_RunLog2.txt
findstr /v /b /c:"Skipping HTTPS certificate checks altogether. Note that this is not secure at all." %jobName%_RunLog2.txt > %jobName%_RunLog_%timeStamp%.txt
del %jobName%_RunLog2.txt