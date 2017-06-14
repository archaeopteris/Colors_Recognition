import cv2
import numpy as np
from time import localtime, time,sleep
#from serial import Serial

cam=cv2.VideoCapture(0)

#cv2.resize(,(640,480))
"""
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)
"""


#For opening
while cam.isOpened()==False:
    cam=cv2.VideoCapture(0)

print cam.isOpened()

matching_dict={'1':'Red',
               '2':'Green',
               '3':'Blue',
               '4':'Yellow',
               '5':'Black'
               }

ranges_list=[[[0,0,76],[255,153,255],0],     # 0 Red
             [[0,76,153],[102,178,255],1],   # 1 Orange
             [[0,102,0],[153,255,102],2],    # 2 Green
             [[153,0,0],[255,255,102],3],    # 3 Blue
             [[153,0,76],[255,102,255],4],   # 4 Pink
             [[0,76,153],[102,255,255],5],   # 5 Yellow
             [[96,96,96],[160,160,160],6],   # 6 Gray
             [[0,0,0],[96,96,96],7]          # 7 Black
            ]

head_ranges=[[[20,20,150],[120,120,255],1],      #Red 
             [[20,120,20],[120,255,120],2],      #Green
             [[150,20,20],[255,130,100],3],      #Blue
             [[20,200,200],[150,255,255],4],     #Yellow
             [[0,0,0],[20,20,20],5]]             #Black

"""

head_ranges=[[[0,0,76],[255,153,255],1],     #Red 
             [[0,102,0],[153,255,102],2],    #Green
             [[153,0,0],[255,255,102],3],    #Blue
             [[0,76,153],[102,255,255],4],   #Yellow
             [[0,0,0],[96,96,96],5]]         #Black

"""

from_head_to_list={'1':'0',
                   '2':'1',
                   '3':'2',
                   '4':'3',
                   '5':'4',
                   '6':'5',
                   '7':'6',
                   }

min_head_array,max_head_array=[],[]

for diapason in head_ranges:
    min_head_array.append(np.array([diapason[0][0],diapason[0][1],diapason[0][2]],dtype=np.uint8))#cv2.cv.Scalar(minimum[0],minimum[1],minimum[2]) Don't working on RPi
    max_head_array.append(np.array([diapason[1][0],diapason[1][1],diapason[1][2]],dtype=np.uint8))#cv2.cv.Scalar(maximum[0],maximum[1],maximum[2]) Don't working on RPi

while 1:

    time_1=time()
    
    ret,raw_img=cam.read()
    cv2.imshow("Test",raw_img)
    cv2.waitKey(27)
    if not ret:
        break
    
    returned_values,j=[],0
    for diapason in head_ranges:
        stop=False
        
        ############

        min_=min_head_array[j]
        max_=max_head_array[j]
        

        img_trash=cv2.inRange(np.array(raw_img,dtype=np.uint8),min_,max_)
        i=0
        count=len(img_trash.nonzero()[0])

        ############


        if count>=1000:#1156:#12741

            '''
            ranges=from_head_to_list['%s' % diapason[2]].split('/')
            ranges=[int(x) for x in ranges]
            print ranges
            '''
            

            #############
      
            min_=np.array([head_ranges[j][0][0],head_ranges[j][0][1],head_ranges[j][0][2]],dtype=np.uint8)#cv2.cv.Scalar(minimum[0],minimum[1],minimum[2]) Don't working on RPi
            max_=np.array([head_ranges[j][1][0],head_ranges[j][1][1],head_ranges[j][1][2]],dtype=np.uint8)#cv2.cv.Scalar(maximum[0],maximum[1],maximum[2]) Don't working on RPi
            img_trash=cv2.inRange(np.array(raw_img,dtype=np.uint8),min_,max_)

            i=len(img_trash.nonzero()[0])
            
            #######
            returned_values.append([i,diapason[2]])
            if returned_values[len(returned_values)-1][0]>=63705:
                stop=True
                
            if stop!=True: #!!!!!!!!!
                returned_values.append([count-i,j])
                if returned_values[len(returned_values)-1][0]>=63705:
                    stop=True
        j+=1


       
        
    if stop!=True:
        returned_values.sort()
    #######
    """
    if len(returned_values)!=0:
        com.write(matching_dict['%i' % returned_values[len(returned_values)-1][1]][0])
        print matching_dict['%i' % returned_values[len(returned_values)-1][1]][0]
    else:
        com.write("W")
    """
    ######
    if len(returned_values)>0:
        print '%s Color Detected \n' % matching_dict["%s" % returned_values[len(returned_values)-1][1]]
        #matching_dict[
        #at %i.%i.%i , localtime()[3],localtime()[4],localtime()[5]
    else:
        print "White Color Detected\n"
        #at %i.%i.%i \n"%(localtime()[3],localtime()[4],localtime()[5])
        
    print time()-time_1,'\n'
cv2.destroyAllWindows()
cam.release()
