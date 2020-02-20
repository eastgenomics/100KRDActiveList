## 100KRareDisease_ActiveList
## Using the CIPAPI to identify Nottingham (RX1) rare disease cases 
## that are ready for review by the GMC
## CIP API documentation: https://cipapi.genomicsengland.nhs.uk/api/2/docs/#
## Author: Rebecca Haines (rebecca.haines@nuh.nhs.uk)
## Date: 20/02/2020
## Code reviewed by: _______________ 
## (v1.0 reviewed by Simon BOARDMAN 05/06/2018)
## Version: 1.2


import requests
import datetime
import json


def get_token():
    '''Return access token for CIPAPI using AD client credentials
    Credentials are stored in the file "credentials.json"
    '''
    credentials_file = open('credentials.json')
    credentials = json.load(credentials_file)
    tenant_ID = credentials['tenant_ID']
    client_ID = credentials['client_ID']
    client_secret = credentials['client_secret']

    url = "https://login.microsoftonline.com/{tenant_ID}/oauth2/token".\
    format(tenant_ID=tenant_ID)

    payload = "grant_type=client_credentials"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
       }

    response = requests.request("POST", url, data=payload, \
    headers=headers, auth=(client_ID, client_secret))
    token = response.json()['access_token']
    return token


def get_results(token,page):
    '''Return a page of interpretation-request results. 
    Takes a token as input as well as a page number- 
    allows looping through multiple pages
    '''
    #required header for the API request
    auth_header = {
        'Accept': 'application/json',
        'Authorization': 'JWT ' + token
    }
    page_no = page
    page_size = 100
    url = 'https://cipapi-gms-beta.genomicsengland.nhs.uk/api/2/interpretation-request?page={page}&page_size={page_size}&category=100k&workspace=RGT' # pulls 100k results only from RGT
    response2 = requests.get(url.format(page=page_no, page_size=page_size), \
    headers=auth_header)
    result = response2.json()
    return(result)


def write_results(token):
    '''uses the get_results() function to get a page of results from the API, 
    write them to a file, then get the next page.
    '''
    date= datetime.datetime.now().strftime("%y-%m-%d")
    outfilename = str("CIPAPI_Output_"+date + ".csv")
    f = open(outfilename, 'a')
    #add headers to the output file
    f.write('ProbandID,Family_ID,last_status,build,IR_id,date_updated,CIP'+'\n') 
    f.close()
    page_no = 1
    while True:
        result = get_results(token,page_no)
        f = open(outfilename, 'a')
        total_cases = result["count"]
        for case in result["results"]:
            if case["cip"] == "genomics_england":
                proband = case["proband"]
                family = case["family_id"]
                last_status = case["last_status"]
                build = case["assembly"]
                IR_id = case["interpretation_request_id"] 
                date_updated = case["last_update"]   
                CIP = case["cip"]
                f.write(proband + ',' + family + ',' + last_status + ',' \
                + build + ',' + IR_id + ',' + date_updated + ',' + CIP + '\n')
            elif case["cip"] == "omicia":
                proband = case["proband"]
                family = case["family_id"]
                last_status = case["last_status"]
                build = case["assembly"]
                IR_id = case["interpretation_request_id"] 
                date_updated = case["last_update"]   
                CIP = case["cip"]
                f.write(proband + ',' + family + ',' + last_status + ',' \
                + build + ',' + IR_id + ',' + date_updated + ',' + CIP + '\n')
            elif case["cip"] == "congenica":
                proband = case["proband"]
                family = case["family_id"]
                last_status = case["last_status"]
                build = case["assembly"]
                IR_id = case["interpretation_request_id"] 
                date_updated = case["last_update"]   
                CIP = case["cip"]
                f.write(proband + ',' + family + ',' + last_status + ',' \
                + build + ',' + IR_id + ',' + date_updated + ',' + CIP + '\n')    
            else:
                #cancer cases have no family ID
                proband = case["proband"]
                last_status = case["last_status"]
                build = case["assembly"]
                IR_id = case["interpretation_request_id"] 
                date_updated = case["last_update"]   
                CIP = case["cip"]
                f.write(proband + ',' + ' ' + ',' + last_status + ',' \
                + build + ',' + IR_id + ',' + date_updated + ',' + CIP + '\n')
        f.close()
        next_page = result["next"]
        print(next_page)
        last_page = str(next_page)
        if last_page == "None":
            print("total cases: "+ str(total_cases))
            break
        page_no = page_no + 1
        print(page_no)


new_token = get_token()
print("token: " + new_token)
write_results(new_token)
