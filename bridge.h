#include <opencv2/opencv.hpp>

#ifdef __cplusplus
extern "C" {
#endif
// Include darknet as a C Library
#include <darknet.h>
#include <image.h>

#ifdef __cplusplus
}
#endif


using namespace cv;
image get_darknet_image(const Mat &input);