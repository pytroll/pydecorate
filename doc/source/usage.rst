
Usage
-----

When using the decorator the following
modules might need to be imported,

  >>> from PIL import Image
  >>> from pydecorate import DecoratorAGG
  >>> import aggdraw

From the extracted source directory, you can read
in a demonstration image to play with,

  >>> img = Image.open('BMNG_clouds_201109181715_areaT2.png')

To begin work on decorating this PIL image object you simply
instantiate a decorator object with the PIL image as argument,

  >>> dc = DecoratorAGG(img)

Logos
^^^^^
A simple use case is to add a couple of logos.
From the extracted source directory you can add a couple of
demonstration logos:

  >>> dc.add_logo("logos/pytroll_light_big.png",height=80.0)
  >>> dc.add_logo("logos/NASA_Logo.gif")
  >>> 
  >>> img.show()

.. image:: images/logo_image.png
	:width: 400px
	:align: center

Text
^^^^^^^
To add text, you could do:

  >>> dc.add_text("MSG SEVIRI\nThermal blue marble\n1/1/1977 00:00")
  >>> dc.add_logo("logos/pytroll_light_big.png")
  >>> dc.add_logo("logos/NASA_Logo.gif")
  >>> 
  >>> img.show()

.. image:: images/text_and_logo_image.png
	:width: 400px
	:align: center

Notice how the height style of the logos follow the height of the
text that was entered.  This is because the current height style of
the decorator is automatically set to match the space required by the text.

If the add_text operation fails it is may be necessary to specify the full
path to your truetype font by loading an aggdraw font object:

  >>> font=aggdraw.Font("blue","/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",size=16)

In doing so, you also can also control the font size and font colour.
To use this font you must pass it as an optional argument as so,

  >>> dc.add_text("MSG SEVIRI\nThermal blue marble\n1/1/1977 00:00",font=font)

more to come...::
