# Copyright (C) 2025
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *
import math


class RightTriangleBox(Boxes):
    """Closed box with right-angled triangular cross-section"""

    ui_group = "Box"

    description = """A closed box with a right-angled triangular cross-section.
The box has two triangular end faces (top and bottom) and three rectangular
wall faces connecting the triangle edges."""

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        
        # Add standard box arguments
        self.buildArgParser("outside")
        
        # Custom arguments for triangle box
        self.argparser.add_argument(
            "--base", action="store", type=float, default=100.0,
            help="length of the base edge (horizontal leg) in mm"
        )
        self.argparser.add_argument(
            "--height", action="store", type=float, default=80.0,
            help="height of the triangle (vertical leg) in mm"
        )
        self.argparser.add_argument(
            "--depth", action="store", type=float, default=50.0,
            help="depth/thickness of the box (extends triangle into 3D) in mm"
        )
        self.argparser.add_argument(
            "--bottom_edge", action="store", type=str, default="f",
            help="type of edge for bottom triangle"
        )
        self.argparser.add_argument(
            "--top_edge", action="store", type=str, default="F",
            help="type of edge for top triangle"
        )
        self.argparser.add_argument(
            "--wall_edge", action="store", type=str, default="f",
            help="type of edge for rectangular walls"
        )

    def render(self):
        base = self.base
        height = self.height
        depth = self.depth
        bottom_edge = self.bottom_edge
        top_edge = self.top_edge
        wall_edge = self.wall_edge
        t = self.thickness

        # Adjust dimensions if outside measurements specified
        if self.outside:
            base = self.adjustSize(base)
            height = self.adjustSize(height)
            depth = self.adjustSize(depth)

        # Calculate hypotenuse (diagonal edge of right triangle)
        hypotenuse = math.sqrt(base ** 2 + height ** 2)

        # Wall 1: Along the base edge (horizontal)
        # Edges: bottom, right, top, left (in order around the rectangle)
        self.rectangularWall(
            base, depth,
            edges=f"{bottom_edge}{wall_edge}{top_edge}{wall_edge}",
            move="right",
            label="Wall 1 (base)"
        )

        # Wall 2: Along the height edge (vertical)
        self.rectangularWall(
            height, depth,
            edges=f"{bottom_edge}{wall_edge}{top_edge}{wall_edge}",
            move="right",
            label="Wall 2 (height)"
        )

        # Wall 3: Along the hypotenuse (diagonal)
        self.rectangularWall(
            hypotenuse, depth,
            edges=f"{bottom_edge}{wall_edge}{top_edge}{wall_edge}",
            move="right",
            label="Wall 3 (hypotenuse)"
        )

        # Bottom triangular face
        # Edges: bottom, right, diagonal/hypotenuse
        self.rectangularTriangle(
            base, height,
            edges=f"{bottom_edge}{wall_edge}{wall_edge}",
            move="right",
            label="Bottom triangle"
        )

        # Top triangular face
        self.rectangularTriangle(
            base, height,
            edges=f"{top_edge}{wall_edge}{wall_edge}",
            move="right",
            label="Top triangle"
        )

