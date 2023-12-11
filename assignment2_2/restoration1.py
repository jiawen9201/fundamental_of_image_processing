# SECV3213-02 FUNDAMENTAL OF IMAGE PROCESSING #
#            ASSIGNMENT 2 DATASET 6           #
# ------------------GROUP 9------------------ #
# 1. Gan Qi You    A21EC0178                  #
# 2. Lai Kai Chian A21EC0041                  #
# 3. Wai Jia Wen   A21EC0139                  #

import sys
import cv2 as cv
import numpy as np
import math

# Default values
BORDER_SIZE = 15
CAPTION_SIZE = 60

def restoration1(srcImage1, srcImage1Restored):
    # median blur to reduce salt & pepper noise, then treat this as the original image
    imgA_ori = cv.medianBlur(srcImage1,7)

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) # laplacian composite - for emphasizing edges while retaining detail at the same time
    # apply HPF lapacian composite to sharpen the image
    imgA_filtered = cv.filter2D(imgA_ori, -1, kernel)
    
    # get the high frequency details by subtracting the original image with sharpen image
    imgA_subtract = cv.subtract(imgA_filtered, imgA_ori)

    # adding the high frequency details (fine details, points, lines, and edges) back to the original image
    imgA_restored = cv.addWeighted(imgA_ori, 1.05, 3*imgA_subtract, -0.05, 0) # 64.31, 81.41, 65.87

    # Save image
    cv.imwrite(srcImage1Restored, imgA_restored)

    return imgA_restored

def processCommandLine():
    argc = len(sys.argv) - 1

    if argc < 2:
        print('\n** Error: need one image file as input and one output file path\n')
        print('Syntax (Bash and PowerShell): ./restoration1.py image1 image1OutputFilePath/image1Output')
        print(
            'Syntax (Command Prompt): restoration1.py image1 image1OutputFilePath/image1Output')

        print('\n  The first argument is the Noised Image and the second argument is the output file path is the file path to save the Restored Image. Must in order.')
        print('\nExample:  ./solutionq.py ref_image.jpg  Restored/restored_ref_image.jpg')
        sys.exit(1)
        return

    if argc == 2:
        _, file1, file2 = sys.argv
        return file1, file2

def display(image1, image2):
    height, width, channel = image1.shape

    border = np.ones((height, BORDER_SIZE, channel), np.uint8)*255
    caption = np.ones((CAPTION_SIZE, 2*width+BORDER_SIZE,channel), np.uint8)*255
    caption = cv.putText(caption, "Noise", (10, 20), cv.FONT_HERSHEY_SIMPLEX,
                         0.7, (0, 0, 0), 2, cv.LINE_AA)
    caption = cv.putText(caption, "Restored", (width+BORDER_SIZE+10, 20), cv.FONT_HERSHEY_SIMPLEX,
                         0.7, (0, 0, 0), 2, cv.LINE_AA)
    image = np.concatenate((image1, border, image2), axis=1)
    image = np.concatenate((image, caption), axis=0,)

    cv.imshow('Image Restoration', image)

def main():
    images = [None, None]
    files = [None, None]

    files[0], files[1] = processCommandLine()

    images[0] = cv.imread(files[0])

    images[1] = restoration1(images[0], files[1])

    display(images[0], images[1])

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
