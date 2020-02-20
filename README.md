# 100KRDActiveList
To extract cases from the CIPAPI to update the local NUH active list for 100K rare disease validation and reporting.

This version (v1.2) is an update to use the client credentials authentication with AD

Takes a username and password for the CIPAPI, generates a token and returns: 
* proband ID
* family ID (not for rare disease cases)
* last_status 
* genome build 
* IR_id 
* date_updated
* CIP 

output is to a text file (comma separated) that can be added to the active list.
