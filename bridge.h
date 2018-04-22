#if USE_CV == 1
    #include <opencv2/opencv.hpp>
#endif

#ifdef __cplusplus
extern "C" {
#endif
// Include darknet as a C Library
#include <darknet.h>
#include <image.h>

#ifdef __cplusplus
}
#endif


#if USE_CV == 1
    using namespace cv;
    image get_darknet_image(const Mat &input);
#endif