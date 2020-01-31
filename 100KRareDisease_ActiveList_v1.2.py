## 100KRareDisease_ActiveList
## Using the CIPAPI to identify Nottingham (RX1) rare disease cases that are ready for review by the GMC
## CIP API documentation: https://cipapi.genomicsengland.nhs.uk/api/2/docs/#
## Author: Rebecca Haines (rebecca.haines@nuh.nhs.uk)
## Date: 31/01/2020
## Code reviewed by: _______________ (v1.0 reviewed by Simon BOARDMAN 05/06/2018)
## Version: 1.2

### use the swagger page to get the info https://cipapi.genomicsengland.nhs.uk/api/2/docs/#

## as of 31/01/2020 the below code works to pull cases from the CIPAPI-GMS-Beta. 
## only the first 10 cases will be pulled. The While loop in write_results has been commented out at the moment as don't want to pull all cases in there. This will need updating for actual use.

import requests
import datetime
#import sys


def get_token():
    tenant_ID = "afee026d-8f37-400e-8869-72d9124873e4"
    client_ID = "9d4863b1-be8d-4e32-af99-4355ef0d1a08"
    client_secret = "FTYPOubPuIbQF2MBE/UkHuDw3nQfoHiVu3OVRzNGkec="

    url = "https://login.microsoftonline.com/{tenant_ID}/oauth2/token".format(tenant_ID=tenant_ID)

    payload = "grant_type=client_credentials"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
       }

    response = requests.request("POST", url, data=payload, headers=headers, auth=(client_ID, client_secret))

    token = response.json()['access_token']

    return token



def get_results(token,page):
    '''Return a page of interpretation-request results. 
    Takes a token as input as well as a page number- allows looping through multiple pages
    '''
    #required header for the API request
    auth_header = {
        'Accept': 'application/json',
        'Authorization': 'JWT ' + token
    }
    page_no = page
    page_size = 10
    url = 'https://cipapi-gms-beta.genomicsengland.nhs.uk/api/2/interpretation-request?page={page}&page_size={page_size}'
    response2 = requests.get(url.format(page=page_no, page_size=page_size), headers=auth_header)
    result = response2.json() #contains all results from the page and page info in json format
    return(result)


def write_results(token):
    '''uses the get_results() function to get a page of results from the API, write them to a file, then get the next page.
    '''
    date= datetime.datetime.now().strftime("%y-%m_%d")
    outfilename = str("CIPAPI_Output_"+date + ".csv")
    f = open(outfilename, 'a')
    f.write('ProbandID,Family_ID,last_status,build,IR_id,date_updated,CIP'+'\n') #add headers to the output file
    f.close()
    page_no = 1
#    while True:
    result = get_results(token,page_no)
    f = open(outfilename, 'a')
    total_cases = result["count"]
    for case in result["results"]:
        proband = case["proband"]
        last_status = case["last_status"]
        build = case["assembly"]
        IR_id = case["interpretation_request_id"] 
        date_updated = case["last_update"]   
        CIP = case["cip"]
        f.write(proband + ',' + " " + ',' + last_status + ',' + build + ',' + IR_id + ',' + date_updated + ',' + CIP + '\n')
    f.close()
#        next_page = result["next"]
#        print(next_page)
#        last_page = str(next_page)
#        if last_page == "None":
#            print("total cases: "+ str(total_cases))
#            break
#        page_no = page_no + 1
#        print(page_no)

#get the token
#username = input("Enter username: ")
#password = input("Enter password: ")
new_token = get_token()
print("token: " + new_token)
#write results to file
write_results(new_token)
