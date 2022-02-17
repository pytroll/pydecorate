#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Pydecorate developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Tests for the aggdraw-based decorator."""

import numpy as np
import pytest
from PIL import Image
from trollimage.colormap import rdbu

from pydecorate import DecoratorAGG


@pytest.mark.parametrize(
    "orientation_func_name", ["write_vertically", "write_horizontally"]
)
@pytest.mark.parametrize(
    "align_func_name", ["align_top", "align_bottom", "align_left", "align_right"]
)
@pytest.mark.parametrize("clims", [(-90, 10), (10, -90)])
def test_colorbar(tmp_path, orientation_func_name, align_func_name, clims):
    img = Image.fromarray(np.zeros((200, 100, 3), dtype=np.uint8))
    dc = DecoratorAGG(img)
    getattr(dc, align_func_name)()
    getattr(dc, orientation_func_name)()
    cmap = rdbu.set_range(*clims, inplace=False)
    dc.add_scale(cmap, extend=True, tick_marks=5.0, line_opacity=100, unit="K")
    img.save(tmp_path / "style_retention.png")
