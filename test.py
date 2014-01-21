#!/usr/bin/python
# -*- coding: latin-1 -*-

from PIL import Image
from pydecorate import DecoratorAGG
import aggdraw

font=aggdraw.Font("navy","/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",size=20)
font_scale=aggdraw.Font("white","/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",size=12)

from trollimage.colormap import rdbu
rdbu.set_range(-90, 10)
print type(rdbu)


img = Image.open('BMNG_clouds_201109181715_areaT2.png')
dc = DecoratorAGG(img)
font=aggdraw.Font("blue","/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",size=16)

#dc.write_vertically()
#dc.add_text("MSG SEVIRI\nThermal blue marble\n1/1/1977 00:00",font=font)
dc.add_logo("logos/pytroll_light_big.png")
dc.add_logo("logos/NASA_Logo.gif")
dc.add_scale(rdbu,extend=True)


img.show()
exit()


















#dc.align_right()
#dc.align_bottom()
#dc.add_logo("logos/pytroll_light_big.png")
#dc.add_logo("logos/NASA_Logo.gif")
#dc.add_text("This is manually\nplaced text\nover here.",cursor=[400,480])
dc.new_line()
dc.add_text("This here is\na new line\nof features")
dc.add_logo("logos/pytroll_light_big.png")

dc.align_right()
dc.write_vertically()
dc.add_text("Now writing\nvertically",height=0)
dc.add_logo("logos/pytroll_light_big.png")
dc.add_logo("logos/NASA_Logo.gif")


img.show()
exit()



#dc.toggle_direction()
dc.add_logo("logos/pytroll_light_big.png",height=60)
dc.add_logo("logos/NASA_Logo.gif")

dc.toggle_direction()
dc.bottom_align()
dc.right_align()
dc.add_text("MSG SEVIRI\nThermal",font=font)

dc.bottom_align()
dc.add_logo("logos/NASA_Logo.gif")

img.show()
exit()

dc.new_line()
dc.add_logo("logos/pytroll_light_big.png")
dc.add_logo("logos/NASA_Logo.gif")
dc.toggle_direction()
dc.bottom_align()
dc.right_align()
dc.add_text("MSG SEVIRI\nThermal",font=font)
dc.add_logo("logos/NASA_Logo.gif")
dc.bottom_align()
dc.left_align()
dc.add_text("MSG SEVIRI\nThermal",font=font)
dc.add_logo("logos/NASA_Logo.gif")
dc.new_line()
dc.add_text("MSG SEVIRI\nThermal",font=font)
dc.add_logo("logos/NASA_Logo.gif")
dc.right_align()
dc.add_text("MSG SEVIRI\nThermal",font=font)
dc.add_logo("logos/NASA_Logo.gif")
dc.new_line()
dc.add_text("MSG SEVIRI\nThermal",font=font)
dc.add_logo("logos/NASA_Logo.gif")
img.show()
exit()


dc.add_logo("logos/NASA_Logo.gif")
dc.bottom_align()
dc.add_logo("logos/NASA_Logo.gif")
dc.add_logo("logos/NASA_Logo.gif")
dc.new_line()
dc.add_logo("logos/NASA_Logo.gif")
dc.add_text("MSG SEVIRI\nThermal blue marble\n1/1/1977 00:00",font=font)
dc.right_align()
dc.add_logo("logos/NASA_Logo.gif")
dc.add_logo("logos/NASA_Logo.gif")
dc.new_line()
dc.add_logo("logos/NASA_Logo.gif")
dc.add_text("MSG SEVIRI\nThermal blue marble\n1/1/1977 00:00",font=font)
dc.top_align()
dc.add_logo("logos/pytroll_light_big.png")

#dc.add_logo("logos/eumetsat2.png")
#dc.add_logo("logos/NASA_Logo.gif",height=80.0,bg='white',bg_opacity=130,outline=None,margins=(5,5))
#dc.add_logo("logos/vi-logo-350x350.gif",bg='white',bg_opacity=130,outline=None,margins=(5,5))
#dc.add_text("Hello\nDate so and so\nand more\nandmore", font=font)


img.show()

