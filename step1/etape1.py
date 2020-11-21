import xmltodict
import json
from pprint import pprint


with open("/Users/zarmi/Desktop/platon/etape1/plat.tet45_eng.xml", "r") as xml_file:
    xml = xml_file.read()

converted_xml = xmltodict.parse(xml)

with open("plat.tet45_eng.json", "w") as json_file:
    json.dump(converted_xml, json_file)

