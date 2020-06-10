import json

people_string = """
{
    "people": [
        {
            "name": "John Smith",
            "phone": "9849345678",
            "emails": ["sandhya.sheri@gmail.com", "sdfg@ght.com"],
            "has_license": false
        },
        {
            "name": "Sandya Sheri",
            "phone": "7766558894",
            "emails": null,
            "has_license": true
        }
    ]
}
"""
data = json.loads(people_string)
# print(data)
# print(type(data))
# print(type(data['people']))
for person in data["people"]:
    # print(person)
    # print(person['name'])
    print(person["emails"])


print(data["people"][0]["emails"][1])
