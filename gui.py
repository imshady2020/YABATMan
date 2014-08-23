__author__ = 'joe'
# -*- coding: utf-8 -*-
from Tkinter import *
import Tkinter as tk
import piper as Piper
import electrumHandling as electrum
from threading import Thread, Event, Timer
import serial


state = "welcome"
maxAmountTransaction = 800
rate = 40000
feeATM = 0.05
feeTx=0.00000
ticketCM=18
paperDistCM = 1524 - 300 # 300 M of pink shitz in the end of the roll...
priv = 0
pub = 0
ticketPrinted=0
idAfter = None
timeout=20000
amountWanted=0
cashInserted=0
sent = 0


def genKey():

    global sent, pub, priv

    # Gen Keys
    import genkeys as btckeys
    btckeys.genKeys()

    if btckeys.keysAreValid == False:
        print("Error: The generated keys (public/private) are not the correct length.  Please try again.")


    pub = btckeys.pubkey
    priv = btckeys.privkey

    f = open('customers', 'a+')
    strToWrite = "\nPublic Key: " + btckeys.pubkey + "\nPrivate Key: " + btckeys.privkey + "\nWanted " + "XXX" + " BTC"
    f.write(strToWrite)
    f.write("\n---------------------------------\n")
    f.close()


    amountBTC = round(((float(amountWanted)/rate)*(1-feeATM))-feeTx, 5)

    # Send BTC !
    # alright = electrum.sendBTC(pub, amountBTC)
    # sent = alright
    sent = 1
    # return 1
    #return btckeys.pubkey, btckeys.privkey

    root.after(100, fsm, 'd')


def disableCash():
    ser.write('o')

def enableCash():
    ser.write('i')

def disableKb():
    ser.write('b')

def enableKb():
    ser.write('a')

def printKey():

    global paperDistCM, ticketCM
    paperDistCM = paperDistCM-ticketCM
    Piper.print_keypair(pub, priv)
    root.after(100, fsm, 'd')

    #fsm("d")


def backToNormalDisplay():
    textWarn.set('')

def fade_in(self):
        alpha = self.attributes("-alpha")
        alpha = min(alpha + .01, 1.0)
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(10, self.fade_in)

def fade_out(self):
        alpha = self.attributes("-alpha")
        alpha = min(alpha - .01, 1.0)
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(10, self.fade_out)

def idleState():
        text.set('')
        textPound.set('')
        textTwo.set('')
        textThree.set('')
        textWarn.set('We sell Bitcoins !')

def textReset():
    text.set('')
    textPound.set('')
    textTwo.set('')
    textThree.set('')
    textWarn.set('')

def fsm(newChar):
    global state,shitz,maxAmountTransaction,rate,feeATM,paperDistCM,ticketCM,priv,pub,ticketPrinted,idAfter,timeout, \
        amountWanted, cashInserted, funcId, sent


    # ##### Input Handling FSM  #####
    if state == "welcome":  # Welcome
        if newChar != None:
            state = "disclaimer"

            # Start Timer
            #idAfter = root.after(timeout, fsm, '!')
            #print "KILLING >>  " +  testId + "   NAO"
            #root.after_cancel(testId)


    # Disclaimer
    elif state == "disclaimer":
        if newChar == '!':  # Return to Welcome, timer elapsed
            state = "welcome"

        elif newChar == 'v':
            state = "enterAmount"

            # Restart Timer
            #root.after_cancel(idAfter)
            #idAfter = root.after(timeout, fsm, '!')



    # Enter Amount
    elif state == "enterAmount":

        # Return to Welcome, timer elapsed
        if newChar == '!':
            state = "welcome"


        # + pressed, next Step
        elif newChar == 'v':

            # Empty Text
            if textTwo.get() == "":
                return

            # Text Not Valid
            elif ((int(textTwo.get()) < 4) or (int(textTwo.get())%5!=0)):
                textWarn.set('Please, insert multiples of £5. Minimum of £5')
                root.after(5000, backToNormalDisplay)

            # Text Valid
            else:
                amountWanted = int(textTwo.get())
                cashInserted = 0

                state = "checkCash"
                enableCash()
                #root.after_cancel(idAfter)



        # Reset Timer if a digit, or c pressed
        #elif newChar.isdigit() or newChar == "c":
            #root.after_cancel(idAfter)
            #idAfter = root.after(timeout, fsm, '!')


    # Check Cash
    elif state == "checkCash":

        if newChar == 'x': cashInserted = cashInserted + 5
        elif newChar == 'y': cashInserted = cashInserted + 10
        elif newChar == 'z': cashInserted = cashInserted + 20

        if (amountWanted-cashInserted) <= 0 :
            disableKb()
            disableCash()
            state = "sendBTC"



    # Send BTC
    elif state == "sendBTC":
        root.after(100, genKey)
        state = "tempSend"


    # Dumb state
    elif state == "tempSend":
        if(sent): state = "print"
        else: state = ""


    # Print
    elif state == "print":

        if newChar == "d":
            enableKb()
            state ='check'

        else: return



    elif state == "check":
        #if idAfter != '': root.after_cancel(idAfter)
        #idAfter = root.after(60000, fsm, 'r')

        #root.bind('<KeyPress>', onKeyPress)

        if newChar == 'r' :
            state = "thanks"
        elif newChar == 'l' and ticketPrinted < 3:
            state = "print"



    # Thanks
    elif state == "thanks": # Thx
        state = "welcome"






    # ######  Outputs FSM    ######

    # Welcome
    if state=="welcome":
        textReset()
        text.set('HI !')


    # Disclaimer
    elif state == "disclaimer":
        textReset()
        text.set('Beware ! BTC kills da kitteh !')


    # Enter Amount
    elif state == "enterAmount":
        text.set('Enter Amount Wanted :')
        textPound.set('£')


        # Sanitize and display amount

        # Remove 1 char
        if newChar == 'c' and (textTwo.get() != None):
            textTwo.set(textTwo.get()[:-1])
            if textTwo.get() != '':
                amount=str(round(((float(textTwo.get())/rate)*(1-feeATM))-feeTx, 5))
                textThree.set('You will get ' + amount + ' Bitcoins !')

        # Add 1 char, and update BTC Count
        elif newChar.isdigit() and (int(textTwo.get() + newChar)) < maxAmountTransaction+1:
            textTwo.set(textTwo.get() + newChar)  # Add Char
            amount=str(round(((float(textTwo.get())/rate)*(1-feeATM))-feeTx,5))
            textThree.set('You will get ' + amount + ' Bitcoins !')

        # Going over limit
        elif newChar.isdigit():
            textWarn.set('£' + str(maxAmountTransaction) + ' is the maximum allowed !')
            root.after(2000, backToNormalDisplay)

        # Empty both string if amount is none
        if textTwo.get() == '':
            textThree.set('')



    # Enter Amount
    elif state=="checkCash":
        textReset()
        text.set('Insert Cash...')
        toInsert = amountWanted-cashInserted
        print str(toInsert)
        disp = 'Insert £ ' + str(toInsert)
        textTwo.set(disp)



    # Send BTC
    elif state=="sendBTC":
        textReset()
        text.set('Bitcoins are being sent...')
        # Return TRUE == Go back into the FSM
        return TRUE






    # Print BTC
    elif state=="print":

        textReset()
        text.set('Printing in progess...')

        # Print and update ticket printed cound
        root.after(1000, printKey)

        ticketPrinted = ticketPrinted + 1



    # Check Integrity
    elif state == "check":

        #funcId = root.bind('<KeyPress>', onKeyPress)

        textReset()
        text.set('Take your receipt')

        if ticketPrinted == 2:
            textTwo.set('This is your last attempt to print a ticket')
            textThree.set('Press continue, or reprint if the quality isn\'t good enough')
            textWarn.set('By pressing continue, you acknowledge the quality of the printed material')

        elif ticketPrinted == 3:
            textThree.set('and press continue')


        else:
            #textTwo.set('Please check that everything is readable')
            textThree.set('Press continue, or reprint if the quality isn\'t good enough')
            textWarn.set('By pressing continue, you acknowledge the quality of the printed receipt')



    elif state == "thanks": # Thx
        pub = 0
        priv = 0
        ticketPrinted = 0
        cashInserted = 0
        amountWanted = 0
        sent = 0
        textReset()
        text.set('Cheers')

        root.after(5000, fsm, 'b')



def onKeyPress(event):

    print "GOT  >  " + event.char

    # Disable input in cpu consuming tasks
    if state == "print" or state == "sendBTC":
        return

    goback = fsm(event.char)
    if goback: root.after(200, fsm, 'd')




root = tk.Tk()
root.geometry('480x234')
root.configure(background='#2C3E50')

# Frame 1
firstFrame = tk.Frame(root, background='#2C3E50')
firstFrame.pack(pady=50)


text = StringVar()
text.set('Ohai !')
textTwo = StringVar()
textTwo.set('')
textWarn = StringVar()
textWarn.set('')
textThree = StringVar()
textWarn.set('')
textPound = StringVar()
textPound.set('')

#image = Image.open("pic1.png")
#photo = ImageTk.PhotoImage(image)


# Pic
"""
im = Image.open("pic1.bmp")
img = ImageTk.PhotoImage(im)
print im.mode
label = tk.Label(firstFrame, image=img)
label.grid(row=0, column=0, columnspan=4)
"""

# Label 1
lab = tk.Label(firstFrame, textvariable=text, background='#2C3E50', foreground='#fff',font=('font.ttf', 20))
lab.grid(row=0, column=0, columnspan=2)
#lab.pack(pady=20, fill=X)

# Label Pound
labPound = tk.Label(firstFrame, textvariable=textPound, background='#2C3E50', foreground='#fff',font=('font.ttf', 20))
labPound.grid(row=1, column=0, sticky=E)
#labPound.pack(side=LEFT, padx=195)

# Label 2
labTwo = tk.Label(firstFrame, textvariable=textTwo, background='#2C3E50', foreground='#fff',font=('font.ttf', 20))
labTwo.grid(row=1, column=1, sticky=W)
#labTwo.pack(fill=X)

# Label 3
labThree = tk.Label(firstFrame, textvariable=textThree, background='#2C3E50', foreground='#fff',font=('font.ttf', 20))
labThree.grid(row=2, column=0, columnspan=2 )
#labThree.pack(fill=X, side=TOP)

# Label Warn
labWarn = tk.Label(firstFrame, textvariable=textWarn, background='#2C3E50', foreground='#E74C3C',font=('font.ttf', 20))
labWarn.grid(row=3, column=0, columnspan=2)
#labWarn.pack(fill=X, side=TOP)

#lab.grid(row=0, column=0, sticky=W+N, padx=80, pady=75)
#lab.pack()

ser = serial.Serial('/dev/tty.usbserial-A9MXHFZB', 9600)


root.bind('<KeyPress>', onKeyPress)
root.mainloop()
