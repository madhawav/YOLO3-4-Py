#include "bridge.h"

#if USE_CV == 1

#include <iostream>

#include <stdio.h>



#ifdef __cplusplus
extern "C" {
#endif
// Include darknet as a C Library
image ipl_to_image(IplImage* src);

#ifdef __cplusplus
}
#endif

using namespace cv;

image get_darknet_image(const Mat &input){
    // Darknet requires RGB order. Convert BGR to RGB.
    Mat flipped;
    cvtColor(input, flipped, CV_RGB2BGR);

    // Darknet uses IPL Image
    IplImage* iplImage;
    iplImage = cvCreateImage(cvSize(flipped.cols,flipped.rows),8,3);

    IplImage ipltemp=flipped;
    cvCopy(&ipltemp,iplImage);

    flipped.release();

    // Convert to Darknet Image
    image darknet_image = ipl_to_image(iplImage);

    // Free memory
    cvReleaseImage(&iplImage);
    return darknet_image;
}

#endif