import numpy as np
import cv2
import random
import time

class gameOfLife:

    def __init__(self, width, height, percent, color_life=[255,255,255], color_death=[0,0,0]):
        #Setting the size of the playing field
        self.old_state = np.zeros(( height, width), dtype=bool)
        self.new_state = np.zeros((height, width), dtype=bool)
        self.width = width
        self.height = height
        self.percent = 0.5
        self.color_life = color_life
        self.color_death = color_death
        #catch percent if it is a float or integer value!!
        if percent > 1:
            self.percent = percent/100
        else:
            self.percent = percent

        #set random alive using percentage
        amount = (self.width)*(self.height)
        amount = int(amount*self.percent)
        for i in range(amount):
            row = random.randint(0, height-1)
            col = random.randint(0, width-1)
            self.old_state[row][col]= True


    def alive_neighbours(self, i, j):
        an = 0 #number of alive neighbours
        for k in [i-1, i, i+1]:
            for l in [j-1, j, j+1]:
                if ( k == i and l == j):
                    continue # We do not want to incorporate our own state
                if(k!=self.height and l !=self.width):
                    an+=int(self.old_state[k][l])
                #check if elements are not out of bound!! else loop back around -> grid becomes a "toroidal array"
                elif(k==self.height and l !=self.width):
                    an+=int(self.old_state[0][l])
                elif(k!=self.height and l ==self.width):
                    an+=int(self.old_state[k][0])
                else:
                    an+=int(self.old_state[0][0])
        return an

    def rules_of_life(self):
        for i in range(self.old_state.shape[0]):
            for j in range(self.old_state.shape[1]):
                neighbours = self.alive_neighbours(i,j)
                if(self.old_state[i,j]==True):
                    if(neighbours < 2 or neighbours > 3):
                        self.new_state[i][j] = False
                else:
                    if(neighbours==3):
                        self.new_state[i][j] = True

        self.old_state = self.new_state.copy()

    def change_to_image(self):
        img = self.old_state.astype(np.uint8)  # convert to an unsigned byte
        # img *= 255
        #set life and death color:
        img1 = img.copy()
        img2 = img.copy()
        img3 = img.copy()
        img1[img1==1] = self.color_life[0] 
        img1[img1==0] = self.color_death[0] 
        img2[img2==1] = self.color_life[1] 
        img2[img2==0] = self.color_death[1] 
        img3[img3==1] = self.color_life[2] 
        img3[img3==0] = self.color_death[2] 
        #going from 1 channel to 3 channels with color:
        image = np.array((img1,img2,img3)).T
        return image


def play(game):
    result = cv2.VideoWriter('GameOfLife.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, (640,480))
    while True:
        game.rules_of_life()
        image = game.change_to_image()
        image = cv2.resize(image,(640,480), interpolation=cv2.INTER_AREA)
        result.write(image)
        cv2.imshow("Game of Life", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            result.release()
            break
            



if __name__ == "__main__":
    #color in BGR mode 
    width=200
    height=200
    start_percent = 0.3
    color_life =[255,255,255]
    color_death =[100,0,0]
    game = gameOfLife(width,height,start_percent, color_life, color_death)
    play(game)