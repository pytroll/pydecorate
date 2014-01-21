
.. sectnum::
   :depth: 4
   :start: 2
   :suffix: .

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

logos
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

text
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

placement
^^^^^^^^^^^^^^
The decorator allows the cursor to be relocated and alligned to different sides of the image.
By default the cursor writes horizontally from the top-left corner. The cursor can however be
easily relocated at any other side of the image, and the vertical and horizontal write orientation
can be changed.

alignment
++++++++++++++
Continuing from the previous example, 
we can align the cursor to the bottom-right corner, by executing

  >>> dc.align_right()
  >>> dc.align_bottom()

New features will now be written horizontally from the bottom-right corner
progressing leftwards. E.g.

  >>> dc.add_logo("logos/pytroll_light_big.png")
  >>> dc.add_logo("logos/NASA_Logo.gif")

.. image:: images/alignment_image1.png
	:width: 400px
	:align: center

Note: Currently the decorator does not provide an easy option for centered placement
of features. However the cursor position may be set manually as part of the style
arguments to achieve this kind of placement, e.g.

  >>> dc.add_text("This is a manually\nplaced text\nover here.", cursor=[400,480])

.. image:: images/alignment_image2.png
	:width: 400px
	:align: center

new line
+++++++++
As with typewriters, the decorator can also progress to a new line of features.
Starting from our first example,

  >>> dc.new_line()
  >>> dc.add_text("This here is\na new line\nof features")
  >>> dc.add_logo("logos/pytroll_light_big.png")

.. image:: images/alignment_image3.png
	:width: 400px
	:align: center

horizontal/vertical writing
++++++++++++++++++++++++++++
The orientation of the cursor writes can be changed from vertical to horizontal writing.
The following statements will write some features vertically,

  >>> dc.align_right()
  >>> dc.write_vertically()
  >>>
  >>> dc.add_text("Now writing\nvertically", height=0)
  >>> dc.add_logo("logos/pytroll_light_big.png")
  >>> dc.add_logo("logos/NASA_Logo.gif")

Note that resetting the height of text to zero prevents the text feature from inheriting the height
of the previously added feature and allows it to expand to the necessary height.

.. image:: images/alignment_image4.png
	:width: 400px
	:align: center

Styles
^^^^^^^^^^^^^^
more to come here...


