### Imports
from tkinter import *
from tkinter import filedialog
from tkinter import _setit as setit
import pyautogui, keyboard, mouse, time, random, ctypes, sys, os, json
from PIL import Image

rootWindow = Tk()


def is_admin(): # simple function
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

  
if not is_admin(): # I want a better way to use this rather than having the entirety of the code wrapped in an `else`. But my smol Python brain says this is the best I can do.
	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) # only works as executable 
else:
  # the actual code
  
	if os.path.exists("C:\\Program Files\\JesseBS2\\GCAutoSpam\\GCAutospam.config.json"):
		config = json.load(open("C:\\Program Files\\JesseBS2\\GCAutoSpam\\GCAutospam.config.json","r"))
		print("Found Configuration file, running normally....")
	else:
		
		config = {
			"stopshort": "esc",
			"send": "enter",
			"skipPrompt": False,
			"prgrmName": "GameChat AutoSpam v2.0.0",
			"doFilePath": False,
			"selectTimers": [
				"5 Loops",
				"10 Loops",
				"50 Loops",
				"100 Loops", 
				"200 Loops",
				"500 Loops",
				"1000 Loops",
				"2 Minutes",
				"5 Minutes",
				"10 Minutes"
			],
			"selectDelays": [
				0.02,
				0.05,
				0.1,
				0.5,
				1,
				3,
				5,
				10
			],
			"selectEscapes": [
				"esc",
				"tab",
				"backspace"
			],
			"selectTextWidth": [
				10,
				25,
				30,
				50,
				60,
				75,
				100,
				200
			],
			"TimersDefault": 50,
			"DelaysDefault": 0.02,
			"ClicksDefault": 0,
			"TextWidthDefault": 50,
			"RePressDefault": 1,
			"ChatKeyDefault": "t"
		}

		os.makedirs("C:\\Program Files\\JesseBS2\\GCAutoSpam\\",mode=0o777)
		with open("C:\\Program Files\\JesseBS2\\GCAutoSpam\\GCAutospam.config.json", "w") as outfile:
			outfile.write(json.dumps(config, indent = 2))

		print("No Configuration file, creating default....")


	print("Running Program: "+config["prgrmName"])

	### Window Styling
	rootWindow.title(config["prgrmName"])
	## Screen dimensions
	WindowWidth = 675
	WindowHeight = 250
	ScreenWidth = rootWindow.winfo_screenwidth()
	ScreenHeight = rootWindow.winfo_screenheight()

	rootWindow.geometry("%dx%d+%d+%d"%(WindowWidth,WindowHeight,(ScreenWidth/2)-WindowWidth/2,(ScreenHeight/2)-WindowHeight/1.5))


	DelaysDefault = DoubleVar()
	RePressDefault = IntVar()
	ClicksDefault = IntVar()
	TextWidthDefault = IntVar()
	FINDTEXT = StringVar()
	usingKey = StringVar()
	TextToUpdate = StringVar()
	stopshort = StringVar()

	DelaysDefault.set(config["DelaysDefault"])
	ClicksDefault.set(config["ClicksDefault"])
	RePressDefault.set(config["RePressDefault"])
	FINDTEXT.set("%s Loops"%(str(config["TimersDefault"])))
	usingKey.set("[%s] Click to Change"%(str(config["ChatKeyDefault"]).lower()))
	stopshort.set(config["stopshort"])


	SelcYes = "Yes(Better for spamming a text file into games)"
	SelcNo = "No(Better for spamming into another text input field)"

	### Functions

	def endPrgm():
		pyautogui.alert("Program has ended",config["prgrmName"]+"- Program End")


	def frmtText(text,counter):
		### Because of how order of operations works, replacing all the X and T's first will allow them to be used as values in operators that have inputs
		## Example is using the system time as an input in a random value as min or max
		### Unfortunately Math can not be done inside a random generator since generators are done first, so that limit's our possibilties some
		### But I've thought about it and I'd rather have random generators be used in math than math used in random generators
		### However if you feel otherwise you can switch there order but just copy/pasting one of the if statements in this function to where the other one is

		#if text.startsWith("^path "):
		#	config["doFilePath"] = True
		#	return True

		text = text.replace("[^x]",str(counter+1)).replace("[^t]","%sh:%sm:%ss"%(time.localtime(time.time()).tm_hour,time.localtime(time.time()).tm_min,time.localtime(time.time()).tm_sec)).replace("\\n","\n")

		if "[^r" in text:
			rGens = []
			for i in range(text.count("[^r")):
				#print(i)	
				#print(text.split("[^r"))
				#print(text.split("[^r")[i+1].split("]"))
				rGens.append([len(text.split("[^r")[i]),len(text.split("[^r")[i+1].split("]")[0])+4,float(text.split("[^r")[i+1].split("]")[0].split("r")[0]), float(text.split("[^r")[i+1].split("]")[0].split("r")[1])])
				### appends to the list an array within the array that hosts some information
				## First item is the length of the string before the rand operator
				## Second item is the length of everything before the operator and including the operator
				### The first two items can be used to get the index of everything before the operator and to get the index of everything after the operator
				## Third item is the minimum random value
				## Fourth item is the maximum random value
				### Then you can just take the two indexes that don't include the operator and generate a random number in place of where the operator was

			rGenLoop = 0
			while rGenLoop < len(rGens):
				chosenOne = 0
				if rGens[rGenLoop][2] > rGens[rGenLoop][3]:
					temp = rGens[rGenLoop][2]
					rGens[rGenLoop][2] = rGens[rGenLoop][3]
					rGens[rGenLoop][3] = temp
				chosenOne = random.randrange(rGens[rGenLoop][2],rGens[rGenLoop][3]+1)
				if rGens[rGenLoop][3]-rGens[rGenLoop][2] == 1:
					chosenOne = float(random.randrange(rGens[rGenLoop][2]*100,rGens[rGenLoop][3]*1000)/1000)

				text = text[:(rGens[rGenLoop][0])] + str(chosenOne) +  text[(rGens[rGenLoop][0]+rGens[rGenLoop][1]):]
				#print(rGens[rGenLoop])
				#print(text)
				rGenLoop += 1


		if "[^^" in text:
			createMath = []
			for i in range(text.count("[^^")):

				createMath.append([len(text.split("[^^")[i]),len(text.split("[^^")[i+1].split("]")[0])+4,text.split("[^^")[i+1].split("]")[0]])

			xLoop = 0
			while xLoop < len(createMath):
				text = text[:(createMath[xLoop][0])] + str(eval(createMath[xLoop][2])) +  text[(createMath[xLoop][0]+createMath[xLoop][1]):]
				xLoop += 1

		return text


	def browseFiles(src,inputparam):
		filename = filedialog.askopenfilename(
			initialdir = "/",
			title = "Select a plain text file .txt",
			filetypes = [("Text Files", '*.txt')]
		)

		if not filename.endswith(".txt"):
			pyautogui.alert("Not a text file",config["prgrmName"]+" - Error")
			return False

		src.delete(0,END)
		src.insert(0,"^path "+filename)



	def SpamDef(texttospam,openchat,gettimes,delaytime,doubleClick,sixthparam):
		## Set the input parameters as the default for the next time you use it!
		config["TimersDefault"] =  FINDTEXT.get().split(" ")[0]
		config["DelaysDefault"] = DelaysDefault.get()
		config["ClicksDefault"] = ClicksDefault.get()
		config["TextWidthDefault"] = TextWidthDefault.get()
		config["RePressDefault"] = RePressDefault.get()
		config["ChatKeyDefault"] = usingKey.get().split("]")[0].split("[")[1]
		config["stopshort"] = stopshort.get()
		with open("C:\\Program Files\\JesseBS2\\GCAutoSpam\\GCAutospam.config.json", "w") as outfile:
			outfile.write(json.dumps(config, indent = 2))

		if texttospam == "":
			pyautogui.alert("You didn't input any text!",config["prgrmName"]+" - Error!")
			return False
		pyautogui.alert("%s to start spamming.\n\nHold down `%s` while running ot stop(must be done near an interval when the message is sent)"%("`"+[config["ChatKeyDefault"]+"`","Use mouse double click"][doubleClick],stopshort.get()),config["prgrmName"])
		print("Opening chat with [%s]. Spamming \"%s\" for %s times with a %s seconds delay"%(openchat,texttospam,gettimes,float(delaytime)))
		print(doubleClick,sixthparam)



		if doubleClick == 1:
			mouse.wait("left","double")
		else:
			keyboard.wait(openchat)



		if texttospam.startswith("^path "):
			pretime = time.time()
			escapeFlag = False
			i = 0

			with open(texttospam.split("^path ")[1],"r") as infile:
				for lineoffile in infile:
					i += 1
					if escapeFlag == True: # check if the program should break or not
						break
						pyautogui.alert("Cancelled Spam",config["prgrmName"])

					time.sleep(0.05)
					# a slight delay helps to open up the game's chat and then send the message
					keyboard.write(frmtText(lineoffile.split("\n")[0],i))
					keyboard.press_and_release(config["send"])

					print("Sent "+str(i)+" Messages")

					# convert the delay into a readable range then loop through that range with a 0.01 second delay(this is where that 1.55 second error comes in)
					for detectHaltDelay in range(int((float(delaytime)/1.55)*100.00)): # convert the delay to an integer in the hundreds, accounting for the error
						if keyboard.is_pressed(stopshort.get()): # check if the user is hitting escape
							# flag the escape and exit the loop
							escapeFlag = True 
							pyautogui.alert("Escape key pressed, stopping spam.",config["prgrmName"])
							print("Escape key pressed, halting program")
							break
						time.sleep(0.01) # sleep in the loop so that the delay between sending messages still occurs, but you can also stop the program at any time during the loop

					if doubleClick == 0 and sixthparam == 1:
						keyboard.press_and_release(openchat)
			return

		elif gettimes.endswith(" Loops"):

			pretime = time.time()
			escapeFlag = False
			thisroundtime = time.time()
			"""
				thiroundtime was used during testing to find that a 0.01 second delay has about a 1.55 second error margin.

				So a 5 second delay would be 5*1.55 = 7.75 seconds. A whole 2 3/4th seconds longer than wanted!
				However this loop-inside loop method was needed so that the escape key could be pressed and stop spamming at any time during the run not just when it tries to send a message.
			"""

			for i in range(int(gettimes.replace(" Loops",""))): # Get the number of loops and iterate through them

				if escapeFlag == True: # check if the program should break or not
					break
					pyautogui.alert("Cancelled Spam",config["prgrmName"])

				time.sleep(0.05)
				# a slight delay helps to open up the game's chat and then send the message
				keyboard.write(frmtText(texttospam,i))
				keyboard.press_and_release(config["send"])

				print(time.time()-thisroundtime)
				print("Sent "+str(i+1)+" Messages")
				thisroundtime = time.time()

				# convert the delay into a readable range then loop through that range with a 0.01 second delay(this is where that 1.55 second error comes in)
				for detectHaltDelay in range(int((float(delaytime)/1.55)*100.00)): # convert the delay to an integer in the hundreds, accounting for the error
					if keyboard.is_pressed(stopshort.get()): # check if the user is hitting escape
						# flag the escape and exit the loop
						escapeFlag = True 
						pyautogui.alert("Escape key pressed, stopping spam.",config["prgrmName"])
						print("Escape key pressed, halting program")
						break
					time.sleep(0.01) # sleep in the loop so that the delay between sending messages still occurs, but you can also stop the program at any time during the loop

				if doubleClick == 0 and sixthparam == 1:
					keyboard.press_and_release(openchat)

			extime = time.time()
			print("Finished in "+format((extime-pretime),".2f")+" seconds")


		elif gettimes in ["2 Minutes","5 Minutes","10 Minutes"]:
			startTime = time.time()
			timerLoop = 0

			minConverts = int(gettimes.replace(" Minutes",""))

			while time.time()-startTime < 60*minConverts:
				if keyboard.is_pressed(stopshort.get()):
					print("Escape key pressed, halting program")
					break
					pyautogui.alert("Cancelled Spam",config["prgrmName"])

				if doubleClick == 0 and sixthparam == 1:
					keyboard.press_and_release(openchat)
				time.sleep(0.05)

				keyboard.write(frmtText(texttospam,timerLoop))
				keyboard.press_and_release(config["send"])
				print("Sent "+str(timerLoop)+" Messages")
				timerLoop += 1
		
	## An information Window exlpaining some things
	def showSpecialWindow():
		cheatWindow = Toplevel()
		cheatWindow.title("%s - Information"%config["prgrmName"])
		tipLabel = Label(cheatWindow,text="\n[^x] will be replaced with the amount of loops that have been run through")
		tipLabel2 = Label(cheatWindow,text="[^t] will be replaced with the current time of your device")
		tipLabel3 = Label(cheatWindow,text="[^r#r#] will generate a random number between and including the min/max values of the inputs, where # is an integer")
		tipLabel4 = Label(cheatWindow,text="[^^EQ] will do simple math where EQ is a math equation")
		tipLabel6 = Label(cheatWindow,text="After pressing the 'Start Spam' button, the window will not be useable until spamming has completed. But holding down the selected 'stop program' key(last input field) will halt the program. This must be done while one of the messages is being sent.")
		copyright = Label(cheatWindow,text="\n\nMade by JesseBS2")
		seperator = Label(cheatWindow,text="Tips for spamming with text")

		seperator.pack()
		tipLabel.pack(anchor="w")
		tipLabel2.pack(anchor="w")
		tipLabel3.pack(anchor="w")
		tipLabel4.pack(anchor="w")
		copyright.pack(anchor="se")

		cheatWindow.mainloop()

	# A better way to do this? Maybe. do I care? No.
	def DisableAlt(items):
		for item in items:
			item.set(0)

	## Main Window, get's all the inputz
	def LoadWindow():

		#basic labels
		label1 = Label(rootWindow, text="Text:")
		label2 = Label(rootWindow, text="How many loops:")
		label3 = Label(rootWindow, text="Open Gamechat key:")
		label4 = Label(rootWindow, text="How many seconds in between sending each message:")
		label5 = Label(rootWindow, text="Key to stop program:")
		entry1 = Entry(rootWindow, width=50,textvariable=TextToUpdate)
		chkbx1 = Checkbutton(rootWindow,text="Use Double click instead of keys",variable=ClicksDefault,command=lambda:DisableAlt([RePressDefault]))
		chkbx2 = Checkbutton(rootWindow,text="Press key again before sending text",variable=RePressDefault,command=lambda:DisableAlt([ClicksDefault]))
		dropmenu1 = OptionMenu(rootWindow, FINDTEXT,*config["selectTimers"])
		dropmenu2 = OptionMenu(rootWindow, DelaysDefault,*config["selectDelays"])
		dropmenu3 = OptionMenu(rootWindow, stopshort,*config["selectEscapes"])
		button1 = Button(rootWindow,text="Nevermind",command=closeWindow)
		button2 = Button(rootWindow,text="Start Spam",command=lambda:SpamDef(str(entry1.get()),config["ChatKeyDefault"],FINDTEXT.get(),DelaysDefault.get(),ClicksDefault.get(),RePressDefault.get()))
		button3 = Button(rootWindow,textvariable=usingKey,command=lambda:PopupKeys(button3))
		button4 = Button(rootWindow,text="Information",command=showSpecialWindow)
		button5 = Button(rootWindow,text="Use File",command=lambda:browseFiles(entry1,[label2,dropmenu1]))


		button4.grid(row=0,columnspan=2)
		label1.grid(row=1,column=0,sticky=W)
		entry1.grid(row=1,column=1)
		TextToUpdate.trace("w", lambda name, index, mode, sv=entry1: fixBrowseFilesUpdate(entry1,[label2,dropmenu1]))
		button5.grid(row=1,column=2)
		label3.grid(row=2,column=0,sticky=W)
		button3.grid(row=2,column=1)
		chkbx1.grid(row=4,columnspan=2,sticky=E)
		chkbx2.grid(row=5,columnspan=2,sticky=E)
		label2.grid(row=6,column=0,sticky=W)
		dropmenu1.grid(row=6,column=1)
		label4.grid(row=7,column=0,sticky=W)
		dropmenu2.grid(row=7,column=1)
		label5.grid(row=8,column=0,sticky=W)
		dropmenu3.grid(row=8,column=1)
		button1.grid(row=10,column=0)
		button2.grid(row=10,column=1)


		rootWindow.mainloop()


	def fixBrowseFilesUpdate(sv,inputparam):
		if sv.get().startswith("^path ") == False:
			inputparam[0].config(text="How many loops:")
			inputparam[1]['menu'].delete(0, 'end')
			
			for choice in config["selectTimers"]:
				inputparam[1]['menu'].add_command(label=choice, command=setit(FINDTEXT, choice))
		
		else:
			if sv.get().endswith(".txt") or sv.get().endswith(".rtf"):
				inputparam[0].config(text="Press send key:")
				inputparam[1]['menu'].delete(0, 'end')

				inputparam[1]['menu'].add_command(label=SelcYes, command=setit(FINDTEXT, SelcYes))
				inputparam[1]['menu'].add_command(label=SelcNo, command=setit(FINDTEXT, SelcNo))

			else:
				inputparam[0].config(text="Columns of text:")
				inputparam[1]['menu'].delete(0, 'end')

				for choice in config["selectTextWidth"]:
					inputparam[1]['menu'].add_command(label=choice, command=setit(FINDTEXT, choice))


	def closeWindow():

		config["TimersDefault"] =  FINDTEXT.get().split(" ")[0]
		config["DelaysDefault"] = DelaysDefault.get()
		config["ClicksDefault"] = ClicksDefault.get()
		config["TextWidthDefault"] = TextWidthDefault.get()
		config["RePressDefault"] = RePressDefault.get()
		config["ChatKeyDefault"] = usingKey.get().split("]")[0].split("[")[1]
		config["stopshort"] = stopshort.get()
		with open("C:\\Program Files\\JesseBS2\\GCAutoSpam\\GCAutospam.config.json", "w") as outfile:
			outfile.write(json.dumps(config, indent = 2))

			
		rootWindow.quit()
		config["skipPrompt"] = True

	 
	def PopupKeys(buttonFFF):
		mouselocation = mouse.get_position()
		keyboardWindow = Toplevel(rootWindow)
		keyboardWindow.title("Keyboard")
		keyboardWindow.geometry("400x170+%d+%d"%(mouselocation[0],mouselocation[1]))

		line0 = Frame(keyboardWindow)
		lineNums = Frame(keyboardWindow)
		line1 = Frame(keyboardWindow)
		line2 = Frame(keyboardWindow)
		line3 = Frame(keyboardWindow)
		line4 = Frame(keyboardWindow)

		line0.pack(side=TOP)
		lineNums.pack()
		line1.pack()
		line2.pack()
		line3.pack()
		line4.pack()

		currentKey = Label(line0,text="Current Key: "+config["ChatKeyDefault"])

		buttonTa = Button(lineNums,text="`~",command=lambda:Execute("`",keyboardWindow,buttonFFF),width=1)
		button1 = Button(lineNums,text="1",command=lambda:Execute("1",keyboardWindow,buttonFFF),width=1)
		button2 = Button(lineNums,text="2",command=lambda:Execute("2",keyboardWindow,buttonFFF),width=1)
		button3 = Button(lineNums,text="3",command=lambda:Execute("3",keyboardWindow,buttonFFF),width=1)
		button4 = Button(lineNums,text="4",command=lambda:Execute("4",keyboardWindow,buttonFFF),width=1)
		button5 = Button(lineNums,text="5",command=lambda:Execute("5",keyboardWindow,buttonFFF),width=1)
		button6 = Button(lineNums,text="6",command=lambda:Execute("6",keyboardWindow,buttonFFF),width=1)
		button7 = Button(lineNums,text="7",command=lambda:Execute("7",keyboardWindow,buttonFFF),width=1)
		button8 = Button(lineNums,text="8",command=lambda:Execute("8",keyboardWindow,buttonFFF),width=1)
		button9 = Button(lineNums,text="9",command=lambda:Execute("9",keyboardWindow,buttonFFF),width=1)
		button0 = Button(lineNums,text="0",command=lambda:Execute("0",keyboardWindow,buttonFFF),width=1)
		buttonMi = Button(lineNums,text="-",command=lambda:Execute("-",keyboardWindow,buttonFFF),width=1)
		buttonEq = Button(lineNums,text="+",command=lambda:Execute("=",keyboardWindow,buttonFFF),width=1)
		emptyButton2 = Button(lineNums,text="Back",width=5,state = DISABLED)

		emptyButton3 = Button(line1,text="Tab",width=3,state = DISABLED)
		buttonQ = Button(line1,text="Q",command=lambda:Execute("q",keyboardWindow,buttonFFF),width=1)
		buttonW = Button(line1,text="W",command=lambda:Execute("w",keyboardWindow,buttonFFF),width=1)
		buttonE = Button(line1,text="E",command=lambda:Execute("e",keyboardWindow,buttonFFF),width=1)
		buttonR = Button(line1,text="R",command=lambda:Execute("r",keyboardWindow,buttonFFF),width=1)
		buttonT = Button(line1,text="T",command=lambda:Execute("t",keyboardWindow,buttonFFF),width=1)
		buttonY = Button(line1,text="Y",command=lambda:Execute("y",keyboardWindow,buttonFFF),width=1)
		buttonU = Button(line1,text="U",command=lambda:Execute("u",keyboardWindow,buttonFFF),width=1)
		buttonI = Button(line1,text="I",command=lambda:Execute("i",keyboardWindow,buttonFFF),width=1)
		buttonO = Button(line1,text="O",command=lambda:Execute("o",keyboardWindow,buttonFFF),width=1)
		buttonP = Button(line1,text="P",command=lambda:Execute("p",keyboardWindow,buttonFFF),width=1)
		buttonBr = Button(line1,text="[ {",command=lambda:Execute("[",keyboardWindow,buttonFFF),width=1)
		buttonCB = Button(line1,text="] }",command=lambda:Execute("]",keyboardWindow,buttonFFF),width=1)
		buttonBS = Button(line1,text="\\ |",command=lambda:Execute("\\",keyboardWindow,buttonFFF),width=3)

		emptyButton4 = Button(line2,text="Caps",width=3,state = DISABLED)
		buttonA = Button(line2,text="A",command=lambda:Execute("a",keyboardWindow,buttonFFF),width=1)
		buttonS = Button(line2,text="S",command=lambda:Execute("s",keyboardWindow,buttonFFF),width=1)
		buttonD = Button(line2,text="D",command=lambda:Execute("d",keyboardWindow,buttonFFF),width=1)
		buttonF = Button(line2,text="F",command=lambda:Execute("f",keyboardWindow,buttonFFF),width=1)
		buttonG = Button(line2,text="G",command=lambda:Execute("g",keyboardWindow,buttonFFF),width=1)
		buttonH = Button(line2,text="H",command=lambda:Execute("h",keyboardWindow,buttonFFF),width=1)
		buttonJ = Button(line2,text="J",command=lambda:Execute("j",keyboardWindow,buttonFFF),width=1)
		buttonK = Button(line2,text="K",command=lambda:Execute("k",keyboardWindow,buttonFFF),width=1)
		buttonL = Button(line2,text="L",command=lambda:Execute("l",keyboardWindow,buttonFFF),width=1)
		buttonSe = Button(line2,text="; :",command=lambda:Execute(";",keyboardWindow,buttonFFF),width=1)
		buttonQu = Button(line2,text="' \"",command=lambda:Execute("'",keyboardWindow,buttonFFF),width=1)
		emptyButton5 = Button(line2,text="Enter",width=5,state = DISABLED)

		emptyButton6 = Button(line3,text="L_Shift",width=5,state = DISABLED)
		buttonZ = Button(line3,text="Z",command=lambda:Execute("z",keyboardWindow,buttonFFF),width=1)
		buttonX = Button(line3,text="X",command=lambda:Execute("x",keyboardWindow,buttonFFF),width=1)
		buttonC = Button(line3,text="C",command=lambda:Execute("c",keyboardWindow,buttonFFF),width=1)
		buttonV = Button(line3,text="V",command=lambda:Execute("v",keyboardWindow,buttonFFF),width=1)
		buttonB = Button(line3,text="B",command=lambda:Execute("b",keyboardWindow,buttonFFF),width=1)
		buttonN = Button(line3,text="N",command=lambda:Execute("n",keyboardWindow,buttonFFF),width=1)
		buttonM = Button(line3,text="M",command=lambda:Execute("m",keyboardWindow,buttonFFF),width=1)
		buttonCo = Button(line3,text=", <",command=lambda:Execute(",",keyboardWindow,buttonFFF),width=1)
		buttonPe = Button(line3,text=". >",command=lambda:Execute(".",keyboardWindow,buttonFFF),width=1)
		buttonFS = Button(line3,text="/ ?",command=lambda:Execute("/",keyboardWindow,buttonFFF),width=1)
		emptyButton7 = Button(line3,text="R_Shift",width=5,state = DISABLED)

		buttonLC = Button(line4,text="L_Ctrl",width=4,state = DISABLED)
		buttonCmd = Button(line4,text=" ",width=1,state = DISABLED)
		buttonLA = Button(line4,text="L_Alt",width=3,state = DISABLED)
		buttonSp = Button(line4,text="____",command=lambda:Execute("Space",keyboardWindow,buttonFFF),width=9)
		buttonRA = Button(line4,text="R_Alt",width=3,state = DISABLED)
		buttonFN = Button(line4,text="Fn",width=1,state = DISABLED)
		buttonThing = Button(line4,text="",width=1,state = DISABLED)
		buttonRC = Button(line4,text="R_Ctrl",width=4,state = DISABLED)



		currentKey.pack(side=TOP)

		buttonTa.pack(side=LEFT)
		button1.pack(side=LEFT)
		button2.pack(side=LEFT)
		button3.pack(side=LEFT)
		button4.pack(side=LEFT)
		button5.pack(side=LEFT)
		button6.pack(side=LEFT)
		button7.pack(side=LEFT)
		button8.pack(side=LEFT)
		button9.pack(side=LEFT)
		button0.pack(side=LEFT)
		buttonMi.pack(side=LEFT)
		buttonEq.pack(side=LEFT)
		emptyButton2.pack(side=LEFT)


		emptyButton3.pack(side=LEFT)
		buttonQ.pack(side=LEFT)
		buttonW.pack(side=LEFT)
		buttonE.pack(side=LEFT)
		buttonR.pack(side=LEFT)
		buttonT.pack(side=LEFT)
		buttonY.pack(side=LEFT)
		buttonU.pack(side=LEFT)
		buttonI.pack(side=LEFT)
		buttonO.pack(side=LEFT)
		buttonP.pack(side=LEFT)
		buttonBr.pack(side=LEFT)
		buttonCB.pack(side=LEFT)
		buttonBS.pack(side=LEFT)

		emptyButton4.pack(side=LEFT)
		buttonA.pack(side=LEFT)
		buttonS.pack(side=LEFT)
		buttonD.pack(side=LEFT)
		buttonF.pack(side=LEFT)
		buttonG.pack(side=LEFT)
		buttonH.pack(side=LEFT)
		buttonJ.pack(side=LEFT)
		buttonK.pack(side=LEFT)
		buttonL.pack(side=LEFT)
		buttonSe.pack(side=LEFT)
		buttonQu.pack(side=LEFT)
		emptyButton5.pack(side=LEFT)

		emptyButton6.pack(side=LEFT)
		buttonZ.pack(side=LEFT)
		buttonX.pack(side=LEFT)
		buttonC.pack(side=LEFT)
		buttonV.pack(side=LEFT)
		buttonB.pack(side=LEFT)
		buttonN.pack(side=LEFT)
		buttonM.pack(side=LEFT)
		buttonCo.pack(side=LEFT)
		buttonPe.pack(side=LEFT)
		buttonFS.pack(side=LEFT)
		emptyButton7.pack(side=LEFT)

		buttonLC.pack(side=LEFT)
		buttonCmd.pack(side=LEFT)
		buttonLA.pack(side=LEFT)
		buttonSp.pack(side=LEFT)
		buttonRA.pack(side=LEFT)
		buttonFN.pack(side=LEFT)
		buttonThing.pack(side=LEFT)
		buttonRC.pack(side=LEFT)


		keyboardWindow.mainloop()

	def Execute(key,window,button):
		usingKey.set("[%s] Click to Change"%key)
		window.withdraw()
		config["ChatKeyDefault"] = key
		button.config(textvariable=usingKey)



	LoadWindow()

	endPrgm()
