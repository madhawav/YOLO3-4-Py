# distutils: language = "c++"

import numpy as np
import time

from libc.string cimport memcpy
from libc.stdlib cimport malloc

cdef class Image:
    cdef image img;

    def __cinit__(self, np.ndarray ary):
        # Code adapted from https://github.com/solivr/cython_opencvMat
        assert ary.ndim==3 and ary.shape[2]==3, "ASSERT::3channel RGB only!!"

        # Re-arrange to suite Darknet input format
        ary = ary.transpose(2, 0, 1)

        # RGB to BGR
        ary = ary[::-1,:,:]

        # 0..1 Range
        ary = ary/255.0

        # To c_array
        cdef np.ndarray[np.float32_t, ndim=3, mode ='c'] np_buff = np.ascontiguousarray(ary, dtype=np.float32)
        cdef int c = ary.shape[0]
        cdef int h = ary.shape[1]
        cdef int w = ary.shape[2]

        # Copy to Darknet image
        self.img.w = w
        self.img.h = h
        self.img.c = c
        self.img.data = <float*>malloc(h*w*c*4)
        memcpy(self.img.data, np_buff.data, h*w*c*4)

    def show_image(self, char* title):
        show_image(self.img, title)

    def __dealloc__(self):
        free_image(self.img)

cdef class Detector:
    cdef network* net
    cdef metadata meta
    cdef float average_internal_time

    def __cinit__(self, char* config, char* weights, int p, char* meta):
        self.net = load_network(config, weights, p)
        self.meta = get_metadata(meta)
        self.average_internal_time = 0

    def _get_average_time(self):
        # Used for efficiency measurements
        return self.average_internal_time

    # Code adapted from https://github.com/pjreddie/darknet/blob/master/python/darknet.py

    def classify(self, Image img):
        out = network_predict_image(self.net, img.img)
        res = []
        for i in range(self.meta.classes):
            res.append((self.meta.names[i], out[i]))
        res = sorted(res, key=lambda x: -x[1])
        return res

    def detect(self, Image image, float thresh=.5, float hier_thresh=.5, float nms=.45):
        cdef int num = 0
        cdef int* pnum = &num

        internal_start = time.time()
        network_predict_image(self.net, image.img)
        dets = get_network_boxes(self.net, image.img.w, image.img.h, thresh, hier_thresh, <int*>0, 0, pnum)

        num = pnum[0]
        if (nms > 0):
            do_nms_obj(dets, num, self.meta.classes, nms)

        internal_end = time.time()
        self.average_internal_time = self.average_internal_time * 0.8 + (internal_end-internal_start) * 0.2
        # print("Internal Time:",internal_end-internal_start, ":", self.average_internal_time)

        res = []
        for j in range(num):
            for i in range(self.meta.classes):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox
                    res.append((self.meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
        res = sorted(res, key=lambda x: -x[1])

        free_detections(dets, num)
        return res

    # End of adapted code block

    def __dealloc__(self):
        free_network(self.net)