import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

font_scale = 1.5
font = cv2.FONT_HERSHEY_PLAIN

#file_path = input("give file path of video you want to open)
#cap =cv2.VideoCapture(file_path)

#file_name= input("give a file name:\n")
#f = open(file_name+".txt", "a")


def OCRFunction(filePath, id):
    cap =cv2.VideoCapture(filePath)# file path of video
    f = open("static/video/"+str(id)+"OCR.vtt", "a")

    if not cap.isOpened():
        cap =cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open video")

    previous_line = '' # initialising previous line tracker
    counter= 0
    while True:
        ret,frame=cap.read()
        counter +=1
        if ((counter%30)==0): # reads every 30 frames
            
            imgchar = pytesseract.image_to_string(frame)# reads words from image
            
            #prevents sentences from frames from repeating in text file // this is not working
            if imgchar is not previous_line:
                previous_line = imgchar #previous lines value become imgchar value
                print(imgchar) # prints value to command line so i can see while debugging
                f.write(imgchar)# writes line to text
                breakpoint()
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            #cv2.imshow('Text Detection Tutorial',frame) # shows video I will not delete yet
            
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        if ret == False: # breaks loop when video ends
            break

    f.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    inputPath = """static/video/borrowed_223.mp4"""
    print("Running OCR Function")
    OCRFunction(inputPath,1)
