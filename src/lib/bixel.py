# bixel.py
# (c) Ralf Huwald

from epaper_37 import EPD_3in7
import random


class Bixel:
    
    def __init__(self, X_Size = 4, Y_Size = 4, X_Spacing = 1, Y_Spacing = 1, X_Offset = 3, Y_Offset = 0):
        self.ePaper = EPD_3in7()
        
        self.X_Size    = X_Size
        self.Y_Size    = Y_Size
        self.X_Spacing = X_Spacing
        self.Y_Spacing = Y_Spacing
        self.X_Width   = self.X_Size + self.X_Spacing
        self.Y_Width   = self.Y_Size + self.Y_Spacing
        self.X_Max     = int(self.ePaper.width / self.X_Width)
        self.Y_Max     = int(self.ePaper.height / self.Y_Width) - 1
        self.X_Offset  = X_Offset
        self.Y_Offset  = Y_Offset
        
        self.letters      = {}
        self.letters['A'] = [[1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1]]
        self.letters['B'] = [[1,1,1,1],   [1,0,0,0,1], [1,1,1,1],   [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1]]
        self.letters['C'] = [[1,1,1,1,1], [1],         [1],         [1],         [1],         [1,1,1,1,1]]
        self.letters['D'] = [[1,1,1,1],   [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1]]
        self.letters['E'] = [[1,1,1,1,1], [1],         [1,1,1,1],   [1],         [1],         [1,1,1,1,1]]
        self.letters['F'] = [[1,1,1,1,1], [1],         [1,1,1,1],   [1],         [1],         [1]]
        self.letters['G'] = [[1,1,1,1,1], [1],         [1,0,0,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1]]
        self.letters['H'] = [[1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1]]
        self.letters['I'] = [[1,1,1,1,1], [0,0,1],     [0,0,1],     [0,0,1],     [0,0,1],     [1,1,1,1,1]]
        self.letters['J'] = [[0,0,0,0,1], [0,0,0,0,1], [0,0,0,0,1], [0,0,0,0,1], [0,1,0,0,1], [0,0,1,1,1]]
        self.letters['K'] = [[1,0,0,0,1], [1,0,0,1],   [1,1,1],     [1,0,0,1],   [1,0,0,0,1], [1,0,0,0,1]]
        self.letters['L'] = [[1],         [1],         [1],         [1],         [1],         [1,1,1,1,1]]
        self.letters['M'] = [[1,0,0,0,1], [1,1,0,1,1], [1,0,1,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1]]
        self.letters['N'] = [[1,0,0,0,1], [1,1,0,0,1], [1,0,1,0,1], [1,0,0,1,1], [1,0,0,0,1], [1,0,0,0,1]]
        self.letters['O'] = [[1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1]]
        self.letters['P'] = [[1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1], [1],         [1],         [1]]
        self.letters['Q'] = [[1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,1,0,1], [1,0,0,1,1], [1,1,1,1,1]]
        self.letters['R'] = [[1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,1],     [1,0,0,1],   [1,0,0,0,1]]
        self.letters['S'] = [[1,1,1,1,1], [1],         [1,1,1,1,1], [0,0,0,0,1], [0,0,0,0,1], [1,1,1,1,1]]
        self.letters['T'] = [[1,1,1,1,1], [0,0,1],     [0,0,1],     [0,0,1],     [0,0,1],     [0,0,1]]
        self.letters['U'] = [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1]]
        self.letters['V'] = [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,0,1],   [0,0,1]]
        self.letters['W'] = [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,1,0,1], [1,1,0,1,1], [1,0,0,0,1]]
        self.letters['X'] = [[1,0,0,0,1], [0,1,0,1],   [0,0,1],     [0,1,0,1],   [1,0,0,0,1], [1,0,0,0,1]]
        self.letters['Y'] = [[1,0,0,0,1], [0,1,0,1],   [0,0,1],     [0,0,1],     [0,0,1],     [0,0,1]]
        self.letters['Z'] = [[1,1,1,1,1], [0,0,0,1],   [0,0,1],     [0,1],       [1],         [1,1,1,1,1]]
        self.letters['Ä'] = [[1,0,0,0,1], [0],         [1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1]]
        self.letters['Ö'] = [[1,0,0,0,1], [0],         [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1]]
        self.letters['Ü'] = [[1,0,0,0,1], [0],         [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1]]
        
        self.letters[' '] = [[0],         [0],         [0],         [0],         [0],         [0]]
        self.letters[':'] = [[0],         [0],         [0,0,1],     [0],         [0],         [0,0,1]]
        self.letters['.'] = [[0],         [0],         [0],         [0],         [0],         [0,0,1]]
        self.letters[','] = [[0],         [0],         [0],         [0],         [0,0,0,1],   [0,0,1]]
        self.letters['!'] = [[0,0,1],     [0,0,1],     [0,0,1],     [0],         [0],         [0,0,1]]
        self.letters['?'] = [[1,1,1,1,1], [0,0,0,0,1], [0,0,1,1,1], [0,0,1],     [0],         [0,0,1]]
        self.letters['_'] = [[0],         [0],         [0],         [0],         [0],         [1,1,1,1,1]]
        self.letters['+'] = [[0,0,1],     [0,0,1],     [1,1,1,1,1], [0,0,1],     [0,0,1],     [0]]
        self.letters['-'] = [[0],         [0],         [1,1,1,1,1], [0],         [0],         [0]]
        self.letters['*'] = [[0],         [0],         [0,0,1],     [0],         [0],         [0]]
        self.letters['/'] = [[0,0,0,0,1], [0,0,0,1],   [0,0,1],     [0,1],       [1],         [1]]
        self.letters['='] = [[0],         [1,1,1,1,1], [0],         [1,1,1,1,1], [0],         [0]]
        
        self.letters['0'] = [[1,1,1,1,1], [1,0,0,0,1], [1,0,1,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1]]
        self.letters['1'] = [[0,0,1],     [0,0,1],     [0,0,1],     [0,0,1],     [0,0,1],     [0,0,1]]
        self.letters['2'] = [[1,1,1,1,1], [0,0,0,0,1], [1,1,1,1,1], [1],         [1],         [1,1,1,1,1]]
        self.letters['3'] = [[1,1,1,1,1], [0,0,0,0,1], [0,1,1,1,1], [0,0,0,0,1], [0,0,0,0,1], [1,1,1,1,1]]
        self.letters['4'] = [[1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1], [0,0,0,0,1], [0,0,0,0,1], [0,0,0,0,1]]
        self.letters['5'] = [[1,1,1,1,1], [1],         [1,1,1,1,1], [0,0,0,0,1], [0,0,0,0,1], [1,1,1,1,1]]
        self.letters['6'] = [[1,1,1,1,1], [1],         [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1]]
        self.letters['7'] = [[1,1,1,1,1], [0,0,0,0,1], [0,0,0,0,1], [0,0,0,0,1], [0,0,0,0,1], [0,0,0,0,1]]
        self.letters['8'] = [[1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1]]
        self.letters['9'] = [[1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1], [0,0,0,0,1], [0,0,0,0,1], [1,1,1,1,1]]
    
    # Einen einzelnen Bixel zeichnen
    def Draw(self, x, y, color = None, filled = True):
        if (x >= 0) and (x <= self.X_Max):
            if (y >= 0) and (y <= self.Y_Max):
                self.ePaper.image4Gray.rect(x * self.X_Width + self.X_Offset, y * self.Y_Width + self.Y_Offset, self.X_Size, self.Y_Size, self.ePaper.black if color == None else color, filled)
    
    
    # Einen Buchstaben zeichnen (Unbekannte Buchstaben werden als "?" dargestellt)
    def Draw_Letter(self, x, y, letter, color = None, filled = True, rotation = 0):
        if rotation not in (0, 90, 180, 270):
            rotation = 0
        
        letter_ = self.letters[letter] if letter in self.letters else self.letters['?']
        
        x_current = x
        y_current = y
        
        for line_number in range(len(letter_)-1, -1, -1):
            line = letter_[line_number]
            if rotation == 0:
                x_current = x
            if rotation == 90:
                y_current = y
            if rotation == 180:
                x_current = x
            if rotation == 270:
                y_current = y
            for col_number in range(0, len(line)):
                if line[col_number] == 1: self.Draw(x_current, y_current, color, filled)
                if rotation == 0:   x_current += 1
                if rotation == 90:  y_current += 1
                if rotation == 180: x_current -= 1
                if rotation == 270: y_current -= 1
            if rotation == 0:   y_current -= 1
            if rotation == 90:  x_current += 1
            if rotation == 180: y_current += 1
            if rotation == 270: x_current -= 1
    
    
    # Ein Wort zeichnen
    def Draw_Word(self, x, y, word, color = None, filled = True, rotation = 0):
        if rotation not in (0, 90, 180, 270):
            rotation = 0
        
        x_current = x
        y_current = y
        
        for letter in word:
            self.Draw_Letter(x_current, y_current, letter, color, filled, rotation)
            if rotation == 0:   x_current += 6
            if rotation == 90:  y_current += 6
            if rotation == 180: x_current -= 6
            if rotation == 270: y_current -= 6
    
    def Draw_Mosaic(self, color = None, filled = None):
        self.ePaper.image1Gray.fill(self.ePaper.black)
        self.ePaper.image4Gray.fill(self.ePaper.black)
        
        for x in range(0, self.X_Max + 1):
            for y in range(0, self.Y_Max + 1):
                self.Draw(
                    x,
                    y,
                    random.choice([self.ePaper.white,self.ePaper.grayish,self.ePaper.darkgray,self.ePaper.black]) if color == None else color,
                    random.choice([True,False]) if filled == None else filled
                )
        
        self.ePaper.EPD_3IN7_4Gray_Display(self.ePaper.buffer_4Gray)
