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

from pathlib import Path
from unittest import mock

import numpy as np
import pytest
from numpy.typing import NDArray
from PIL import Image
from trollimage.colormap import rdbu

from pydecorate import DecoratorAGG

HERE = Path(__file__).parent
REPO = HERE.parent.parent


@pytest.mark.parametrize(
    "orientation_func_name", ["write_vertically", "write_horizontally"]
)
@pytest.mark.parametrize(
    "align_func_name", ["align_top", "align_bottom", "align_left", "align_right"]
)
@pytest.mark.parametrize("clims", [(-90, 10), (10, -90)])
def test_colorbar(tmp_path, orientation_func_name, align_func_name, clims):
    fn = tmp_path / "test_colorbar.png"
    shape = (
        (400, 100, 3) if orientation_func_name == "write_vertically" else (100, 400, 3)
    )
    img = Image.fromarray(np.zeros(shape, dtype=np.uint8))
    dc = DecoratorAGG(img)
    getattr(dc, align_func_name)()
    getattr(dc, orientation_func_name)()
    cmap = rdbu.set_range(*clims, inplace=False)
    with mock.patch.object(dc, "_draw_text", wraps=dc._draw_text) as draw_text_wrapper:
        dc.add_scale(
            cmap,
            extend=True,
            tick_marks=40.0,
            minor_tick_marks=20.0,
            line_opacity=100,
            unit="K",
        )
    img.save(fn)
    assert_colorbar_increasing_tick_order(draw_text_wrapper)

    # check results
    output_img = Image.open(fn)
    arr = np.array(output_img)
    clims_flipped = clims[0] > clims[1]
    assert_colorbar_orientation_alignment(
        arr, orientation_func_name, align_func_name, clims_flipped
    )


def test_add_logo(tmp_path):
    fn = tmp_path / "add_logo_pytroll.png"
    img = Image.fromarray(np.zeros((200, 200, 3), dtype=np.uint8))
    dc = DecoratorAGG(img)
    dc.add_logo(REPO / "logos" / "pytroll_light_big.png")
    img.save(fn)

    # Check results
    output_img = Image.open(fn)
    arr = np.array(output_img)
    assert not (arr == 0).all()
    assert (arr[-1, -1, :] == 0).all(), "logo is in top left corner"


def assert_colorbar_increasing_tick_order(draw_text_wrapper) -> None:
    last_float_text = None
    for call_args in draw_text_wrapper.call_args_list:
        if call_args.args[1] == (0, 0):
            # skip call to draw text for size reference
            continue

        try:
            txt_as_float = float(call_args.args[2])
        except ValueError:
            continue

        if last_float_text is None:
            last_float_text = txt_as_float
            continue

        assert last_float_text <= txt_as_float
        last_float_text = txt_as_float


def assert_colorbar_orientation_alignment(
    img_arr: NDArray,
    orientation_func_name: str,
    align_func_name: str,
    clims_flipped: bool,
) -> None:
    cbar_size = 60
    check_idx = int(cbar_size // 2.5)  # not likely to run into ticks or tick labels
    cbar_len_start_offset = 5
    cbar_len_stop_offset = 45
    cbar_offset_slice = slice(cbar_len_start_offset, -cbar_len_stop_offset)
    # NOTE: "top" of image is row 0
    if orientation_func_name == "write_vertically":
        if align_func_name in ("align_left", "align_top", "align_bottom"):
            assert np.unique(img_arr[cbar_offset_slice, check_idx]).size >= 100
            np.testing.assert_allclose(img_arr[:, cbar_size:], 0)
            _check_color_orientation(
                img_arr[-cbar_len_stop_offset - 20, check_idx],  # bottom pixel
                img_arr[cbar_len_start_offset + 25, check_idx],  # top pixel
                clims_flipped,
            )
        else:
            assert np.unique(img_arr[:, -check_idx]).size >= 100
            np.testing.assert_allclose(img_arr[:, :-cbar_size], 0)
            _check_color_orientation(
                img_arr[-cbar_len_stop_offset - 20, -check_idx],  # bottom pixel
                img_arr[cbar_len_start_offset + 25, -check_idx],  # top pixel
                clims_flipped,
            )
    else:
        if align_func_name in ("align_top", "align_left", "align_right"):
            assert np.unique(img_arr[check_idx, :]).size >= 100
            np.testing.assert_allclose(img_arr[cbar_size:, :], 0)
            _check_color_orientation(
                img_arr[check_idx, cbar_len_start_offset + 25],  # left pixel
                img_arr[check_idx, -cbar_len_stop_offset - 20],  # right pixel
                clims_flipped,
            )
        else:
            assert np.unique(img_arr[-check_idx:, :]).size >= 100
            np.testing.assert_allclose(img_arr[:-cbar_size, :], 0)
            _check_color_orientation(
                img_arr[-check_idx, cbar_len_start_offset + 25],  # left pixel
                img_arr[-check_idx, -cbar_len_stop_offset - 20],  # right pixel
                clims_flipped,
            )


def _check_color_orientation(
    first_pixel: NDArray, last_pixel: NDArray, clims_flipped: bool
) -> None:
    if clims_flipped:
        _check_expected_blue_colorbar_pixel(first_pixel)
        _check_expected_red_colorbar_pixel(last_pixel)
    else:
        _check_expected_red_colorbar_pixel(first_pixel)
        _check_expected_blue_colorbar_pixel(last_pixel)


def _check_expected_red_colorbar_pixel(red_pixel: NDArray) -> None:
    assert red_pixel[0] > 140  # decently red
    assert red_pixel[1] < 64  # not a lot of green
    assert red_pixel[2] < 64  # not a lot of blue


def _check_expected_blue_colorbar_pixel(blue_pixel: NDArray) -> None:
    assert blue_pixel[0] < 32  # not a lot of red
    assert blue_pixel[1] < 100  # not a lot of green
    assert blue_pixel[2] > 128  # decently blue
