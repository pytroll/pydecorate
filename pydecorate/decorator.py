"""PIL-based image decoration class."""

from PIL import ImageDraw, ImageFont

from .decorator_base import DecoratorBase


class Decorator(DecoratorBase):
    """PIL-based image decoration class."""

    def add_scale(
        self,
        color_def,
        font=None,
        size=None,
        fill="black",
        outline=None,
        outline_width=1,
        bg="white",
        extend=False,
        unit="",
        margins=None,
        minortick=0.0,
        nan_color=(0, 0, 0),
        nan_check_color=(1, 1, 1),
        nan_check_size=0,
    ):
        self._add_scale(
            color_def,
            font=font,
            size=size,
            fill=fill,
            outline=outline,
            outline_widht=outline_width,
            bg=bg,
            extend=extend,
            unit=unit,
            margins=margins,
            minortick=minortick,
            nan_color=nan_color,
            nan_check_color=nan_check_color,
            nan_check_size=nan_check_size,
        )

    def _load_default_font(self):
        return ImageFont.load_default()

    def add_text(self, txt, **kwargs):
        self._add_text(txt, **kwargs)

    def add_logo(self, logo_path, **kwargs):
        self._add_logo(logo_path, **kwargs)

    def _get_canvas(self, image):
        """Return PIL image object."""
        return ImageDraw.Draw(image)
