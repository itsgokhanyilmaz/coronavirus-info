import requests
import json

def get_information(country="Turkey"):
    response = requests.get("https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=\
        Country_Region%3D%27{}%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50&cacheHint=true".format(country))

    dict_data = json.loads(response.text)

    for info in dict_data.get("features"):
        result = info.get("attributes")
    
    return result 

def write_to_file(content):
    with open("message.txt", "w") as f: 
        f.write(str(content)) 

def main():
    write_to_file(get_information(country))
    mail_send.main()
