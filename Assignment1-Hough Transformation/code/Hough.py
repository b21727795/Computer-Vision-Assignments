from utils import *
import numpy as np
import cv2 as cv
import math
import itertools
from sympy import Point, Line, Segment
import sys
import xml.etree.ElementTree as ET

#Read an image then returns Canny edge maps

def Hough_Transform(image_path,min_theta,max_theta,threshold):
    """
    In my case min theta is -90, max theta is +90
    It can be try as 0 to 180,it is up to you
    If you change 0 to 180 you should uptade accumulator[ro][theta+90] with proper indexes
    
    """
    original_image = cv.imread(image_path,1)
    edge_image = canny_edge_detection(image_path) #it return canny edge maps
    
    thetas_range = [x for x in range(min_theta,max_theta,1)] #-90 to +90
    
    max_ro = int (math.hypot(edge_image.shape[0], edge_image.shape[1])) #  find maximum range of ro value, it is diagonal lenght from origin to polar edge
    ro_range = [x for x in range(-1 * max_ro, max_ro +1 , 1)] #ro range is [-max_ro to +max_ro]

    accumulator = [[0 for i in range(len(thetas_range)+1)] for j in range((len(ro_range)) + 1)] #accumulator (row = ro range,column = theta range)
    
    
    
    for x in range(edge_image.shape[0]):
        for y in range(edge_image.shape[1]):
            if (edge_image[x,y] == 255): #255 means edge pixel
                for theta in range(len(thetas_range)): #np.cos function need radyan so i convert them to radyan
                    
                    theta -= 90
                    ro = int((y * np.cos((np.pi/180) * theta) ) + (x * np.sin((np.pi/180) * theta))) + max_ro 
                    
                    #actually y means x, x means y , image coordinat and cartesian coordinat are different
                    #we need use radyan, for calculations 1 radyan * theta,e.g. 1 radyan * 30 is equal cos(30) or sin(30) 
                    #tested and find negative value for d so I added diagonal length(max_ro) to formula 
                    
                    
                    try:
                        accumulator[ro][theta+90] += 1
                    except IndexError:
                        print('Boundary issue ro:{} theta:{} '.format(str(ro),str(theta)))

    #local maxima ,most most most most important part
    #Firstly i did not use np matrix but I need now so, I converted to np aray
    accumulator = np.array(accumulator)
    
    kernel = 13
    lines = list()
    
    for row_index in range(accumulator.shape[0] -(kernel-1)):
        for column_index in range(accumulator.shape[1] -(kernel-1)):
            kernel_slice = accumulator[row_index:row_index+kernel,column_index:column_index+kernel]
            
            
            local_maxima = np.where(kernel_slice == np.amax(kernel_slice))
            #local_maxima = (int(sum(local_maximas[0])/len(local_maximas[0])), int(sum(local_maximas[1])/len(local_maximas[1])))
            if(local_maxima[1][0]+column_index == 90):
                if(accumulator[local_maxima[0][0]+row_index][local_maxima[1][0]+column_index] >= threshold/3):
                    #print(accumulator[local_maxima[0][0]+row_index][local_maxima[1][0]+column_index])
                    line = (local_maxima[0][0]+row_index,local_maxima[1][0]+column_index)
                    lines.append(line)
            
            if (accumulator[local_maxima[0][0]+row_index][local_maxima[1][0]+column_index]>= threshold):

                line = (local_maxima[0][0]+row_index,local_maxima[1][0]+column_index)
                lines.append(line)
    
    
    
    
    return accumulator, list(set(lines)), thetas_range, ro_range,max_ro
def find_x_y_coordinat(line, ro_range, thetas_range):
    x = line[0]
    y = line[1] 
    #y = thetas, 90 vertical,0-180 horizontal
    #x,y = 567,19
    ro = ro_range[x] 
    theta = thetas_range[y]
    
    #print(x,y,ro,theta)
    a = np.cos(theta * np.pi/180)
    b = np.sin(theta * np.pi/180)
    
    x0 = a * ro
    y0 = b * ro
    x1 = int(round(x0 + 1000 * (-b)))
    y1 = int(round(y0 + 1000 * (a)))
    x2 = int(round(x0 - 1000 * (-b)))
    y2 = int(round(y0 - 1000 * (a)))
    return x1,y1,x2,y2
def calculate_IOU(predicted,original_image,annotation_path):
    

    tree = ET.parse(annotation_path)
    root = tree.getroot()

   
    p_x1,p_y1,p_x2,p_y2 = int(predicted[0][0][0]),int(predicted[1][0][1]),int(predicted[1][0][0]) ,int(predicted[0][0][1])
    g_x1,g_y1,g_x2,g_y2 = int ((root[4][5][0].text)),int ((root[4][5][3].text)),int ((root[4][5][2].text)),int ((root[4][5][1].text))

    img = cv.rectangle(original_image, (p_x1,p_y1), (p_x2,p_y2), (255,0,0), 2)
    img =cv.rectangle(img, (g_x1,g_y1), (g_x2,g_y2), (0,255,0), 2)        
    
    x_i_1 = max(p_x1,g_x1)
    y_i_1 = max(p_y1,g_y1)
    x_i_2 = max(p_x2,g_x2)
    y_i_2 = max(p_y2,g_y2)
    
    intersection_width = abs(x_i_2 - x_i_1)
    intersection_height = abs(y_i_2 - y_i_1)
    intersection_area = abs(max(intersection_height,0) * max(intersection_width,0)) 
  
    p_area = abs((p_x2 -  p_x1) * (p_y2 -  p_y1))
    g_area = abs((g_x2 - g_x1) * (g_y2 - g_y1))
    union_area = g_area + p_area - intersection_area #a birlesim b - a kesisim b
    
    iou = intersection_area / float(union_area)
    
    return (img,iou)


def draw_and_detect(original_image,lines,ro_range,thetas_range,annotation_path):
    
    horizontal_lines = list()
    vertical_lines = list()

    for line in lines:
        
        x,y = line[0],line[1]
        x1,y1,x2,y2 = find_x_y_coordinat(line,ro_range,thetas_range)
        
        p1,p2 = Point(x1,y1),Point(x2,y2)
        line = Line(p1, p2)
        if (y == 90):           
            vertical_lines.append(line)
        elif (y<=15 or y>=165):
            horizontal_lines.append(line)
    
    print('Number of Vertical Lines: {}'.format(len(vertical_lines)))
    print('Number of Horizontal Lines: {}'.format(len(horizontal_lines)))
    if(len(vertical_lines) <2 or len(horizontal_lines)  <2):
        print('There is not enough found line')
        return -1
    
    rectangles = list()
    detected_part = [-1000000000,None]
    for line1, line2 in itertools.combinations(vertical_lines, 2):
        
        if(line1.p1[0] > line2.p2[0]):
            temp = line1
            line1= line2
            line2= temp
            #aim is line1 is left part
        
        for line3,line4 in itertools.combinations(horizontal_lines, 2):
            
            if(max(line3.p1[1],line3.p2[1]) < max(line4.p1[1],line4.p2[1])):
                temp = line3
                line3= line4
                line4 = temp
            
            
            inters_1 = line1.intersection(line3)
            inters_2 = line1.intersection(line4)
            
            left_top = inters_1
            #left_top = inters_2 if inters_2[0][0]>inters_1[0][0] else inters_1

            inters_3 = line2.intersection(line3)
            inters_4 = line2.intersection(line4)
            
            right_bottom = inters_4
            #right_bottom = inters_4 if inters_4[0][1]>inters_3[0][1] else inters_3
            
            
            
            tall_edge = abs(right_bottom[0][0]-left_top[0][0])
            short_edge = abs(left_top[0][1]-right_bottom[0][1])
            
            area =int(tall_edge * short_edge)
            is_rect = (tall_edge) / (short_edge)
            
            
            if(area<=13000 and area >=6500):#9500 average#area<=13000 and area >=6500
                #print('alana girdi')
                if(is_rect >= 3.5 and is_rect <=6):#is_rect >= 3.5 and is_rect <=6
                    #print('boyut tamam')
                    diag_length = math.hypot(((tall_edge/2)+left_top[0][0]),(short_edge/2)+right_bottom[0][1])
                    

                    if(diag_length>detected_part[0]):
                        detected_part[0] = diag_length
                        detected_part[1] = (left_top,right_bottom)
                    #(left_top[0][0],left_top[0][1]),(right_bottom[0][0],right_bottom[0][1])                
    
    
    
    if(detected_part[1] == None):
        print("It couldn't find any plate")
        
        return -1
    return calculate_IOU(detected_part[1],original_image,annotation_path)
            
            #constraint
def all_images_evaluate(Images_Folder,Annotation_Folder,threshold):
    sample = 0
    sum_acc = 0
    if 'Results_detected' not in os.listdir(os.getcwd()):
        os.mkdir('Results_detected')
    if 'Results_undetected' not in os.listdir(os.getcwd()):
        os.mkdir('Results_undetected')
    for i in range(0,151):#we have images 0-150
        car_name = 'Cars'
        print('Detection Start for Car{}'.format(str(i)))
        image_path = os.path.join(Images_Folder,car_name + str(i) +'.png')
        annot_path = os.path.join(Annotation_Folder,car_name + str(i) +'.xml')
        original_image = cv.imread(image_path,1)
        accumulator, lines, thetas_range, ro_range,max_ro = Hough_Transform(image_path,-90, 90,threshold)
        result = draw_and_detect(original_image,lines,ro_range,thetas_range,annot_path)
        if(result == -1):
            sample+=1
            cv.imwrite('Results_undetected/result{}.png'.format(i),original_image)
            print('Accuracy : 0')
            continue
        #cv.imshow(result[0]) I used colab, I didnt try on other systems you may use this on diff systems
        
        sum_acc += result[1]
        cv.imwrite('Results_detected/result{}.png'.format(i),result[0])
        print('Accuracy : {}'.format(str(result[1])))
        sample+=1
    print('All accuracy : {}'.format(str(summ_acc/sample)))   
  