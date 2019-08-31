#------------------------------------------------------------------------------+
#
#   Nathan A. Rooy
#   Create a three color triangle
#   2017-DEC
#
#------------------------------------------------------------------------------+

#--- IMPORT DEPENDENCIES ------------------------------------------------------+

from __future__ import division
from math import sin
from math import radians

#--- MAIN ---------------------------------------------------------------------+

def calc_dist(x0, y0, x1, y1):
    return ((x0 - x1)**2 + (y0 - y1)**2)**0.5

def clamp(x): 
  return max(0, min(int(round(x,0)), 255))

def interpolate_color(color_info, x, y):
    c1_dist = calc_dist(color_info['c1_x'], color_info['c1_y'], x, y)
    c2_dist = calc_dist(color_info['c2_x'], color_info['c2_y'], x, y)
    c3_dist = calc_dist(color_info['c3_x'], color_info['c3_y'], x, y)

    dist_total = c1_dist + c2_dist + c3_dist

    c1_norm = 1 - (c1_dist / color_info['max dist'])
    c2_norm = 1 - (c2_dist / color_info['max dist'])
    c3_norm = 1 - (c3_dist / color_info['max dist'])

    new_r = (c1_norm * color_info['c1'][0]) + (c2_norm * color_info['c2'][0]) + (c3_norm * color_info['c3'][0])
    new_g = (c1_norm * color_info['c1'][1]) + (c2_norm * color_info['c2'][1]) + (c3_norm * color_info['c3'][1])
    new_b = (c1_norm * color_info['c1'][2]) + (c2_norm * color_info['c2'][2]) + (c3_norm * color_info['c3'][2])

    new_color_hex = "#{0:02x}{1:02x}{2:02x}".format(clamp(new_r), clamp(new_g), clamp(new_b))
    return new_color_hex


def svg_color_triangle(tri_rows, edge_len, c1, c2, c3, file_name):

    # CALCULATE GEOMETRY CONSTANTS
    tri_base_len = edge_len / tri_rows
    tri_height = sin(radians(60)) * edge_len
    tri_row_height = tri_height / tri_rows

    # CALCULATE COLOR CONSTANTS
    color_info = {}
    color_info['c1_x'] = edge_len / 2
    color_info['c1_y'] = tri_height - (tri_row_height / 2)
    color_info['c2_x'] = tri_base_len / 2
    color_info['c2_y'] = tri_row_height * 0.5
    color_info['c3_x'] = edge_len - (tri_base_len / 2)
    color_info['c3_y'] = tri_row_height * 0.5

    color_info['max dist'] = color_info['c3_x'] - color_info['c2_x']

    color_info['c1'] = c1
    color_info['c2'] = c2
    color_info['c3'] = c3
    
    # CREATE INITIAL SVG FILE
    svg_file = open(file_name+'.svg','wb')
    svg_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    svg_file.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="'+str(edge_len)+'px" height="'+str(tri_height)+'px">\n')

    # START WITH THE TOP OF THE TRIANGLE AND WORK DOWN
    for row in range(0, tri_rows):

        # CALCULATE ROW CONSTANTS
        row_y_top = tri_height - (tri_row_height * row)
        row_y_bot = tri_height - (tri_row_height * (row + 1))
        row_x_top = (edge_len/2) - (row * tri_base_len * 0.5)
        row_x_bot = (edge_len/2) - ((row + 1) * tri_base_len * 0.5)

        # GENERATE TRIANGLES
        if row >= 1:

            # CYCLE THROUGH EACH ROW
            for i in range(0,row):

                # GENERATE TWO TRIANGLE PAIRS
                t1_0_x = row_x_top + (i * tri_base_len)         # top
                t1_0_y = row_y_top                              # top
                t1_1_x = row_x_bot + (i * tri_base_len)         # bottom left
                t1_1_y = row_y_bot                              # bottom left
                t1_2_x = row_x_bot  + ((i+1) * tri_base_len)    # bottom right
                t1_2_y = row_y_bot                              # bottom right

                t1_c_x = t1_0_x                                 # triangle centroid
                t1_c_y = (row_y_bot + row_y_top) / 2            # triangle centroid
                t1_color = interpolate_color(color_info, t1_c_x, t1_c_y)

                t2_0_x = row_x_top + ((i+1) * tri_base_len)     # top right
                t2_0_y = row_y_top                              # top right
                t2_1_x = row_x_top + (i * tri_base_len)         # top left
                t2_1_y = row_y_top                              # top left
                t2_2_x = row_x_bot + ((i+1) * tri_base_len)     # bottom
                t2_2_y = row_y_bot                              # bottom

                t2_c_x = row_x_bot + ((i+1) * tri_base_len)         # triangle centroid
                t2_c_y =(row_y_bot + row_y_top) / 2         # triangle centroid
                t2_color = interpolate_color(color_info, t2_c_x, t2_c_y)

                # WRITE TRIANGLES TO SVG FILE
                svg_file.write('<polygon points="'+str(t1_0_x)+','+str(t1_0_y)+' '+str(t1_1_x)+','+str(t1_1_y)+' '+str(t1_2_x)+','+str(t1_2_y)+'" fill="'+t1_color+'" stroke="'+t1_color+'"/>\n')
                svg_file.write('<polygon points="'+str(t2_0_x)+','+str(t2_0_y)+' '+str(t2_1_x)+','+str(t2_1_y)+' '+str(t2_2_x)+','+str(t2_2_y)+'" fill="'+t2_color+'" stroke="'+t2_color+'"/>\n')
            
        # GENERATE LAST TRIANGLE IN ROW
        t3_0_x = edge_len - row_x_top                   # top
        t3_0_y = row_y_top                              # top
        t3_1_x = edge_len - row_x_bot - tri_base_len    # bottom left
        t3_1_y = row_y_bot                              # bottom left
        t3_2_x = edge_len - row_x_bot                   # bottom right
        t3_2_y = row_y_bot                              # bottom right

        t3_c_x = t3_0_x                              # triangle centroid
        t3_c_y = (row_y_bot + row_y_top) / 2         # triangle centroid
        t3_color = interpolate_color(color_info, t3_c_x, t3_c_y)

        # WRITE TRIANGLE TO SVG FILE
        svg_file.write('<polygon points="'+str(t3_0_x)+','+str(t3_0_y)+' '+str(t3_1_x)+','+str(t3_1_y)+' '+str(t3_2_x)+','+str(t3_2_y)+'" fill="'+t3_color+'" stroke="'+t3_color+'"/>\n')

    # FINISH SVG FILE AND CLOSE
    svg_file.write('</svg>')
    svg_file.close()
    pass


#--- EXAMPLE RUN --------------------------------------------------------------+

##c1 = [234,47,131]   # BOTTOM    (PINK)
##c2 = [254,167,6]    # TOP LEFT  (ORANGE)
##c3 = [66,218,67]    # TOP RIGHT (GREEN)
##
##c1 = [0,255,255]    # BOTTOM    (CYAN)
##c2 = [255,0,255]    # TOP LEFT  (MAGENTA)
##c3 = [255,255,0]    # TOP RIGHT (YELLOW)

c1 = [255,0,0]      # BOTTOM    (RED)
c2 = [0,255,0]      # TOP LEFT  (BLUE)
c3 = [0,0,255]      # TOP RIGHT (GREEN)

edge_len = 1000     # edge length (px) of whole triangle
tri_rows = 10       # number of triangles to subdivide each edge

svg_color_triangle(tri_rows, edge_len, c1, c2, c3, 'new_triangle')

#--- END ----------------------------------------------------------------------+
