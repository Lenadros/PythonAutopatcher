# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 10:36:15 2015

@author: brianl
"""



# this module provides code to identify cell bodies in IR-DIC Images
# 

# in its current format, it's a collection of functions with the highest level function
# 'combine_features' intended to be called from the command line or console or whatever.  

#  CRITICAL NOTES:
#     the 'celldiameter' input should be roughly the diameter of the largest cell, but will likely require tuning for
#     a particular dataset. 

#     the current code has had zero optimization.  there are probably lots of ways to improve the speed, but currently the 
#     biggest offender is the large number of calls to cv2.matchTemplate

# import what I need
import numpy as np
import cv2
import matplotlib.pyplot as plt




# currently hard-coded parameters that may need to be determined algorithmically at seme point:

TEXTURE_SMALL = 0.2
TEXTURE_LARGE = 0.9
OTSU_MULTIPLIER = 1.1


FINAL_BLUR = 9   # pixel size dependent


MIN_TEMPLATE = 0.5   # in units of cell radius
MAX_TEMPLATE = 1.5 # in units of cell radius
TEMPLATE_SIDE  = 1.25*MAX_TEMPLATE  # times cell diameter  

N_RADII = 9
N_ANGLES = 5



Z_TO_16_WIDTH = 2**12 # parameters for converting z score (ish) to 16bit image  could likely be done in 8 bits if the normalization is done carefully
Z_TO_16_MID  = 2**15
Z_TO_16_MAX = 2**16-5
def combine_features(img, celldiameter, angle_deg, shear_blur=3, showstuff = False):
    
# derive some intermediate parameters for the individual features:

    dirIntAngle = angle_deg+180    
    textureSmall = np.int(TEXTURE_SMALL*celldiameter)
    textureBig =   np.int(TEXTURE_LARGE*celldiameter)
    template_out = feat_template(img , celldiameter , angle_deg , np.int(shear_blur) )
    dirInt_out = feat_dirInt(img, dirIntAngle)
    texture_out = feat_texture(img,textureBig, textureSmall )
    
# z score for each and spread out over 16 bits
    template_z16 = zscore16UINT(template_out)
    dirInt_z16 = zscore16UINT(dirInt_out)
    texture_z16 = zscore16UINT(texture_out)
    tr, tc= np.shape(template_z16)
    dr, dc= np.shape(dirInt_z16)
    txr, txc =  np.shape(texture_z16)
    print np.min(template_z16)
    print np.max(template_z16)
    print np.min(dirInt_z16)
    print np.max(dirInt_z16)
    print np.min(texture_z16)
    print np.max(texture_z16)
    featureSum = template_z16/3+ dirInt_z16/3 + texture_z16/3
    print np.min(featureSum)
    print np.max(featureSum)
    featureSum8 = np.uint8(cv2.GaussianBlur(featureSum,(FINAL_BLUR,FINAL_BLUR),0)/256)
    thresholdVal, thresholdImg = cv2.threshold(featureSum8, 0,255, cv2.THRESH_TOZERO+ cv2.THRESH_OTSU)
    val2, thresholdImg = cv2.threshold(featureSum8,thresholdVal*OTSU_MULTIPLIER, 255, cv2.THRESH_TOZERO) 
    if showstuff:
        plt.figure(1)
        ax = plt.subplot(2,3,1); ax.imshow(img, cmap = 'gray'); ax.set_title('original image')
        ax = plt.subplot(2,3,4); ax.imshow(template_z16, cmap='gray'); ax.set_title('template matching')
        ax = plt.subplot(2,3,5); ax.imshow(dirInt_z16, cmap = 'gray'); ax.set_title('directional integration')
        ax = plt.subplot(2,3,6); ax.imshow(texture_z16, cmap = 'gray'); ax.set_title('texture filtering')
        ax = plt.subplot(2,3,2); ax.imshow(featureSum8, cmap = 'gray'); ax.set_title('combined feature map')
        ax = plt.subplot(2,3,3); ax.imshow(thresholdImg, cmap = 'gray'); ax.set_title('thresholded feature map')
    
    # now calculate a threshold for segmentation.  empirically, a modified otsu's method threshold works reasonably well
        
        
    return featureSum
    
    
    
def feat_template(img, celldiameter, angle_deg, blur_width):
    print 'feat_template'    
    side = np.ceil(celldiameter*TEMPLATE_SIDE)
    halfside = np.int(side/2)
    bordertype = cv2.BORDER_REFLECT #just to avoid line breakup in PDF file
    img = cv2.copyMakeBorder(img, halfside, halfside , halfside , halfside ,bordertype)
    img = np.float32(img)
    # call external function to generate filterbank
    rlist = np.linspace(np.floor(MIN_TEMPLATE*celldiameter/2.),np.ceil(MAX_TEMPLATE*celldiameter/2.),N_RADII)
    alist =np.linspace(angle_deg-4, angle_deg+4, N_ANGLES)

    filterbank = gen_filterbank(rlist, alist ,blur_width, side)

    # do template matching on these one at a time
    fbrows, fbcols, f1, f2 = np.shape(filterbank)
    first = True
    for i in range(fbrows):
        for j in range(fbcols):
            featureOut = cv2.matchTemplate(img,np.float32(filterbank[i][j]), cv2.TM_CCOEFF_NORMED)
            if first:
                maxFeature = featureOut
                first = False
            else:
                maxFeature = np.max(np.dstack((maxFeature,featureOut)),axis = 2)

                
    # use argmax to combine into single feature
                maxFeature[maxFeature<0]=0
    return maxFeature


    
def feat_dirInt(img, angle_deg, showstuff = False):
    print 'feat_dirInt'
    radangle = deg2rad(angle_deg)
    # convert to float and make image zero mean
    img = np.float32(img)
    img = img-img.mean()
    # pad for optimal FFT speed
    rows,cols = img.shape

    nrows = cv2.getOptimalDFTSize(rows)
    ncols = cv2.getOptimalDFTSize(cols)
    right = ncols - cols
    bottom = nrows - rows
    bordertype = cv2.BORDER_CONSTANT #just to avoid line breakup in PDF file
    img = cv2.copyMakeBorder(img,0,bottom,0,right,bordertype, value = 0)
            
    # do FFT on image
    dft = cv2.dft(img, flags=cv2.DFT_COMPLEX_OUTPUT)



    # generate frequency grid:  
    originColShift = ncols/2
    originRowShift = nrows/2
    colFrac = 1.*ncols
    rowFrac = 1.*nrows
    
    wy, wx = np.float32(np.mgrid[0:nrows,0:ncols]);
    wy = np.flipud(wy)
    wx = wx-originColShift
    wx = wx/colFrac
    wx = np.fft.fftshift(wx)    
    wy = wy-originRowShift
    wy = wy/rowFrac
    wy = np.fft.fftshift(wy)
    # before we can do the integral, we need to make openCV happy about types:
   
    # figure out the tilted frequency grid
    wAngleY =  (np.sin(radangle)*wx+np.cos(radangle)*wy);
    
    # and the factor that does the integral:
    fftintegrate =  (wAngleY) / (wx**2+wy**2+np.spacing(1))#
    txOut = dft
    txOut[:,:,0] = dft[:,:,0]*fftintegrate
    txOut[:,:,1] = dft[:,:,1]*fftintegrate
    # the next two lines are equivalent to multiplying by -i 
    txOut = txOut[:,:,::-1] 
    txOut[:,:,1] = -txOut[:,:,1] 
        
    # back transform FFT

    outputC = cv2.idft(txOut)#(txOutshift)
    output =outputC[0:rows,0:cols,0]#cv2.magnitude(outputC[:,:,0], outputC[:,:,1])
    if showstuff:
        plt.figure()
        plt.subplot(1,3,1)
        plt.imshow(img, cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(1,3,3)
        plt.imshow(output, cmap = 'gray'   )
        plt.title('Output Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(1,3,2)
        plt.imshow((np.fft.fftshift(fftintegrate)))        
        plt.title('FFT integration mask')        
        plt.show()    
    output = output- cv2.GaussianBlur(output, (2*(cols/8)+1, 2*(cols/8)+1),0)
    return  output   
    # normalize if needed

def feat_texture(img, window_big, window_small, showstuff = False):
    print 'feat_texture'

    img = np.float32(img)
    a2 = img*img
    avbig = cv2.blur(img,(window_big,window_big))
    av2big = avbig*avbig
    ava2big = cv2.blur(a2,(window_big,window_big))
    
    avsmall = cv2.blur(img,(window_small,window_small))
    av2small = avsmall*avsmall
    ava2small = cv2.blur(a2,(window_small,window_small))
    stdbig = (ava2big-av2big)**.5 
    stdsmall = (ava2small-av2small)**.5
    output = stdbig-stdsmall
    if showstuff:
        plt.figure()
        plt.subplot(2,2,1)
        plt.imshow(img, cmap = 'gray')
        plt.title('Input Image')
        plt.subplot(2,2,2)
        plt.imshow(output, cmap = 'gray')
        plt.title('Output Image')
        plt.subplot(2,2,3)
        plt.imshow(stdbig, cmap = 'gray')
        plt.title('big window variance image')
        plt.subplot(2,2,4)
        plt.imshow(stdsmall, cmap = 'gray')
        plt.title('small window variance image')
        plt.show()
        
    return output
#        
    


    # I could either
    #rewrite the original neighborhood operation

    # OR
    # try to use the fast way to estimate variance in different window sizes

#def combine_features(f1image, f2image, f3image):
    #  this function will import the three feature images and 
    # combine them into a single cell_map 
    # naive version will just normalize each image and do some linear combination
    # 
    # maybe more advance version will take the results of  LDA ...

# helper functions below... many likely available somewhere else!
def deg2rad(degrees):
    radians = np.pi*degrees/180.    
    return radians
    
    
    
def rad2deg(radians):
    degrees = 180*radians/np.pi    
    return degrees
    
#def texture_operation(argument):
    #not sure what form the argument should be... 
    # original was average of  absolute value from the mean 
def gen_filterbank(radii, angle_degs, blur_width, template_side):
    print 'gen_filterbank'    
    n_angles = len(angle_degs)
    n_radii = len(radii)
    filterbank = [[0 for x in range(n_angles)] for x in range(n_radii)]
    anumber  = 0
    rnumber = 0
    # for a range of radii and angles, define kernels 
    for angle in angle_degs:
        for r in radii:
            fbar = circlemask(r,angle,template_side, blur_width = blur_width)
            fbar = fbar-np.mean(fbar)
            filterbank[rnumber][anumber] = fbar
            rnumber = rnumber+1
        anumber = anumber+1
        rnumber= 0
    return filterbank
          
def circlemask(radius, angle_deg, template_side, blur_width=1):
    # the radius should be smaller than half the template side
    # this is checked here, but will be handled more rigorously outside
    # this function    
    template_halfside = np.max([np.float(template_side)/2., np.float(radius)])        
    # make mask square with odd number of elements on a side
    xgrid, ygrid = np.meshgrid(np.arange(-np.floor(template_halfside),np.floor(template_halfside)+1), np.arange(-np.floor(template_halfside),np.floor(template_halfside)+1))
    disk = (np.sqrt(xgrid**2+ygrid**2) < (radius)) 
    #blur the disk
    blurred = cv2.blur(np.float32(disk), (blur_width,blur_width))
    single_mask = dirDerivative(blurred, angle_deg,blur_width=blur_width)
    return single_mask      
    
def dirDerivative(img, angle_deg,blur_width=1):

    radangle = deg2rad(angle_deg)
    # convert to float and make image zero mean
    img = np.float32(img)
    # pad for optimal FFT speed
    rows,cols = img.shape

    nrows = cv2.getOptimalDFTSize(rows)+16
    ncols = cv2.getOptimalDFTSize(cols)+16
    right = (ncols - cols )/2
    bottom = (nrows - rows)/2
    bordertype = cv2.BORDER_CONSTANT 
    img = cv2.copyMakeBorder(img,bottom,bottom,right,right,bordertype, value = 0.)
            
    # do FFT on image
    dft = cv2.dft(img, flags=cv2.DFT_COMPLEX_OUTPUT)

    # generate frequency grid:  
    originColShift = ncols/2
    originRowShift = nrows/2
    colFrac = 1.*ncols
    rowFrac = 1.*nrows
    arows,acols = img.shape
    wy, wx = np.float32(np.mgrid[0:arows,0:acols]);
    wy = np.flipud(wy)
    wx = wx-originColShift
    wx = wx/colFrac
    wx = np.fft.fftshift(wx)    
    wy = wy-originRowShift
    wy = wy/rowFrac
    wy = np.fft.fftshift(wy)
    # before we can do the integral, we need to make openCV happy about types:
   
    # figure out the tilted frequency grid
    wAngleY =  (np.sin(radangle)*wx+np.cos(radangle)*wy);
    
    # this is the factor that does the derivative
    fftDerivative =  (wAngleY)
    txOut = dft
    txOut[:,:,0] = dft[:,:,0]*fftDerivative
    txOut[:,:,1] = dft[:,:,1]*fftDerivative
    # the next two lines are equivalent to multiplying by -i 
    txOut = txOut[:,:,::-1] 
    txOut[:,:,1] = -txOut[:,:,1] 
        
    # back transform FFT

    outputC = cv2.idft(txOut)#(txOutshift)
    output =outputC[:,:,0]#cv2.magnitude(outputC[:,:,0], outputC[:,:,1])
       

    return  cv2.blur(output[bottom:-bottom, right:-right], (blur_width,blur_width))    
    # normalize if needed

def zscore16UINT(img):
    img = np.float32(img)
    ostd = np.std(img)
    img = img-np.mean(img)
    img = img/ostd
    img = (img*Z_TO_16_WIDTH+Z_TO_16_MID)  # 

    img[img>(Z_TO_16_MAX)]=Z_TO_16_MAX
    img[img<0]=0
    img = np.uint16(img)

    return img