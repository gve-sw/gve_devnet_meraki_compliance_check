""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

# Import Section
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
import meraki_code
import openpyxl

# load all environment variables
load_dotenv()
api_key= os.environ["MERAKI_API_KEY"]


# Global variables
app = Flask(__name__)
selected_org=None
selected_network=None
networks=[]
success = []
error = ""
##Routes
#Instructions

#Index
@app.route('/', methods=["GET", "POST"])
def index():
    global selected_org, selected_network, networks
    if request.method == "POST":
        selected_org=request.form.get('organizations_select')
        selected_network=request.form.get('network')
        meraki_code.read_input_file()
        compliant_list,non_compliant_list =meraki_code.get_saml_and_security(selected_org)
        ssid_non_compliant_list=meraki_code.get_networks_ssids(selected_org)
        vlan_non_compliant_list=meraki_code.get_networks_vlans(selected_org)
        sw_non_compliant_list,ap_non_compliant_list,net_non_compliant_list=meraki_code.get_org_devices(selected_org)

        return render_template('home.html', hiddenLinks=True, networks=networks, selected_elements={'organization':selected_org, 'network_id':selected_network},compliant_list=compliant_list,non_compliant_list=non_compliant_list,ssid_non_compliant_list=ssid_non_compliant_list,vlan_non_compliant_list=vlan_non_compliant_list,sw_non_compliant_list=sw_non_compliant_list,ap_non_compliant_list=ap_non_compliant_list,net_non_compliant_list=net_non_compliant_list, url="https://dashboard.meraki.com")
    else:
        try:
            return render_template('home.html', hiddenLinks=True, dropdown_content=get_orgs_and_networks(), networks=networks, selected_elements={'organization':selected_org, 'network_id':selected_network}, success=success, error=error, url="https://dashboard.meraki.com")
        except Exception as e: 
            print(e)  
            return render_template('home.html', error=False, errormessage="Something went wrong.", errorcode=e, hiddenLinks=True)


@app.route("/extract-input", methods=["GET","POST"])
def upload_file_function():
    global CSV_UPLOADED
    uploaded_file = request.files
    file_dict = uploaded_file.to_dict()
    the_file = file_dict["file"]
    if not the_file.filename.lower().endswith('.xlsx'):
        return "Please upload a valid xlsx format"
    with open('uploaded.xlsx', 'wb') as f:
        f.write(the_file.read())
    
    return "Read xlsx file"

def get_orgs_and_networks():
    url = "https://api.meraki.com/api/v1/organizations"

    payload = None

    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": api_key
    }

    orgs = requests.request('GET', url, headers=headers, data = payload).json()
    result=[]
    
    for org in orgs:
        
            org_entry = {
                "orgaid" : org['id'],
                "organame" : org['name'],
                "networks" : []
            }
            orgId=org['id']

            url = "https://api.meraki.com/api/v1/organizations/"+orgId+"/networks"

            payload = None

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Cisco-Meraki-API-Key": api_key
                    }

            networks = requests.request('GET', url, headers=headers, data = payload).json()
            for network in networks:
                    org_entry['networks'] += [{
                    'networkid' : network['id'],
                    'networkname' : network['name']
                }]
            result += [org_entry]
    return result

def read_input_file():
    dataframe = openpyxl.load_workbook("uploaded.xlsx" )

    excel_sheets=[]
    global templates_list
    templates_list={}
    for sheet in dataframe.worksheets:
        excel_sheets.append(sheet.title)
        templates_list[sheet.title]=[]

    for sheet in excel_sheets:
        dataframe1 = dataframe[sheet]
        templates_list[sheet]=[]
        for row in range(1,dataframe1.max_row+1):  
            for column in "A":  
                cell_name = "{}{}".format(column, row)
                i=dataframe1[cell_name].value 
            for column in "B": 
                cell_name = "{}{}".format(column, row)
                ii=dataframe1[cell_name].value 
                entry={}
                entry={str(i):str(ii)}
                templates_list[sheet].append(entry)
    return templates_list


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5100, debug=True)