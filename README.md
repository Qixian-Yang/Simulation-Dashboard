# Pipeline Simulation with Arena, Python and ISBM 2.0a

## Model:
The Model requires Rockwell’s Arena simulation tool as a minimum to run. Microsoft Access Runtime 2013 and Crystal Report Runtime are optional but are __HIGHLY RECCOMENDED__.

## To run:
Firstly open pipeline.doe in arena and then press run. A window will appear asking you to input some values and data. The only data necessary is the filename and path for the file to be saved to. Once these have been inputted you are free to choose your scenario whether it be normal operation or another one of the preselected scenarios.
It is worth noting that scenarios are modelled to certain circumstances. This is because the pipeline is modelled on a 20KM High Density Polyurethane (HDPE) pipe. This pipe can with stand ~290 PSI of pressure as well as being able to withstand at 120-degree heat for short amounts of time. 

## Scenarios:
* *Normal Operation*: all variables will fluctuate within an acceptable range.
* *Blocked Pipe *: Pressure will fluctuate around dangerous levels.
* *Leaking Pipe*: Pressure will slowly drop over time to reflect a small leak within the HDPE pipe.
* *Temperature Rising*: Temperature will slowly rise to dangerous levels and slowly drop. Temperature will remain within a range of 70-120 degrees as this reflects what HDPE pipe is rated for.

## Possible Errors:
When running for the first time the simulation may error. If this happens then run it again and it will run correctly. 
Arena has a bad habit of crashing for no apparent reason. It is __HIGHLY RECCOMENDED__ that you install the above optional programs to minimise these crashes.

## Stream controller：
The controller is based on c# and .net core. The controller gives users a way to access Azure Service Bus. And use the specifications stipulated by the ISBM2.0 message service model to push information and manage the service bus.

Prerequisites:
1. Azure account
2. The computer is turned on local SQL sever
3. Software that can connect to remote database (SQL management is recommended)


This project also uses the following class libraries/packages, please confirm whether the environment or generation location exists before using:
       
       Azure.Messaging.ServiceBus
       
       Microsoft.AspNet.WebApi.Core
       
       Microsoft.Azure.Management.ServiceBus
       
       Microsoft.Azure.ServiceBus
       
       Newtonsoft.Json
       
       System.Data.SqlClient

Frame：

        NETCore.APP
        
        WindowsDesktop.App.WindowsForm


## Dashboard:
dashboard is developed by python 3.7.8, it can present the data in the form of graphs and provide some analysis of the data.
it have static and reply model, and support to export image or pdf file.

## requirement package:
wxpython
pyodbc
azure
re
fpdf

## how to use:
1. run main.py to start
2. if you have csv document in local, just click start by local. Or you need to input channel id or topic and click start by internet.
3. checkbox can select sensor for display
4. In the menu, dashboard have static and reply model.
5. You can export files to save result

## Links:
1. https://www.rockwellautomation.com/en-au/products/software/arena-simulation/buying-options/download.html
2. https://www.tektutorialshub.com/crystal-reports/how-to-download-and-install-crystal-report-runtime/
3. https://www.microsoft.com/en-US/download/details.aspx?id=39358
4. http://www.openoandm.org/files/standards/ISBM-2.0.pdf
5. https://www.mimosa.org/mimosa-ccom/
6. https://visualstudio.microsoft.com/downloads/
