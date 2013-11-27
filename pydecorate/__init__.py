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

    def _add_text(self,txt,font=None,**kwargs): 
        # update current outline
        if self._outline is None:
            self._outline=kwargs['outline']
        else:
            kwargs['outline']=self._outline

        # update line height if set
        if kwargs['height'] is not None:
            self._line_size[1]=kwargs['height']

        # draw object
        draw = self._get_canvas(self.image)

        # image size
        x_size, y_size = self.image.size

        # split text into newlines '\n'
        txt_nl=txt.split('\n')

        # current xy and margins
        x=self._cursor[0]
        y=self._cursor[1]
        if kwargs['margins'] is None:
            mx=self._margins[0]
            my=self._margins[1]
        else:
            (mx,my)=kwargs['margins']
            self._margins=(mx,my)

        # set text fonts
        if font == None: font = ImageFont.load_default()

        # text space
        w,h = draw.textsize(txt_nl[0],font)
        for t in txt_nl:
            tw,tmp = draw.textsize(t,font)
            if tw > w: w=tw
        hh=len(txt_nl)*h

        # if first draw-object set line_size for subsequent draw operations
        if self._line_size[1] is None: self._line_size[1]=hh+2*my

        # draw text bg
        #self._add_rectangle(draw,[x,y,x+w+2*mx,y+hh+2*my],**kwargs)
        x1=x+w+2*mx
        y1=y+self._line_size[1]
        self._add_rectangle(draw,[x,y,x1,y1],**kwargs)
        
        # draw
        for i in range(len(txt_nl)):
            self._add_text_line(draw,(x+mx,y+i*h+my),txt_nl[i], font, fill=kwargs['fill'])

        # update cursor
        self._cursor[0]+=w+2*mx

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
          self._add_scale(color_def,font=font,size=size,fill=fill,
                          outline=outline,outline_widht=outline_width,bg=bg,extend=extend,unit=unit,margins=margins,minortick=minortick,
                          nan_color=nan_color, nan_check_color=nan_check_color, nan_check_size=nan_check_size)

    def add_text(self,txt,font=None,height=None,fill='black',outline=None,bg='white',margins=None):
        self._add_text(txt,font=font,height=height,fill=fill,outline=outline,bg=bg,margins=margins)

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

    def add_text(self,txt,font=None,height=None,fill='black',outline=None,bg='white',bg_opacity=255,margins=None):
        self._add_text(txt,font=font,height=height,fill=fill,outline=outline,bg=bg,bg_opacity=bg_opacity,margins=margins)

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

class ContourWriterBase(object):
    """Base class for contourwriters. Do not instantiate.
    
    :Parameters:
    db_root_path : str
        Path to root dir of GSHHS and WDBII shapefiles
    """
    
    _draw_module=None 
    # This is a flag to make _add_grid aware of which draw.text subroutine,
    # from PIL or from aggdraw is being used (unfortunately they are not fully compatible)
    # This may well be a clumbsy implementation.

    def __init__(self, db_root_path):
        self.db_root_path = db_root_path


    def _add_grid(self, image, area_def, Dlon, Dlat, dlon, dlat, font=None, **kwargs):
        """Add a lat lon grid to image
        """

        try:
            proj4_string = area_def.proj4_string
            area_extent = area_def.area_extent
        except AttributeError:
            proj4_string = area_def[0]
            area_extent = area_def[1]

        draw = self._get_canvas(image)

        if self._draw_module == "AGG": is_agg=True
        else: is_agg=False

        # use kwargs for major lines ... but reform for minor lines:
        minor_line_kwargs=kwargs.copy()
        minor_line_kwargs['outline']=kwargs['minor_outline']
        if is_agg:
            minor_line_kwargs['outline_opacity']=kwargs['minor_outline_opacity']
            minor_line_kwargs['width']=kwargs['minor_width']

        # set text fonts
        if font == None: font = ImageFont.load_default()
        # text margins (at sides of image frame)
        y_text_margin=4
        x_text_margin=4

        # Area and projection info
        x_size, y_size = image.size        
        prj = pyproj.Proj(proj4_string)
        
        x_offset=0
        y_offset=0
        
        # Calculate min and max lons and lats of interest        
        lon_min, lon_max, lat_min, lat_max = \
                _get_lon_lat_bounding_box(area_extent, x_size, y_size, prj) 
        

        # Draw lonlat grid lines ...
        round_lon_min=(lon_min-(lon_min%Dlon))
        maj_lons=frange(round_lon_min,lon_max,Dlon) # major lon lines
        min_lons=frange(round_lon_min,lon_max,dlon) # minor lon lines (ticks)
        for l in maj_lons: 
            if l in min_lons: min_lons.remove(l)
        lin_lats=frange(lat_min,lat_max,(lat_max-lat_min)/y_size) # lats along major lon lines
        # lin_lats in rather high definition so that it can be used to posituion text labels near edges of image...
        ##### perhaps better to find the actual length of line in pixels...

        round_lat_min=(lat_min-(lat_min%Dlat))
        maj_lats=frange(round_lat_min,lat_max,Dlat) # major lat lines
        min_lats=frange(round_lat_min,lat_max,dlat) # minor lon lines (ticks)
        for l in maj_lats: 
            if l in min_lats: min_lats.remove(l)
        lin_lons=frange(lon_min,lon_max,Dlon/10.0) # lons along major lat lines
        
        # create dummpy shape object
        tmpshape=shapefile.Writer("")

   
        ##### MINOR LINES ######
        if not kwargs['minor_is_tick']:
            # minor lat lines
            for lat in min_lats:
                lonlats = [(x,lat) for x in lin_lons]
                tmpshape.points=lonlats
                index_arrays, is_reduced = _get_pixel_index(tmpshape, area_extent, 
                                                            x_size, y_size, 
                                                            prj, 
                                                            x_offset=x_offset,
                                                            y_offset=y_offset)
                # Skip empty datasets               
                if len(index_arrays) == 0:
                    continue
                # make PIL draw the tick line...
                for index_array in index_arrays:
                    self._draw_line(draw, index_array.flatten().tolist(),  **minor_line_kwargs)
            # minor lon lines
            for lon in min_lons:
                lonlats = [(lon,x) for x in lin_lats]
                tmpshape.points=lonlats
                index_arrays, is_reduced = _get_pixel_index(tmpshape, area_extent, 
                                                            x_size, y_size, 
                                                            prj, 
                                                            x_offset=x_offset,
                                                            y_offset=y_offset)
                # Skip empty datasets               
                if len(index_arrays) == 0:
                    continue
                # make PIL draw the tick line...
                for index_array in index_arrays:
                    self._draw_line(draw, index_array.flatten().tolist(),  **minor_line_kwargs)
                
        ##### MAJOR LINES AND MINOR TICKS ######
        # major lon lines and tick marks:
        for lon in maj_lons:
            # Draw 'minor' tick lines dlat separation along the lon
            if kwargs['minor_is_tick']:
                tick_lons = frange(lon-Dlon/20.0,lon+Dlon/20.0,Dlon/50.0)
                for lat in min_lats:
                    lonlats = [(x,lat) for x in tick_lons]
                    tmpshape.points=lonlats
                    index_arrays, is_reduced = _get_pixel_index(tmpshape, area_extent, 
                                                                x_size, y_size, 
                                                                prj, 
                                                                x_offset=x_offset,
                                                                y_offset=y_offset)
                    # Skip empty datasets               
                    if len(index_arrays) == 0:
                        continue
                    # make PIL draw the tick line...
                    for index_array in index_arrays:
                        self._draw_line(draw, index_array.flatten().tolist(), **minor_line_kwargs)

            # Draw 'major' lines
            lonlats = [ (lon,x) for x in lin_lats ]
            tmpshape.points=lonlats
            index_arrays, is_reduced = _get_pixel_index(tmpshape, area_extent, 
                                                            x_size, y_size, 
                                                            prj, 
                                                            x_offset=x_offset,
                                                            y_offset=y_offset) 
            # Skip empty datasets               
            if len(index_arrays) == 0:
                continue
            
            # make PIL draw the lines...
            for index_array in index_arrays:
                self._draw_line(draw, index_array.flatten().tolist(), **kwargs)

            # add lon text markings at each end of longitude line
            if lon>0.0: txt="%.2dE"%(lon)
            else: txt="%.2dW"%(-lon)
            #w,h = font.getsize(txt)
            w,h = draw.textsize(txt,font)
            bot_xy=index_array[0]
            if bot_xy[0] > 0 and bot_xy[0] < x_size:
                i=0
                while bot_xy[1] > y_size:
                    i+=1
                    bot_xy = index_array[i]    
                bot_xy[1]=(y_size-1)-(h+y_text_margin)
                if is_agg: draw.text(bot_xy,txt, font)     
                else: draw.text(bot_xy,txt, font=font, fill=kwargs['fill'])     
            top_xy=index_array[-1]
            if top_xy[0] > 0 and top_xy[0] < x_size:
                i=-1
                while top_xy[1] < 0:
                    i-=1
                    top_xy = index_array[i]    
                top_xy[1]=(y_text_margin)
                if is_agg: draw.text(top_xy,txt, font)
                else: draw.text(bot_xy,txt, font=font, fill=kwargs['fill']) 

        # major lat lines and tick marks:
        for lat in maj_lats:
            # Draw 'minor' tick dlon separation along the lat
            if kwargs['minor_is_tick']: 
                tick_lats = frange(lat-Dlat/20.0,lat+Dlat/20.0,Dlat/50.0)
                for lon in min_lons:
                    lonlats = [(lon,x) for x in tick_lats]
                    tmpshape.points=lonlats
                    index_arrays, is_reduced = _get_pixel_index(tmpshape, area_extent, 
                                                                x_size, y_size, 
                                                                prj, 
                                                                x_offset=x_offset,
                                                                y_offset=y_offset)
                    # Skip empty datasets               
                    if len(index_arrays) == 0:
                        continue
                    # make PIL draw the tick line...
                    for index_array in index_arrays:
                        self._draw_line(draw, index_array.flatten().tolist(),  **minor_line_kwargs)

            # Draw 'major' lines
            lonlats = [ (x,lat) for x in lin_lons ]
            tmpshape.points=lonlats
            index_arrays, is_reduced = _get_pixel_index(tmpshape, area_extent, 
                                                            x_size, y_size, 
                                                            prj, 
                                                            x_offset=x_offset,
                                                            y_offset=y_offset) 
            # Skip empty datasets               
            if len(index_arrays) == 0:
                continue
            
            # make PIL draw the lines...
            for index_array in index_arrays:
                self._draw_line(draw, index_array.flatten().tolist(), **kwargs)

            # add lat text markings at each end of parallels ...
            if lat>=0.0: txt="%.2dN"%(lat)
            else: txt="%.2dS"%(-lat)
            #w,h=font.getsize(txt)
            w,h = draw.textsize(txt,font)
            bot_xy=index_array[0]
            if bot_xy[1] > 0 and bot_xy[1] < y_size:
                i=0
                while bot_xy[0] < 0:
                    i+=1
                    bot_xy = index_array[i]    
                bot_xy[0]=(x_text_margin)
                if is_agg: draw.text(bot_xy,txt, font)
                else: draw.text(bot_xy,txt, font=font, fill=kwargs['fill'])     
            top_xy=index_array[-1]
            if top_xy[1] > 0 and top_xy[1] < y_size:
                i=-1
                while top_xy[0] > x_size:
                    i-=1
                    top_xy = index_array[i]    
                top_xy[0]=(x_size-1)-(w+x_text_margin)
                if is_agg: draw.text(top_xy,txt, font)
                else: draw.text(bot_xy,txt, font=font, fill=kwargs['fill'])     


        self._finalize(draw)

    def _add_feature(self, image, area_def, feature_type, 
                     db_name, tag=None, zero_pad=False, resolution='c', 
                     level=1, x_offset=0, y_offset=0, **kwargs):
        """Add a contour feature to image
        """

        try:
            proj4_string = area_def.proj4_string
            area_extent = area_def.area_extent
        except AttributeError:
            proj4_string = area_def[0]
            area_extent = area_def[1]

        draw = self._get_canvas(image)
        
        # Area and projection info
        x_size, y_size = image.size        
        prj = pyproj.Proj(proj4_string)
        
        
        # Calculate min and max lons and lats of interest        
        lon_min, lon_max, lat_min, lat_max = \
                _get_lon_lat_bounding_box(area_extent, x_size, y_size, prj) 
        
        # Iterate through detail levels        
        for shapes in self._iterate_db(db_name, tag, resolution, 
                                       level, zero_pad):

            # Iterate through shapes
            for i, shape in enumerate(shapes):
                # Check if polygon is possibly relevant
                s_lon_ll, s_lat_ll, s_lon_ur, s_lat_ur = shape.bbox
                if (lon_max < s_lon_ll or lon_min > s_lon_ur or 
                    lat_max < s_lat_ll or lat_min > s_lat_ur):
                    # Polygon is irrelevant
                    continue          
                
                # Get pixel index coordinates of shape
                
                index_arrays, is_reduced = _get_pixel_index(shape, area_extent, 
                                                            x_size, y_size, 
                                                            prj, 
                                                            x_offset=x_offset,
                                                            y_offset=y_offset)       
                
                # Skip empty datasets               
                if len(index_arrays) == 0:
                    continue

                # Make PIL draw the polygon or line
                for index_array in index_arrays:
                    if feature_type.lower() == 'polygon' and not is_reduced:
                        # Draw polygon if dataset has not been reduced
                        #draw.polygon(index_array.flatten().tolist(), fill=fill, 
                        #             outline=outline)
                        self._draw_polygon(draw, index_array.flatten().tolist(), **kwargs)
                    elif feature_type.lower() == 'line' or is_reduced:
                        # Draw line
                        self._draw_line(draw, index_array.flatten().tolist(), **kwargs)
                        #draw.line(index_array.flatten().tolist(), fill=outline)
                    else:
                        raise ValueError('Unknown contour type: %s' % feature_type)
                        
        self._finalize(draw)

    def _iterate_db(self, db_name, tag, resolution, level, zero_pad):
        """Iterate trough datasets
        """
        
        format_string = '%s_%s_'
        if tag is not None:
            format_string += '%s_'
            
        if zero_pad:
            format_string += 'L%02i.shp' 
        else:
            format_string += 'L%s.shp'
            
        for i in range(level):
            
            # One shapefile per level
            if tag is None:
                shapefilename = \
                        os.path.join(self.db_root_path, '%s_shp' % db_name, 
                                     resolution, format_string % 
                                     (db_name, resolution, (i + 1)))
            else:
                shapefilename = \
                        os.path.join(self.db_root_path, '%s_shp' % db_name, 
                                     resolution, format_string % 
                                     (db_name, tag, resolution, (i + 1)))
            try:
                s = shapefile.Reader(shapefilename)
                shapes = s.shapes()
            except AttributeError:
                raise ShapeFileError('Could not find shapefile %s' % shapefilename)
            yield shapes
            
    def _finalize(self, draw):
        """Do any need finalization of the drawing
        """
        
        pass    


class ContourWriter(ContourWriterBase):
    """Adds countours from GSHHS and WDBII to images
    
    :Parameters:
    db_root_path : str
        Path to root dir of GSHHS and WDBII shapefiles
    """
    
    _draw_module="PIL"
    # This is a flag to make _add_grid aware of which text draw routine
    # from PIL or from aggdraw should be used (unfortunately they are not fully compatible)


    def _get_canvas(self, image):
        """Returns PIL image object
        """
        
        return ImageDraw.Draw(image)
        
    def _draw_polygon(self, draw, coordinates, **kwargs):
        """Draw polygon
        """
        
        draw.polygon(coordinates, fill=kwargs['fill'], outline=kwargs['outline'])
        
    def _draw_line(self, draw, coordinates, **kwargs):
        """Draw line
        """
        
        draw.line(coordinates, fill=kwargs['outline'])
        
    def add_grid(self,image, area_def, (Dlon,Dlat), (dlon,dlat),font=None,fill=None,outline='white',minor_outline='white',minor_is_tick=True):
        """Add a lon-lat grid to a PIL image object
        
        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        (Dlon,Dlat): (float,float)
            Major grid line separation
        (dlon,dlat): (float,float)
            Minor grid line separation
        font: PIL ImageFont object, optional
            Font for major line markings
        fill : str or (R, G, B), optional
            Text color
        outline : str or (R, G, B), optional
            Major line color
        minor_outline : str or (R, G, B), optional
            Minor line/tick color
        minor_is_tick : boolean, optional
            Use tick minor line style (True) or full minor line style (False)
        """
        self._add_grid(image, area_def, Dlon, Dlat, dlon, dlat,font,fill=fill,outline=outline, 
                       minor_outline=minor_outline,minor_is_tick=minor_is_tick)

   
    def add_coastlines(self, image, area_def, resolution='c', level=1, 
                       fill=None, outline='white', x_offset=0, y_offset=0):
        """Add coastlines to a PIL image object
        
        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4}
            Detail level of dataset
        fill : str or (R, G, B), optional
            Land color
        outline : str or (R, G, B), optional
            Coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        
        self._add_feature(image, area_def, 'polygon', 'GSHHS', 
                          resolution=resolution, level=level, 
                          fill=fill, outline=outline, x_offset=x_offset,
                                                y_offset=y_offset)
                              
    def add_coastlines_to_file(self, filename, area_def, resolution='c', 
                               level=1, fill=None, outline='white', 
                               x_offset=0, y_offset=0):
        """Add coastlines to an image file
        
        :Parameters:
        filename : str
            Image file
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4}
            Detail level of dataset
        fill : str or (R, G, B)
            Land color
        outline : str or (R, G, B), optional
            Coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction        
        """
        
        image = Image.open(filename)
        self.add_coastlines(image, area_def, 
                            resolution=resolution, level=level, 
                            fill=fill, outline=outline, x_offset=x_offset,
                            y_offset=y_offset)
        image.save(filename)

    def add_borders(self, image, area_def, resolution='c', level=1, 
                    outline='white', x_offset=0, y_offset=0):
                            
        """Add borders to a PIL image object
        
        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3}
            Detail level of dataset
        outline : str or (R, G, B), optional
            Border color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        
        self._add_feature(image, area_def, 'line', 'WDBII', 
                          tag='border', resolution=resolution, level=level, 
                          outline=outline, x_offset=x_offset,
                                                y_offset=y_offset)

    def add_borders_to_file(self, filename, area_def, resolution='c', level=1, 
                            outline='white', x_offset=0, y_offset=0):
        """Add borders to an image file
        
        :Parameters:
        image : object
            Image file
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3}
            Detail level of dataset
        outline : str or (R, G, B), optional
            Border color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        image = Image.open(filename)
        self.add_borders(image, area_def, resolution=resolution, 
                         level=level, outline=outline, x_offset=x_offset,
                         y_offset=y_offset)
        image.save(filename)
        
    def add_rivers(self, image, area_def, resolution='c', level=1, 
                   outline='white', x_offset=0, y_offset=0):
        """Add rivers to a PIL image object
        
        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
            Detail level of dataset
        outline : str or (R, G, B), optional
            River color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        
        self._add_feature(image, area_def, 'line', 'WDBII', 
                          tag='river', zero_pad=True, resolution=resolution, 
                          level=level, outline=outline, x_offset=x_offset,
                          y_offset=y_offset)
                          
    def add_rivers_to_file(self, filename, area_def, resolution='c', level=1, 
                           outline='white', x_offset=0, y_offset=0):
        """Add rivers to an image file
        
        :Parameters:
        image : object
            Image file
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
            Detail level of dataset
        outline : str or (R, G, B), optional
            River color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        
        image = Image.open(filename)
        self.add_rivers(image, area_def, resolution=resolution, level=level, 
                        outline=outline, x_offset=x_offset, y_offset=y_offset)
        image.save(filename)



class ContourWriterAGG(ContourWriterBase):
    """Adds countours from GSHHS and WDBII to images 
       using the AGG engine for high quality images.
    
    :Parameters:
    db_root_path : str
        Path to root dir of GSHHS and WDBII shapefiles
    """
    _draw_module="AGG" 
    # This is a flag to make _add_grid aware of which text draw routine
    # from PIL or from aggdraw should be used (unfortunately they are not fully compatible)


    def _get_canvas(self, image):
        """Returns AGG image object
        """
        
        import aggdraw
        return aggdraw.Draw(image)
        
    def _draw_polygon(self, draw, coordinates, **kwargs):
        """Draw polygon
        """
        
        import aggdraw
        pen = aggdraw.Pen(kwargs['outline'], kwargs['width'], kwargs['outline_opacity'])
        if kwargs['fill'] is None:
            fill_opacity = 0
        else:
            fill_opacity = kwargs['fill_opacity']
        brush = aggdraw.Brush(kwargs['fill'], fill_opacity)
        draw.polygon(coordinates, pen, brush)
        
    def _draw_line(self, draw, coordinates, **kwargs):
        """Draw line
        """
        
        import aggdraw
        pen = aggdraw.Pen(kwargs['outline'], kwargs['width'], kwargs['outline_opacity'])
        draw.line(coordinates, pen)
        
    def _finalize(self, draw):
        """Flush the AGG image object
        """
        
        draw.flush()
           
    def add_grid(self,image, area_def, (Dlon,Dlat), (dlon,dlat),font=None,fill=None, fill_opacity=255, 
                 outline='white', width=1, outline_opacity=255,
                 minor_outline='white', minor_width=0.5, minor_outline_opacity=255, minor_is_tick=True):
        """Add a lon-lat grid to a PIL image object
        
        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        (Dlon,Dlat): (float,float)
            Major grid line separation
        (dlon,dlat): (float,float)
            Minor grid line separation
        font: Aggdraw Font object, optional
            Font for major line markings
        fill_opacity : int, optional {0; 255}
            Opacity of text
        outline : str or (R, G, B), optional
            Major line color
        width : float, optional
            Major line width
        outline_opacity : int, optional {0; 255}
            Opacity of major lines
        minor_outline : str or (R, G, B), optional
            Minor line/tick color
        minor_width : float, optional
            Minor line width
        minor_outline_opacity : int, optional {0; 255}
            Opacity of minor lines/ticks
        minor_is_tick : boolean, optional
            Use tick minor line style (True) or full minor line style (False)
        """
        self._add_grid(image, area_def, Dlon, Dlat, dlon, dlat,font,fill=fill, fill_opacity=fill_opacity, 
                       outline=outline, width=width, outline_opacity=outline_opacity,
                       minor_outline=minor_outline, minor_width=minor_width, minor_outline_opacity=minor_outline_opacity,minor_is_tick=minor_is_tick)

    def add_coastlines(self, image, area_def, resolution='c', level=1, 
                       fill=None, fill_opacity=255, outline='white', width=1, 
                       outline_opacity=255, x_offset=0, y_offset=0):
        """Add coastlines to a PIL image object
        
        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4}
            Detail level of dataset
        fill : str or (R, G, B), optional
            Land color
        fill_opacity : int, optional {0; 255}
            Opacity of land color
        outline : str or (R, G, B), optional
            Coastline color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        
        self._add_feature(image, area_def, 'polygon', 'GSHHS', 
                          resolution=resolution, level=level, 
                          fill=fill, fill_opacity=fill_opacity, 
                          outline=outline, width=width,
                          outline_opacity=outline_opacity, x_offset=x_offset,
                          y_offset=y_offset)
                              
    def add_coastlines_to_file(self, filename, area_def, resolution='c', 
                               level=1, fill=None, fill_opacity=255, 
                               outline='white', width=1, outline_opacity=255, 
                               x_offset=0, y_offset=0):
        """Add coastlines to an image file
        
        :Parameters:
        filename : str
            Image file
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4}
            Detail level of dataset
        fill : str or (R, G, B), optional
            Land color
        fill_opacity : int, optional {0; 255}
            Opacity of land color
        outline : str or (R, G, B), optional
            Coastline color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction      
        """
        
        image = Image.open(filename)
        self.add_coastlines(image, area_def, resolution=resolution, 
                            level=level, fill=fill, 
                            fill_opacity=fill_opacity, outline=outline, 
                            width=width, outline_opacity=outline_opacity, 
                            x_offset=x_offset, y_offset=y_offset)
        image.save(filename)

    def add_borders(self, image, area_def, resolution='c', level=1, 
                    outline='white', width=1, outline_opacity=255, 
                    x_offset=0, y_offset=0):
                            
        """Add borders to a PIL image object
        
        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3}
            Detail level of dataset
        outline : str or (R, G, B), optional
            Border color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        
        self._add_feature(image, area_def, 'line', 'WDBII', tag='border', 
                          resolution=resolution, level=level, outline=outline, 
                          width=width, outline_opacity=outline_opacity, 
                          x_offset=x_offset, y_offset=y_offset)

    def add_borders_to_file(self, filename, area_def, resolution='c', 
                            level=1, outline='white', width=1, 
                            outline_opacity=255, x_offset=0, y_offset=0):
        """Add borders to an image file
        
        :Parameters:
        image : object
            Image file
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3}
            Detail level of dataset
        outline : str or (R, G, B), optional
            Border color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        image = Image.open(filename)
        self.add_borders(image, area_def, resolution=resolution, level=level, 
                         outline=outline, width=width, 
                         outline_opacity=outline_opacity, x_offset=x_offset,
                         y_offset=y_offset)
        image.save(filename)
        
    def add_rivers(self, image, area_def, resolution='c', level=1, 
                   outline='white', width=1, outline_opacity=255, 
                   x_offset=0, y_offset=0):
        """Add rivers to a PIL image object
        
        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
            Detail level of dataset
        outline : str or (R, G, B), optional
            River color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        
        self._add_feature(image, area_def, 'line', 'WDBII', tag='river', 
                          zero_pad=True, resolution=resolution, level=level, 
                          outline=outline, width=width, 
                          outline_opacity=outline_opacity, x_offset=x_offset,
                          y_offset=y_offset)
                          
    def add_rivers_to_file(self, filename, area_def, resolution='c', level=1, 
                           outline='white', width=1, outline_opacity=255, 
                           x_offset=0, y_offset=0):
        """Add rivers to an image file
        
        :Parameters:
        image : object
            Image file
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
            Detail level of dataset
        outline : str or (R, G, B), optional
            River color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        
        image = Image.open(filename)
        self.add_rivers(image, area_def, resolution=resolution, level=level, 
                        outline=outline, width=width, 
                        outline_opacity=outline_opacity, x_offset=x_offset,
                        y_offset=y_offset)
        image.save(filename)


def _get_lon_lat_bounding_box(area_extent, x_size, y_size, prj):
    """Get extreme lon and lat values
    """
            
    x_ll, y_ll, x_ur, y_ur = area_extent
    x_range = np.linspace(x_ll, x_ur, num=x_size)
    y_range = np.linspace(y_ll, y_ur, num=y_size)
    
    lons_s1, lats_s1 = prj(np.ones(y_range.size) * x_ll, y_range, inverse=True)
    lons_s2, lats_s2 = prj(x_range, np.ones(x_range.size) * y_ur, inverse=True)
    lons_s3, lats_s3 = prj(np.ones(y_range.size) * x_ur, y_range, inverse=True)
    lons_s4, lats_s4 = prj(x_range, np.ones(x_range.size) * y_ll, inverse=True)
    
    angle_sum = 0
    prev = None
    for lon in np.concatenate((lons_s1, lons_s2, lons_s3[::-1], lons_s4[::-1])):
        if prev is not None:
            delta = lon - prev
            if abs(delta) > 180:
                delta = (abs(delta) - 360) * np.sign(delta)
            angle_sum += delta
        prev = lon
 
    if round(angle_sum) == -360:
        # Covers NP
        lat_min = min(lats_s1.min(), lats_s2.min(), lats_s3.min(), lats_s4.min())
        lat_max = 90
        lon_min = -180
        lon_max = 180
    elif round(angle_sum) == 360:
        # Covers SP
        lat_min = -90
        lat_max = max(lats_s1.max(), lats_s2.max(), lats_s3.max(), lats_s4.max())
        lon_min = -180
        lon_max = 180        
    elif round(angle_sum) == 0:
        # Covers no poles
        lon_min = lons_s1.min()
        lon_max = lons_s3.max()
        lat_min = lats_s4.min()
        lat_max = lats_s2.max()
    else:
        # Pretty strange
        lat_min = -90
        lat_max = 90
        lon_min = -180
        lon_max = 180

    if not (-180 <= lon_min <= 180):
        lon_min = -180
    if not (-180 <= lon_max <= 180):
        lon_max = 180
    if not (-90 <= lat_min <= 90):
        lat_min = -90    
    if not (-90 <= lat_max <= 90):
        lat_max = 90
        
    return lon_min, lon_max, lat_min, lat_max
    
def _get_pixel_index(shape, area_extent, x_size, y_size, prj, 
                     x_offset=0, y_offset=0):
    """Map coordinates of shape to image coordinates
    """
    
    # Get shape data as array and reproject    
    shape_data = np.array(shape.points)
    lons = shape_data[:, 0]
    lats = shape_data[:, 1]

    x_ll, y_ll, x_ur, y_ur = area_extent

    x, y = prj(lons, lats)
 
    #Handle out of bounds
    i = 0
    segments = []
    if 1e30 in x or 1e30 in y:
        # Split polygon in line segments within projection
        is_reduced = True
        if x[0] == 1e30 or y[0] == 1e30:
            in_segment = False
        else:
            in_segment = True
            
        for j in range(x.size):
            if (x[j] == 1e30 or y[j] == 1e30):
                if in_segment:
                    segments.append((x[i:j], y[i:j]))
                    in_segment = False
            elif not in_segment:
                in_segment = True
                i = j
        if in_segment:
            segments.append((x[i:], y[i:]))
        
    else:
        is_reduced = False
        segments = [(x, y)]
                
    # Convert to pixel index coordinates                
    l_x = (x_ur - x_ll) / x_size
    l_y = (y_ur - y_ll) / y_size

    index_arrays = []
    for x, y in segments:
        n_x = ((-x_ll + x) / l_x) + 0.5 + x_offset
        n_y = ((y_ur - y) / l_y) + 0.5 + y_offset

        index_array = np.vstack((n_x, n_y)).T
        index_arrays.append(index_array)
    
    return index_arrays, is_reduced
                        
