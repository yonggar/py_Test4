import json
import matplotlib.pyplot as plt

jstring = open("py_Test4/weather/myjsonfile.json", "r").read()
jsonData = json.loads(jstring)

jan = []
aug = []

for item in jsonData:
    month = item["date"].split('-')[1]
    if month == '01':
        item["maxTemp"] = float(item["maxTemp"])
        jan.append(item["maxTemp"])
    if month == '08':
        item["maxTemp"] = float(item["maxTemp"])
        aug.append(item["maxTemp"])

plt.hist(jan, bins=100, color='r', label='max')
plt.hist(aug, bins=100, color='b', label='min')
plt.show()
