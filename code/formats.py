# Custom formats
import sys
class notify:
	# A class to format our warnings, errors, and notifications as they are printed to command line
	# To use: call constructor and pass optional arguments for warning color, error color, and notification color (defaults are
	# yellow, red, and blue). warn(), error(), and notice() methods will take in a string and format it appropriately,
	# printing it to the command line. Syntax: notify(warncolor='some color', errorcolor='some color', noticecolor='some color').
	# Uses ANSI formatting codes.
	
	# Define some default values that can be called from any instance for quick custom formatting
	RED='\033[91m'
	YELLOW='\033[93m'
	GREEN='\033[92m'
	BLUE='\033[94m'
	CYAN='\033[96'
	MAGENTA='\033[95m'
	BLACK='\033[90m'
	WHITE='\033[97m'
	END='\033[0m'
	BOLD='\033[1m'
	
	# Constructor - takes in a few optional arguments that allows you to change the default notification values based on
	# the class of notification (warning, error, or notice)
	def __init__(self,warncolor='YELLOW',errorcolor='RED',noticecolor='GREEN'):
		codes=['\033[91m','\033[93m','\033[92m','\033[94m','\033[95m']
		colors=['RED','YELLOW','GREEN','BLUE','PURPLE']
		colordict = dict(zip(colors,codes))
		# print(colordict)
		self.warn_color=colordict[warncolor]
		self.error_color=colordict[errorcolor]
		self.notice_color=colordict[noticecolor]
		if warncolor in colors:
			self.warn_color=colordict[warncolor]
		if errorcolor in colors:
			self.error_color=colordict[errorcolor]
		if noticecolor in colors:
			self.notice_color=colordict[noticecolor]

	# Notify functions that will automatically format and print a notification depending on its classification
	# Will optionally return the formatted message instead of printing if if passed toprint=False
	def warn(self,msg,toprint=True):
		fmsg='{}{}[WARNING]: {}{}'.format(self.warn_color,self.BOLD,msg,self.END)
		if toprint:
			print(fmsg)
		else:
			return fmsg

	def error(self,msg,toprint=True):
		fmsg='{}{}[ERROR]: {}{}'.format(self.error_color,self.BOLD,msg,self.END)
		if toprint:
			print(fmsg)
		else:
			return fmsg

	def notice(self,msg,toprint=True):
		fmsg='{}{}{}{}'.format(self.notice_color,self.BOLD,msg,self.END)
		if toprint:
			print(fmsg)
		else:
			return fmsg

class progressBar:
	# A class used for indicating progress in a task with a defined endpoint
	_RED='\033[91m'
	_YELLOW='\033[93m'
	_GREEN='\033[92m'
	_BLUE='\033[94m'
	_CYAN='\033[96'
	_MAGENTA='\033[95m'
	_BLACK='\033[90m'
	_WHITE='\033[97m'
	_END='\033[0m'
	_BOLD='\033[1m'

	_PROGRESS= 0                # Hidden variable for tracking progress of bar

	# The way it works: call the constructor and define the aspects of the progress bar if so desired. 
	# Next, call the .update() method and pass it an optional message to display beneath the progress bar 
	def __init__(self, btype="\u2588", blen=20, bcolor1=_WHITE, bcolor2=_BLACK, msg=""):

		codes=['\033[91m','\033[92m','\033[93m','\033[94m','\033[95m','\033[96m','\033[97m','\033[90m']
		colors=['RED','GREEN','YELLOW','BLUE','MAGENTA','CYAN','WHITE','BLACK']
		colorpicker=dict(zip(colors,codes))

		self.barType=btype
		self.barLength=blen
		self.display=msg
		self.colorStart=bcolor1
		self.colorEnd=bcolor2

		if bcolor1.upper() in colors:
			self.colorStart=colorpicker[bcolor1.upper()]
		if bcolor2.upper() in colors:
			self.colorEnd=colorpicker[bcolor2.upper()]
		
	# Here is where we update progress. This value is called with an increment (number from 0 to 1) that will define how much progress has transpired since the last call
	def update(self, increment, msg="", pmsg=False):

		eraseScreen="\033[2J"
		toHome="\033[H"
		eraseLine="\033[2K\r"
		nextLine="\033[1E"
		prevLine="\033[1F"

		# Build the string that will serve as this iteration of our progress bar
		# The progress bar is a string of "barType" characters, "barLength" in number.
		# To build it, we create the string of "barType" characters (it's the same every time)
		# and increment where the color change occurs.

		# Check to see if we are at the beginning of the progress bar.
		if self._PROGRESS>0:
			print(eraseLine+prevLine+eraseLine+prevLine)

		if pmsg:
			print(pmsg)

		self._PROGRESS+=increment
		# Some code to ensure the printed progress bar will never be longer than specified by the user
		if self._PROGRESS>1:
			self._PROGRESS=1
		
		numComplete=int(self._PROGRESS*self.barLength)
		numToGo=self.barLength-numComplete

		bar_str=self.colorStart
		for i in range(0,numComplete):
			bar_str=bar_str+self.barType

		bar_str=bar_str+self._END+self.colorEnd
		for i in range(0,numToGo):
			bar_str=bar_str+self.barType

		bar_str=bar_str+self._END
		bar_str=bar_str+"   |   {0:.1f}%".format(self._PROGRESS*100)

		if msg != "":
			self.display=msg

		print(bar_str+f"\n{self.display}",end="\r")

	def reset(self):
		eraseScreen="\033[2J"
		toHome="\033[H"
		eraseLine="\033[2K\r"
		nextLine="\033[1E"
		prevLine="\033[1F"
		# Simple method to reset progress to 0
		self._PROGRESS=0
		self.display=""
		print(eraseLine+prevLine+eraseLine+prevLine)

		