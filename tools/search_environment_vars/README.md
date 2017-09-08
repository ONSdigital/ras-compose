# Search For Environment Variables
This tool should be run to ensure your code base does not contain hard coded environment variables when deploying to
a cloud environment. 

This is a small python tool which reads a list of environment variables in from a spread sheet file (csv) which is comma
delimited. It then searches a root folder provided as an argument for those environment variables in the code base. If
it finds a variable that is populated directly e.g.: SECRET_KEY="change_me_before_going_live" it will flag this as 
being a security risk.

If it finds an environment variable which uses the 'os.get_env' function and passes in a developer value it flags this
as a warning e.g. 

	RM_CASE_SERVICE_HOST = os.getenv('RM_CASE_SERVICE_HOST', 'localhost')
	
In the above example we might not want a mistake in deployment causing the system to use the 'localhost' variable.


## Format Of CSV File
The CSV file should have the titles name, occurrence and file names. Occurence and file names are populated after the
search is complete. e.g.


		name,                           occurrence ,                    file_names,                 date
		RM_CASE_SERVICE_PORT
		RM_CASE_GET
		PASSWORD_MIN_LENGTH
		

There is an example CSV file in this folder.


## Running The Program
The program can be run with:

	/> python search_env

The toll will search the current directory in this case
Output is displayed like:



If the program is run with a directory path parameter it will search from this location. e.g.

	/> python search_env.py /home/<name>/virtualenv/mystuff/myprog
	



