# 100KRDActiveList
To extract cases from the CIPAPI to update the local active list for 100K rare disease validation and reporting.

Takes a username and password for the CIPAPI, generates a token and returns: 
* proband ID
* family ID (not for cancer cases)
* last_status 
* genome build 
* IR_id 
* date_updated  
* CIP 

output is to a text file that can be added to the active list.
