import json
types = {
    "0": "Государство",
    "1": "Дипломатический паспорт",
    "2": "Служебный паспорт",
    "3": "Служебный паспорт",
    "4": "Общегражданский паспорт"
}

with open('data.json', 'rb') as f:
    data = json.load(f)
    for val in data:
        country = val.pop("0")
        for i in types:
            if i != "0":
                print(types[i])
                print(val[i])
