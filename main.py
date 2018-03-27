"""HacktheTesla code by Anil  Özen and Jan-Paul Konijn. Code gathers data form the Tesla using the TeslaApi. Documentation on the TeslaApi can be found at the following linkt
https://timdorr.docs.apiary.io/ , """

from tesla import *
import threading
import schedule          # """This import needs a external download"""
import time
if __name__ == '__main__':

    myUI = UI()
    myUI.Start()
    mycar = Datareceive_tesla("")
    mycar.get_Token()
    cal = CalculatorClass()
    mycar.get_carlistdata()


    shift = "D"


    def push_efficientcy():

        try:
            if mycar.get_data('drive_state')['response']['speed']  == None and shift == "D":

                print("hello world")
            else:
                print("not printed")
        except:
            print("failed to push data")
    schedule.every(1).minutes.do(push_efficientcy)

    def push_charging():
        battery_logged = False

        try:
            if data == "Engaged" and data2 > 0:
                battery_logged = True
            if data == "Blocking" and battery_logged == True:
                battery_logged = False

                cal.price_calculator()
                pushdata
        except:
            print("failed to push data")





        
    push_efficientcy()
    
    # print(mycar.get_data("charge_state"))
    # print(mycar.get_data("drive_state"))
    # print(mycar.get_data('drive_state')['response']['speed'])




    def UI():
        app = gui()
        app.addGoogleMap("m1")
        app.setGoogleMapSize("m1", "300x500")
        app.searchGoogleMap("m1","{},{}".format(mycar.get_data('drive_state')['response']['latitude'],mycar.get_data('drive_state')['response']['longitude']))
        app.setGoogleMapMarker("m1","{},{}".format(mycar.get_data('drive_state')['response']['latitude'],mycar.get_data('drive_state')['response']['longitude']), size=None, colour=None, label=None, replace=False)
        app.go()


    def main():
        print(mycar.get_data("charge_state"))
    main()
    UI()



 
        



    #some test comment





    # def update():
    #     
    #
    # def prec():
    #
    #     schedule.every(1).seconds.do(print(str(cal.efficiency(mycar.get_data("charge_state")['response']['est_battery_range'],mycar.get_data("charge_state")['response']['ideal_battery_range']))+"%"))
    # def update2():
    #     schedule.every(1).seconds.do(prec)
    #
    # t1= threading.Thread(update2())
    #
    # t2=threading.Thread(update())
    # t1.start
    # t2.start
    # t1.join
    # t2.join
    #
    #





    while True:
        schedule.run_pending()
        time.sleep(1)



  

