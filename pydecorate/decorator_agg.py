"""Aggdraw-based image decoration class."""

from pathlib import Path

import aggdraw

from pydecorate.decorator_base import DecoratorBase

HERE = Path(__file__).parent


class DecoratorAGG(DecoratorBase):
    """Aggdraw-based image decoration class."""

    def add_scale(self, colormap, **kwargs):
        self._add_scale(colormap, **kwargs)

    def _load_default_font(self):
        font_path = HERE / "fonts" / "DejaVuSerif.ttf"
        return aggdraw.Font("black", font_path.as_posix(), size=16)

    def _load_font(self):
        try:
            return aggdraw.Font(
                self.style["line"], self.style["font"], self.style["font_size"]
            )
        except IOError:
            raise

    def add_text(self, txt, **kwargs):
        self._add_text(txt, **kwargs)

    def add_logo(self, logo_path, **kwargs):
        self._add_logo(logo_path, **kwargs)

    def _get_canvas(self, image):
        """Return AGG image object."""
        return aggdraw.Draw(image)

    def _finalize(self, draw):
        """Flush the AGG image object."""
        draw.flush()

    def _draw_text_line(self, draw, xy, text, font, fill="black"):
        draw.text(xy, text, font)

    def _draw_rectangle(
        self,
        draw,
        xys,
        outline="white",
        bg="white",
        bg_opacity=255,
        outline_width=1,
        outline_opacity=255,
        **kwargs,
    ):
        pen = aggdraw.Pen(outline, width=outline_width, opacity=outline_opacity)
        brush = aggdraw.Brush(bg, opacity=bg_opacity)
        # draw bg and outline
        # bg unaliased (otherwise gaps between successive bgs)

        if bg is not None:
            draw.setantialias(False)
            draw.rectangle(xys, None, brush)
            draw.setantialias(True)
        # adjust to correct for outline exceeding requested area,
        # due to outline width expanding outwards.
        xys[0] += outline_width / 2.0
        xys[1] += outline_width / 2.0
        xys[2] -= outline_width / 2.0
        xys[3] -= outline_width / 2.0
        if outline is not None:
            draw.rectangle(xys, pen, None)

    def _draw_line(self, draw, xys, **kwargs):
        if kwargs["line"] is None:
            pen = None
        else:
            pen = aggdraw.Pen(
                kwargs["line"],
                width=kwargs["line_width"],
                opacity=kwargs["line_opacity"],
            )
        xys_straight = [item for t in xys for item in t]
        draw.line(xys_straight, pen)

    def _draw_polygon(
        self,
        draw,
        xys,
        outline=None,
        fill="white",
        fill_opacity=255,
        outline_width=1,
        outline_opacity=255,
    ):
        if outline is None:
            pen = None
        else:
            pen = aggdraw.Pen(outline, width=outline_width, opacity=outline_opacity)
        if fill is None:
            brush = None
        else:
            brush = aggdraw.Brush(fill, opacity=fill_opacity)
        xys_straight = [item for t in xys for item in t]
        draw.polygon(xys_straight, pen, brush)
