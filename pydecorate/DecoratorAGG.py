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
from DecoratorBase import DecoratorBase
from PIL import Image, ImageFont
import ImageDraw

class DecoratorAGG(DecoratorBase):
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


                        
