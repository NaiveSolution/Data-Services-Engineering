import requests
import base64


def print_house(house):
    print("House {")
    for key in house.keys():
        attr = str(key)
        # if isinstance(book[key], str):
        #     val = str(book[key].encode('utf-8'))
        # else:
        val = str(house[key])

        print("\t" + attr + ":" + val)
    print("}")

def get_token():
    client_id = 'client_e4a667055d79c4cfaf1731dd7902ff58'
    client_secret = 'secret_4d87819c8e80fb3f5d89055673b4d2b1'
    authCredentials = client_id + ':' + client_secret
    encodedAuth = base64.b64encode(authCredentials.encode('UTF-8')).decode('UTF-8')
    house_data = {
        "grant_type": "client_credentials",
        "scope": "api_agencies_read api_listings_read",
    }
    house_headers = {
        "Authorization": f"Basic {encodedAuth}",
        "Content-Type" : "application/x-www-form-urlencoded",
    }

    r = requests.post('https://auth.domain.com.au/v1/connect/token', data=house_data, headers=house_headers)
    print("Status Code:" + str(r.status_code))
    resp = r.json()
    return resp

if __name__ == '__main__':
    token = get_token()['access_token']
    r = requests.get("https://api.domain.com.au/v1/listings/", headers={"Authorization" : "Bearer" + " " + token})
    print("Status Code:" + str(r.status_code))
    houses = r.json()
    print_house(houses)