#if USE_CV == 1
    #include <opencv2/opencv.hpp>
#endif

#if USE_GPU == 1
    // Set GPU tag so darknet.h is imported with GPU features
    #define GPU
    #include <cuda_runtime.h>
#endif

#ifdef __cplusplus
extern "C" {
#endif
// Types and methods included from darknet.h
// We cannot directly import darknet.h since it links to C++ header files from CUDA.
// The above happens because __cplusplus flag stays active within the extern "C" block.
struct network;
typedef struct network network;

typedef struct{
    float x, y, w, h;
} box;

typedef struct detection{
    box bbox;
    int classes;
    float *prob;
    float *mask;
    float objectness;
    int sort_class;
} detection;

typedef struct{
    int classes;
    char **names;
} metadata;

typedef struct {
    int w;
    int h;
    int c;
    float *data;
} image;

// Re-definition of methods imported from darknet
float *network_predict_image(network *net, image im);
network *load_network(char *cfg, char *weights, int clear);
metadata get_metadata(char *file);
void free_network(network *net);
void free_detections(detection *dets, int n);
void do_nms_obj(detection *dets, int total, int classes, float thresh);
int show_image(image p, const char *name, int ms);
void free_image(image m);
detection *get_network_boxes(network *net, int w, int h, float thresh, float hier, int *map, int relative, int *num);

#if USE_GPU == 1
    void cuda_set_device(int n);
#endif

#ifdef __cplusplus
}
#endif


#if USE_CV == 1
    using namespace cv;
    image get_darknet_image(const Mat &input);
#endif