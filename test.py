#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Basic test cases of pydecorate.

NOTE: These aren't proper unit tests

"""


def test_style_retention():
    from PIL import Image
    from pydecorate import DecoratorAGG
    import aggdraw
    from trollimage.colormap import rdbu

    font = aggdraw.Font("navy", "pydecorate/fonts/DejaVuSerif.ttf", size=20)
    font_scale = aggdraw.Font("black", "pydecorate/fonts/DejaVuSerif.ttf", size=12)

    rdbu.colors = rdbu.colors[::-1]
    rdbu.set_range(-90, 10)

    img = Image.open('BMNG_clouds_201109181715_areaT2.png')
    dc = DecoratorAGG(img)


    #dc.write_vertically()
    #dc.add_logo("logos/pytroll_light_big.png")
    #dc.add_logo("logos/NASA_Logo.gif",margins=[10,10],bg='yellow')
    #dc.add_logo("logos/pytroll_light_big.png")
    font = aggdraw.Font("blue", "pydecorate/fonts/DejaVuSerif.ttf", size=16)
    #dc.add_text("Some text",font=font)


    #dc.align_right()
    dc.add_scale(rdbu, extend=True, tick_marks=5.0, line_opacity=100, unit='K')

    #dc.align_bottom()
    #dc.add_scale(rdbu, extend=True, tick_marks=2.0, line_opacity=100, width=60)

    #dc.align_right()
    #dc.write_vertically()
    dc.align_bottom()
    dc.add_scale(rdbu, extend=True, tick_marks=5.0, line_opacity=100, unit='K')

    #dc.align_left()
    #dc.add_scale(rdbu, extend=True, font=font_scale, tick_marks=2.0, minor_tick_marks=1.0, line_opacity=100, width=60, unit='K')

    # img.show()
    img.save("style_retention.png")

    # #dc.align_right()
    # #dc.align_bottom()
    # #dc.add_logo("logos/pytroll_light_big.png")
    # #dc.add_logo("logos/NASA_Logo.gif")
    # #dc.add_text("This is manually\nplaced text\nover here.",cursor=[400,480])
    # dc.new_line()
    # dc.add_text("This here is\na new line\nof features")
    # dc.add_logo("logos/pytroll_light_big.png")
    #
    # dc.align_right()
    # dc.write_vertically()
    # dc.add_text("Now writing\nvertically",height=0)
    # dc.add_logo("logos/pytroll_light_big.png")
    # dc.add_logo("logos/NASA_Logo.gif")
    #
    #
    # img.show()
    # return
    #
    #
    #
    # #dc.toggle_direction()
    # dc.add_logo("logos/pytroll_light_big.png",height=60)
    # dc.add_logo("logos/NASA_Logo.gif")
    #
    # dc.toggle_direction()
    # dc.bottom_align()
    # dc.right_align()
    # dc.add_text("MSG SEVIRI\nThermal",font=font)
    #
    # dc.bottom_align()
    # dc.add_logo("logos/NASA_Logo.gif")
    #
    # img.show()
    # return
    #
    # dc.new_line()
    # dc.add_logo("logos/pytroll_light_big.png")
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.toggle_direction()
    # dc.bottom_align()
    # dc.right_align()
    # dc.add_text("MSG SEVIRI\nThermal",font=font)
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.bottom_align()
    # dc.left_align()
    # dc.add_text("MSG SEVIRI\nThermal",font=font)
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.new_line()
    # dc.add_text("MSG SEVIRI\nThermal",font=font)
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.right_align()
    # dc.add_text("MSG SEVIRI\nThermal",font=font)
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.new_line()
    # dc.add_text("MSG SEVIRI\nThermal",font=font)
    # dc.add_logo("logos/NASA_Logo.gif")
    # img.show()
    # return
    #
    #
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.bottom_align()
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.new_line()
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.add_text("MSG SEVIRI\nThermal blue marble\n1/1/1977 00:00",font=font)
    # dc.right_align()
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.new_line()
    # dc.add_logo("logos/NASA_Logo.gif")
    # dc.add_text("MSG SEVIRI\nThermal blue marble\n1/1/1977 00:00",font=font)
    # dc.top_align()
    # dc.add_logo("logos/pytroll_light_big.png")
    #
    # #dc.add_logo("logos/eumetsat2.png")
    # #dc.add_logo("logos/NASA_Logo.gif",height=80.0,bg='white',bg_opacity=130,outline=None,margins=(5,5))
    # #dc.add_logo("logos/vi-logo-350x350.gif",bg='white',bg_opacity=130,outline=None,margins=(5,5))
    # #dc.add_text("Hello\nDate so and so\nand more\nandmore", font=font)
    #
    #
    # img.show()


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main())
