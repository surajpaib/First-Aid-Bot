from wit import Wit

wit_token='V5RTD2FOM3PFJE4DJ5XEI4E7FNWS3RHE'

client=Wit(access_token=wit_token)


def wit_client(text):
    resp = client.message(text)
    print resp

    value=resp['entities']['intent'][0]['value']
    return value