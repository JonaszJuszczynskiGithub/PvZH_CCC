# PvZHCCC.py

# PvZH_CCC Version 1.0.1

# to do list:
# web application port
# toggle option of adding flavour text, changes card height
# Change rarity text color
# add credit/ creator name
# icons ( i.e abilites like deadly armored etc) to text and health/strength
# bold and underlined words to card text ( hard )
# double class cards
# superpowers
# heros with 4 superpowers
# more backgrounds + custom backgrounds
# resize final image
# bug when image not transparent, prevent crashes
# updates screen + docs + quick start guide + contact
# save custom card as template
# make custom sets, store all cards as one and navigate through them

# imports
import io
import os
import string
import textwrap
import PySimpleGUI as sg
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
sg.set_options(font=("Cafeteria-Bold", 20))
sg.theme('DarkGray9')

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("PNG (*.png)", "*.png"),
              ("All files (*.*)", "*.*")]

# window layout

# column 1 layout

types = ['Zombie', 'Zombie Trick', 'Zombie Environment', 'Plant', 'Plant Trick', 'Plant Environment']
typesc = ['Zombie Trick', 'Zombie Environment', 'Plant Trick', 'Plant Environment']
typesd = ['Zombie', 'Zombie Trick', 'Zombie Environment']
rarity = ['Legendary', 'Super-Rare','Rare', 'Uncommon', 'Common', 'Event']
zclasses = ['Beastly', 'Brainy', 'Crazy', 'Hearty', 'Sneaky']
pclasses = ['Guardian', 'Kabloom', 'Mega-Grow', 'Smarty', 'Solar']
classes = ['Beastly', 'Brainy', 'Crazy', 'Hearty', 'Sneaky', 'Guardian', 'Kabloom', 'Mega-Grow', 'Smarty', 'Solar']

z = [sg.Text('Strength', expand_x=False), sg.Input(size=(3, 10), expand_x=False, k='-STINPUT-'), sg.Text('Health', expand_x=False), sg.Input(size=(3, 10), expand_x=False, k='-HEINPUT-')],[sg.Text('1', visible=False)]

# form layout
inputs = [     
            [sg.Text('Name'), sg.Input(size=(12, 10), k='-NINPUT-'), sg.Text('Cost'), sg.Input(size=(3, 10), k='-COINPUT-')], 
            [sg.Column(z, key='-c-')],
            [sg.Text('Card Type'), sg.Combo(types, size=(20, 10), expand_x=True, enable_events=True,  readonly=True, k='-TCOMBO-')],
            [sg.Text('Class'), sg.Combo(classes, size=(10, 10), expand_x=True, enable_events=True,  readonly=True,  k='-CCOMBO-')],
            [sg.Text('Tribes'), sg.Input(size=(10, 10), expand_x=True, k='-TRINPUT-')],
            [sg.Push(), sg.Text('Card Text'), sg.Push()],
            [sg.Multiline(size=(10, 10), expand_x=True, enable_events=True, k='-CARDTEXT-')],
            [sg.Text('Rarity'), sg.Combo(rarity, size=(10, 10), expand_x=True, enable_events=True, readonly=True, key='-RCOMBO-')],
            [sg.Text('Set'), sg.Input('Premium', size=(10, 10), expand_x=True, k='-SETINPUT-')],
            [sg.Push(), sg.Text('Flavour Text'), sg.Push()],
            [sg.Multiline(size=(10, 3), expand_x=True, k='-FLAVOURTEXT-')], 
         ]

# image generator layout
card = [    
            # card image
            [sg.Push(), sg.Text('Image'), sg.Push()],
            [sg.Image( key="myimg", expand_x=True, expand_y=True)],
            # options for card art 
            [sg.Push(), sg.Text('Card Art'), sg.Push()],
            [sg.Input(size=(25, 1), enable_events=True, key="-FILE-", expand_x=True),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Generate Card")],
            [sg.Text('Adjust Card Art Position', expand_x=True),
            sg.Button('Reset Position'),
            sg.Text('x'), sg.Input(size=(5,1), default_text='0', enable_events=True, key='-CARDXPOSITION-'),
            sg.Text('y'), sg.Input(size=(5,1), default_text='0', enable_events=True, key='-CARDYPOSITION-')],
            [sg.Text('Adjust Card Art Size', expand_x=True),
            sg.Button('Reset Size'),
            sg.Text('width'), sg.Input(size=(5,1), default_text='300', enable_events=True, key='-CARDWIDTH-'),
            sg.Text('height'), sg.Input(size=(5,1), default_text='350', enable_events=True, key='-CARDHEIGHT-')],
            [sg.Text('Change Background'), sg.Combo(['PvZ Heroes Website', 'PvZ Heroes Lawn', 'Transparent'], default_value='PvZ Heroes Website', expand_x=True, enable_events=True,  readonly=True, key='-BACKGROUNDSELECT-')],
            # options to save the image
            [sg.Push(),sg.Text('Save Image'), sg.Push()],
            [sg.Input(size=(25, 1), enable_events=True, key="-SAVEIMAGE-", expand_x=True),
            sg.FolderBrowse(),
            sg.Input(size=(25, 1), enable_events=True, key="-FILENAME-", expand_x=True),
            sg.Button("Save")],
       ]

# complete layout
layout = [
            [sg.vtop(   
            [
                sg.Frame('Card Creator', inputs),
                sg.Column(card),
            ])]
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

# events
while True:
    event, values = window.read()
    #print('event:', event)
    #print('values:', values)
    if event == sg.WIN_CLOSED:
        break

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
        print(sclass)
    
    if event == "-RCOMBO-":    
        vrarity = values['-RCOMBO-']
        vrarity = vrarity.lower()
        print(vrarity)

    # resets position of art
    if event == "Reset Position":
        window['-CARDXPOSITION-'].update(0)
        window['-CARDYPOSITION-'].update(0)

    # resets size of art
    if event == "Reset Size":
        window['-CARDWIDTH-'].update(300)
        window['-CARDHEIGHT-'].update(350)

    # starts generating the custom image
    if event == "Generate Card":
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
            if values['-BACKGROUNDSELECT-'] == 'PvZ Heroes Website':
                image = Image.open("./Platforms/Icons/PvZ_Heroes_website_background.jpg").convert("RGBA").resize((1920,1160))
            elif values['-BACKGROUNDSELECT-'] == 'PvZ Heroes Lawn':
                image = Image.open("./Platforms/Icons/PvZLawn.jpg").resize((1920,1160)).convert("RGBA")
            elif values['-BACKGROUNDSELECT-'] == 'Transparent':
                image = Image.open("./Platforms/Icons/transparent.png").convert("RGBA").resize((990,1060))
            else:
                image = Image.open("./Platforms/Icons/PvZ_Heroes_website_background.jpg").convert("RGBA")

            platform = Image.open(os.path.join(fr'./Platforms/{typepvz}/{sclass}.png')).resize((824,629)).convert("RGBA")
            platformart = Image.open(fr'./Platforms/{typepvz}/{sclass}2.png').resize((350,350)).convert("RGBA")
            iconart = Image.open(fr'./Platforms/Icons/PvZH_{sclass}_Icon.png').resize((120,120)).convert("RGBA")
            rarityart = Image.open(fr'./Platforms/Icons/{vrarity}.png').resize((853,300)).convert("RGBA")
            # checks whether to use brains or sun
            if ctype == 'Zombie' or ctype == 'Zombie Trick' or ctype == 'Zombie Environment':
                costart = Image.open(fr'./Platforms/Icons/UI_brain.png').resize((125,125)).convert("RGBA")
            else:
                costart = Image.open(fr'./Platforms/Icons/icon_sun.png').resize((130,130)).convert("RGBA")

            # sets health and strength to transparent if not a minion
            if values['-TCOMBO-'] in typesc:
                strengthart = Image.open(fr'./Platforms/Icons/Strength.png').resize((110,110)).convert("RGBA")
                healthart = Image.open(fr'./Platforms/Icons/Heart.png').resize((100,100)).convert("RGBA")
                strengthart.putalpha(0)  
                healthart.putalpha(0)  
            else:
                strengthart = Image.open(fr'./Platforms/Icons/Strength.png').resize((110,110)).convert("RGBA")
                healthart = Image.open(fr'./Platforms/Icons/Heart.png').resize((100,100)).convert("RGBA")        
 
            # Gets art from user, otherwise sets missing default image
            artw = int(values['-CARDWIDTH-'])
            arth = int(values['-CARDHEIGHT-'])        
            if os.path.exists(values['-FILE-']):
                cardart = Image.open(values['-FILE-']).resize((artw,arth)).convert("RGBA")
            else:
                cardart = Image.open(fr'./Platforms/Icons/MISSING_ASSET.png').resize((300,450)).convert("RGBA")

            if values['-BACKGROUNDSELECT-'] == 'Transparent':
                istransparent = 470
            else:
                istransparent = 0

            # pastes the images
            image.paste(platform, (548-istransparent,318), mask=platform)
            image.paste(platformart, (785-istransparent,88), mask=platformart)
            image.paste(iconart, (1177-istransparent, 293), mask=iconart)
            image.paste(rarityart, (535-istransparent, 823), mask=rarityart)

            # changes arts position
            artx = int(values['-CARDXPOSITION-'])
            arty = int(values['-CARDYPOSITION-'])         
            image.paste(cardart, (810-istransparent + artx, 7 + arty), mask=cardart)

            image.paste(costart, (1055-istransparent, 93), mask=costart)          
            image.paste(healthart, (955-istransparent, 326), mask=healthart)
            image.paste(strengthart, (862-istransparent, 323), mask=strengthart)
            
            # draws the name
            cname = values['-NINPUT-']
            W, H = (300, 300)
            d1 = ImageDraw.Draw(image)       
            myFont = ImageFont.truetype("Cafeteria-Bold.otf", 80)
            w, h = myFont.getsize(cname)
            d1.text(( ((W-w)/2)+815-istransparent,((H-h)/2)+328), cname, font=myFont, fill=(255,255,255))

            # draws the cost health and strength
            ccost = values['-COINPUT-']
            chealth = values['-HEINPUT-']
            cstrength = values['-STINPUT-']

            #cost
            W10, H10 = (30, 30)
            d10 = ImageDraw.Draw(image)
            myFont10 = ImageFont.truetype("Cafeteria-Bold.otf", 80)
            w10, h10 = myFont10.getsize(ccost)
            d10.text(( ((W10-w10)/2)+1105-istransparent,((H10-h10)/2)+133), ccost, font=myFont10, fill=(0,0,0))
            
            #health
            W11, H11 = (30, 30)
            d11 = ImageDraw.Draw(image)
            myFont11 = ImageFont.truetype("Cafeteria-Bold.otf", 82)
            w11, h11 = myFont11.getsize(chealth, stroke_width=3)
            d10.text(( ((W11-w11)/2)+992-istransparent,((H11-h11)/2)+357), chealth, font=myFont11, fill=(255,255,255), stroke_width=3, stroke_fill=(0,0,0))

            #strength
            W12, H12 = (30, 30)
            d12 = ImageDraw.Draw(image)
            myFont12 = ImageFont.truetype("Cafeteria-Bold.otf", 82)
            w12, h12 = myFont12.getsize(cstrength, stroke_width=3)
            d12.text(( ((W12-w12)/2)+903-istransparent,((H12-h12)/2)+356), cstrength, font=myFont12, fill=(255,255,255), stroke_width=3, stroke_fill=(0,0,0))
            

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
            myFont1 = ImageFont.truetype("Cafeteria-Bold.otf", 42)
            w1, h1 = myFont1.getsize(ctypet)
            d2.text(( ((W1-w1)/2)+814-istransparent,((H1-h1)/2)+393), ctypet, font=myFont1, fill=(205,205,205))

            vrarity 
            cset = values['-SETINPUT-']
            settext = cset + " - " + vrarity

            # draws the set and rarity
            W2, H2 = (300,300)
            d3 = ImageDraw.Draw(image)
            myFont2 = ImageFont.truetype("Cafeteria-Bold.otf", 70)
            w2, h2 = myFont2.getsize(settext, stroke_width=1)
            d3.text(( ((W2-w2)/2)+785-istransparent,((H2-h2)/2)+772), settext.upper(), font=myFont2, fill=(255,255,255), stroke_width=1, stroke_fill=(0,0,0))

            # draws the text box
            cardtext = values['-CARDTEXT-']
            d4 = ImageDraw.Draw(image)
            myFont3 = ImageFont.truetype("Cafeteria-Bold.otf", 42)
            w3, h3 = (300,300)
            _, _, W3, H3 = d4.textbbox((0, 0), cardtext, font=myFont3)
            d4.text((((w3 - W3)/2) + 811-istransparent, 573), cardtext, font = myFont3, align="center")

            # draws the flavour text
            flavourtext = values['-FLAVOURTEXT-']
            d5 = ImageDraw.Draw(image)
            myFont4 = ImageFont.truetype("Cafeteria-Bold.otf", 45)
            w4, h4 = (300,300)
            _, _, W4, H4 = d5.textbbox((0, 0), flavourtext, font=myFont4)
            d5.text((((w4 - W4)/2) + 811-istransparent, 985), flavourtext, font = myFont4, align="center", fill=(255,255,255), stroke_width=2, stroke_fill=(0,0,0))
       
            #generates and saves the images
            imagetemp = image.copy()
            imagetemp.thumbnail((733,400))
            bio = io.BytesIO()
            imagetemp.save(bio, format="PNG")
            window["myimg"].update(data=bio.getvalue())

    # saves the image
    if event == "Save":    
        cardfilename = values['-FILENAME-']
        cardfilepath = values['-SAVEIMAGE-']
        finalpath = os.path.join(cardfilepath, cardfilename)
        image.save(finalpath + '.png', 'PNG')
        sg.popup('Card Saved!')
        
# closes the window
window.close()
