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

import os
import numpy as np
from PIL import Image, ImageFont
import ImageDraw
import math

# style dictionary defines default options
# some only used by aggdraw version of the decorator
default_style_dict = {
'cursor':[0,0],
'margins':[5,5],
'height':60,
'width':60,
'propagation':[1,0],
'newline_propagation':[0,1],
'bg':'white',
'bg_opacity':127,
'outline':None,
'outline_opacity':255,
'fill':'black',
'fill_opacity':255,
'font':None,
'start_border':[0,0]
}

class DecoratorBase(object):
    def __init__(self,image):
        """
        Probably users only want to instantiate DecoratorAgg or the Decorator implementations.
        DecoratorBase is a base class outlining common operations and interface for the Decorator (PIL drawing engine) and DecoratorAgg (Aggdraw drawing engine)
        """
        self.image = image
        
        import copy
        self.style = copy.deepcopy(default_style_dict)

    def set_style(self, **kwargs):
        self.style.update(kwargs)
        self.style['cursor'] = list(self.style['cursor'])

    def _finalize(self, draw):
        """Do any need finalization of the drawing
        """
        pass

    def bottom_align(self):
        x_size, y_size = self.image.size
        self.style['cursor'][1] = y_size

    def top_align(self):
        self.style['cursor'][1] = 0

    def right_align(self):
        pass

    def left_align(self):
        pass

    def new_line(self):
        self.style['cursor'][0] += self.style['newline_propagation'][0] * self.style['propagation'][0] * self.style['width'] 
        self.style['cursor'][1] += self.style['newline_propagation'][1] * self.style['propagation'][1] * self.style['height'] 

    def _step_cursor(self):
        self.style['cursor'][0] += self.style['propagation'][0] * self.style['width']
        self.style['cursor'][1] += self.style['propagation'][1] * self.style['height']

    #def start_border(self):
    #    self.style['start_border'] = list( self.style['cursor'] )
    #    
    #def end_border(self,**kwargs):
    #    x0=self._start_border[0]
    #    y0=self._start_border[1]
    #    x1=self._cursor[0]
    #    y1=self._cursor[1]+self._line_size[1]
    #    draw=self._get_canvas(self.image)
    #    self._add_rectangle(draw,[x0,y0,x1,y1],bg=None,**kwargs)
    #    self._finalize(draw)

    def _add_polygon(self,draw,xys,**kwargs):
        draw.polygon(xys,fill=kwargs['fill'],outline=kwargs['outline'])

    def _get_canvas(self, img):
        raise NotImplementedError("Derived class implements this.")

    def _load_default_font(self):
        raise NotImplementedError("Derived class implements this.")

    def _add_text(self,txt,**kwargs): 
        # synchronize kwargs into style
        self.set_style(**kwargs)

        # draw object
        draw = self._get_canvas(self.image)

        # check for font object
        if self.style['font'] is None: 
            self.style['font'] = self._load_default_font()

        # image size
        x_size, y_size = self.image.size

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
        tw,th = draw.textsize(txt_nl[0],self.style['font'])
        for t in txt_nl:
            w,tmp = draw.textsize(t,self.style['font'])
            if w > tw: tw = w
        hh=len(txt_nl)*th

        # set height/width for subsequent draw operations
        if prev_height < int(hh+2*my): 
            self.style['height'] = int(hh+2*my)
        self.style['width'] = int(tw+2*mx)

        # draw text bg
        x1 = x + tw + 2*mx
        y1 = y + self.style['height']
        self._add_rectangle(draw,[x,y,x1,y1],**self.style)
        
        # draw
        for i in range(len(txt_nl)):
            self._add_text_line(draw,(x+mx,y+i*th+my),txt_nl[i], self.style['font'], fill=self.style['fill'])

        # update cursor
        self._step_cursor()

        # finalize
        self._finalize(draw)

    def _add_text_line(self,draw,xy,text,font,fill='black'):
        draw.text(xy,text, font=font, fill=fill)
        
    def _add_line(self,draw,xys,outline='black'):
        draw.line(xys,fill=outline) # inconvenient to use fill for a line so swapped def.

    def _add_rectangle(self,draw,xys,**kwargs):
        # adjust extent of rectangle to draw up to but not including xys[2/3]
        xys[2]-=1
        xys[3]-=1
        if kwargs['bg'] or kwargs['outline']:
            draw.rectangle(xys,fill=kwargs['bg'],outline=kwargs['outline'])

    def _add_logo(self, logo_path, **kwargs):
        # synchronize kwargs into style
        self.set_style(**kwargs)

        # current xy and margins
        x=self.style['cursor'][0]
        y=self.style['cursor'][1]

        mx=self.style['margins'][0]
        my=self.style['margins'][1]

        # draw object
        draw = self._get_canvas(self.image)

        # get logo image
        logo=Image.open(logo_path,"r").convert('RGBA')
        
        # default size is _line_size set by previous draw operation
        # else do not resize
        nx,ny=logo.size
        aspect=float(ny)/nx
        
        # default logo sizes ...
        # use previously set line_size
        ny = self.style['height']
        nyi = int(round(ny-2*my))
        nxi = int(round(nyi/aspect))
        nx = nxi + 2*mx
        logo = logo.resize((nxi,nyi),resample=Image.ANTIALIAS)
        
        # draw base
        self._add_rectangle(draw,[x,y,x+nx,y+ny],**self.style)

        #finalize
        self._finalize(draw)

        # paste logo
        box=(int(round(x+mx)),int(round(y+my)),int(round(x+mx+nxi)),int(round(y+my+nyi)))
        self._insert_RGBA_image(logo,box)
 
        # update cursor
        self.style['width'] = int(nx)
        self.style['height'] = int(ny)
        self._step_cursor()

    def _insert_RGBA_image(self,img,box):
        # crop area for compositing
        crop=self.image.crop(box)
        comp=Image.composite(img,crop,img)
        self.image.paste(comp,box)

class Decorator(DecoratorBase):
    def add_scale(self,color_def,font=None,size=None,fill='black',
                  outline=None, outline_width=1, bg='white',extend=False,unit='',margins=None,minortick=0.0,
                  nan_color=(0,0,0), nan_check_color=(1,1,1), nan_check_size=0):
        """ Todo
        """
        self._add_scale(color_def,font=font,size=size,fill=fill,
                        outline=outline,outline_widht=outline_width,bg=bg,extend=extend,unit=unit,margins=margins,minortick=minortick,
                        nan_color=nan_color, nan_check_color=nan_check_color, nan_check_size=nan_check_size)

    def _load_default_font(self):
        return ImageFont.load_default()

    def add_text(self,txt,**kwargs):
        self._add_text(txt,**kwargs)

    def add_logo(self,logo_path,**kwargs):
        self._add_logo(logo_path,**kwargs)
        

    def _get_canvas(self,image):
        """Returns PIL image object
        """    
        return ImageDraw.Draw(image)

class DecoratorAGG(DecoratorBase):
    def add_scale(self,color_def,font=None,size=None,fill='black',fill_opacity=255,
                  outline=None,outline_width=1.0,outline_opacity=255,bg='white',bg_opacity=255,extend=False,unit='',margins=None,minortick=0.0,
                  nan_color=(0,0,0), nan_check_color=(1,1,1), nan_check_size=0):
          self._add_scale(color_def,font=font,size=size,fill=fill,fill_opacity=fill_opacity,
                          outline=outline,outline_opacity=outline_opacity,outline_width=outline_width,bg=bg,bg_opacity=bg_opacity,extend=extend,unit=unit,margins=margins,minortick=minortick,
                          nan_color=nan_color, nan_check_color=nan_check_color, nan_check_size=nan_check_size)

    def _load_default_font(self):
        import aggdraw
        return aggdraw.Font("black","/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",size=16)

    def add_text(self,txt,**kwargs):
        self._add_text(txt,**kwargs)

    def add_logo(self,logo_path,**kwargs):
        self._add_logo(logo_path,**kwargs)
        
    def _get_canvas(self,image):
        """Returns AGG image object
        """
        import aggdraw
        return aggdraw.Draw(image)

    def _finalize(self, draw):
        """Flush the AGG image object
        """
        
        draw.flush()

    def _add_text_line(self,draw,xy,text,font,fill='black'):
        draw.text(xy,text, font)

    def _add_rectangle(self,draw,xys,outline='white',bg='white',bg_opacity=255,outline_width=1,outline_opacity=255,**kwargs):
        import aggdraw
        pen=aggdraw.Pen(outline,width=outline_width,opacity=outline_opacity)
        brush=aggdraw.Brush(bg,opacity=bg_opacity)
        # draw bg and outline
        # bg unaliased (otherwise gaps between successive bgs)

        if bg is not None: 
            draw.setantialias(False)
            draw.rectangle(xys,None,brush)
            draw.setantialias(True)
        # adjust to correct for outline exceeding requested area,
        # due to outline width expanding outwards.
        xys[0]+=outline_width/2.0
        xys[1]+=outline_width/2.0
        xys[2]-=outline_width/2.0
        xys[3]-=outline_width/2.0
        if outline is not None: draw.rectangle(xys,pen,None)

        

    def _add_line(self,draw,xys,outline='black',outline_width=1,outline_opacity=255):
        import aggdraw
        if outline is None: 
            pen=None
        else:
            pen=aggdraw.Pen(outline,width=outline_width,opacity=outline_opacity)
        xys_straight=[ item for t in xys for item in t ]
        draw.line(xys_straight,pen)

    def _add_polygon(self,draw,xys,outline=None,fill='white',fill_opacity=255,outline_width=1,outline_opacity=255):
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


                        
