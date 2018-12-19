import requests
username = "fernando.gomes"
apikey = "c857ef43875e7c2e61934de6b2f57accfc3bddcf"
headers = {
    'Authorization': 'ApiKey %s:%s' %(username, apikey),
    'Content-Type': 'application/json',
}
url = "https://sandbox.unbabel.com/tapi/v2/translation/"
source_language = "en"
target_language = "pt"
text_format = "text"
texts = ["Hello, world!", "this"]
text = "Hello, world!"
for text in texts:
    data = '{"text" : "%s", "source_language" : "%s", "target_language" : "%s", "text_format" : "%s"}' % (
    text, source_language, target_language, text_format)
    print "Getting uid ..."
    r1 = requests.post(url, headers=headers, data=data)
    uid = r1.json().get('uid')
    print "Translating ........", r1.status_code

# not translating we are getting just UID
# attempt = 1
# status = 'new'
# while status != 'completed':
#     print "attempt ........: %s", attempt, status
#     r2 = requests.get('%s%s/' %(url,uid), headers=headers)
#     status = r2.json().get('status')
#     attempt += 1
# print r2.json()
# if status == 'completed' :
#     print r2.json().get('translatedText')

text =" this" \
      "is              " \
      "          nice"