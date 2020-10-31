import winsound

playing = False

def alarm():
    global playing
    if playing == False:
        playing = True

        for i in range(10):
            winsound.Beep(700, 250)
            winsound.Beep(600, 250)

        playing = False