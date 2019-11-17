import requests
import base64
import json

client_inputs = {}
def get_client_inputs():

    # No input validation yet
    client_inputs['listingType'] = 'Sold'
    print("Enter a suburb or postcode: ")
    suburb = input()
    print("Enter property type: ")
    client_inputs['propertyTypes'] = [input()]
    print("Number of bedrooms: ")
    client_inputs['minBedrooms'] = int(input())
    print("Number of bathrooms: ")
    client_inputs['minBathrooms'] = int(input())
    print("Number of parking spaces: ")
    client_inputs['minCarSpaces'] = int(input())
    print("Minimum land area (m^2): ")
    client_inputs['minLandArea'] = int(input())

    client_inputs['locations'] = [{'state' : 'NSW', 'region' : '', 'area' : '', 'suburb' : suburb, 'postCode' : ''}]

def print_house(house):
    for i in house:
        parsed = json.dumps(i, indent=4,sort_keys=True)
        print(parsed)
        print()

def get_token():

    # Tariqs credentials from Domain.com.au
    client_id = 'client_e4a667055d79c4cfaf1731dd7902ff58'
    client_secret = 'secret_4d87819c8e80fb3f5d89055673b4d2b1'

    # Encode the id and secret thats required for OAuth HTTP access
    authCredentials = client_id + ':' + client_secret
    encodedAuth = base64.b64encode(authCredentials.encode('UTF-8')).decode('UTF-8')

    # the required data as required by Domain.com.au API
    house_data = {
        "grant_type": "client_credentials",
        "scope": "api_agencies_read api_listings_read api_salesresults_read",
    }

    # header fields required for authentication
    house_headers = {
        "Authorization": f"Basic {encodedAuth}",
        "Content-Type" : "application/x-www-form-urlencoded",
    }

    # send the request for a token
    r = requests.post('https://auth.domain.com.au/v1/connect/token', data=house_data, headers=house_headers)
    print("Status Code:" + str(r.status_code))
    resp = r.json()
    return resp

if __name__ == '__main__':
    token = get_token()['access_token']
    get_client_inputs()
    print(client_inputs)
    r = requests.post("https://api.domain.com.au/v1/listings/residential/_search", json=client_inputs,headers={"Authorization" : "Bearer" + " " + token})
    print("Status Code:" + str(r.status_code))
    houses = r.json()
    print_house(houses)