## 100KRareDisease_ActiveList
## Using the CIPAPI to identify Nottingham (RX1) rare disease cases that are ready for review by the GMC
## CIP API documentation: https://cipapi.genomicsengland.nhs.uk/api/2/docs/#
## Author: Rebecca Haines (rebecca.haines@nuh.nhs.uk)
## Date: 06/07/2018
## Code reviewed by: Simon BOARDMAN 05/06/2018
## Version: 1.0

### use the swagger page to get the info https://cipapi.genomicsengland.nhs.uk/api/2/docs/#

import requests
import datetime
import sys

def get_token(username,password):
    '''Return an authentication token using the get-token endpoint.'''
    token = ''
    response = requests.post('https://cipapi.genomicsengland.nhs.uk/api/2/get-token/', {'username': username, 'password': password})
    try:
        token = response.json()['token']
    except KeyError:
        print("Failed to get token- unable to proceed. Check the username and password were entered correctly.")
        sys.exit()
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
    page_size = 100
    url = 'https://cipapi.genomicsengland.nhs.uk/api/2/interpretation-request?page={page}&page_size={page_size}&workspace=RX1'
    response2 = requests.get(url.format(page=page_no, page_size=page_size), headers=auth_header)
    result = response2.json() #contains all results from the page and page info in json format
    return(result)


def write_results(token):
    '''uses the get_results() function to get a page of results from the API, write them to a file, then get the next page.
    '''
    date= datetime.datetime.now().strftime("%y-%m_%d")
    outfilename = str("CIPAPI_Output_"+date + ".csv")
    f = open(outfilename, 'a')
    f.write('ProbandIF,Family_ID,last_status,build,IR_id,date_updated,CIP'+'\n') #add headers to the output file
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
                f.write(proband + ',' + family + ',' + last_status + ',' + build + ',' + IR_id + ',' + date_updated + ',' + CIP + '\n')
            elif case["cip"] == "omicia":
                proband = case["proband"]
                family = case["family_id"]
                last_status = case["last_status"]
                build = case["assembly"]
                IR_id = case["interpretation_request_id"] 
                date_updated = case["last_update"]   
                CIP = case["cip"]
                f.write(proband + ',' + family + ',' + last_status + ',' + build + ',' + IR_id + ',' + date_updated + ',' + CIP + '\n')
            else:
                #cancer cases have no family ID
                proband = case["proband"]
                last_status = case["last_status"]
                build = case["assembly"]
                IR_id = case["interpretation_request_id"] 
                date_updated = case["last_update"]   
                CIP = case["cip"]
                f.write(proband + ',' + " " + ',' + last_status + ',' + build + ',' + IR_id + ',' + date_updated + ',' + CIP + '\n')
        f.close()
        next_page = result["next"]
        print(next_page)
        last_page = str(next_page)
        if last_page == "None":
            print("total cases: "+ str(total_cases))
            break
        page_no = page_no + 1
        print(page_no)

#get the token
username = input("Enter username: ")
password = input("Enter password: ")
new_token = get_token(username,password)
print("token: " + new_token)
#write results to file
write_results(new_token)
