This repository will hold project related to weather data.

Key information about the goal and rationale are provided in the Jupyter
Notebook 'Hawaii_oh_five.jypnb'.  This notebook contains all of the 
intended exploratory analysis activities.  In addition, the notebook
'Hawaii_oh_five_code_test.jypnb' also contains the basic exploratory
data anlsysis functions, as well as the adaptations to the code made
for each of the API routes. The code_test notebook thus provides an
interactive way to test the code for each API route. 

The server for the API is provided in the 'server-app.py' file.  The
server is configured for localhost access (127.0.0.1 : 5000).  The
default page lists each of the API endpoints and instructions for those
endpoints that accept variable names.  

One additional image file, 'precip_data.jpg' is provided because the
notebook version of this graphic is somewhat small.  For more detailed
examination, the image file presents this graphic in a high-resolution
format.

Both the notebook and the Python program require the sqalchemy and flask
libraries.  They also require a folder called 'Resources' co-located
with the application and the notebook.  Inside this folder, the file
'hawaii.sqlite' provides the required database, while the files 
'hawaii_measurements.csv' and 'hawaii_stations.csv' provide an alternate
way to view the database tables.  

The 'Images' and '.jypnb_checkpoints' folders are not required but
are helpful.  The 'Images' folder provides a reference for the intended
output from the exploratory data analysis, while the checkpoints folder
enables roll-back to earlier notebook versions if desired.






