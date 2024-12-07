@echo off
setlocal enabledelayedexpansion

REM Create the results directory if it doesn't exist
if not exist "results_greedy" mkdir "results_greedy"

REM Loop through all .dat files in the instances directory
for %%f in (instances\*.dat) do (
    REM Get the filename without the extension
    set "filename=%%~nf"
    REM Execute project.exe with the current file and store the result
    echo !filename!
    .\project.exe < "instances/!filename!.dat" > "results_greedy/!filename!_result.txt"
)

endlocal