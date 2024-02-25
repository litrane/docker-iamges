import requests

chatid = 1
prompt = 'Your prompt text here'

# The URL to which the POST request is to be sent, with placeholders for chatid and prompt
url_template = 'http://localhost:8008/api/chat/{chatid}/question?prompt={prompt}'

# Headers to be sent with the request
headers = {
    'accept': 'application/json'
}

# Data to be sent with the request, if any
data = {}

# Make the POST request
response = requests.post(url, headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content if the request was successful
    print(response.json())
else:
    # Print the error if the request failed
    print('Failed to make request:', response.status_code, response.text)
