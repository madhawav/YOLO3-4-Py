# distutils: language = "c++"

import numpy as np
cimport numpy as np

cdef extern from "bridge.h":
    cdef int CV_8UC3

    cdef cppclass Mat:
        Mat() except +
        void create(int, int, int)
        void* data
        int rows
        int cols
        int channels()
        void deallocate()
        void release()

    ctypedef struct box:
        float x, y, w, h

    ctypedef struct detection:
        box bbox
        int classes
        float *prob
        float *mask
        float objectness
        int sort_class

    cdef struct network:
        pass

    ctypedef struct metadata:
        int classes
        char** names

    ctypedef struct image:
        int w
        int h
        int c
        float *data

    float *network_predict_image(network *net, image im)

    int getCV_8UC3()
    image get_darknet_image(const Mat &input)

    network* load_network(char* config, char* weights, int p)

    metadata get_metadata(char *file)

    void free_network(network* net)

    void free_detections(detection *dets, int n)

    void do_nms_obj(detection *dets, int total, int classes, float thresh)

    void show_image(image img, char* title, int ms)
    void free_image(image img)

    detection *get_network_boxes(network *net, int w, int h, float thresh, float hier, int *map, int relative, int *num)

    IF USE_GPU == 1:
        void cuda_set_device(int n)
