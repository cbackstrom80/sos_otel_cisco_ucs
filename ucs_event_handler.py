#from UcsSdk import *
from ucsmsdk import *
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.ucseventhandler import UcsEventHandle
import time
if __name__ == "__main__":
    try:
        # variable declaration
        ucsm_ip = '0.0.0.0'
        user = 'username'
        password = 'password'
        def callback_allevents(mce):
            print ('Received a New Event with ClassId: ' + str(mce.mo.classId) )
            print ("ChangeList: ", mce.changeList)
            print ("EventId: ", mce.eventId)
        handle = UcsHandle()
        handle.Login(ucsm_ip,user, password)
        ## As per the usage, choose the respective AddEventHandler format (As shown below).
        # It will watch UCS system for all events.
        allEventWatcher = handle.AddEventHandler()

        # It will watch UCS system for 100 sec.
        eventWatcherTimeOut = handle.AddEventHandler(timeoutSec = 60)

        # It will trigger callback function “callback_all” for the respective event.
        eventWatcherCB = handle.AddEventHandler( callBack= callback_allevents)
        time.sleep(90) handle.RemoveEventHandler(allEventWatcher)
        handle.RemoveEventHandler(eventWatcherTimeOut)
        handle.RemoveEventHandler(eventWatcherCB)

        # loop that keeps the script running for us to get events/callbacks
        while True:
            time.sleep(5)
        handle.Logout()

        except Exception, err:
            print ("Exception:", str(err))
            import traceback, sys
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60 )
            handle.Logout()