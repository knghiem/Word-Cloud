#Khanh Nghiem COM110
#Oct 23, 2016

from graphics import *
from random import *
from time import *
from math import *

#Graphical functions:
def drawButton(gwin, pt1, pt2, col, word):
    button1=Rectangle(pt1, pt2)
    button1.setFill(col)
    button1.draw(gwin)
    upperLeftX=pt1.getX()
    upperLeftY=pt1.getY()
    lowerRightX=pt2.getX()
    lowerRightY=pt2.getY()
    centerPoint=Point((upperLeftX+lowerRightX)/2,(upperLeftY+lowerRightY)/2)
    button1Label = Text(centerPoint,word)
    button1Label.setSize(11)
    button1Label.setFill("white")
    button1Label.draw(gwin)

def inputBox(gwin,height,word):
    prompt=Text(Point(155,height),word)
    prompt.setSize(10)
    prompt.draw(gwin)
    inputBox=Entry(Point(400,height),30)
    inputBox.setFill("white")
    inputBox.draw(gwin)
    return inputBox

def intro(gwin):
    #Making the welcoming screen
    welcome=Text(Point(300,300),"WELCOME!")
    size=16
    welcome.setSize(size)
    welcome.draw(gwin)
    for i in range(10):
        size=size+2
        welcome.setSize(size)
        r=randint(0,255)
        g=randint(0,255)
        b=randint(0,255)
        welcome.setTextColor(color_rgb(r,g,b))
        sleep(0.2)
    welcome.undraw()
    
    #Draw the program name
    progName=Text(Point(300,50),"WORD CLOUD GENERATOR")
    progName.setSize(16)
    progName.setTextColor("blue4")
    progName.draw(gwin)
    cloud=Image(Point(130,50), "cloud.png")
    cloud.draw(gwin)
    cloud2=Image(Point(470,50), "cloudcopy.png")
    cloud2.draw(gwin)

    #Draw the introduction
    introText="Word Cloud is a visualization that show frequencies of words\nby varying font size and font colors. The program excludeds English \"stop words\",\nwhich have little meanings, such as \"a\",\"an\",\"and\", and similar words.\n\nInstruction: Put in a .txt file name and the number of words to be included in the Word Cloud.\n\nNotice: The Word Cloud of a default text will be created if text file name is blank.\n\nDeveloper: Khanh Nghiem\n\nVersion: 1.0.0"
    intro=Text(Point(300,175),introText)
    intro.setSize(10)
    intro.draw(gwin)

#Generating Word Cloud Functions

def getInputs(inputBox1, inputBox2): #get file name and number of words
                #to be included in the word cloud from GUI input boxes
    fname=inputBox1.getText()
    n=int(inputBox2.getText())
    
    return fname,n #return file name, and number of words

def processTextInput(fname): #lowercase, get rid of special character
    inputFile=open(fname,'r')
    text=inputFile.read() 
    text=text.lower() 
    for ch in "0123456789!@#^&*()_-—<>[]{}+-=|\/~`$“”.,()%;:?…'''":
        text = text.replace(ch, " ")
    inputFile.close()
    return text

def wordList(text,n): 
    words=text.split()        
    counts={} #initiate a dict that holds words and corresponding freqs
    for w in words:
        counts[w]=counts.get(w,0)+1
    
    items=list(counts.items()) #a list of tuples,
                            #tuples hold words and corresponding freqs
    items.sort() #sort the 1st time by alphabet

    def byFreq(pair): 
        return pair[1]

    items.sort(key=byFreq,reverse=True) #sort the 2nd time by freq

    wordList=[] #initiate a list that holds words and corresponding freqs
            #these are words that will go to the word cloud

    #get a list of stop words here
    stopWords=open("stopwords.txt",'r').read()
    stopWords=stopWords.split("\n")

    while len(wordList)<n and not len(items)==0:
        #while we don't have enough n words in the word cloud list
        #n is the user input number of words that they want to
        #include in the cloud
        #and while we don't run out of words in the text
        
        word, count=items[0]

        #we check if the word is a stop word
        if word not in stopWords:
            x=items.pop(0)
            wordList.append(x)
            #if not, put it in the word cloud list
        else:
            items.remove(items[0])
            #if so, toss it in the memory heaven #byeFelicia
            
    return wordList #return the word cloud list

"""
This function basically convert point (fontSize) to pixels
This way, we can approximately how much space a word would take
We will caluculate the width and height of the words that are going to be drawn
We draw invisible rectangles surrouding the words, and we will make sure
that now rectangles overlap

I was crazy enough to type letters into Photoshop and literally count pixels,
and then put them into relationship with one another and pixels.
I also tried drawing rectangles to see if the approximation is accurate.
But it's such a long process that I don't really want to include.
"""

def wordListSize(wordList):
    #We initiate a new list to keep track of the words and their widths and heights
    wordListSize=[]

    #We get maxFreq and minFreq of the list,
    #which will help with determining the fontSize of each word
    maxWord,maxFreq=wordList[0]
    minWord,minFreq=wordList[len(wordList)-1]

    #I want to approximate how much space IN TOTAL all of my words will take,
    #so that I can create a Word Cloud window of that corresponding size
    aggArea=0

    #We loop through the words to be included in the cloud
    for i in range(len(wordList)):
        word,count=wordList[i]
        if len(wordList)>1: #if the user want to include more than 1 word in the cloud
            #these2 equations make sure the fontSize of word with maxFreq is always 50
            #and the fontSize of word with minFreq is always 10
            #and the ones in between are scaled properly
            scale=(maxFreq-minFreq)/45
            fontSize=int((count-minFreq)/scale+10)

            
        else:
        #but if the user only want to print 1 word, then it automatically gets 50
            fontSize=50

        #this is the crazy part, took me at least 3 hours to get done
        #it works, explaining will take too much time lol
        #but basically approximating the width and height in pixels of words based on
        #their spelling and fontSize
            
        height=0.9*fontSize
        if any([char in "ibdfhl" for char in word]):
            height=height+0.27*fontSize
        if any([char in "gjpqy" for char in word]):
            height=height+0.27*fontSize
        width=0
        for char in word:
            if char in "a,b,d,e,g,p,s":
                width=width+(0.95*fontSize)
            elif char in "il":
                width=width+(0.22*fontSize)
            elif char in "mw":
                width=width+(2.1*fontSize)
            elif char in "rfjty":
                width=width+(0.75*fontSize)
            else:
                width=width+(0.88*fontSize)

        #this variable will hold all the information we need
        oneWord=(word,fontSize,width,height)

        #I calculate the space that this word will take in pixels
        #and then double it up to account for the blank space surrounding it
        area=width*height*2

        #Add it to the total area
        aggArea=aggArea+area

        #Append this word to our list
        wordListSize.append(oneWord)

    return wordListSize,aggArea #append the list or words with their size
                #in both points and pixels, as well as the approx. total area

#This function check if two words overlap, we'll use it later :D
def ifOverlap(drawWordi,drawWordt):
    xi,yi,wordi,fontSizei,widthi,heighti=drawWordi
    xt,yt,wordt,fontSizet,widtht,heightt=drawWordt

    #two words overlap when the invisible rectangles that surround them overlap
    #on both axes, if the difference between the centers' x values or y values
    #is less than half the total of the width or heights respectively of the
    #invisible rectangles, they must overlap.

    #I figured this out by drawing rectangles on a piece of paper
    
    if abs(xi-xt)<0.5*(widthi+widtht) and abs(yi-yt)<0.5*(heighti+heightt):
        return "overlap"
    else:
        return "not overlap"

def drawingWC(gwin,widthWC,wordSize):
    #getting info about the first word
    word0,fontSize0,width0,height0=wordSize[0]

    #drawWordi holds the info that we need to draw a word,
    #and avoid collision with others,
    #(widthWC/2,widthC/2) is the center of the Word Cloud window,
    #that's where we want to draw the first word
    drawWord0=(widthWC/2,widthWC/2,word0,fontSize0,width0,height0)

    #we get out the info we need to draw the 1st word
    x,y,word,fontSize,width,height=drawWord0

    wordDraw=Text(Point(x,y),word)
    wordDraw.setSize(fontSize)
    wordDraw.draw(gwin)

    #drawList keeps track of the words that have been drawn already
    drawList=[drawWord0]

    #Now, we need to draw the rest of the words in our word list
    for i in range(1,len(wordSize)):
        #we get the information we need from the wordSize list
        #be reminded that each element of wordSize have info about
        #word,fontSize,width,height.
        wordi,fontSizei,widthi,heighti = wordSize[i]

        #we generate a random center point for this wordi
        #we spare a margin of 100, so the cloud will be prettier

        margin=100
        xi=randint(margin,widthWC-margin)
        yi=randint(margin,widthWC-margin)

        #Now, like drawWord0, each drawWordi will hold these pieces of info:        
        drawWordi=(xi,yi,wordi,fontSizei,widthi,heighti)

        #Now, we need to check if the random center point we generated above
        #is appropriate or not. An appropriate center point will make sure that
        #no words are overlapping

        #So, we assume that the it's NOT appropriate first.
        
        isAppropriate="inappropriate"

        #while an appropriate drawWordi is not found
        while isAppropriate=="inappropriate": 
            isOverlap="" #we will check if the new word would overlap
                        #with any previously drawn words

            while isAppropriate!="found it!": #until we find the appropriate center

                #we check if our word, given the random center,
                #will overlap with previously drawn words

                #so we loop through the list of previously drawn words
                for t in range(len(drawList)):
                    drawWordt=drawList[t]

                    #we use the ifOverlap(drawWordi,drawWordt) function
                    #to check whether they overlap
                    #we store the result in the variable isOverlap
                    #there are 2 potential resutls: "overlap" and "not overlap"
                    
                    isOverlap=ifOverlap(drawWordi,drawWordt)

                    #as soon as our word overlaps with one previously drawn word,
                    #break this loop, and generate a new random center
                    if isOverlap=="overlap":
                        break

                    #If the loop is not broken, and it can make it until
                    #the last element of the previously drawn word lists,
                    #then our center is a appropriate one!
                    #we FOUND IT!
                    
                    if t==len(drawList)-1 and isOverlap=="not overlap":

                        #We inform the program that we found an appropriate center!
                        isOverlap="found it!"
                        isAppropriate="found it!"

                        #We draw the word to the word cloud window
                        x,y,word,fontSize,width,height=drawWordi
                        wordDraw=Text(Point(x,y),word)
                        wordDraw.setSize(fontSize)
                        r=randrange(0,200)
                        g=randrange(0,200)
                        b=randrange(0,200)
                        wordDraw.setFill(color_rgb(r,g,b))
                        wordDraw.draw(gwin)

                        #We append drawWordi to our drawn words list
                        drawList.append(drawWordi)

                #So, if the loop is broken, which mean our center is
                #inappropriate, we generate a new random center
                #to test out
                xi=randint(100,widthWC-100)
                yi=randint(100,widthWC-100)
                drawWordi=(xi,yi,wordi,fontSizei,widthi,heighti)

        print("drawWord",i,drawWordi)


def main():
    win=GraphWin("Word Cloud",600,600)
    intro(win)

    inputBox1=inputBox(win,300,"Enter text file name:")
    inputBox2=inputBox(win,325,"Number of words:")

    wordCloudButton=drawButton(win, Point(150,400), Point(450,425), "blue4", "Generate")
    exitButton=drawButton(win, Point(550,25), Point(575,50), "red", "X")

    pt=win.getMouse()
    x=pt.getX()
    y=pt.getY()

    Message=False #At this point, there has been no user input error
    
    #while user don't click the exit button
    while not (x>=550 and x<=575 and y>=25 and y<=50):
    #Mouse click on button
    #If the user clicked Generate word cloud:
        if x>=150 and x<=450 and y>=400 and y<=425:
            if Message: #if there has been a error message printed, undraw it
                Message.undraw()
            try:
                fname,n=getInputs(inputBox1,inputBox2)
                print("File name:",fname,"\nNumber of words:",n)
                if fname=="":
                    fname="freeman.txt"
                text=processTextInput(fname)
                print("Processed text:",text)
                words=wordList(text,n)
                print("List of words and their frequencies:",words)
                wordsSize,area=wordListSize(words)
                print(wordsSize)
                width=int(sqrt(area))+150
                print("width=",width)
                winWC=GraphWin("Word Cloud "+fname,width,width)
                drawingWC(winWC,width,wordsSize)
                Message=Text(Point(300,500),"Your Word Cloud has been created!")
                Message.draw(win)
            except:
                Message=Text(Point(300,500),"Invalid Input. Please try again")
                Message.draw(win)

        pt=win.getMouse()
        x=pt.getX()
        y=pt.getY()

    win.close() #if user clicked exit, close window
main()
    

        
    
            
    
