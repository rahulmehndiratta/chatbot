import json
from os import name

def getData():
    return {
        "status": "success",
        "data": [
            {
                "name": "rahul",
                "age": 20,
                "city": "delhi"
            },
            {
                "name": "rohan",
                "age": 21,
                "city": "mumbai"
            }
        ]
    }

print(getData());