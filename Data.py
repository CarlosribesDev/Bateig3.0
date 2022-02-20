import json

def update_data(name,value):

    data = load_data()
    with open('data.json','w') as file:
        
        data[name] = value
        json.dump(data,file)

  
def load_data():
    with open('data.json','rb') as json_file:
        json_data = json.load(json_file)

        return json_data



    