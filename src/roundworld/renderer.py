
import numpy as np
    

class Palette:

    def __init__(self, palette):

        if palette == "default":
            self._palette = default_palette
        elif palette == "defaultgrey":
            self._palette = default_greypalette
        elif palette == "random":
            self._palette = random_palette()
        elif palette == "randomgrey":
            self._palette = random_greypalette()
        else:
            self._palette = palette

    @property
    def sky(self):
        return self._palette['sky']
    
    @property
    def ground(self):
        return self._palette['ground']
    
    @property
    def depth_fade(self):
        return self._palette.get('depth_fade', 0.01)

    @property
    def type(self):
        return self._palette['type']

    def color(self, obid):
        return self._palette[obid]





default_palette = {
    'type': "rgb",
    'sky': (174, 214, 241),
    'ground': (243, 156, 18),
    1: (142, 68, 173)
}

default_greypalette = {
    'type': "mono",
    'sky': 0.9,
    'ground': 0.3,
    1: 0.7
}

def random_palette(Nobjs=1):
    """Create a random palette of RGB values for sky, ground, and Nobjs objects (default=1)
    """

    palette = {
        'type' : 'rgb',
        'sky': (np.random.randint(256), np.random.randint(256), np.random.randint(256)),
        'ground': (np.random.randint(256), np.random.randint(256), np.random.randint(256))}

    for i in range(Nobjs):
        palette[i+1] = (np.random.randint(256), np.random.randint(256), np.random.randint(256))
    return palette


def random_greypalette(Nobjs=1):
    """Create a random palette of single channel values for sky, ground, and Nobjs objects (default=1)
    """
    palette = {
        'type' : 'mono',
        'sky': np.random.random(),
        'ground': np.random.random()}
    for i in range(Nobjs):
        palette[i+1] =  np.random.random()
    return palette


class Renderer:

    def __init__(self, screen, palette):
        self.palette = palette
        self.screen = screen
        self.is_rgb = palette.type == "rgb"
        self.calc_background()

    def calc_background(self):

        blist = []
        halfheight = self.screen.imwidth // 2
        c_sky = self.palette.sky

        if self.is_rgb:
            r, g, b = self.palette.ground
        else:
            r = self.palette.ground

        for i in range(halfheight):
            d = 1+self.palette.depth_fade*(halfheight-1-i)
            if self.is_rgb:
                blist.append((int(r/d),int(g/d),int(b/d)))
            else:
                blist.append(int(r/d))

        self.c_sky = c_sky
        self.c_blist = np.array(blist)
        self.blist = blist

    def get_background(self):
        return self.c_sky, self.blist

    def calc_fading(self, odist):
        return min(1, 1/(1+self.palette.depth_fade*odist))

    def calc_color(self, obid, odist):
        dfade = self.calc_fading(odist)
        if self.is_rgb:
            r, g, b = self.palette.color(obid)
            return (int(dfade*r), int(dfade*g), int(dfade*b))
        else:
            r = self.palette.color(obid)
            return dfade*r


    def render_visual(self, rects):
        """
        Returns an array with the visual input.

        """
        imheight = self.screen.imwidth
        halfheight = int(imheight/2)

        if self.is_rgb:
            rgb = np.zeros((3,self.screen.imwidth,imheight), dtype=np.uint8)
            rgb[0,:,0:halfheight] = self.c_sky[0]
            rgb[1,:,0:halfheight] = self.c_sky[1]
            rgb[2,:,0:halfheight] = self.c_sky[2]

            rgb[0,:,halfheight:] = self.c_blist[:,0]
            rgb[1,:,halfheight:] = self.c_blist[:,1]
            rgb[2,:,halfheight:] = self.c_blist[:,2]

        else:
            r = np.zeros((self.screen.imwidth,imheight))
            r[:,0:halfheight] = self.c_sky
            r[:,halfheight:] = self.c_blist

        for i, jmin, jmax, ob_id, odist in rects:

            if self.is_rgb:
                irob, igob, ibob = self.calc_color(ob_id, odist)
                rgb[0,i,jmin:(jmax+1)] = irob
                rgb[1,i,jmin:(jmax+1)] = igob
                rgb[2,i,jmin:(jmax+1)] = ibob

            else:
                rob = self.calc_color(ob_id, odist)
                r[i,jmin:jmax] = rob

        if self.is_rgb:
            return rgb
        else:
            return r


    def render_saliency(self, rects):
        """
        Return a 2D array with the saliency map highlighting objects in the visual field

        """

        r = np.zeros((self.screen.imwidth,self.screen.imwidth),dtype=np.uint8)

        for i, jmin, jmax, _, _ in rects:
            r[i,jmin:(jmax+1)] = 1

        return r

    def render(self, recs, saliency=False):
        
        m =  self.render_visual(recs)
        if saliency:
            salmap = self.render_saliency(recs)
            return m, salmap
        else:
            return m

    def colorize_rectangles(self, oblist):
        return [(ob[0], ob[1], ob[2], self.calc_color(ob[3], ob[4]))
            for ob in oblist]

