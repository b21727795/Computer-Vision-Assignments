import os
import cv2 as cv
from matplotlib import pyplot as plt
#from google.colab.patches import cv2_imshow as cv_imshow

def show_filter_results(img_path):
    """
    This function takes any image as input and returns that image's edge information as  image's
    of three different method.
    
    """

    example_image = cv.imread(img_path,1) #1 means read as rgb
    example_image = cv.GaussianBlur(example_image, (3, 3), 0) # I applied gaussian blur for reduce to noise
    example_image_gray = cv.cvtColor(example_image, cv.COLOR_BGR2GRAY) #Converted to grayscale image

    #canny edge detection
    example_image_canny = cv.Canny(example_image_gray,100,200)

    #sobel filter
    example_image_vertical = cv.Sobel(example_image_gray, cv.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv.BORDER_DEFAULT)  #(1,0) GRADYAN X-VERTICAL    
    example_image_horizontal = cv.Sobel(example_image_gray, cv.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv.BORDER_DEFAULT) #(0,1) GRADYAN Y-HORIZONTAL

    #laplacian filter
    example_image_laplacian = cv.Laplacian(example_image_gray,cv.CV_64F)

    #plot part
    plt.subplot(221),plt.imshow(example_image_canny,cmap = 'gray')
    plt.title('Canny Edge Detection'), plt.xticks([]), plt.yticks([])

    plt.subplot(222),plt.imshow(example_image_laplacian,cmap = 'gray')
    plt.title('Laplacian Filter'), plt.xticks([]), plt.yticks([])

    plt.subplot(223),plt.imshow(example_image_vertical, 'gray')
    plt.title('Sobel Filter - Vertical Edges'), plt.xticks([]), plt.yticks([])

    plt.subplot(224),plt.imshow(example_image_horizontal,cmap = 'gray')
    plt.title('Sobel Filter - Horizontal Edges'), plt.xticks([]), plt.yticks([])

    plt.show()

def canny_edge_parameter_selection(read_img_path,  write_image_path):
    """
    read_img_path: images/*.png
    write_img_path: current directory path 'os.getcwd()'
    """
    if 'Parameter_Images' not in os.listdir(write_image_path):
        os.mkdir(os.path.join(write_image_path,'Parameter_Images'))
    
    write_image_path = os.path.join(write_image_path,'Parameter_Images')
    
    example_image = cv.imread(read_img_path,1) #1 means read as rgb
    
    example_image = cv.GaussianBlur(example_image, (3, 3), 0) # I applied gaussian blur for reduce to noise
    example_image_gray = cv.cvtColor(example_image, cv.COLOR_BGR2GRAY) #Converted to grayscale image

    #canny edge detection
    #default parameters for min value = 100 max value = 200
    #let's try to find better parameters
    parameter_list = [50,75,100,125,150,175,200]
    
    for i in (parameter_list):  
        for j in (parameter_list):
            if (i != j and i < j):
                example_image_canny = cv.Canny(example_image_gray,i,j)
                cv.imwrite(os.path.join(write_image_path,'example_image_min{}_max{}.png'.format(i,j)),example_image_canny)

def canny_edge_detection(img_path):
    """
    It takes image as input,returns canny edge maps
    """
    example_image = cv.imread(img_path,1) #1 means read as rgb
    example_image = cv.GaussianBlur(example_image, (3,3), 0) # I applied gaussian blur for reduce to noise
    example_image_gray = cv.cvtColor(example_image, cv.COLOR_BGR2GRAY) #Converted to grayscale image

    #canny edge detection
    example_image_canny = cv.Canny(example_image_gray,125,200) #choosen parameters

    return example_image_canny

def canny_edge_detection_on_10_dif_images(images_folder):
    """
    It takes car images folder as an input,then return edge maps of ten of them.
    """
    fig = plt.figure(figsize=(2, 7)) #Create template for all images 
    
    rows = 3 #I showed them 2 row 5 column,may be I change it depends report page
    columns = 3
    
    image_count = 0
    for img_path in os.listdir(images_folder):
        if (image_count < 10): #total 10 images
            img = canny_edge_detection(os.path.join(images_folder,img_path))
            fig.add_subplot(rows, columns, image_count + 1) 
  
           
            plt.imshow(img,cmap = 'gray') #represent in grayscale
            plt.axis('off') 
            plt.title("Edge Image - {}".format(image_count + 1)) 
  
        image_count += 1



