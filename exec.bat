@echo off
for %%f in (instances\*.dat) do (
    if not exist results\%%~nf_results.txt (
        echo Running with %%f
        oplrun project.mod %%f > results\%%~nf_results.txt
    ) else (
        echo Skipping %%f, result already exists
    )
)
