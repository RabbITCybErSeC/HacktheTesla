"""HacktheTesla code by Anil  Özen and Jan-Paul Konijn. Code gathers data form the Tesla using the TeslaApi. Documentation on the TeslaApi can be found at the following linkt
https://timdorr.docs.apiary.io/ , """


import json
from urllib.request import Request, urlopen
import requests
import time
import datetime
from appJar import gui
import objectpath


class Datareceive_tesla(object):

#ACCESTOKEN FOR THE TESLA IS REQUIRED
    def __init__(self, email, password):

        self.accescodetesla =0
        self.vehicleid= 0
        self.vehicle_engery_amout = {}
        self.email = email
        self.password = password

    def get_Token(self): #This function generates an accesstoken that is needed to acces the Tesla data

        req = requests.post('https://owner-api.teslamotors.com/oauth/token', data={'grant_type': 'password', 'client_id': 'e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e', 'client_secret': 'c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220', 'email': self.email, 'password': self.password})
        if req.status_code == 200:
            response = req.json()
            self.accescodetesla = response['access_token']
            print ('Your token is: %s' % response['access_token'])
            print ('This token will expire: %s' % (datetime.datetime.fromtimestamp(response['created_at']) + datetime.timedelta(seconds=response['expires_in'])))
        elif req.status_code == 401:
            print ('Incorrect username or password')
        elif req.status_code == 404:
            print ('API server has changed, contact the developer of this script: j.konijn@student.utwente.nl')
        elif req.status_code == 500:
            print ('An internal server error occurred. Either Tesla API is down or the API has changed since this script was developed.')
        else:
            print (req.reason)

    def get_carlistdata(self): 
         headers = {"Authorization": "Bearer %s" % self.accescodetesla}
         request = Request('https://owner-api.teslamotors.com/api/1/vehicles', headers=headers)
         response_body=urlopen(request)
         data = json.load(response_body)
         self.vehicleid = data['response'][0]['id_s']
         return data


    #to get the data insert the datatype: The following datatypes can be used, climate_state, drive_state, gui_settings, vehicle_state,  charge_state. Insert these to get the right
    #data that is wanted. Documentation on the data can be found at the following website:


    def get_data(self,datatype):
        headers = {"Authorization": "Bearer %s" % self.accescodetesla}
        request = Request('https://owner-api.teslamotors.com/api/1/vehicles/{}/data_request/{}'.format(self.vehicleid, datatype), headers=headers)
        response_body = urlopen(request)
        data = json.load(response_body)
        return data

    #returns an array of values from specified data table of API. Values are obtained by being searched with json_parameters 

    def retrieve_data(self, datatype, json_parameters): 
        headers = {"Authorization": "Bearer %s" % self.accescodetesla}
        request = Request('https://owner-api.teslamotors.com/api/1/vehicles/{}/data_request/{}'.format(self.vehicleid, datatype), headers=headers)
        response_body = urlopen(request)
        data = json.load(response_body)

        json_parameters.insert(0, "timestamp") 
        retrived_data = []

        for item in json_parameters:
            tree_obj = objectpath.Tree(data)
            tree_obj_query_string = []
            tree_obj_query_string.append('$..')
            tree_obj_query_string.append(item)
            tree_obj_query = ''.join(tree_obj_query_string)
            json_data =  tuple(tree_obj.execute(tree_obj_query))
            retrived_data.append(json_data[0])

        return retrived_data

class CalculatorClass(object):

    def efficiency(self, rangedriv, idealrange):
        precentageEfficiency = (rangedriv/ idealrange)*100
        return round(precentageEfficiency,2)


    def start_time(self):
        start = time.time()
        return start
    def stop_time(self):
        stop = time.time()
        return stop

    def time_calculator(self, startime,stoptime):
        return stoptime-startime

        #deliver time in seconds, power in W
    def price_calculator(self, added_KWH, price_KWH):

        return added_KWH * price_KWH

    def Refesh_Rate(self, refreshtime):
        return refreshtime


class UI(object):
    def __init__(self):
        self.username = ""
        self.password = ""
    def Prepare(self, app):

        app.setTitle("Login Form")
        app.setFont(16)
        app.setStopFunction(self.BeforeExit)
        app.addLabel("userLab", "Username:", 0, 0)
        app.addEntry("username", 0, 1)
        app.addLabel("passLab", "Password:", 1, 0)
        app.addSecretEntry("password", 1, 1)
        app.addButtons(["Submit", "Cancel"], self.Submit, colspan=2)
        return app

    def Start(self):

        app = gui()
        app = self.Prepare(app)
        self.app = app
        app.go()

    def BeforeExit(self):
        return self.app.yesNoBox("Confirm Exit", "Are you sure you want to exit the application?")

    def Submit(self, btnName):

        if btnName == "Submit":
            self.username = self.app.getEntry("username")
            self.password = self.app.getEntry("password")






