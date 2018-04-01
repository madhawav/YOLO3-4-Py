import numpy as np

from libc.string cimport memcpy

cdef class Image:
    cdef image img;

    def __cinit__(self, np.ndarray ary):
        assert ary.ndim==3 and ary.shape[2]==3, "ASSERT::3channel RGB only!!"

        cdef np.ndarray[np.uint8_t, ndim=3, mode ='c'] np_buff = np.ascontiguousarray(ary, dtype=np.uint8)
        cdef unsigned int* im_buff = <unsigned int*> np_buff.data
        cdef int r = ary.shape[0]
        cdef int c = ary.shape[1]
        cdef Mat m

        cdef int a = CV_8UC3
        # print(a)

        m.create(r, c, a)
        memcpy(m.data, im_buff, r*c*3)
        m.deallocate()

        self.img = get_darknet_image(m)

    def show_image(self, char* title):
        show_image(self.img, title)

    def __dealloc__(self):
        free_image(self.img)

cdef class Detector:
    cdef network* net
    cdef metadata meta

    def __cinit__(self, char* config, char* weights, int p, char* meta):
        self.net = load_network(config, weights, p)
        self.meta = get_metadata(meta)

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
        network_predict_image(self.net, image.img)
        dets = get_network_boxes(self.net, image.img.w, image.img.h, thresh, hier_thresh, <int*>0, 0, pnum)

        num = pnum[0]
        if (nms > 0):
            do_nms_obj(dets, num, self.meta.classes, nms)

        res = []
        for j in range(num):
            for i in range(self.meta.classes):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox
                    res.append((self.meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
        res = sorted(res, key=lambda x: -x[1])

        free_detections(dets, num)
        return res

    def __dealloc__(self):
        free_network(self.net)