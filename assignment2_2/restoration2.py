# SECV3213-02 FUNDAMENTAL OF IMAGE PROCESSING #
#            ASSIGNMENT 2 DATASET 6           #
# ------------------GROUP 9------------------ #
# 1. Gan Qi You    A21EC0178                  #
# 2. Lai Kai Chian A21EC0041                  #
# 3. Wai Jia Wen   A21EC0139                  #

import sys
import cv2 as cv
import numpy as np

# Default values
BORDER_SIZE = 15
CAPTION_SIZE = 50

def restoration2(srcImage1, srcImage1Restored):
    # median blur to reduce salt & pepper noise, then treat this as the original image
    imgA_ori = cv.medianBlur(srcImage1,7)

    # reduce the amount of noise present in the image
    imgA_blurred = cv.blur(imgA_ori, (7,7))
    
    # keep the fine details in the image and preserve low frequency components
    imgA_subtract = cv.subtract(imgA_blurred, imgA_ori)

    # adding the fine details back to the original image
    imgA_add = cv.addWeighted(imgA_ori, 0.75, imgA_subtract, 0.25, 0)

    kernel1 = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]) # laplacian - for emphasizing edges
    # apply HPF lapacian to get the enhanced edges of the image
    imgA_emphasize_edge = cv.filter2D(imgA_ori, -1, kernel1)

    # adding the enhanced edges back to the image with added fine details from previous addition
    imgA_restored = cv.addWeighted(imgA_add, 1.4, imgA_emphasize_edge, -0.4, 0) # 64.6, 80.97, 66.3

    # Save image
    cv.imwrite(srcImage1Restored, imgA_restored)

    return imgA_restored

def processCommandLine():
    argc = len(sys.argv) - 1

    if argc < 2:
        print('\n** Error: need one image file as input and one output file path\n')
        print('Syntax (Bash and PowerShell): ./restoration2.py image1 image1OutputFilePath/image1Output')
        print(
            'Syntax (Command Prompt): restoration2.py image1 image1OutputFilePath/image1Output')

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

    images[1] = restoration2(images[0], files[1])

    display(images[0], images[1])

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
