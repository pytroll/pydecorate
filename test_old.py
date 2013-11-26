#!/usr/bin/python
# -*- coding: latin-1 -*-

from PIL import Image, ImageFont
from pydecorate_old import DecoratorAGG
import aggdraw
from pydecorate_old.colormap import ColorMap

proj4_string = '+proj=stere +lon_0=8.00 +lat_0=50.00 +lat_ts=50.00 +ellps=WGS84'
area_extent = (-3363403.31,-2291879.85,2630596.69,2203620.1)
area_def = (proj4_string, area_extent)



#font=ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",22)
#font_scale=ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",16)
font=aggdraw.Font("blue","/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",size=16)
font_scale=aggdraw.Font("white","/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",size=12)

img = Image.open('BMNG_clouds_201109181715_areaT2.png')


scale_def={-0.3:[(1,0,0),"lin"],
       0.123:[(0,0,0),"con"],
       0.5:[(0,1,1),"con"],
       1:[(0,0.5,1),""],
       1.4:[(1.0,0.3,0.0),"lin"],
       2.55:[(1,1,0),"lin"]}
cm = ColorMap(scale=scale_def)
cm.above_extend=None

dc = DecoratorAGG(img)
#dc.add_scale(cm,extend=True,font=font_scale,fill='white',bg='black',bg_opacity=70,outline=None,outline_width=1.0,unit='°C',margins=(15,5),minortick=0.05,nan_color=(1,0,0),nan_check_color=(0,0.5,0.5),nan_check_size=5)
#dc.new_line()
#dc.start_border()
dc.add_logo("logos/NASA_Logo.gif",height=80.0,bg='white',bg_opacity=130,outline=None,margins=(5,5))
dc.add_logo("logos/eumetsat2.png",bg='white',bg_opacity=130,outline=None)
dc.add_logo("logos/vi-logo-350x350.gif",bg='white',bg_opacity=130,outline=None,margins=(5,5))
dc.add_text("Hello\nDate so and so", font=font,outline=None,fill='black',bg='white',bg_opacity=130)
dc.add_scale(cm,extend=True,font=font_scale,fill='white',bg='black',bg_opacity=70,outline=None,outline_width=1.0,unit='°C',margins=(15,5),minortick=0.05,nan_color=(1,0,0),nan_check_color=(0,0.5,0.5),nan_check_size=5)
#dc.end_border(outline='blue',outline_width=1.0)
dc.bottom_align()
dc.add_scale(cm,extend=True,font=font_scale,fill='blue',bg_opacity=130,outline='blue',outline_width=1.0,unit='°C',margins=(15,5),minortick=0.05,nan_check_size=5)
dc.new_line()
dc.add_scale(cm,extend=True,font=font_scale,fill='blue',bg_opacity=130,outline='blue',outline_width=1.0,unit='°C',margins=(15,5),minortick=0.05,nan_check_size=5)

img.show()
     
