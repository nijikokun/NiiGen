# Author: Nijiko Yonskai <nijikokun@gmail.com>

""" NiiGen v1.0
    Psuedo-Random Password/Key Generator
    Made for windows, unsure if it will work in other OS. It should.
    
        - Supports lower and upper case, digits, special characters.
        - Preventing Ambigious Characters
            - These are characters that may be seen as others: ilo, 10
        - Allowing of the requirement of every character type
        - Generating To Input
        - Generating To Input and Clipboard
"""

import wx
import sys
import random

# Window Properties
title = "NiiGen"
size = (170,200)

"""
# Debugging
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    raw_input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit
"""

# Sorting
def rand(x, y):
    return random.randint(0,1) * 2 - 1;
    
class Frame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__(*args, **kwargs)
        
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetBackgroundColour(wx.WHITE)
        
        # Settings
        self.length = 11
        self.lower = True
        self.upper = True
        self.digit = True
        self.specs = False
        self.ambig = False
        self.reqev = False
        
        # Chars
        self.lowerChars = "abcdefghjkmnpqrstuvwxyz"
        self.upperChars = "ABCDEFGHJKMNPQRSTUVWXYZ"
        self.digitChars = "23456789"
        self.specsChars = "!@#$%^&*"
        self.lowerAmbig = "ilo"
        self.upperAmbig = "ILO"
        self.digitAmbig = "10"

        # Building
        self.build()
        self.defaults()
        self.bind()
        
        # Initializing
        self.Show(True)
        self.style = self.GetWindowStyle()
        self.onTop()
        
    def build(self):
        self.txtLength = wx.TextCtrl(self.panel, -1, '', pos=(4, 5), size=(155, 20))
        self.txtOutput = wx.TextCtrl(self.panel, -1, '', pos=(4, 115), size=(155, 20)) 
        self.chkLower = wx.CheckBox(self.panel, -1, 'a-z', (5, 30))
        self.chkUpper = wx.CheckBox(self.panel, -1, 'A-Z', (70, 30))
        self.chkDigits = wx.CheckBox(self.panel, -1, '0-9', (128, 30))
        self.chkSpecial = wx.CheckBox(self.panel, -1, 'Special', (5, 50))
        self.chkAmbigious = wx.CheckBox(self.panel, -1, 'Avoid Ambiguous Characters', (5, 70))
        self.chkRequired = wx.CheckBox(self.panel, -1, 'Require Every Char Type', (5, 90))
        self.btnGenerate = wx.Button(self.panel, -1, 'Generate', (3, 145))
        self.btnGenCopy = wx.Button(self.panel, -1, 'Gen + Copy', (83, 145))
        
    def defaults(self):
        for control, value in \
        [(self.chkLower, self.lower),
        (self.chkUpper, self.upper),
        (self.chkDigits, self.digit),
        (self.chkSpecial, self.specs),
        (self.chkAmbigious, self.ambig),
        (self.chkRequired, self.reqev),
        (self.txtLength, str(self.length))]:
            control.SetValue(value)
    
    def bind(self):
        for control, event, handler in \
        [(self.chkLower, wx.EVT_CHECKBOX, self.onLower),
        (self.chkUpper, wx.EVT_CHECKBOX, self.onUpper),
        (self.chkDigits, wx.EVT_CHECKBOX, self.onDigits),
        (self.chkSpecial, wx.EVT_CHECKBOX, self.onSpecial),
        (self.chkAmbigious, wx.EVT_CHECKBOX, self.onAmbigious),
        (self.chkRequired, wx.EVT_CHECKBOX, self.onRequired),
        (self.txtLength, wx.EVT_TEXT, self.onLengthUpdate),
        (self.btnGenerate, wx.EVT_BUTTON, self.onGenerate),
        (self.btnGenCopy, wx.EVT_BUTTON, self.onGenCopy)]:
            control.Bind(event, handler)
    
    def onTop(self):
        self.SetWindowStyle( self.style | wx.STAY_ON_TOP )
    
    def onUpper(self, event):
        self.upper = event.Checked()
    def onLower(self, event):
        self.lower = event.Checked()
    def onDigits(self, event):
        self.digit = event.Checked()
    def onSpecial(self, event):
        self.specs = event.Checked()
    def onAmbigious(self, event):
        self.ambig = event.Checked()
    def onRequired(self, event):
        self.reqev = event.Checked()
    def onLengthUpdate(self, event):
        try:
            self.length = int(self.txtLength.GetValue())
        except:
            self.length = 11
            self.txtLength.SetValue('11')
        if self.length > 256:
            self.length = 256
            self.txtLength.SetValue('256')
    def onGenerate(self, event):
        self.Clear()
        output = self.Generate()
        self.txtOutput.SetValue(output)
    def onGenCopy(self,event):
        self.Clear()
        output = self.Generate()
        self.txtOutput.SetValue(output)
        clip = wx.TextDataObject()
        clip.SetText(output)
        if not wx.TheClipboard.IsOpened():
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(clip)
            wx.TheClipboard.Close()
    def Generate(self):
        positions = []
        chars = []
        output = ""
        minLower = 0
        minUpper = 0
        minSpecs = 0
        minDigit = 1
        if self.reqev:
            minLower = 1
            minUpper = 1
            minSpecs = 1
        if not self.ambig:
            lowerChars = list(self.lowerChars + self.lowerAmbig)
            upperChars = list(self.upperChars + self.upperAmbig)
            digitChars = list(self.digitChars + self.digitAmbig)
            specsChars = list(self.specsChars)
        else:
            lowerChars = list(self.lowerChars)
            upperChars = list(self.upperChars)
            digitChars = list(self.digitChars)
            specsChars = list(self.specsChars)
        if self.upper: chars += upperChars
        if self.lower: chars += lowerChars
        if self.digit: chars += digitChars
        if self.specs: chars += specsChars
        if self.lower and minLower > 0:
            for j in range(minLower):
                positions.append('L')
        if self.upper and minUpper > 0:
            for j in range(minUpper):
                positions.append('U')
        if self.digit and minDigit > 0:
            for j in range(minDigit):
                positions.append('D')
        if self.specs and minSpecs > 0:
            for j in range(minSpecs):
                positions.append('S')
        while len(positions) < self.length:
            positions.append('A')
        positions = positions[0:self.length]
        positions.sort(cmp=rand)
        for j in positions:
            if j is 'L':   output += random.choice(lowerChars)
            elif j is 'U': output += random.choice(upperChars)
            elif j is 'D': output += random.choice(digitChars)
            elif j is 'A': output += random.choice(chars)
            elif j is 'S': output += random.choice(specsChars)
        return output
    def Clear(self):
        self.txtOutput.Clear()
    
# Finalize
app = wx.App(False)
frame = Frame(None, wx.ID_ANY, title, size=size, style=wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU)

# Icon
_icon = wx.Icon('lib/lock.ico', wx.BITMAP_TYPE_ICO)
frame.SetIcon(_icon)

# Start
app.MainLoop()


