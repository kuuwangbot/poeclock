import urllib2,cookielib,json,time,sys,re
from Tkinter import *

url = "https://api.warframestat.us/pc/cetusCycle"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

#def updateColor():
    #Ra,Ga,Ba = '00','00','00'
    #Ra = text1.get("1.0",'end-1c')
    #Ga = text2.get("1.0",'end-1c')
    #Ba = text3.get("1.0",'end-1c')
    #RGBa = '#'+Ra+Ga+Ba
    #label.configure(fg=RGBa)
    #return 0


def convertDN(isDay):
	if isDay:
		return 'Night'
	else:
		return 'Day'
	return 'NA'

def updateDayTime():
	data = json.loads(urllib2.urlopen(urllib2.Request(url, headers=hdr)).read())
	timeLeft = data["timeLeft"]
	isDay = data["isDay"]

	hrS,minS,secS = '0h','0m','0s'
	hr,min,sec = 0,0,0
	if timeLeft.count(' ') == 2:
		hrS,minS,secS = timeLeft.split(" ")
	elif timeLeft.count(' ') == 1:
		minS,secS = timeLeft.split(" ")
	else:
		hrS,minS,secS = '0h','0m','0s'

	hr = int(re.sub("\D", "", hrS))
	min = int(re.sub("\D", "", minS))
	sec = int(re.sub("\D", "", secS))
	DN = convertDN(isDay)

	return hr,min,sec,DN

time_start = time.time()
hr,min,sec,DN = updateDayTime()

root = Tk()
root.title("Warframe Plains Time")
#text1 = Text(root,height=2,width=30)
#text3 = Text(root,height=2,width=30)
#text2 = Text(root,height=2,width=30)
#button1 = Button(root,text='Set',command = updateColor)

top = Toplevel()
top.title("Warframe Plains Time Window")
top.overrideredirect(1)
top.lift()
top.wm_attributes("-topmost", True)
top.geometry('%dx%d+%d+%d' % (400, 60, 0, -30))
top.configure(bg='white')
#top.wm_attributes("-disabled", True)
#top.wm_attributes("-transparentcolor", "white")
s = StringVar()
label = Label(top,textvariable=s,font=("Helvetica", 20),bg='white')

label.pack()
#text1.pack()
#text2.pack()
#text3.pack()
#button1.pack()

Ra,Ga,Ba = '00','00','00'

RGBa = '#'+Ra+Ga+Ba

label.configure(fg=RGBa)

while True:
    try:
        time.sleep(1)
        sec = sec - 1
        if sec <= 0:
            min -= 1
            sec = 60
            if min < 0:
				hr -= 1
				min = 60
            hr,min,sec,DN = updateDayTime()
        s.set("\r{hr} Hours {min} Minutes".format(hr=hr, min=min)+" until "+DN)

        root.update_idletasks()
        root.update()
    except KeyboardInterrupt, e:
        break
