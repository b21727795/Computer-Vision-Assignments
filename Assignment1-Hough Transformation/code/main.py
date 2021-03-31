import sys
from Hough import*

def main(image_path,annotation_path,threshold,is_all,Images_Folder,Annotation_Folder):
    
    if(is_all == '0'):
        original_image = cv.imread(image_path,1)
        accumulator, lines, thetas_range, ro_range,max_ro = Hough_Transform(image_path,-90, 90,threshold)
        draw_and_detect(original_image,lines,ro_range,thetas_range,annotation_path)
    elif(is_all == '1'):
       
        all_images_evaluate(Images_Folder,Annotation_Folder,threshold)    
    
if  __name__ == '__main__':
    image_path = sys.argv[1]
    annotation_path = sys.argv[2]
    threshold = int(sys.argv[3])
    is_all = sys.argv[4]
    Images_Folder = sys.argv[5]
    Annotation_Folder = sys.argv[6]
    main(image_path,annotation_path,threshold,is_all,Images_Folder,Annotation_Folder)