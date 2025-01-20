import cv2 as cv
import numpy as np


#"main" function of the file, this takes the filepath of two images of the chessboard, and returns which squares moved. Only works on moves involving two squares, for now.
def get_two_squares(filepath_img_1, filepath_img_2) :
    #Turns the pictures into squares
    img1 = cv.imread(filepath_img_1)
    img2 = cv.imread(filepath_img_2)
    extracted1 = extractboard(img1)
    extracted2 = extractboard(img2)

    #get the difference between the two
    diff = difference(extracted1, extracted2)
    cv.imwrite('test_inbetween/diff.jpg', diff)


    #height, width = img1.shape[:2]
    square_proportions = (200, 200)
    resized_diff = cv.resize(diff, square_proportions, interpolation= cv.INTER_LINEAR)

    cv.imwrite('test_inbetween/diffSquare.jpg', resized_diff)

    #Extract the red from the difference and turn it into an 8 by 8 grid of red quantities
    redchannel = get_channel(resized_diff, 'r')
    quad = quadrillage(redchannel, 255)

    #get the biggest two
    tup = biggestTwo(quad)

    ret1 = indexToChess(tup[0], tup[1]) 
    #print(ret1)
    ret2 = indexToChess(tup[2], tup[3])
    #print(ret2)

    return ret1, ret2

def get_two_squaresBis(img1, img2,couleur) :
    extracted1 = extractboard(img1)
    extracted2 = extractboard(img2)
    extracted1 = cv.GaussianBlur(extracted1,(3,3),0)
    extracted2 = cv.GaussianBlur(extracted2,(3,3),0)
    #get the difference between the two
    diff = difference(extracted1, extracted2)
    cv.imshow("diff", diff)
    cv.imshow("extracted1", extracted1)
    cv.imshow("extracted2", extracted2)
    cv.imshow("img1", img1)
    cv.imshow("img2", img2)

    cv.imwrite("diff.png", diff)
    cv.imwrite("extracted1.png", extracted1)
    cv.imwrite("extracted2.png", extracted2)

    cv.waitKey(0)  # Wait for a key press to close the window
    cv.destroyAllWindows()
    cv.imwrite('test_inbetween/diff.jpg', diff)


    #height, width = img1.shape[:2]
    square_proportions = (200, 200)
    resized_diff = cv.resize(diff, square_proportions, interpolation= cv.INTER_LINEAR)

    cv.imwrite('test_inbetween/diffSquare.jpg', resized_diff)

    #Extract the red from the difference and turn it into an 8 by 8 grid of red quantities
    redchannel = get_channel(resized_diff, 'r')
    quad = quadrillage(redchannel, 255)

    #get the biggest two
    tup = biggestTwo(quad)

    ret1 = indexToChess(tup[0], tup[1],couleur) 
    #print(ret1)
    ret2 = indexToChess(tup[2], tup[3],couleur)
    #print(ret2)

    return ret1, ret2

#Takes as parameters a matrix and a sought value, outputs a matrix of size 8 by default with the count of the value in each "square" of the grid.
def quadrillage(mat, soughtValue, gridCountX=8, gridCountY=-1) :
    #mat is a 2d matrix
    #soughtValue is the value you're looking for
    #gridCountX and Y are the end matrix's dimensions. Leave both blank for a chess 8x8, leave 1 blank for a square matrix.
    if(gridCountY==-1) :
        gridCountY=gridCountX
    
    x = np.size(mat,0)
    squarelen = x/gridCountX
    
    ret = np.zeros(((gridCountX, gridCountY)))
    #print(ret)
    for i in range(np.size(mat,0)) :
        for j in range(np.size(mat,1)) :
            if(mat[i][j]==soughtValue) :
                ret[i//(x/gridCountX)][j//(x/gridCountX)] +=1
                
    #print(ret)
    return ret


#returns the index of the biggest two values in the matrix
def biggestTwo(mat) :
    #mat is a 2d matrix with numbered values
    biggest = -1 
    biggester = -1
    xbv1 = -1
    xbv2 = -1
    ybv1 = -1
    ybv2 = -1

    for i in range(np.size(mat,0)) :
        for j in range(np.size(mat,1)) :
            if (mat[i][j]>biggest) :
                if(mat[i][j]>biggester) :
                    biggest = biggester
                    xbv1 = xbv2
                    ybv1 = ybv2
                    biggester = mat[i][j]
                    xbv2 = i
                    ybv2 = j
                else :
                    biggest = mat[i][j]
                    xbv1 = i
                    ybv1 = j
    #print(xbv1, ybv1, xbv2, ybv2)
    return xbv1, ybv1, xbv2, ybv2


#takes positions in an index, returns them as a square on a chessboard
def indexToChess(a, b, pov='WHITE') :
    
    chessboardLinesWhite='abcdefgh'
    chessboardLinesBlack='hgfedcba'
    if(pov=='WHITE') :
        return (chessboardLinesWhite[a]+str(8-b))
    else :
        return (chessboardLinesBlack[a]+str(b+1))

#singles out a channel of the image.
def get_channel (img, color) :
    b,g,r = cv.split(img)
    if (color=='r') :
        ret = r
    elif (color == 'b') :
        ret = b
    else :
        ret = g
    return ret


#gets the difference between two pictures.
def difference(image1, image2) :
    # compute difference
    difference1 = cv.subtract(image2, image1)
    difference2 = cv.subtract(image1, image2)
    difference = difference1+difference2

    # color the mask red
    Conv_hsv_Gray = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(Conv_hsv_Gray, 0, 255,cv.THRESH_BINARY_INV |cv.THRESH_OTSU)
    difference[mask != 255] = [0, 0, 255]

    # add the red mask to the images to make the differences obvious
    #image1[mask != 255] = [0, 0, 255]
    #image2[mask != 255] = [0, 0, 255]
    return difference

#return x y of every red dot
def extractRedDot(image):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([5, 255, 255])
    lower_red2 = np.array([175, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    mask = cv.bitwise_or(mask1, mask2)
    result = cv.bitwise_and(image, image, mask=mask)
    cv.imwrite('pra.jpg', result)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    coins = []
    for contour in contours:
        area = cv.contourArea(contour)
        if area < 10000: 
            M = cv.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv.circle(image, (cX, cY), 5, (0, 255, 0), -1) 
                coins.append((cX, cY))
    """
    cv.imshow("Window Name", image)
    cv.waitKey(0)  # Wait for a key press to close the window
    cv.destroyAllWindows()
    """
    return coins

def extractboard(image):
    # Charger l'image
    #image = cv.imread('path')
    
    # Convertir l'image en espace de couleur HSV
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    
    # Dfinir la plage de couleur rouge en HSV
    lower_red1 = np.array([0, 100, 50])  # Plage du rouge clair (0)
    upper_red1 = np.array([5, 255, 255])
    
    # Plage pour les rouges foncs
    lower_red2 = np.array([175, 100, 50])  # Plage du rouge fonc (170  180)
    upper_red2 = np.array([180, 255, 255])
    
    # Crer deux masques pour les deux plages de rouge
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    
    # Combiner les deux masques
    mask = cv.bitwise_or(mask1, mask2)
    
    # Appliquer le masque sur l'image originale
    result = cv.bitwise_and(image, image, mask=mask)
    cv.imwrite('pra.jpg', result)
    # Trouver les contours dan le masque
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    coins = []
    # Boucle pour dessiner les contours et vrifier les points
    for contour in contours:
        # Calculer l'aire du contour
        area = cv.contourArea(contour)
        
        # Si l'aire est assez petite (ex. pour un point), dessiner le contour
        if area < 100000:  # Ajustez ce seuil selon la taille de votre point
            # Trouver le centre du contour (le centre du point)
            M = cv.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
    
                # Dessiner un cercle au centre du point rouge
                #cv.circle(image, (cX, cY), 5, (0, 255, 0), -1)  # Cercle vert de rayon 5
                coins.append((cX, cY))
    cv.imwrite('pr.jpg', image)
    points = coins
    # tape 1: Sparer les points par leur position (gauche/droite)
    # On dtermine le point le plus  gauche (minimum x) et  droite (maximum x)
    left_points = sorted([point for point in points], key=lambda x: x[0])[:2]  # 2 points  gauche (les plus petits x)
    right_points = sorted([point for point in points], key=lambda x: x[0])[2:]  # 2 points  droite (les plus grands x)
    
    # tape 2: Trier les points  gauche par y (haut-bas) et  droite aussi
    left_sorted = sorted(left_points, key=lambda x: x[1])  # Trier par y pour les points  gauche
    right_sorted = sorted(right_points, key=lambda x: x[1])  # Trier par y pour les points  droite
    
    # Rsultat final: organiser les points dans l'ordre gauche-bas, gauche-haut, droite-haut, droite-bas
    sorted_points = [left_sorted[0], left_sorted[1], right_sorted[1], right_sorted[0]]
    
    # Define the 4 points (x, y) coordinates of the quadrilateral in the image
    # These points should be ordered in a clockwise or counterclockwise manner (top-left, top-right, bottom-right, bottom-left)
    pts = np.array(sorted_points, dtype="float32")
    
    # Define the 4 points for the destination (the rectangle)
    # Here, we're assuming a rectangle with width=300 and height=200
    width, height = 300, 200
    dst_pts = np.array([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype="float32")
    
    # Get the perspective transform matrix
    matrix = cv.getPerspectiveTransform(pts, dst_pts)
    
    # Apply the perspective transform to the image
    warped_image = cv.warpPerspective(image, matrix, (width, height))
    
    # Show the extracted (warped) image
    return warped_image

def get_8_corners(image) :
    
    height, width = image.shape[:2]

    #sens horaire, commencant en haut a gauche
    ret = [
        (0,0),                   #haut gauche
        (0,int(width/2)),        #haut millieu
        (0,width),               #haut droite
        (int(height/2), width),  #millieu droite
        (height, width),         #bas droite
        (height, int(width/2)),  #bas millieu
        (height, 0),             #bas gauche
        (int(height/2), 0)       #millieu gauche
    ]
    return ret

def get_biggest_distance(list1, list2) :
    biggestVal = -1
    biggestIndex = -1
    for i in range(len(list2)) :
        seum = 0 #vu que "sum" est un mot clef...
        for j in range(len(list1)) :

            seum += int(np.linalg.norm(np.asarray(list2[i])-np.asarray(list1[j])))#on rcupere la somme des distances des points a cet lment de list2

        if ( seum >= biggestVal ) :
            biggestVal = seum
            biggestIndex = i
    return biggestIndex


def describe_problem(problem) :
    if( problem == 0 ) :
        return "Camera trop haute et trop a gauche"
    elif( problem == 1 ) :
        return "Camera trop haute"
    elif( problem == 2 ) :
        return "Camera trop haut et trop a droite"
    elif( problem == 3 ) :
        return "Camera trop a droite"
    elif( problem == 4 ) :
        return "Camera trop basse et trop a droite"
    elif( problem == 5 ) :
        return "Camera trop basse"
    elif( problem == 6 ) :
        return "Camera trop haut et trop a gauche"
    elif( problem == 7 ) :
        return "Camera trop a gauche"
    elif( problem == 8 ) :
        return "Pas de probleme"


def cameraman(image, points) :
    height, width = image.shape[:2]

    arrayPoints = list(points)
    arrayCoins = get_8_corners(image)
    center = [
        (int(height/2), int(width/2))
    ]

    if( len(points) > 3) :
        return 8

    if( len(points) == 3) :
        coin_a_virer = get_biggest_distance(center, arrayPoints)
        arrayPoints.pop(coin_a_virer)
        #print("wowee")
        return (cameraman(image, tuple(arrayPoints)))
    else :
        coin_lointain  = get_biggest_distance(arrayPoints, arrayCoins)
        return coin_lointain

    return -1