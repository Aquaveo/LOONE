# LOONE Quick Guide

## Packages: 
* Platypus (in Packages dir)
* pandas
* scipy
* matplotlib

## Installing Guide:
1. Through Python, browse to the LOONE_Model Folder in your computer.
2. In the Model_Config script, Edit the working_Path to match the directory in your computer and choose the simulation type (i.e., scenario simulation, optimization validation, or optimization scenario).
3. Update all the required Data into the Data Folder.
4. Design the simulation via the Pre_defined_Variables script through changing the different parameters. 
5. You can run a simulation scenario through the LOONE_Scen_Run script: First, the LOONE_Q module is executed and then the LOONE_Nut module is executed using the outputs from LOONE_Q module as inputs.
6. You can run an optimization scenario through LOONE_Opt script where you can design the optimization problem (the decision variables, the objective functions, and the constraints).