# pydecorate - python module for labelling 
# and adding colour scales to images
# 
#Copyright (C) 2011  Hrobjartur Thorsteinsson
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from pydecorate.DecoratorBase import DecoratorBase

try:
    from PIL import Image, ImageFont
except ImportError:
    print "ImportError: Missing PIL image objects"

try:
    import cairo
except ImportError:
    print "ImportError: Missing module: Cairo"

try:
    from PIL import ImageDraw
except ImportError:
    print "ImportError: Missing module: ImageDraw"
    
import numpy

   
class DecoratorCairo(DecoratorBase):

    def __init__(self, image):
        self.surface = cairo.ImageSurface.create_from_png('BMNG_clouds_201109181715_areaT2.png')
        self.context = cairo.Context(self.surface)
        super(DecoratorCairo, self).__init__(image)
        print("surface size: %s x %s" % (self.surface.get_width(), self.surface.get_height()))
        self.style['bg'] = (255,255,255)
        self.style['bg_opacity'] = 0.5
        self.style['line'] = (0, 0, 0)
        self.style['line_opacity'] = 1
        
        
    def test_func(self): 
        # self.context.set_source_rgb(1 , 0 , 0.5)
        # self.align_top()
        # self.align_left()
        # self.add_text("TOP L \nancora TOP L")
        # self.align_left()
        # self.align_bottom()
        # self.add_text("BOT L \nancora BOT L")
        # self.align_right()
        # self.add_text("BOT R\nfraseeeeeeee luuuuunnngggghhiiiiiiiiisisssssisssisisissmissisisma")
        # self.align_center_x()
        # self.align_center_y()
        # self.add_text("X")
        # self.context.rectangle(10,10,20,20)
        # self.context.move_to(30,30)
        # self.context.rel_line_to(90,90)
        # self.context.stroke()
        # self.context.fill()
        pass
        
    def write_vertically(self):
        super(DecoratorCairo, self).write_vertically()

    def write_horizontally(self):
        super(DecoratorCairo, self).write_horizontally()
        
    def align_bottom(self):
        super(DecoratorCairo, self).align_bottom()

    def align_top(self):
        super(DecoratorCairo, self).align_top()

    def align_right(self):
        super(DecoratorCairo, self).align_right()
        
    def align_left(self):
        super(DecoratorCairo, self).align_left()
        
    def add_scale(self,colormap,**kwargs):
        self._add_scale(colormap,**kwargs)

    def _load_default_font(self):
        import aggdraw
        return aggdraw.Font("black","/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",size=16)

    def add_text(self,txt,**kwargs):
        self._add_text(txt, **kwargs)
        
    def add_logo(self,logo_path,**kwargs):
        self._add_logo(logo_path,**kwargs)
        
    def _get_canvas(self,image):
        """Returns AGG image object
        """
        import aggdraw
        return aggdraw.Draw(image)
        
    def save_png(self):
        self.context.save()
        self.surface.write_to_png("boh.png")
        self.surface.finish()

    def _finalize(self, draw):
        raise NotImplementedError("not implemented yet")

    def _draw_line(self,draw,xys,**kwargs):
        raise NotImplementedError("not implemented yet")

    def _draw_polygon(self, draw,xys,outline=None,fill='white', fill_opacity=255,outline_width=1, outline_opacity=255):
        import aggdraw
        if outline is None:
            pen=None
        else:
            pen=aggdraw.Pen(outline,width=outline_width,opacity=outline_opacity)
        if fill is None:
            brush=None
        else:
            brush=aggdraw.Brush(fill,opacity=fill_opacity)
        xys_straight=[ item for t in xys for item in t ]
        draw.polygon(xys_straight,pen,brush)
        
    def set_style(self, **kwargs):
        self.style.update(kwargs)
        self.style['cursor'] = list(self.style['cursor'])

    def _finalize(self, draw):
        """Do any need finalization of the drawing
        """
        pass

    def home(self):
        super(DecoratorCairo, self).home()

    def rewind(self):
        super(DecoratorCairo, self).rewind()
        
    def new_line(self):
        super(DecoratorCairo, self).new_line()
        
    def _step_cursor(self):
        super(DecoratorCairo, self)._step_cursor()
    
    def _load_default_font(self):
        #temporary toy-method
        self.context.select_font_face("Serif", 1, 1)
    
        
    #def start_border(self):
    #    self.style['start_border'] = list( self.style['cursor'] )
    #    
    #def end_border(self,**kwargs):
    #    x0=self._start_border[0]
    #    y0=self._start_border[1]
    #    x1=self._cursor[0]
    #    y1=self._cursor[1]+self._line_size[1]
    #    draw=self._get_canvas(self.image)
    #    self._draw_rectangle(draw,[x0,y0,x1,y1],bg=None,**kwargs)
    #    self._finalize(draw)

    def _draw_polygon(self,draw,xys,**kwargs):
        draw.polygon(xys,fill=kwargs['fill'],outline=kwargs['outline'])

    def _get_canvas(self, img):
        raise NotImplementedError("Derived class implements this.")

    def _draw_text(self, draw, xy, txt, font, fill='black', align='cc', dry_run=False, **kwargs):
        """
        Elementary text draw routine,
        with alignment. Returns text size.
        """
        # check for font object
        if font is None:
            font = self._load_default_font()
            
        self.context.set_source_rgb(self.style['line'][0], self.style['line'][1], self.style['line'][2])

        # calculate text space
        tw, th = draw.textsize(txt, font)

        # align text position
        x, y = xy
        if align[0] == 'c':
            x -= tw/2.0
        elif align[0] == 'r':
            x -= tw
        if align[1] == 'c':
            y -= th/2.0
        elif align[1] == 'r':
            y -= th
        
        # draw the text
        if not dry_run:
            self._draw_text_line(draw, (x,y), txt, font, fill=fill)

        return tw,th

    def _add_text(self, txt, **kwargs): 
     
        # synchronize kwargs into style
        self.set_style(**kwargs)

        # check for font object
        if self.style['font'] is None: 
            self.style['font'] = self._load_default_font()

        # image size
        x_size = self.surface.get_height()
        y_size = self.surface.get_width()

        # split text into newlines '\n'
        txt_nl=txt.split('\n')

        # current xy and margins
        x = self.style['cursor'][0]
        y = self.style['cursor'][1]
        mx = self.style['margins'][0]
        my = self.style['margins'][1]
        prev_width  = self.style['width']
        prev_height = self.style['height']

        # calculate text space
        extents = self.context.text_extents(txt_nl[0])
        tw = extents[2]
        th = extents[3]
        bearing_x = extents[0]
        bearing_y = extents[1]
        
        for t in txt_nl:
            w = self.context.text_extents(t)[2]
            if w > tw: tw = w
        hh=len(txt_nl)*th
        
        print("th: %s, hh: %s" % (th, hh))

        # set height/width for subsequent draw operations
        if prev_height < int(hh+2*my): 
            self.style['height'] = int(hh+2*my)
        self.style['width'] = int(tw+2*mx)
        
        # draw base
        px = (self.style['propagation'][0] + self.style['newline_propagation'][0])
        py = (self.style['propagation'][1] + self.style['newline_propagation'][1])
        x1 = x + px*(tw + 2*mx)
        y1 = y + py*self.style['height']
        
        pos_x = x + mx
        pos_y = y + my
        if py < 0:
            pos_y += py*self.style['height']
        if px < 0:
            pos_x += px*self.style['width']
        self._draw_rectangle(None, [pos_x + bearing_x - mx, pos_y + bearing_y - my, tw + 2 * mx, hh + 2 * my], **self.style)
        
        # draw
        for i in range(len(txt_nl)):
            pos_y = y + i*th+my
            if py < 0:
                pos_y += py*self.style['height']
            self._draw_text_line(None, (pos_x, pos_y), txt_nl[i], self.style['font'], fill = self.style['fill'])
    
        # update cursor
        self._step_cursor()

        # finalize
        self._finalize(None)

    def _draw_text_line(self, draw, xy, text, font, fill='black'):
        self.context.set_source_rgb(self.style['line'][0], self.style['line'][1], self.style['line'][2])
        self.context.move_to(xy[0], xy[1])
        self.context.show_text(text)
        
    def _draw_line(self,draw,xys,**kwargs):
        draw.line(xys,fill=kwargs['line']) # inconvenient to use fill for a line so swapped def.

    def _draw_rectangle(self,draw,xys,**kwargs):
        # adjust extent of rectangle to draw up to but not including xys[2/3]
        #xys[2]-=1
        #xys[3]-=1
        self.context.set_source_rgba(self.style['bg'][0], self.style['bg'][0], self.style['bg'][0], self.style['bg_opacity'])
        if kwargs['bg'] or kwargs['outline']:
            self.context.set_line_width(1)
            #draw.rectangle(xys, fill=kwargs['bg'], outline=kwargs['outline'])
            self.context.rectangle(xys[0], xys[1], xys[2], xys[3])
        self.context.fill()
        
        
    def _insert_RGBA_image(self,img,box):
        # make sure box is formed tl to br corners:
        
        #box = self._form_xy_box(box)
        # crop area for compositing
        #crop=self.image.crop(box)
        #comp=Image.composite(img,crop,img)
        #self.image.paste(comp,box)
        x = self.style['cursor'][0]
        y = self.style['cursor'][1]
        mx = self.style['margins'][0]
        my = self.style['margins'][1]
        pos_x = x - mx
        pos_y = y + my
        
        print("pos_x: %s, pos_y: %s" % (pos_x, pos_y))
        print("x: %s, y: %s" % (x, y))
        print("mx: %s, my: %s" % (mx, my))
        
        img.putalpha(256)
        arr = numpy.array(img)
        height, width, channels = arr.shape
        logo_surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, width, height)
        logo_pattern = cairo.SurfacePattern(logo_surface)
        self.context.set_source_surface(logo_surface, pos_x, pos_y)
        #self.context.mask(logo_pattern)
        self.context.paint()
        
    def _add_logo(self, logo_path, **kwargs):
        # synchronize kwargs into style
        self.set_style(**kwargs)

        print("adding logo...")
        
        # current xy and margins
        x=self.style['cursor'][0]
        y=self.style['cursor'][1]

        mx=self.style['margins'][0]
        my=self.style['margins'][1]

        # draw object
        #draw = self._get_canvas(self.image)

        # get logo image
        logo=Image.open(logo_path,"r").convert('RGBA')
        
        # default size is _line_size set by previous draw operation
        # else do not resize
        nx,ny=logo.size
        aspect=float(ny)/nx
        
        # default logo sizes ...
        # use previously set line_size
        if self.style['propagation'][0] != 0:
            ny = self.style['height'] 
            nyi = int(round(ny-2*my))
            nxi = int(round(nyi/aspect))
            nx = (nxi + 2*mx)
        elif self.style['propagation'][1] != 0:
            nx = self.style['width']
            nxi = int(round(nx-2*mx))
            nyi = int(round(nxi*aspect))
            ny = (nyi + 2*my)

        logo = logo.resize((nxi,nyi),resample=Image.ANTIALIAS)
        
        # draw base
        px = (self.style['propagation'][0] + self.style['newline_propagation'][0])
        py = (self.style['propagation'][1] + self.style['newline_propagation'][1])
        box = [x, y, x+px*nx, y+py*ny]
        #self._draw_rectangle(draw,box,**self.style)

        #finalize
        #self._finalize(draw)

        # paste logo
        box = [x+px*mx, y+py*my, x+px*mx+px*nxi, y+py*my+py*nyi]
        self._insert_RGBA_image(logo,box)
 
        # update cursor
        self.style['width'] = int(nx)
        self.style['height'] = int(ny)
        self._step_cursor()


    def _form_xy_box(self,box):
        newbox = box + []
        if box[0] > box[2]:
            newbox[0] = box[2]
            newbox[2] = box[0]
        if box[1] > box[3]:
            newbox[1] = box[3]
            newbox[3] = box[1]
        return newbox
        
    def _add_scale(self, colormap, **kwargs):
        # synchronize kwargs into style
        self.set_style(**kwargs)

        # sizes, current xy and margins
        x=self.style['cursor'][0]
        y=self.style['cursor'][1]
        mx=self.style['margins'][0]
        my=self.style['margins'][1]
        x_size,y_size = self.image.size

        # horizontal/vertical?
        is_vertical = False
        if self.style['propagation'][1] != 0:
            is_vertical = True
        
        # left/right?
        is_right = False
        if self.style['alignment'][0] == 1.0:
            is_right = True

        # top/bottom?
        is_bottom = False
        if self.style['alignment'][1] == 1.0:
            is_bottom = True

        # adjust new size based on extend (fill space) style,
        if self.style['extend']:
            if self.style['propagation'][0] == 1:
                self.style['width'] = (x_size - x)
            elif self.style['propagation'][0] == -1:
                self.style['width'] = x
            if self.style['propagation'][1] == 1:
                self.style['height'] = (y_size - y)
            elif self.style['propagation'][1] == -1:
                self.style['height'] = y

        # set scale spacer for units and other
        x_spacer = 0
        y_spacer = 0
        if self.style['unit']:
            if is_vertical:
                y_spacer = 40
            else:
                x_spacer = 40

        # draw object
        draw = self._get_canvas(self.image)
        
        # draw base
        px = (self.style['propagation'][0] + self.style['newline_propagation'][0])
        py = (self.style['propagation'][1] + self.style['newline_propagation'][1])
        x1 = x + px*self.style['width']
        y1 = y + py*self.style['height']
        self._draw_rectangle(draw,[x,y,x1,y1],**self.style)

        # scale dimensions
        scale_width = self.style['width'] - 2*mx - x_spacer
        scale_height = self.style['height'] - 2*my - y_spacer
        
        # generate color scale image obj inset by margin size mx my,
        from trollimage.image import Image as TImage
        
        #### THIS PART TO BE INGESTED INTO A COLORMAP FUNCTION ####
        minval,maxval = colormap.values[0],colormap.values[-1]

        if is_vertical:
            linedata = np.ones((scale_width,1)) * np.arange(minval,maxval,(maxval-minval)/scale_height)
            linedata = linedata.transpose()
        else:
            linedata = np.ones((scale_height,1)) * np.arange(minval,maxval,(maxval-minval)/scale_width)

        timg = TImage(linedata,mode="L")
        timg.colorize(colormap)
        scale = timg.pil_image()
        ###########################################################

        # finalize (must be before paste)
        self._finalize(draw)

        # paste scale onto image
        pos =(min(x,x1)+mx,min(y,y1)+my)
        self.image.paste(scale,pos)

        # reload draw object
        draw = self._get_canvas(self.image)

        # draw tick marks
        val_steps =  _round_arange2( minval, maxval , self.style['tick_marks'] )
        minor_steps =  _round_arange( minval, maxval , self.style['minor_tick_marks'] )

        ffra, fpow = _optimize_scale_numbers( minval, maxval, self.style['tick_marks'] )
        form = "%"+"."+str(ffra)+"f"
        last_x = x+px*mx
        last_y = y+py*my
        ref_w, ref_h = self._draw_text(draw, (0,0), form%(val_steps[0]), dry_run=True, **self.style)

        if is_vertical:
            # major
            offset_start = val_steps[0]  - minval
            offset_end   = val_steps[-1] - maxval 
            y_steps = py*(val_steps - minval - offset_start - offset_end)*scale_height/(maxval-minval)+y+py*my
            y_steps = y_steps[::-1]
            for i, ys in enumerate(y_steps):
                self._draw_line(draw,[(x+px*mx,ys),(x+px*(mx+scale_width/3.0),ys)],**self.style)
                if abs(ys-last_y)>ref_h:
                    self._draw_text(draw,(x+px*(mx+2*scale_width/3.0),ys), (form%(val_steps[i])).strip(), **self.style)
                    last_y = ys
            # minor
            y_steps = py*(minor_steps - minval)*scale_height/(maxval-minval)+y+py*my
            y_steps = y_steps[::-1]
            for i, ys in enumerate(y_steps):
                self._draw_line(draw,[(x+px*mx,ys),(x+px*(mx+scale_width/6.0),ys)],**self.style)
        else:
            # major
            x_steps = px*(val_steps - minval)*scale_width/(maxval-minval)+x+px*mx
            for i, xs in enumerate(x_steps):
                self._draw_line(draw,[(xs,y+py*my),(xs,y+py*(my+scale_height/3.0))],**self.style)
                if abs(xs-last_x)>ref_w:
                    self._draw_text(draw,(xs, y+py*(my+2*scale_height/3.0)), (form%(val_steps[i])).strip(), **self.style)
                    last_x = xs
            # minor
            x_steps = px*(minor_steps - minval)*scale_width/(maxval-minval)+x+px*mx
            for i, xs in enumerate(x_steps):
                self._draw_line(draw,[(xs,y+py*my),(xs,y+py*(my+scale_height/6.0))],**self.style)
                

        # draw unit and/or power if set
        if self.style['unit']:
            # calculate position
            if is_vertical:
                if is_right:
                    x = x - mx - scale_width/2.0
                else:
                    x = x + mx + scale_width/2.0
                y = y + my + scale_height + y_spacer/2.0
            else:
                x = x + mx + scale_width + x_spacer/2.0
                if is_bottom:
                    y = y - my - scale_height/2.0
                else:
                    y = y + my + scale_height/2.0
            # draw marking
            self._draw_text(draw,(x,y),self.style['unit'],**self.style)

        # finalize
        self._finalize(draw)

#########################################


# float list generator
def _frange(x,y,jump):
    while x < y:
        yield x
        x += jump
def frange(x,y,jump):
    return [p for p in _frange(x,y,jump) ]

class ShapeFileError(Exception):
    pass


                        
