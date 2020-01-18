import paralleldots
# Setting your API key
paralleldots.set_api_key("br13ubwK9UvtgVahL09oDrw2KxLtRGKygrgonAmLqjY")
# Get your API key here
# Viewing your API key
paralleldots.get_api_key()

url ="G://passport.jpg"
s = (paralleldots.facial_emotion(url))
ans =dict(s)
if("facial_emotion" in ans):
    a = list(ans['facial_emotion'])
    b = dict(a[0])
    print(b['tag'])
else:
    print("Face Failed...")