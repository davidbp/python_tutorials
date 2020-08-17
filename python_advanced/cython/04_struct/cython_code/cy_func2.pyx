from cymem.cymem cimport Pool
from libc.stdlib cimport rand

cdef struct Rectangle:
    float w
    float h

cdef int check_rectangles(Rectangle* rectangles, int n_rectangles, float threshold):
    cdef int n_out = 0
    cdef int i
    # C arrays contain no size information => we need to give it explicitly
    for rectangle in rectangles[0:n_rectangles]:
        if rectangle.w * rectangle.h > threshold:
            n_out += 1
    return n_out

cdef void fill_rectangles(Rectangle* rectangles, int n_rectangles):
    cdef int i
    for i in range(n_rectangles):
         rectangles[i].w = rand()
         rectangles[i].h = rand()


def verify_rectangles(N):
    cdef:
        int i
        int n_rectangles = N
        float threshold = 0.25
        Pool mem = Pool()
        Rectangle* rectangles = <Rectangle*>mem.alloc(n_rectangles, sizeof(Rectangle))

    # fill rectangles compiled version
    fill_rectangles(rectangles, N)

    n_out = check_rectangles(rectangles, n_rectangles, threshold)
    #print(n_out)
