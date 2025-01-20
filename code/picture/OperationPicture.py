
# Replace this with your robot's IP address

import os
import sys
import time
import numpy as np
import cv2 as cv
from naoqi import ALProxy
from chessReader import *
import math

def CaptureVue(ip, port, camera=1, resolution=1, colorspace=13):
    # Connect to the camera
    camProxy = ALProxy("ALVideoDevice", ip, port)
    camProxy.openCamera(camera)
    videoClient = camProxy.subscribeCamera("python_client", camera, resolution, colorspace, 5)
    naoImage = camProxy.getImageRemote(videoClient)
    camProxy.unsubscribe(videoClient)
    camProxy.closeCamera(camera)
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    image_data = naoImage[6] #array d hexa
    nparr = np.frombuffer(image_data, np.uint8) #en 8int
    grouped = np.array([nparr[i:i+3] for i in range(0, len(nparr), 3)]) #group par pxl
    pixel_array = np.array(grouped, dtype=np.uint8).reshape((imageHeight, imageWidth, 3)) #reshape en matrice
    
    return pixel_array

def regardRobot(ip, port):
    
    camProxy = ALProxy("ALVideoDevice", ip, port)
    camProxy.openCamera(1)
    videoClient = camProxy.subscribeCamera("python_client", 1, 1, 13, 5)
    motion = ALProxy("ALMotion", ip, port)
    current_head_yaw = 0
    current_head_pitch = 0
    motion.angleInterpolationWithSpeed("HeadYaw", math.radians(current_head_yaw), 0.1)
    motion.angleInterpolationWithSpeed("HeadPitch", math.radians(current_head_pitch), 0.1)
    gap = 10
    while 1 :
        naoImage = camProxy.getImageRemote(videoClient)
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        image_data = naoImage[6] #array d hexa
        nparr = np.frombuffer(image_data, np.uint8) #en 8int
        grouped = np.array([nparr[i:i+3] for i in range(0, len(nparr), 3)]) #group par pxl
        pixel_array = np.array(grouped, dtype=np.uint8).reshape((imageHeight, imageWidth, 3)) #reshape en matrice
        """
        cv.imshow("Window Name", pixel_array)
        cv.waitKey(0)  # Wait for a key press to close the window
        cv.destroyAllWindows()
        """
        problem = cameraman(pixel_array,extractRedDot(pixel_array))
        
        if( problem == 0 ) :
            current_head_yaw -= gap
            current_head_pitch += gap
            print("Camera trop haute et trop a gauche")
           
        elif( problem == 1 ) :
            current_head_pitch += gap
            print "Camera trop haute"
        
        elif( problem == 2 ) :
            current_head_yaw -= gap
            current_head_pitch += gap
            print "Camera trop haut et trop a droite"
        elif( problem == 3 ) :
            current_head_yaw -= gap
            print"Camera trop a droite"
        elif( problem == 4 ) :
            current_head_yaw += gap
            current_head_pitch += gap
            print "Camera trop basse et trop a droite"
        elif( problem == 5 ) :
            current_head_yaw += gap
            print "Camera trop basse"
        elif( problem == 6 ) :
            current_head_yaw +=gap
            current_head_pitch += gap
            print "Camera trop haut et trop a gauche"
        elif( problem == 7 ) :
            current_head_yaw +=gap
            print "Camera trop a gauche"
        elif( problem == 8 ) :
            break
        """

        if( problem == 8 ) :
            break
        current_head_pitch += gap
        """ 
        motion.angleInterpolationWithSpeed("HeadYaw", math.radians(current_head_yaw), 0.1)
        motion.angleInterpolationWithSpeed("HeadPitch", math.radians(current_head_pitch), 0.1)
        #time.sleep(1)
    camProxy.unsubscribe(videoClient)
    camProxy.closeCamera(1)

def isRobotWhite(ip, port):

    camProxy = ALProxy("ALVideoDevice", ip, port)
    camProxy.openCamera(1)
    videoClient = camProxy.subscribeCamera("python_client", 1, 1, 13, 5)
    motion = ALProxy("ALMotion", ip, port)
    
    naoImage = camProxy.getImageRemote(videoClient)
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    image_data = naoImage[6] #array d hexa
    nparr = np.frombuffer(image_data, np.uint8) #en 8int
    grouped = np.array([nparr[i:i+3] for i in range(0, len(nparr), 3)]) #group par pxl
    pixel_array = np.array(grouped, dtype=np.uint8).reshape((imageHeight, imageWidth, 3)) #reshape en matrice
    extract = extractboard(pixel_array)
    extract = cv.cvtColor(extract, cv.COLOR_BGR2GRAY)

    num_cols = extract.shape[1]
    a =  extract[:,: num_cols // 2 ]
    second_half = extract[:, num_cols // 2 :]
    
    cv.imshow("a"+ str(np.sum(a == 0)), a)
    cv.imshow("left"+ str(np.sum(second_half == 0)), second_half)
    cv.imshow("Window Name", pixel_array)
    cv.imshow("extractboard Name",extract )

    cv.imwrite("extractboard.png",extract)
    cv.imwrite("right.png",a)
    cv.imwrite("left.png",second_half)

    cv.waitKey(0)  # Wait for a key press to close the window
    cv.destroyAllWindows()
    
    camProxy.unsubscribe(videoClient)
    camProxy.closeCamera(1)
    return np.sum(a == 0)>np.sum(second_half == 0)
    
def submatrix(matrix,x1=None,y1=None,x2=None,y2=None):
    return matrix[x1:x2][y1:y2]

def rgb_mean(image):
    (r,g,b) = cv.split(image)
    return (r.mean(),g.mean(),b.mean())

def showNaoImage(IP, PORT, camera):
    """
    First get an image from Nao, then show it on the screen with PIL.
    """

    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    resolution = 2    # VGA
    colorSpace = 11   # RGB
    camProxy.openCamera(camera)
    videoClient = camProxy.subscribeCamera("python_client", camera, resolution, colorSpace, 5)

    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    naoImage = camProxy.getImageRemote(videoClient)

    t1 = time.time()

    # Time the image transfer.
    print "acquisition delay ", t1 - t0

    camProxy.unsubscribe(videoClient)
    camProxy.closeCamera(camera)
    # Now we work with the image returned and save it as a PNG  using ImageDraw
    # package.
    # Get the image size and pixel array.
    if naoImage == None:
        return 1
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
    # Create a PIL Image from our pixel array.
    im = Image.frombytes("RGB", (imageWidth, imageHeight), array)
    # Save the image.
    im.save("cam"+str(camera)+"Image.png", "PNG")


def ReperageBoard(image):
    filename=get_latest_file("/home/nao/recordings/cameras/")
    img = cv.imread(filename)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    
    gray = np.float32(gray)
    dst = cv.cornerHarris(gray,2,3,0.04)
    
    #result is dilated for marking the corners, not important
    dst = cv.dilate(dst,None)
    
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[0,0,255]
    
    cv.imshow('dst',img)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()

def get_latest_file(directory):
    # Liste tous les fichiers dans le dossier
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Verifie s'il y a des fichiers
    if not files:
        return None

    # Recupere le dernier fichier en fonction de la date de modification
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def diff(image1,image2):
    return cv.max(cv.subtract(image1,image2),cv.subtract(image2,image1))

def threshold(image,thresh,max_value,type):
    (r,g,b) = cv.split(image)
    r_out = cv.threshold(r,thresh,max_value,type)
    g_out = cv.threshold(g,thresh,max_value,type)
    b_out = cv.threshold(b,thresh,max_value,type)
    return cv.merge([r_out[1],g_out[1],b_out[1]])

def adaptive_threshold(image,max_value,adaptive_method,threshold_type,block_size,c):
    (r,g,b) = cv.split(image)
    r_out = cv.adaptiveThreshold(r,max_value,adaptive_method,threshold_type,block_size,c)
    g_out = cv.adaptiveThreshold(g,max_value,adaptive_method,threshold_type,block_size,c)
    b_out = cv.adaptiveThreshold(b,max_value,adaptive_method,threshold_type,block_size,c)
    return cv.merge([r_out,g_out,b_out])

def corners(image):
    pts = []
    pt = []
    return pts

def reshape(image,pts1):
    img = cv.imread(image)
    rows,cols,ch = img.shape

    #pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
    
    M = cv.getPerspectiveTransform(pts1,pts2)
    
    dst = cv.warpPerspective(img,M,(300,300))
    
    plt.subplot(121),plt.imshow(img),plt.title('Input')
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    plt.show()

    return dst

def filter(image,r_weight = 1,g_weight = -1, b_weight = -1, min_value=0, max_value = 255):
    (b,g,r) = cv.split(image)
    output = (np.int32(r_weight)*r) + (np.int32(g_weight)*g) + (np.int32(b_weight)*b) 
    return output.clip(min_value,max_value)

def posterize(matrix,high = 0,low = 255,threshold = 8):
    return np.vectorize((lambda t : high if t > threshold  else low))(matrix)


# This call returns ['/home/nao/recordings/cameras/image_0.jpg', '/home/nao/recordings/cameras/image_1.jpg', '/home/nao/recordings/cameras/image_2.jpg']
