# Developed by Ashton Williams, Brien Schmaltz, Nick Ianni, Mak, Shivani

import cv2 as cv2
import numpy as np
import glob
import os, os.path
import cv2 as cv2
import numpy as np

from datetime import datetime
from statistics import mode
from tqdm import tqdm

#  *** MAIN ***
def main():                                     
    print("\n*** Uranium Image Cleanup Tool ***")           
    while(True):
        mainMenu()

def mainMenu():         
    # Create array of images extracted from folder                                                  
    images_retrieved = []                                                   

    #Print out options, then verify input
    while(True):
        print("-------------------------------------------")
        print("[1]: New Directory\n[2]: Quit")   
        print("\nInput: ", end="")                                         
        UserInput = input()
        print("")

        #Validate user input is an int
        try:
            Val = int(UserInput)                     
        except ValueError:
            print("*Error: Enter [1] to begin program - Enter [2] to quit program.\n")
            continue #Return to start of while(True)

        if int(UserInput) == 1:         
            directoryInput = input("Enter Image/s Retrieval Directory:")       
            break
        elif int(UserInput)  == 2:
            exit()

        #Second validation for integer numbers != 1 or 2
        else:                                                                   
            print("*Error: Enter [1] to begin program - Enter [2] to quit program.\n")
            continue

    #Send Folder to be inspected        
    folderInspection(directoryInput, images_retrieved)                      
    whatsIsInside(images_retrieved)

    #if the given directory has no valid images in them, restart.
    if(not images_retrieved):
        print("\nNo valid files in the given directory.")
        print("Restarting...\n")
        return

    print("")
    directoryOutput = input("Enter Image/s Output Directory: ")     
    # Check if directory given is a valid pathname
    while(True):
        print("Checking Folder Path (" + directoryOutput + ")...")
        if os.path.isdir(directoryOutput) :                               # If directory is a valid pathname...
            print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +  "]: " + "Directory Found.")
            break                  
        else :
            print("Error: Input is not a valid pathname")                   
            directoryOutput = input ("Enter Image/s Output Directory: ")   # User Input of Retrieval Directory

   # Create writable activityLog file
    activityLogPath = os.path.join(directoryOutput, "activityLog.txt")   
    activityLogFile = open(activityLogPath, "a")

    activityLogFile.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +  "]: " + "Input Directory: " + directoryInput + "\n")
    activityLogFile.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +  "]: " + "Output Directory: " + directoryOutput + "\n")

    # After imageRetrieval completion, send imported images array to be processed
    imageToCV2(images_retrieved, directoryOutput, activityLogFile)

    #Once complete, log out info to the console and write to activity log.    
    print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +  "]: " + "Completed successfully.")
    activityLogFile.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +  "]: " + "Completed successfully.\n----------\n")
    activityLogFile.close()                                           
    
#End of main

#-----------------------------------------------------------------------
# Folder and Input verification functions
#-----------------------------------------------------------------------

# Check to see if 'directoryInput' path exists
def folderInspection(directoryInput, images_retrieved):                     
    print("Checking Folder Path (" + directoryInput + ")...")

    if os.path.exists(directoryInput):                      # Does directory exist?
        print("\n-----------------> File Path Check: OK")

        #Check OS, either windows or unix like system. Windows uses \ Unix uses /
        if os.name == 'nt':
            slash = '\*'
        else: 
            slash = '/*'

        directoryInput = directoryInput + slash                              # the addition of '*' symbol is proper semantics when accessing files in folders
        imageRetrieval(directoryInput, images_retrieved)                    # Sending directyInput & the array to store the images in to the image retrieval function
    else:
        print("\n-----------------> File Path Check: * FAIL * -> Path Does Not Exist")
        newDirectory = input("Please Enter a New Directory: ")
        folderInspection(newDirectory, images_retrieved)                    # If User wants to enter new directory, program will send the new directory to be inspected

# Enter directory and extracts images into images_received
def imageRetrieval(directoryInput, images_retrieved):                       
    for f in glob.iglob(directoryInput):
        print('File Found: ' + f)
        #activityLogFile.write("* Found " + f + "\n")
        images_retrieved.append(f)                                          # Adds Image to Array
    
    imageIntegrity(images_retrieved)                                        # Sends Retrieved Images to get checked for file integrity


# Print out image array (location of each file)
def whatsIsInside(images_retrieved):
    print("Images Ready for Processing: ")
    for f in images_retrieved :
        print(f)


# Check images collected in images_received array for file integrity
def imageIntegrity(images_retrieved):
    print("\n-----------------> Now Checking File Integrity")                   # DEBUG Purposes
    
    print("Files Retrieved:")
    whatsIsInside(images_retrieved)

    index = 0
    lengthOfArray = len(images_retrieved)
    for i in range(lengthOfArray):
        filename = os.path.basename(images_retrieved[index]) 
        print('\nChecking: [', end= "")        
        print(filename + "]")                  # DEBUG purposes

        split_extension = os.path.splitext(images_retrieved[index])[1].lower()  # Split the extension from the path and normalise it to lowercase.
            
        if (split_extension == '.tif' or  split_extension == ".png") and not ("RESULT_" in filename):   # Checks if File is of correct extentsion
            print("File Integrity: OK -> ", end= "")
            print(images_retrieved[index]) 
            print(" ")   
            index = index + 1

        else:
            print("File Integrity: *FAIL For File-> " , end= "")
            print(images_retrieved[index]) 
            print("Accepted Extensions: .tif - .png\n")

            print("Removing File...")

            print("\nRemoved: ", end="")
            print(images_retrieved[index])
            images_retrieved.remove(images_retrieved[index])                    # Pops out (Removes) image with incorrect extension

            if i == (lengthOfArray - 1):
                #print("\n-- NO IMAGES REMAINING IN INPUT FOLDER --")

                if lengthOfArray == 0:                                           # If Image Array is Empty Restart Program
                    print("\n-- NO IMAGES ACCEPTED IN INPUT FOLDER --")
                    mainMenu()

            try:
                images_retrieved[index]
            except IndexError:
                print("\nRemoval Finished...")              
    
def getImageNames(images_retrieved):
    images = []
    imageCount = 0
    for i in tqdm(images_retrieved):
        images[imageCount] = os.path.basename(i)
        imageCount+=1
    return images

#  Display Image To User || Debugging
def showImage(images_retrieved):                                            # Shows user current image
    for images in images_retrieved:
        images.show()                                                       # Shows image received / Debug purposes


#-----------------------------------------------------------------------
#Image noise/text/box removal functions
#-----------------------------------------------------------------------


# Main loop to iterate through each image and write to console and activity log
def imageToCV2(images_retrieved, directoryOutput, activityLogFile):                                       
    imageCounter = 1
    activityLogFile.write("Processing Images...\n") 

    for i in tqdm(images_retrieved):
        
        #Grab image from file array
        img = cv2.imread(i)

        #pass to removeLabel for processing
        result = removeLabel(img) 

        #Create filename suitable for Linux and Windows
        current_result_filename = os.path.join(directoryOutput, "RESULT_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S_") + os.path.basename(i))

        print("\n[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +  "]: " + "Image: " + os.path.basename(i) + " processed")
        
        #Write out result file to output directory
        cv2.imwrite(current_result_filename , result)

        print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +  "]: " + "Image: " + current_result_filename + " saved")
        activityLogFile.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +  "]: " + "* Image: " + current_result_filename + " saved\n")
        imageCounter += 1

#detects the bigger white areas in the image
#returns a mask of the dilated detected white areas
def detectWhite(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #convert to HSV

    #image preprocessing
    hsv_low = np.array([0, 0, 0], np.uint8)
    hsv_high = np.array([179, 255, 254], np.uint8)
    mask = cv2.inRange(hsv, hsv_low, hsv_high)
    mask = cv2.bitwise_not(mask) #inverts the mask (flips black and white)

    #Gaussian blur and adaptive threshold
    blur = cv2.GaussianBlur(mask, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,15)

    #Dilate to combine letters (make detected text a blob)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=6)

    mask = cv2.cvtColor(dilate,cv2.COLOR_GRAY2BGR) #convert back to RGB (3 channels)
    return mask #mask of detected dilated white areas

#returns a mask image that contains just the background (uranium replaced with the background color)
def get_background(img, rows, cols):

    average = (int)(mode(img.flatten())) #gets the mode of image (most common color value)

    #if the mode is over 90, half it
    if(average > 90):
        average = (int)(average/2)
    
    #if after halfing it and it is under 20, use the median instead
    if(average <= 20):
        average = (int)(np.median(img))

        #if the median is over 90 half it
        if(average > 90):
            average = (int)(average/2)

    background = img.copy()

    prevPixel = [average,average,average] #initially define a pixel value that is the average
    for i in range(rows):
        for j in range(cols):

            #if the average of the current pixel value is greater than the overall average, its part of the uraniam
            if (np.average(background[i][j]) > average): 
                if(j == 0):
                    background[i][j] = prevPixel #make the pixel the background value
                else:
                    randomInt = np.random.randint(0,j) #get a random index value in the row
                    prevPixel = background[i][randomInt] #set the prevPixel to the value at that random index
                    background[i][j] = prevPixel #it is the new background pixel

    return background

#returns image with no white pixels. Iterates through each pixel, deletes white pixel and replaces with background pixel nearby.
def remove_white_pixels(original_img, mask_img, rows, cols, background, topLeft, img):

    result_img = original_img.copy() #Copy 
    n=0 #background row index
    m=0 #background column index

    if(topLeft):
        n = 45 #if top left is true, start background row index at 45

    backRow, backCol, _ = np.array(background).shape

    #Loop that iterates through each pixel, determines if white, then makes that pixel black. 
    for i in range(rows):
        for j in range(cols):
            mask_pixel_val = mask_img[i,j] #value/color of the current pixel
            
            # Conditional to determine if pixel is white.
            if (np.array_equal(mask_pixel_val, np.array([255, 255, 255]))):
                # Then eradicate white pixels.
                result_img[i,j] = background[n][m] #make it a color 
                
                #keep going until at the end of the row in the background mask, then go to the next row
                m+=1 #if at the end of the row
                if(m == backCol):
                    n+=1 #increment rows 
                    m=0 #set column index back to 0

    return result_img

#returns the image with the black box removed by filling in the black box pixels with pixels from the background mask
def remove_black_box(img, rows, cols, background, topLeft):
    n=0 #background row index
    m=0 #background column index
    backRow, backCol, _ = np.array(background).shape 
    result_img = img.copy()

    #if there is text in the top left
    if(topLeft):
        n=880 #start n at 880 if top left is true
        
        if (np.array_equal(img[933, 0], np.array([1,1,1]))): #if the first pixel at row 933 is black
            
            #loop through and replace the black with a pixel from the background mask
            for i in range(933, rows): 
                for j in range(cols):
                    result_img[i,j] = background[n][m] 
                    
                    #keep going until at the end of the row in the background mask, then go to the next row
                    m+=1 #if at the end of the row
                    if(m == backCol):
                        n+=1 #increment rows 
                        m=0 #set column index back to 0

        elif (np.array_equal(img[960, 0], np.array([1,1,1]))): #if the first pixel at row 960 is black
            
            #loop through and replace the black with a pixel from the background mask
            for i in range(960, rows):
                for j in range(cols):
                    result_img[i,j] = background[n][m] 
                    
                    #keep going until at the end of the row in the background mask, then go to the next row
                    m+=1 #if at the end of the row
                    if(m == backCol):
                        n+=1 #increment rows 
                        m=0 #set column index back to 0

    #if there isnt white pixels in the top left
    else:
        if (np.array_equal(img[933, 0], np.array([1,1,1]))): #if the first pixel at row 933 is black
            
            #loop through and replace the black with a pixel from the background mask
            for i in range(933, rows):
                for j in range(cols):
                    result_img[i,j] = background[n][m] 
                    
                    #keep going until at the end of the row in the background mask, then go to the next row
                    m+=1 #if at the end of the row
                    if(m == backCol):
                        n+=1 #increment rows 
                        m=0 #set column index back to 0

        elif (np.array_equal(img[960, 0], np.array([1,1,1]))): #if the first pixel at row 960 is black
            
            #loop through and replace the black with a pixel from the background mask
            for i in range(958, rows):
                for j in range(cols):
                    result_img[i,j] = background[n][m] 
                    
                    #keep going until at the end of the row in the background mask, then go to the next row
                    m+=1 #if at the end of the row
                    if(m == backCol):
                        n+=1 #increment rows 
                        m=0 #set column index back to 0

    return result_img

#removes the unwated labels from the images
#returns result/final image
def removeLabel(image):
    #copies of the first image (so I dont overwrite the original one)
    img = image.copy()
    img2 = image.copy()
    img3 = image.copy()

    rows,cols,_ = img.shape #gets the image array shape
    background = get_background(img, rows, cols) #gets the background mask
    n=0 #background row index
    m=0 #background column index
    backRow, backCol, _ = np.array(background).shape
    #return background
    
    #removes labels on images with grey area at the bottom
    if(rows == 1530):

        for i in range(1280, 1530):
            for j in range(cols):
                img2[i,j] = background[n][m] #make it a value in the background mask
                
                #keep going until at the end of the row in the background mask, then go to the next row
                m+=1 #inrement column
                if(m == backCol): #if at the end of the row
                    n+=1 #increment rows 
                    m=0 #set column index back to 0
        result = img2


    #removes labels on images with transparent label in the top right
    elif(rows == 1280 and cols == 1280):

        for i in range(0, 150):
            for j in range(555, 1235):
                img2[i,j] = background[i+1130][j] #make it a value in the background mask

        result = img2
        
    #removes labels for every other image
    else:
        topLeft = False #bool that is true if a rectangle needs to be in the top left

        #check if there is white in top left
        for i in range(0, 45):
            for j in range(0, 150):
                if(np.array_equal(image[i,j], np.array([255, 255, 255]))):
                    topLeft = True
                    break #stop if white is found
            
            if(topLeft):
                break #stop if white is found

        #if there is white in the top left, add a rectangle   
        if (topLeft):
            for i in range(0, 45):
                for j in range(0, 150):
                    img2[i,j] = [255, 255, 255] #add white mask top

        removedBox = remove_black_box(img3, rows, cols, background, topLeft) #gets the background mask of the image (mask that just contains the background with no uranium)
        dect_white = detectWhite(removedBox) #gets mask of detected white
        result = remove_white_pixels(removedBox, dect_white, rows, cols, background, topLeft, img) #removes the remaining white pixels from the image

    return result
   
# Function Main() - Sets "Main()" as the primary driver to the program
if __name__ == "__main__":
    main()
