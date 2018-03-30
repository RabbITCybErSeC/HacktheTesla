"""HacktheTesla code by Anil  Özen and Jan-Paul Konijn. Code gathers data form the Tesla using the TeslaApi. Documentation on the TeslaApi can be found at the following linkt
https://timdorr.docs.apiary.io/ , """

from tesla import *
from dBoperator import *
import schedule          # """This import needs a external download"""
import time


# to get the data insert the datatype: The following datatypes can be used, climate_state, drive_state, gui_settings, vehicle_state,  charge_state. Insert these to get the right
# data that is wanted. Documentation on the data can be found at the following website:


if __name__ == '__main__':

    myUI = UI()
    database = DBoperator()
    cal = CalculatorClass()
    myUI.Start()

    mycar = Datareceive_tesla(myUI.username,myUI.password)
    mycar.get_Token()
    mycar.get_carlistdata()


    def push_efficientcy():
        print("check1")

        try:
            state_check = mycar.retrieve_data("drive_state",["shift_state","speed"])
        except Exception as e:
            print(e)
            print("Unable to load data")



        try:

            if state_check[1]  != None and state_check[2] == "D":
                print("Car is driving")
                response = mycar.retrieve_data("charge_state", ["est_battery_range", "ideal_battery_range"])
                data_push = []
                data_push.append(response[0])
                data_push.append(cal.efficiency(response[1], response[2]))
                database.push_to_database("drive_efficiency", data_push)
                print("Database update succesful")

            else:
                print("No Update")
        except:
            print("failed to push data")


    def push_charging():
        print("check2")
        priceKWH = 0.25

        battery_logged = False

        try:
            state_check = mycar.retrieve_data("charge_state",["charge_port_latch", "charger_power", "charge_energy_added"])


        except Exception as e:
            print(e)
            print("Unable to load data")

        try:
            if state_check[1] == "Engaged" and state_check[2] > 0:

                battery_logged = True
                print("check")

            if state_check[1] == "Blocking" and battery_logged == True:

                state_check = mycar.retrieve_data("charge_state",["charge_port_latch", "charger_power", "charge_energy_added"])
                
                data_push = []
                data_push.append(state_check[0])
                data_push.append(cal.price_calculator(state_check[3], priceKWH))
                data_push.append(state_check[3])
                database.push_to_database("charge_logs", data_push)
                battery_logged = False

        except:
            print("failed to push data")

    def UI():
        app = gui()
        app.addGoogleMap("m1")
        app.setGoogleMapSize("m1", "300x500")
        app.searchGoogleMap("m1","{},{}".format(mycar.get_data('drive_state')['response']['latitude'],mycar.get_data('drive_state')['response']['longitude']))
        app.setGoogleMapMarker("m1","{},{}".format(mycar.get_data('drive_state')['response']['latitude'],mycar.get_data('drive_state')['response']['longitude']), size=None, colour=None, label=None, replace=False)
        app.go()

    schedule.every(1).minutes.do(push_efficientcy)
    schedule.every(1).minutes.do(push_charging)

    # UI()


    while True:
        schedule.run_pending()
        time.sleep(1)



  

