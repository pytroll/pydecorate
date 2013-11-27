
Usage
-----

A simple use case, adding a couple of logos.
From the extracted source directory do::

  >>> from PIL import Image
  >>> from pydecorate import DecoratorAGG
  >>> import aggdraw
  >>>
  >>> img = Image.open('BMNG_clouds_201109181715_areaT2.png')
  >>> dc = DecoratorAGG(img)
  >>> dc.add_logo("logos/pytroll_light_big.png",height=80.0)
  >>> dc.add_logo("logos/NASA_Logo.gif")
  >>> 
  >>> img.show()

.. image:: images/logo_image.png
	:width: 400px
	:align: center

and to add text labes,
more to come...::
