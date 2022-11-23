"""
Ray casting


"""
import numpy as np

sqr3 = np.sqrt(3)

def get_unit(imwidth):
    tani = (1-(1+2*np.arange(imwidth))/imwidth)/sqr3
    den = np.sqrt(tani*tani+1)
    ux = 1/den
    uy = tani/den
    return ux, uy


class Screen:

    def __init__(self, imwidth):
        self.imwidth = imwidth
        self.ux, self.uy = get_unit(imwidth)


def raycast(screen, objlist):
    """Return the view of an object oriented with the x axis

    It assumes a span of 60 degrees

    Args:
        imwidth : the number of segments 
        objlist : list with objects in the environment
    
    Returns:
        a list of tuples (object_id, distance) per segment

    """
    xl = objlist.xl
    yl = objlist.yl
    size = objlist.size
    visible = objlist.visible

    imwidth = screen.imwidth
    ux, uy = screen.ux, screen.uy

    imhalf = imwidth/2
    d2 = xl*xl + yl*yl
    nlist = (imhalf*(1-sqr3*yl/(xl+1e-6))).astype(np.int16)

    nlist[(xl < 0) & (yl > 0)] = -1
    nlist[(xl < 0) & (yl <= 0)] = imwidth + 1

    columns = [[] for i in range(imwidth)]

    for i, ni in enumerate(nlist):
        if visible[i] == 0:
            continue
        b2 = size[i]**2-d2[i]

        if ni < 0:
            nj = 0
            while nj < imwidth:
                tij = xl[i]*ux[nj]+yl[i]*uy[nj]
                dt2 = tij*tij + b2
                if dt2 > 0:
                    dt = np.sqrt(dt2)
                    if tij < dt:
                        tij = tij + dt
                    else:
                        tij = tij - dt
                    columns[nj].append((i,tij))
                    nj += 1
                else:
                    break
        elif ni >= imwidth:
            nj = imwidth-1
            while nj >= 0:
                tij = xl[i]*ux[nj]+yl[i]*uy[nj]
                dt2 = tij*tij + b2
                if dt2 > 0:
                    dt = np.sqrt(dt2)
                    if tij < dt:
                        tij = tij + dt
                    else:
                        tij = tij - dt

                    columns[nj].append((i,tij))
                    nj -= 1
                else:
                    break
        else:
            nj = ni
            while nj < imwidth:
                tij = xl[i]*ux[nj]+yl[i]*uy[nj]
                dt2 = tij*tij + b2
                if dt2 > 0:
                    dt = np.sqrt(dt2)
                    if tij < dt:
                        tij = tij + dt
                    else:
                        tij = tij - dt
                    columns[nj].append((i,tij))
                    nj += 1
                else:
                    break
            nj = ni-1
            while nj >= 0:
                tij = xl[i]*ux[nj]+yl[i]*uy[nj]
                dt2 = tij*tij + b2
                if dt2 > 0:
                    dt = np.sqrt(dt2)
                    if tij < dt:
                        tij = tij + dt
                    else:
                        tij = tij - dt

                    columns[nj].append((i,tij))
                    nj -= 1
                else:
                    break
            
    for c in columns:
        if len(c) > 1:
            c.sort(key=lambda x: -x[1])
    
    return columns

 

def get_rectangles(columns, obj_height, obid, viewheight):

    oblist = []
    d0 = viewheight*np.sqrt(3)
    imwidth = len(columns)
    imheight = imwidth
    halfheight = int(imheight/2)

    for i, cl in enumerate(columns):
        if len(cl) == 0:
            continue
        else:
            for ob_ind, obd in cl:
                ofmax = d0/obd
                ofmin = ofmax*(obj_height[ob_ind]-viewheight)/viewheight
                jmin = halfheight - int(ofmin*halfheight)
                jmax = halfheight + int(ofmax*halfheight)
                if jmin < 0:
                    jmin = 0
                if jmax >= imheight:
                    jmax = imheight-1
                oblist.append((i, jmin, jmax, obid[ob_ind], obd))
    return oblist
