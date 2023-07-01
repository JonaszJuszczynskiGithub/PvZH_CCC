# PvZHCCC.py

# PvZH_CCC Version 1.0.1

# to do list:
# add a github
# redo backgrounds completley
# add guide to menu
# add rightclick menu for thigns like reset, save image, copy paste etc
# double class cards
# superpowers
# heros with 4 superpowers
# save custom card as template
# make custom sets, store all cards as one and navigate through them

# imports
import io
import os
import string
import textwrap
import PySimpleGUI as sg
import re
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import textwrap
sg.set_options(font=("Cafeteria-Black", 18))
sg.theme('DarkGray9')

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("PNG (*.png)", "*.png"),
              ("All files (*.*)", "*.*")]

with open('PvZH_CCC_Release_Notes.txt', 'r') as file:
    versionhistorytext = file.read()

with open('about.txt', 'r') as file:
    abouttext = file.read()

# window layout
menu_def = [
            ['File', ['New', 'Save', 'Exit',]], ['Info', ['About', 'Version History']],
           ]

types = ['Zombie', 'Zombie Trick', 'Zombie Environment', 'Plant', 'Plant Trick', 'Plant Environment']
typesc = ['Zombie Trick', 'Zombie Environment', 'Plant Trick', 'Plant Environment']
typesd = ['Zombie', 'Zombie Trick', 'Zombie Environment']
rarity = ['Legendary', 'Super-Rare','Rare', 'Uncommon', 'Common', 'Event', 'Token']
zclasses = ['Beastly', 'Brainy', 'Crazy', 'Hearty', 'Sneaky']
pclasses = ['Guardian', 'Kabloom', 'Mega-Grow', 'Smarty', 'Solar']
classes = ['Beastly', 'Brainy', 'Crazy', 'Hearty', 'Sneaky', 'Guardian', 'Kabloom', 'Mega-Grow', 'Smarty', 'Solar']
backgrounds = ['PvZ Heroes Website', 'PvZ Heroes Lawn', 'Transparent', 'Plant Collection', 'Zombie Collection', 'User Background']

z = [[sg.Text('Strength', expand_x=False), sg.Input(size=(3, 10), expand_x=False, k='-STINPUT-'), sg.Text('Health', expand_x=False), sg.Input(size=(3, 10), expand_x=False, k='-HEINPUT-')],[sg.Text('1', visible=False)]]

tabcard = [
            [sg.Text('Card Art', expand_x=True),
            sg.Input(size=(25, 1), enable_events=True, key="-FILE-", expand_x=True),
            sg.FileBrowse(file_types=file_types)],
            [sg.Text('Adjust Card Art Position', expand_x=True),
            sg.Button('Reset Position'),
            sg.Text('x'), sg.Input(size=(5,1), default_text='0', enable_events=True, key='-CARDXPOSITION-'),
            sg.Text('y'), sg.Input(size=(5,1), default_text='0', enable_events=True, key='-CARDYPOSITION-')],
            [sg.Text('Adjust Card Art Size', expand_x=True),
            sg.Button('Reset Size'),
            sg.Text('width'), sg.Input(size=(5,1), default_text='300', enable_events=True, key='-CARDWIDTH-'),
            sg.Text('height'), sg.Input(size=(5,1), default_text='350', enable_events=True, key='-CARDHEIGHT-')],
            [sg.Text('Change Background'), sg.Combo(backgrounds, default_value='PvZ Heroes Website', expand_x=True, enable_events=True,  readonly=True, key='-BACKGROUNDSELECT-')],
          ]

tabsave = [
            # options to save the image
            [sg.Text('Location'),sg.Input(size=(25, 1), enable_events=True, key="-SAVEIMAGE-", expand_x=True, default_text= os.getcwd()+'/Cards'),
            sg.FolderBrowse()],
            [sg.Text('File Name'),sg.Input(size=(25, 1), enable_events=True, key="-FILENAME-", expand_x=True),
            sg.Button("Save")],
          ]

taboptions = [
            [sg.Text('Credit'), sg.Input(size=(10,1), expand_x=True, key="-CREDIT-", enable_events=True)],
            [sg.Text('Upload Background'), sg.Input(size=(25, 1), enable_events=True, key="-UPLOADBG-", expand_x=True),
            sg.FileBrowse(file_types=file_types), sg.Button('Reset', enable_events=True, key='-RESETCUSTOMBG-')],
            [sg.Button('Reset All', key="-RESETALL-", enable_events=True), sg.Push(),
            sg.Text('Resize Image'), sg.Input(size=(3,1), key="-RESIZEIMAGE-", enable_events=True, default_text="100"), sg.Text('%')],
            [sg.Text('Card Text Font Size'), sg.Input(size=(3,1), key="-CTFS-", enable_events=True)]
             ]

tab1=sg.Tab("Card", tabcard)
tab2=sg.Tab("Save", tabsave)
tab3=sg.Tab("Options", taboptions)

# form layout
inputs = [     
            [sg.Text('Name'), sg.Input(size=(12, 10), k='-NINPUT-'), sg.Text('Cost'), sg.Input(size=(3, 10), k='-COINPUT-')], 
            [sg.Column(z, key='-c-')],
            [sg.Text('Card Type'), sg.Combo(types, size=(20, 10), expand_x=True, enable_events=True,  readonly=True, k='-TCOMBO-')],
            [sg.Text('Class'), sg.Combo(classes, size=(10, 10), expand_x=True, enable_events=True,  readonly=True,  k='-CCOMBO-')],
            [sg.Text('Tribes'), sg.Input(size=(10, 10), expand_x=True, k='-TRINPUT-')],
            [sg.Push(), sg.Text('Card Text'), sg.Push()],
            [sg.Multiline(size=(10, 10), expand_x=True, enable_events=True, k='-CARDTEXT-')],
            [sg.Text('Rarity'), sg.Combo(rarity, size=(10, 10), expand_x=True, enable_events=True, readonly=True, key='-RCOMBO-', default_value='Uncommon')],
            [sg.Text('Set'), sg.Input('Premium', size=(10, 10), expand_x=True, k='-SETINPUT-')],
            [sg.Push(), sg.Text('Flavour Text'), sg.Push()],
            [sg.Multiline(size=(10, 3), expand_x=True, k='-FLAVOURTEXT-')], 
         ]

# image generator layout
card = [    
            # card image
            [sg.Push(), sg.Text('Card Image'), sg.Push()],
            [sg.Image( key="myimg", expand_x=True, expand_y=True)],
            [sg.Push(), sg.Button("Generate Card"),
            sg.Button("Quick Save"), sg.Push()],
            [sg.TabGroup([[tab1, tab2, tab3]], size=(733,200))],
       ]

# complete layout
layout = [
            [sg.Menu(menu_def)],
            [sg.vtop(   
            [
                sg.Frame('Card Creator', inputs, key='-LAYOUTCARD1-'),
                sg.Column(card, key='-LAYOUTCARD2-')
            ])],
                ]

# creates the window
window = sg.Window('PvZ Heroes Custom Card Creator', layout, finalize=True)

global sclass 
sclass = 'guardian'
global vrarity
vrarity = 'uncommon'
global cname
cname = "Name"
global ctribe
ctribe = ""
global ctype 
ctype = ""
global cset
cset = "Premium"
global cardtext
cardtext = ""
global ccost
global chealth
global cstrength
global cardfilename
global istransparent
istransparent = 0
cardfilename = "PvZHCustomCard"

# function for drawing an underline
def draw_underline_text(draw, pos, text, font, **options):
    twidth, theight = draw.textsize(text, font=font)
    lx, ly = pos[0], pos[1] + theight
    draw.text(pos, text, font=font, **options)
    draw.line((lx, ly, lx + twidth, ly), fill=(58,213,244), width=4)

def open_info():
    templyinfo = [[sg.Push(), sg.Text('Version History', font=('Cafeteria-Black', 30)), sg.Push()],[sg.Text(versionhistorytext)]]
    layoutinfo = [
        [sg.Column(templyinfo,scrollable=True, vertical_scroll_only=True)],
                 ]
    window = sg.Window("Version History", layoutinfo, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
    window.close()
    
def open_about():
    abouttextwrap = textwrap.fill(abouttext, 70, replace_whitespace=False)
    templyabout = [[sg.Push(), sg.Text('About', font=('Cafeteria-Black', 30)), sg.Push()],[sg.Text(abouttext)]]
    layoutabout = [
        [sg.Column(templyabout)],
                 ]
    window = sg.Window("About", layoutabout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
    window.close()
    
# defines card text size, changable
cardtextfontsize = 42
previouscardname = ''
# events
while True:
    event, values = window.read()
    #print('event:', event)
    #print('values:', values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    # opens version history window
    if event == 'Version History':
        open_info()
        
    # opens about window
    if event == 'About':
        open_about()
    
    # window events
    # updates when form is triggered
    if event == "-TCOMBO-":
        # updates whether health and text inputs are visible for not minion cards
        if values['-TCOMBO-'] in typesc:
            window['-c-'].update(visible=False)
        else:
            window['-c-'].update(visible=True)
        # updates whether zombie or plant classes are used
        if values['-TCOMBO-'] in typesd:
            window['-CCOMBO-'].update(values=zclasses)
        else:
            window['-CCOMBO-'].update(values=pclasses)

    # checks last selected class
    if event == "-CCOMBO-":    
        sclass = values['-CCOMBO-']
        sclass = sclass.lower()
    
    if event == "-RCOMBO-":    
        vrarity = values['-RCOMBO-']
        vrarity = vrarity.lower()

    # resets position of art
    if event == "Reset Position":
        window['-CARDXPOSITION-'].update(0)
        window['-CARDYPOSITION-'].update(0)

    # resets size of art
    if event == "Reset Size":
        window['-CARDWIDTH-'].update(300)
        window['-CARDHEIGHT-'].update(350)
    
    # resets all values of options
    if event == '-RESETALL-' or event == "New":
        window['-NINPUT-'].update(value='')
        window['-COINPUT-'].update(value='')
        window['-TCOMBO-'].update(value='')
        window['-CCOMBO-'].update(value='')
        window['-STINPUT-'].update(value='')
        window['-HEINPUT-'].update(value='')
        window['-TRINPUT-'].update(value='')
        window['-CARDTEXT-'].update(value='')
        window['-RCOMBO-'].update(value='')
        window['-SETINPUT-'].update(value='')
        window['-FLAVOURTEXT-'].update(value='')
        window['-SETINPUT-'].update(value='Premium')
        window['-CARDXPOSITION-'].update(value='0')
        window['-CARDXPOSITION-'].update(value='0')
        window['-CARDWIDTH-'].update(value='300')
        window['-CARDHEIGHT-'].update(value='350')
        window['-BACKGROUNDSELECT-'].update(value='PvZ Heroes Website')
        window['-CREDIT-'].update(value='')
    
    # when user selects a custom background, change background value to custom background
    if event == '-UPLOADBG-':
        window['-BACKGROUNDSELECT-'].update(value='Custom Background')
    
    # resets to no custom background
    if event == '-RESETCUSTOMBG-':
        window['-UPLOADBG-'].update(value='')
        window['-BACKGROUNDSELECT-'].update(value='PvZ Heroes Website')
    
    # changes card text size FIX
    # if event == '-CTFS-':
    #     try:
    #         cardtextfontsize = int(window['-CTFS-'].get())
    #     except:
    #         continue
    
    # starts generating the custom image
    if event == "Generate Card" or event == "Save" or event == "Quick Save" or event == "Save":
        filename = "./Platforms/Icons/PvZ_Heroes_website_background.jpg"
        filename2 = "./Platforms/Plants/Guardian.png"
        if os.path.exists(filename) & os.path.exists(filename2):
            # checks whether to use zombie or plant folder
            global typepvz
            if sclass in [x.lower() for x in pclasses]:
                    typepvz = 'Plants'
            else:
                typepvz = 'Zombies'

             # draws the type
            ctribe = values['-TRINPUT-']
            ctype = values['-TCOMBO-']
            ctypet = ""

            # loads in images                

            # change background
            noft = 0
            if window['-FLAVOURTEXT-'].get() == '':
                noft = 100
    
            if values['-UPLOADBG-'] != '' and values['-BACKGROUNDSELECT-'] == 'Custom Background':
                image = Image.open(window['-UPLOADBG-'].get()).convert("RGBA").resize((1920,1160-noft))
            elif values['-BACKGROUNDSELECT-'] == 'PvZ Heroes Website':
                image = Image.open("./Platforms/Icons/PvZ_Heroes_website_background.jpg").convert("RGBA").resize((1920,1160-noft))
            elif values['-BACKGROUNDSELECT-'] == 'PvZ Heroes Lawn':
                image = Image.open("./Platforms/Icons/PvZLawn.jpg").resize((1920,1160-noft)).convert("RGBA")
            elif values['-BACKGROUNDSELECT-'] == 'Transparent':
                image = Image.open("./Platforms/Icons/transparent.png").convert("RGBA").resize((990,1160-noft))
            elif values['-BACKGROUNDSELECT-'] == 'Plant Collection':
                image = Image.open("./Platforms/Icons/plantingame.png").convert("RGBA").resize((990,1160-noft))
            elif values['-BACKGROUNDSELECT-'] == 'Zombie Collection':
                image = Image.open("./Platforms/Icons/zombieingame.png").convert("RGBA").resize((990,1160-noft))
            else:
                image = Image.open("./Platforms/Icons/PvZ_Heroes_website_background.jpg").convert("RGBA").resize((1920,1160-noft))
                window['-BACKGROUNDSELECT-'].update(value='PvZ Heroes Website')

            platform = Image.open(os.path.join(fr'./Platforms/{typepvz}/{sclass}.png')).resize((824,629)).convert("RGBA")
            platformart = Image.open(fr'./Platforms/{typepvz}/{sclass}2.png').resize((350,350)).convert("RGBA")
            iconart = Image.open(fr'./Platforms/Icons/PvZH_{sclass}_Icon.png').resize((120,120)).convert("RGBA")
            rarityart = Image.open(fr'./Platforms/Icons/{vrarity}.png').resize((853,280)).convert("RGBA")
            # checks whether to use brains or sun
            if ctype == 'Zombie' or ctype == 'Zombie Trick' or ctype == 'Zombie Environment':
                costart = Image.open(fr'./Platforms/Icons/UI_brain.png').resize((125,125)).convert("RGBA")
                window['-STINPUT-'].update(value='')
                window['-HEINPUT-'].update(value='')
            else:
                costart = Image.open(fr'./Platforms/Icons/icon_sun.png').resize((130,130)).convert("RGBA")

            # Gets art from user, otherwise sets missing default image
            artw = int(values['-CARDWIDTH-'])
            arth = int(values['-CARDHEIGHT-'])        
            if os.path.exists(values['-FILE-']):
                cardart = Image.open(values['-FILE-']).resize((artw,arth)).convert("RGBA")
            else:
                cardart = Image.open(fr'./Platforms/Icons/MISSING_ASSET.png').resize((300,450)).convert("RGBA")

            if values['-BACKGROUNDSELECT-'] == 'Transparent' or values['-BACKGROUNDSELECT-'] == 'Plant Collection' or values['-BACKGROUNDSELECT-'] == 'Zombie Collection':
                istransparent = 470
            else:
                istransparent = 0

            # pastes the images
            image.paste(platform, (548-istransparent,318), mask=platform)
            image.paste(platformart, (785-istransparent,88), mask=platformart)
            image.paste(iconart, (1177-istransparent, 293), mask=iconart)
            image.paste(rarityart, (535-istransparent, 823), mask=rarityart)
           
            # sets creator credit
            if window['-CREDIT-'].get() != '':
                myFontCredit = ImageFont.truetype("Cafeteria-Bold.otf", 50)
                drawCredit = ImageDraw.Draw(image)
                creditlines = textwrap.wrap(values['-CREDIT-'], width=16)
                ycredittext = 40
                for line in creditlines:
                    creditw, credith = myFontCredit.getsize(line)
                    drawCredit.text((40, ycredittext + 50), line, font=myFontCredit, fill=(255,255,255), stroke_width=1, stroke_fill=(0,0,0))
                    ycredittext += credith

                wcred, hcred = myFontCredit.getsize(values['-CREDIT-'])
                drawCredit.text((40,40), 'Created by:', font=myFontCredit, fill=(255,255,255), stroke_width=1, stroke_fill=(0,0,0))
                
            # changes arts position
            artx = int(values['-CARDXPOSITION-'])
            arty = int(values['-CARDYPOSITION-'])         
            image.paste(cardart, (810-istransparent + artx, 7 + arty), mask=cardart)

            image.paste(costart, (1055-istransparent, 93), mask=costart)          
            
            # draws the name
            cname = values['-NINPUT-']
            W, H = (300, 300)
            d1 = ImageDraw.Draw(image)       
            myFont = ImageFont.truetype("Cafeteria-Black.ttf", 75)
            w, h = myFont.getsize(cname)
            d1.text(( ((W-w)/2)+814-istransparent,((H-h)/2)+324), cname, font=myFont, fill=(255,255,255))

            # draws the cost health and strength
            ccost = values['-COINPUT-']
            chealth = values['-HEINPUT-']
            cstrength = values['-STINPUT-']

            #cost
            W10, H10 = (30, 30)
            d10 = ImageDraw.Draw(image)
            myFont10 = ImageFont.truetype("Cafeteria-Black.ttf", 85)
            w10, h10 = myFont10.getsize(ccost)
            d10.text(( ((W10-w10)/2)+1105-istransparent,((H10-h10)/2)+133), ccost, font=myFont10, fill=(0,0,0))
            
            # sets if type is zombie / plant, trick or environment
            if ctype == "Zombie" or ctype == "Plant":
                ctypet = "- " + ctribe + " " + ctype + " -"
            elif ctype == "Zombie Trick" or ctype == "Plant Trick":
                ctypet = "- " + ctribe + "Trick -"
            elif ctype == "Zombie Environment" or ctype == "Plant Environment":
                ctypet = "- " + ctribe + "Environment -"
            else:
                ctypet= ""

            W1, H1 = (300,300)
            d2 = ImageDraw.Draw(image)
            myFont1 = ImageFont.truetype("Cafeteria-Bold.otf", 40)
            w1, h1 = myFont1.getsize(ctypet)
            d2.text(( ((W1-w1)/2)+813-istransparent,((H1-h1)/2)+393), ctypet, font=myFont1, fill=(170,170,170))

            # draws the set and rarity
            cset = values['-SETINPUT-']
            settext = cset + " - " + vrarity
            # if event card, remove set from text
            if vrarity == 'event' or vrarity == 'token':
                settext = vrarity
            W2, H2 = (300,300)
            settext = settext.upper()
            d3 = ImageDraw.Draw(image)
            myFont2 = ImageFont.truetype("Cafeteria-Black.ttf", 65)
            w2, h2 = myFont2.getsize(settext, stroke_width=1)
            # changes rarity text color if super-rare or rare
            rcolor = 255,255,255
            rbordercolor = 0,0,0
            if vrarity == 'rare':
                rcolor = 248,232,153
                rbordercolor = 0,0,0
            if vrarity == 'super-rare':
                rcolor = 167,202,242
                rbordercolor = 59, 76, 133
            d3.text(( ((W2-w2)/2)+810-istransparent,878), settext, font=myFont2, fill=(rcolor), stroke_width=1, stroke_fill=(rbordercolor))

            # draws the text box
            cardtext = values['-CARDTEXT-']
            boldtext = re.findall(r'(?i)(When played:)|(When destroyed:)|(Before combat here:)|(When hurt:)|(While in an Environment:)|(When played in an Environment:)|(\w Evolution:)|(While in your hand:)|(When played on the ground)|(Start of turn:)|(End of turn:)|(Before combat here:)|(After combat here:)|(When played on heights:)|(When played in water:)|(When revealed:)|(Fusion:)|(^(.+?):)', cardtext, flags=re.MULTILINE)
            myFont3 = ImageFont.truetype("Cafeteria-Bold.otf", 42)
            myFont3Bold = ImageFont.truetype("Cafeteria-Black.ttf", 42)
            myFontsh = ImageFont.truetype("Cafeteria-Bold.otf", 35)
            # list of keywords with icons
            keywordslist = ['Armored', 'Deadly', 'Bullseye', 'Anti-Hero', 'Double Strike', 'Frenzy', 'Overshoot', 'Strikethrough', 'Untrickable','Freeze']
            abilitieslist = ['Amphibious','Bounce','Conjure','Dino-Roar','Freeze','Fusion:','Gravestone','Hunt','Splash Damage','Team-Up']
            shlist = ['Strength', 'Health', 'Brain', 'Sun']
            # code for dynamically changing text box based on icons or bold text
            w3, h3 = (300,300)
            # defines a dictionary of dynamic values, changes with where we draw each line
            dct = {1: 'd4', 2: 'd6', 3: 'd7', 4: 'd8', 5: 'd8'} 
            selecteddctvalue = 1 
            dct["selecteddctvalue"] = ImageDraw.Draw(image)
            splitbt = []
            line1length = 0
            artkeywordtemp = [] # list of which keywords are in first line, so we can change health or strength art
            # if theres bold text, include the : in the split
            tempsplitbt = []
            if boldtext:
                splitbt = re.split('\n|(?<=:)', cardtext)
                boldlength = 0
            else:
                splitbt = re.split('\n', cardtext)    
            # defining variables
            sizeoftextlist = len(splitbt)
            linespacingtextbox = 45
            followbold = 100
            outputline = 1 # increments which line to output text on
            # loops over each line
            for idx, x in enumerate(splitbt):  
                previouswordlength = 0    
                # define specific paste if text is bold, then exits that loop
                if ':' in x:
                    keywordtexttemp = re.findall(r'(?i)(Armored\s\d|Deadly|Bullseye|Anti-Hero|Double Strike|Frenzy|Overshoot\s\d|Strikethrough|Untrickable|Freeze)', splitbt[idx+1])
                    shtemp = re.findall(r"(?i)(-?[0-9]\sStrength|-?[1-9][0-9]\sStrength|-?[0-9]\sHealth|-?[1-9][0-9]\sHealth|\+[0-9]\sStrength|\+[1-9][0-9]\sStrength|\+[0-9]\sHealth|\+[1-9][0-9]\sHealth)", splitbt[idx+1])
                    shlength2 = 0
                    for z in shtemp:
                        shnumber3 = re.split('\s',z)
                        wsh3, hsh3 = myFontsh.getsize(shnumber3[0], stroke_width=1)
                        shlength2 = shlength2 + (myFontsh.getlength(z)/2) - wsh3/2
                    _, _, W3, H3 = dct["selecteddctvalue"].textbbox((0, 0), splitbt[idx] + splitbt[idx+1], font=myFont3)
                    dct["selecteddctvalue"].text((((w3 - W3)/2) + 803-istransparent - (len(keywordtexttemp)*20) + shlength2, 575 + (linespacingtextbox*(outputline-1))), splitbt[idx], font = myFont3Bold, align="center")
                    followbold = idx+1
                    boldlength = myFont3.getlength(splitbt[idx])  
                    continue
                else:
                    _, _, W3, H3 = dct["selecteddctvalue"].textbbox((0, 0), splitbt[idx], font=myFont3)           
                outputline = outputline + 1 # increments to go to next line
                selecteddctvalue = selecteddctvalue + 1 # increments dictionary value                   
                isbold = 0
                splitkt = []
                # finds all keyword instances 
                kwpattern = r"(?i)(Armored\s\d|Deadly|Bullseye|Anti-Hero|Double Strike|Frenzy|Overshoot\s\d|Strikethrough|Untrickable|Freeze|Amphibious|Bounce|Conjure|Dino-Roar|Freeze|Fusion:|Gravestone|Hunt|Splash Damage|Team-Up|-?[0-9]\sStrength|-?[1-9][0-9]\sStrength|-?[0-9]\sHealth|-?[1-9][0-9]\sHealth|\+[0-9]\sStrength|\+[1-9][0-9]\sStrength|\+[0-9]\sHealth|\+[1-9][0-9]\sHealth|-?[0-9]\sBrain.?|-?[1-9][0-9]\sBrain.?|-?[0-9]\sSun.?|-?[1-9][0-9]\sSun.?|\+[0-9]\sBrain.?|\+[1-9][0-9]\sBrain.?|\+[0-9]\sSun.?|\+[1-9][0-9]\sSun.?)"
                keywordtext2 = re.findall(kwpattern, splitbt[idx])
                table = str.maketrans({"+": "\+"})
                keywordtext = []
                for x in keywordtext2:
                    keywordtext.append(x.translate(table))
                if keywordtext:    
                    # splits at each location of keyword
                    if len(keywordtext) == 1:                   
                        keywordregex = r"(?=" + keywordtext[0] + ")|(?<=" + keywordtext[0] +")"
                    elif len(keywordtext) == 2:                   
                        keywordregex = r"(?=" + keywordtext[0] + ")|(?<=" + keywordtext[0] +")|(?=" + keywordtext[1] + ")|(?<=" + keywordtext[1] +")"
                    elif len(keywordtext) == 3:                   
                        keywordregex = r"(?=" + keywordtext[0] + ")|(?<=" + keywordtext[0] +")|(?=" + keywordtext[1] + ")|(?<=" + keywordtext[1] +")|(?=" + keywordtext[2] + ")|(?<=" + keywordtext[2] +")"
                    elif len(keywordtext) == 4:                   
                        keywordregex = r"(?=" + keywordtext[0] + ")|(?<=" + keywordtext[0] +")|(?=" + keywordtext[1] + ")|(?<=" + keywordtext[1] +")|(?=" + keywordtext[2] + ")|(?<=" + keywordtext[2] +")|(?=" + keywordtext[3] + ")|(?<=" + keywordtext[3] +")"
                    elif len(keywordtext) == 5:                   
                        keywordregex = r"(?=" + keywordtext[0] + ")|(?<=" + keywordtext[0] +")|(?=" + keywordtext[1] + ")|(?<=" + keywordtext[1] +")|(?=" + keywordtext[2] + ")|(?<=" + keywordtext[2] +")|(?=" + keywordtext[3] + ")|(?<=" + keywordtext[3] +")|(?=" + keywordtext[4] + ")|(?<=" + keywordtext[4] +")"
                    splitkt = re.split(keywordregex, splitbt[idx])                       
                else:
                    # when no keywords, return regular line
                    splitkt = splitbt[idx]
                # find length of resulting total line  
                splitktnoempty = [x for x in splitkt if x != '']
                if idx == 0:
                    changeart = True
                    artkeywordtext = []
                    for w in splitktnoempty:
                        if w.upper() not in (v.upper() for v in keywordslist) and w.upper() not in (d.upper() for d in abilitieslist) and ',' not in w and 'OVERSHOOT' not in w.upper() and 'ARMORED' not in w.upper(): 
                            changeart = False
                    if changeart == True:   
                        for y in keywordtext:
                            if y.upper() in (v.upper() for v in keywordslist) or 'OVERSHOOT' in y.upper() or 'ARMORED' in y.upper():  
                                artkeywordtext.append(y)
                    artkeywordtemp = artkeywordtext 
                kline = ""
                keywordamount = 0
                shamount = 0
                shlength = 0
                for z in splitkt:
                    kline = kline + z
                    if z.upper() in (v.upper() for v in keywordslist):
                        keywordamount += 1
                    z2 = z.lower()
                    # calculates adjusted line length when converting Strength, Health etc to icon
                    if 'strength' in z2 or 'health' in z2 or 'brain' in z2 or 'sun' in z2:
                        shnumber2 = re.split('\s',z)
                        wsh2, hsh2 = myFontsh.getsize(shnumber2[0], stroke_width=1)
                        wsh4, hsh4 = myFont3.getsize(z)
                        shlength = shlength + wsh4 - wsh2 - 21
                linelength3 = myFont3.getlength(kline) + (45*keywordamount) - shlength
                line1length = myFont3.getlength(kline) 
                # when following a bolded line, add padding
                if idx == followbold:   
                    isbold = boldlength/1.82
                # adds each part of the line back together
                for y in splitkt:
                    y = y.lower()
                    if 'armored' in y:
                        linelength3 += 45
                    if 'overshoot' in y:
                        linelength3 += 45
                for i, z in enumerate(splitkt):
                    # draw keyword as bold if in keyword list
                    z = z.lower()
                    # converts armored 1 to armored for example, to check keywords list for value with the number
                    if 'strength' in z:
                        z = 'strength'
                    if 'health' in z:
                        z = 'health'
                    if 'brain' in z:
                        z = 'brain'
                    if 'sun' in z:
                        z = 'sun'
                    if 'armored' in z:
                        z = 'armored'
                    if 'overshoot' in z:
                        z = 'overshoot'
                    # draw keyword
                    if z.upper() in (v.upper() for v in keywordslist):
                        # makes the cards text
                        draw_underline_text(dct["selecteddctvalue"], (((w3 - W3)/2 + (line1length/2) - (linelength3/2)) + 809-istransparent + previouswordlength + isbold + 45, 575 + (linespacingtextbox*(outputline-2))), splitkt[i], myFont3, fill=(58,213,244))
                        #dct["selecteddctvalue"].text((((w3 - W3)/2 + (line1length/2) - (linelength3/2)) + 808-istransparent + previouswordlength + isbold + 45, 575 + (linespacingtextbox*(outputline-2))), splitkt[i], font = myFont3, align="center", fill=(58,213,244))     
                        # pastes the keyword image     
                        keywordwordlength = myFont3.getlength(z)
                        floattointkeywordx  = int(((w3 - W3)/2 + (line1length/2) - (linelength3/2)) + 809-istransparent + previouswordlength + isbold)
                        floattointkeywordy = int( 575 + (linespacingtextbox*(outputline-2)) + 5)
                        keywordart = Image.open(fr'./Platforms/Icons/{z}.png').resize((42,42)).convert("RGBA")
                        image.paste(keywordart, (floattointkeywordx, floattointkeywordy), mask=keywordart)
                        previouswordlength = previouswordlength + myFont3.getlength(splitkt[i]) + 45
                    # draw ability
                    elif z.upper() in (v.upper() for v in abilitieslist):
                        draw_underline_text(dct["selecteddctvalue"], (((w3 - W3)/2 + (line1length/2) - (linelength3/2)) + 809-istransparent + previouswordlength + isbold, 575 + (linespacingtextbox*(outputline-2))), splitkt[i], myFont3, fill=(58,213,244))
                        previouswordlength = previouswordlength + myFont3.getlength(splitkt[i])
                    # draw strength or health icon
                    elif z.upper() in (v.upper() for v in shlist):
                        shnumber = re.split('\s',splitkt[i])
                        floattointshx  = int(((w3 - W3)/2 + (line1length/2) - (linelength3/2)) + 812-istransparent + previouswordlength + isbold)
                        floattointshy = int( 575 + (linespacingtextbox*(outputline-2)) + 5)
                        #sets default color of white
                        shiconcolor = (255,255,255)
                        shstroke = 1
                        if z == 'health':
                            shart = Image.open(fr'./Platforms/Icons/Heart.png').resize((42,42)).convert("RGBA")
                        if z == 'strength':
                            shart = Image.open(fr'./Platforms/Icons/Strength.png').resize((42,42)).convert("RGBA")
                        if z == 'brain':
                            shart = Image.open(fr'./Platforms/Icons/UI_brain.png').resize((42,42)).convert("RGBA")
                            shiconcolor = (0,0,0) # changes brain text color to black
                            shstroke = 0
                        if z == 'sun':
                            shart = Image.open(fr'./Platforms/Icons/icon_sun.png').resize((42,42)).convert("RGBA")
                            shiconcolor = (0,0,0) # changes sun text color to black
                            shstroke = 0
                        image.paste(shart, (floattointshx, floattointshy), mask=shart)
                        wsh, hsh = myFontsh.getsize(shnumber[0], stroke_width=1)
                        dct["selecteddctvalue"].text((((w3 - W3)/2 + (line1length/2) - (linelength3/2)) + 812-istransparent + previouswordlength + isbold - wsh/2 + 21, 575 + (linespacingtextbox*(outputline-2)) + 24 - hsh/2), shnumber[0], font = myFontsh, fill=(shiconcolor), align="center", stroke_width=shstroke, stroke_fill=(0,0,0)) 
                        previouswordlength = previouswordlength + 45
                    # otherwise draw as normal
                    else:
                        dct["selecteddctvalue"].text((((w3 - W3)/2 + (line1length/2) - (linelength3/2)) + 809-istransparent + previouswordlength + isbold, 575 + (linespacingtextbox*(outputline-2))), splitkt[i], font = myFont3, align="center") 
                        previouswordlength = previouswordlength + myFont3.getlength(splitkt[i])
                          
        # sets health and strength to transparent if not a minion

        hkeywordart = 'Heart'
        skeywordart = 'Strength'
        artkeyword = [x.lower() for x in artkeywordtemp]
        # converts and armored 1 to armored for to get the right image
        for i, x in enumerate(artkeyword):
            if 'armored' in x:
                artkeyword[i] = 'armored'
            if 'overshoot' in x:
                artkeyword[i] = 'overshoot'
        htempkeyword = []
        stempkeyword = []
        # if theres a keyword value, update the appropiate image
        if len(artkeyword) > 0:
            for i in artkeyword:
                if i == 'freeze':
                    break
                elif i == 'armored' or i == 'untrickable':
                    htempkeyword.append(i)
                else:
                    stempkeyword.append(i)
            if len(htempkeyword) > 1:
                hkeywordart = 'multi'
            elif len(htempkeyword) == 1:
                hkeywordart = htempkeyword[0]
            if len(stempkeyword) > 1:
                skeywordart = 'multi'
            elif len(stempkeyword) == 1:
                skeywordart = stempkeyword[0]
        
        # pastes health and strength art, changing art depending on keyword
        healthart = Image.open(fr'./Platforms/Icons/{hkeywordart}.png').convert("RGBA")  
        strengthart = Image.open(fr'./Platforms/Icons/{skeywordart}.png').convert("RGBA")
        if values['-TCOMBO-'] in typesc:
            strengthart.putalpha(0)  
            healthart.putalpha(0)
        # resizes strength to 10% larger
        ssizetemp = strengthart.size
        ssizenew = int(ssizetemp[0]*1.1), int(ssizetemp[1]*1.1)
        strengthartresize = strengthart.resize(ssizenew)
        image.paste(healthart, (1002-istransparent - (int(healthart.size[0]/2)), 379 - (int(healthart.size[1]/2))), mask=healthart)
        image.paste(strengthartresize, (911-istransparent - (int(strengthartresize.size[0]/2)), 379 - (int(strengthartresize.size[1]/2))), mask=strengthartresize)
        
        #health
        W11, H11 = (30, 30)
        d11 = ImageDraw.Draw(image)
        myFont11 = ImageFont.truetype("Cafeteria-Bold.otf", 80)
        w11, h11 = myFont11.getsize(chealth, stroke_width=3)
        d10.text(( ((W11-w11)/2)+992-istransparent,((H11-h11)/2)+359), chealth, font=myFont11, fill=(255,255,255), stroke_width=3, stroke_fill=(0,0,0))

        #strength
        W12, H12 = (30, 30)
        d12 = ImageDraw.Draw(image)
        myFont12 = ImageFont.truetype("Cafeteria-Bold.otf", 80)
        w12, h12 = myFont12.getsize(cstrength, stroke_width=3)
        d12.text(( ((W12-w12)/2)+898-istransparent,((H12-h12)/2)+ 359), cstrength, font=myFont12, fill=(255,255,255), stroke_width=3, stroke_fill=(0,0,0))
            
        # draws the flavour text
        flavourtext = values['-FLAVOURTEXT-']
        d5 = ImageDraw.Draw(image)
        myFont4 = ImageFont.truetype("Cafeteria-Bold.otf", 45)
        w4, h4 = (300,300)
        _, _, W4, H4 = d5.textbbox((0, 0), flavourtext, font=myFont4)
        d5.text((((w4 - W4)/2) + 811-istransparent,((h4 - H4)/2) + 903), flavourtext, font = myFont4, align="center", fill=(255,255,255), stroke_width=2, stroke_fill=(0,0,0))
    
        #generates and saves the images
        imagetemp = image.copy()
        imagetemp.thumbnail((733,400))
        bio = io.BytesIO()
        imagetemp.save(bio, format="PNG")
        window["myimg"].update(data=bio.getvalue())

    # saves the image
    if event == "Save" or event == "Quick Save" or event == "Save":  
        # sets filename to the cards name
        if window['-FILENAME-'].get() == '' or window['-FILENAME-'].get() == previouscardname:
            filetempname = window['-NINPUT-'].get()
            window["-FILENAME-"].update(value=filetempname)
            previouscardname = window['-NINPUT-'].get()
            
        cardfilename = window['-FILENAME-'].get()
        cardfilepath = window['-SAVEIMAGE-'].get()
        finalpath = os.path.join(cardfilepath, cardfilename)
        if values['-RESIZEIMAGE-'] != '100':
            resizer = int(values['-RESIZEIMAGE-'])/100
            resizew, resizeh = image.size
            resizew = int(resizew*resizer)
            resizeh = int(resizeh*resizer)
            imageresize = image.resize((resizew,resizeh))
        else:
            imageresize = image
        try:  
            imageresize.save(finalpath + '.png', 'PNG')
        except:
            sg.popup('        Create an image first!        \x00')
        
        
# closes the window
window.close()
