#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
from PIL import Image
from pydecorate import DecoratorCairo

from trollimage.colormap import rdbu
rdbu.colors = rdbu.colors[::-1]
rdbu.set_range(-90, 10)

base_image_path = '20160902_140512.png'
result_image_path = os.path.splitext(base_image_path)[0] + "_test.png"

dc = DecoratorCairo(base_image_path)

#dc.align_right()
#dc.align_left()
#dc.align_bottom()
#dc.align_top()
#dc.write_vertically()
#dc.write_horizontally()
#dc.add_text("testo e \ntesto")
#dc.add_logo("logos/vi-logo-350x350.png")

dc.align_top()
dc.align_left()
#dc.write_vertically()
dc.add_scale(rdbu, extend=True, tick_marks=5.0, line_opacity=100, unit='C')
dc.align_bottom()
dc.align_right()
dc.add_logo("logos/pytroll_light_big.png")
dc.add_logo("logos/pytroll_light_big.png")
dc.save_png(result_image_path)

result = Image.open(result_image_path)
result.show()

exit()

