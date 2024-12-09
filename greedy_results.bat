@echo off
setlocal enabledelayedexpansion

REM Create the results directory if it doesn't exist
if not exist "results_grasp_noLocalSearch" mkdir "results_grasp_noLocalSearch"

REM Loop through all .dat files in the instances directory
for %%f in (instances_reduced\*.dat) do (
    REM Get the filename without the extension
    set "filename=%%~nf"
    REM Check if the result file already exists
    if not exist "results_grasp_noLocalSearch/!filename!_result.txt" (
        REM Execute project.exe with the current file and store the result
        echo Processing !filename!
        .\project.exe < "instances_reduced/!filename!.dat" > "results_grasp_noLocalSearch/!filename!_result.txt"
    ) else (
        echo Skipping !filename!, result already exists.
    )
)

endlocal