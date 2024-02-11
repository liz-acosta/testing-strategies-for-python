import requests
import json

BASE_URL = 'https://dogapi.dog/api/v2/'

PUG_ID = 'a6ea38ed-f692-478e-af29-378d0e2cc270'

def get_pug_info():
    
    groups_endpoint = BASE_URL + 'groups/'
    groups_response = requests.get(groups_endpoint)
    
    # print(groups_response.content)

    for group in json.loads(groups_response.content)['data']:
        # print(group)
        if group['attributes']['name'] == 'Toy Group':
            toy_group_id = group['id']
            # print(toy_group_id)
    
    breeds_endpoint = BASE_URL + 'breeds/'

    group_endpoint = BASE_URL + 'groups/' + toy_group_id
    group_response = requests.get(group_endpoint)

    for breed in json.loads(group_response.content)['data']['relationships']['breeds']['data']:
        # print(breed)
        breed_response = json.loads(requests.get(breeds_endpoint + breed['id']).content)
        # print(breed_response.content)
        if breed_response['data']['attributes']['name'] == 'Pug':
            pug_id = breed_response['data']['id']
            print(pug_id)
    
    pug_breed_response = requests.get(breeds_endpoint + pug_id).content

    pug_info = json.loads(pug_breed_response)
    print(pug_info)

    return pug_info



get_pug_info()