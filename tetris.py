import machine
from machine import Pin, SoftI2C, PWM
import ssd1306
import time
import random
import _thread




i2c = SoftI2C(scl=Pin(26), sda=Pin(27))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
buzzer = PWM(Pin(13,Pin.OUT))
buttons = [Pin(25, Pin.IN, Pin.PULL_UP),Pin(33, Pin.IN, Pin.PULL_UP),Pin(32, Pin.IN, Pin.PULL_UP)] #left,right,rotate
buttons_zmacknuto = []
for o in range(len(buttons)):
    buttons_zmacknuto.append(False)
kostky = [[[0,1,1,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]],  [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],  [[0,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,0,0]],  [[0,0,1,0],[0,0,1,0],[0,1,1,0],[0,0,0,0]],   [[0,0,0,0],[1,1,0,0],[0,1,1,0],[0,0,0,0]],  [[0,0,0,0],[0,0,1,1],[0,1,1,0],[0,0,0,0]], [[0,0,0,0],[0,1,0,0],[1,1,1,0],[0,0,0,0]]]
buttons_to_make = []
score = 0

buzzer.duty_u16(10000)

tony = {
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
}

tetris_song ="E5 - B4 C5 D5 - C5 B4 A4 A4 C5 E5 - D5 C5 B4 - - C5 D5 - E5 - C5 - A4 A4 P P D5 - - F5 A5 - - G5 F5 E5 - C5 E5 - D5 - C5 - B4 B4 C5 D5 E5 C5 A4 A4 E5 B4 C5 D5 C5 B4 A4 A4 C5 E5 D5 C5 B4 C5 D5 E5 C5 A4 A4 D5 F5 A5 G5 F5 E5 C5 E5 D5 C5 B4 B4 C5 D5 E5 C5 A4 A4 E5 C5 D5 B4 C5 A4 AS4 B4 E5 C5 D5 B4 C5 E5 A5 AS5 E5 B4 C5 D5 C5 B4 A4 A4 C5 E5 D5 C5 B4 C5 D5 E5 C5 A4 A4 D5 F5 A5 G5 F5 E5 C5 E5 D5 C5 B5 B5 C5 D5 E5 C5 A4 A4 E5 B4 C5 D5 C5 B4 A4 A4 C5 E5 D5 C5 B4 C5 D5 E5 C5 A4 A4 D5 F5 A5 G5 F5 E5 C5 E5 D5 C5 B4 B4 C5 D5 E5 C5 A4 A4 E5 C5 D5 B4 C5 A4 AS4 B4 E5 C5 D5 B4 C5 E5 A5 AS5 E5 B4 C5 D5 C5 B4 A4 A4 C5 E5 D5 C5 B4 C5 D5 E5 C5 A4 A4 D5 F5 A5 G5 F5 E5 C5 E5 D5 C5 B4 B4 C5 D5 E5 C5 A4 A4"

tetris_theme = tetris_song.split(" ")

def play_music():
    while True:
        for tutu in range(len(tetris_theme)):
            buzzer.duty_u16(10000)
            if tetris_theme[tutu] == "-":
                time.sleep(0.15)
            elif tetris_theme[tutu] == "P":
                buzzer.duty_u16(0)
                time.sleep(0.15)
            else:
                try:
                    if tony[(tetris_theme[tutu])] == tony[(tetris_theme[tutu-1])]:
                        buzzer.freq(tony[(tetris_theme[tutu])])
                        time.sleep(0.13)
                        buzzer.duty_u16(0)
                        time.sleep(0.02)
                    else:
                        buzzer.freq(tony[(tetris_theme[tutu])])
                        time.sleep(0.15)
                except:
                    print(":(")
                    

def sp_play_music():
    _thread.start_new_thread(play_music, ())

#sp_play_music()

pole = [] # pole[y][x]
for i in range(24):
    pole.append([])
    for g in range(12):
        pole[i].append(0)
                
padajici = []
prechodne_padajici = []
for i in range(4):
    padajici.append([])
    prechodne_padajici.append([])
    for g in range(4):
        padajici[i].append(0)
        prechodne_padajici[i].append(0)
spadne = False
souradky_splynuti = [0,0]

padajici = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]
souradky_splynuti = [0,2]

def detekce():
    global buttons, buttons_zmacknuto, buttons_to_make
    while True:
        for u in range(len(buttons)):
            if buttons[u].value() == 0 and not buttons_zmacknuto[u]:
                buttons_to_make.append(u)
                buttons_zmacknuto[u] = True
            if buttons[u].value() ==1:
                buttons_zmacknuto[u]= False
        time.sleep(0.01)
            

def vl_detekce():
    _thread.start_new_thread(detekce, ())
    
vl_detekce()
clock = 0
while True:
    oled.fill(0)
    for t in range(4):
        for p in range(4):
            if padajici[t][p] == 1:
                for q in range(5):
                    for w in range(5):
                        oled.pixel(6+((t+souradky_splynuti[0])*5)+q,63-(2+((p+souradky_splynuti[1])*5)+w),1)
    for r_l in range(2):
        for r_l_s in range(122):
            oled.pixel(6+r_l_s,63-r_l,1)
            oled.pixel(6+r_l_s,r_l,1)
        for r_l_d in range(63):
            oled.pixel((126+r_l),r_l_d,1)
    for i in range(24):
        for g in range(12):
            if pole[i][g] == 1:
                for q in range(5):
                    for w in range(5):
                        oled.pixel(6+(i*5)+q,63-(2+(g*5)+w),1)
    spadne = True
    for t in range(4):
        for p in range(4):
            if padajici[t][p] == 1:
                if t+souradky_splynuti[0]+1 > 23:
                    spadne = False
                elif pole[t+souradky_splynuti[0]+1][p + souradky_splynuti[1]] == 1:
                    spadne = False
    if clock % 2 == 0:
        if spadne:
            souradky_splynuti[0] += 1
        else:
            for t in range(4):
                for p in range(4): 
                    if padajici[t][p] == 1:
                        pole[t+souradky_splynuti[0]][p+souradky_splynuti[1]] = 1
            souradky_splynuti = [0,2]
            padajici = kostky[(random.randint(0,6))]
    for tl in range(len(buttons_to_make)):
        tla = buttons_to_make[0]
        del buttons_to_make[0]
        if tla == 0:
            mozne_posunuti = True
            for b in range(4):
                for v in range(4):
                    if padajici[v][b] == 1 and souradky_splynuti[1] +b <1:
                        mozne_posunuti = False
                    if padajici[b][v] == 1 and pole[b+souradky_splynuti[0]][v+souradky_splynuti[1]-1]:
                            mozne_posunuti = False
            if mozne_posunuti:
                souradky_splynuti[1] -= 1
        elif tla == 1:
            mozne_posunuti = True
            for b in range(4):
                for v in range(4):
                    if padajici[v][b] == 1 and souradky_splynuti[1] +b >10:
                        mozne_posunuti = False
                    try:
                        if padajici[b][v] == 1 and pole[b+souradky_splynuti[0]][v+souradky_splynuti[1]+1]:
                            mozne_posunuti = False
                    except:
                        mozne_posunuti = False
            if mozne_posunuti:
                souradky_splynuti[1] += 1
        elif tla == 2:
            otoci_se = True
            prechodne_padajici = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
            for b in range(4):
                for v in range(4):
                    prechodne_padajici[b][v] = padajici[3-v][b]
                    try:
                        if prechodne_padajici[b][v] == 1 and (pole[b+souradky_splynuti[0]][v+souradky_splynuti[1]] == 1 or souradky_splynuti[1]+v >11 or souradky_splynuti[1]+v<0):
                            otoci_se = False
                    except:
                        otoci_se = False
            if otoci_se:
                padajici = prechodne_padajici.copy()
    for u in range(24):
        if pole[u] == [1,1,1,1,1,1,1,1,1,1,1,1]:
            score += 1
            for j in range(u):
                k = u-j
                if k > 0:
                    pole[k] = pole[k-1].copy()
                else:
                    pole[k] = [0,0,0,0,0,0,0,0,0,0,0,0]

    oled.show()
    clock += 1 
    
    
    

