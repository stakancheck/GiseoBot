#  Copyright 2023. Artem Sukhanov
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  SPDX-License-Identifier: GPL-3.0-or-later

import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pprint import pprint
from decouple import config
import matplotlib
import matplotlib.pyplot as plt
from tools import DbTools, base_model
matplotlib.use('Agg')
project_path = config('PATH_P')


def plot_image(data, theme, chat_id, file):

    x = [1, 2, 3, 4]
    y = data

    plt.plot(x, y, 'o-r', alpha=0.7, label="first", lw=5, mec='b', mew=2, ms=10)
    plt.grid(True)
    plt.savefig(f'{project_path}\\data\\assets\\user_{chat_id}\\{file}')


def creation_image(data, labels, theme, chat_id, file):
    # Style images
    if theme == 'theme_1':
        facecolor = '#F5F0E1'
        bordercolor = '#1E3D59'
        textcolor = '#1E3D59'

    elif theme == 'theme_2':
        facecolor = '#252525'
        bordercolor = '#515151'
        textcolor = '#FFFFFF'

    else:
        facecolor = '#172532'
        bordercolor = '#FFFFFF'
        textcolor = '#FFFFFF'

    # Create table
    df = pd.DataFrame(np.array(data))
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Hide axes border
    plt.box(on=None)
    table = plt.table(cellText=df.values, loc='center', rowLoc='left', cellLoc='left', colLabels=labels)
    # plt.rcParams["font.family"] = "monospace"
    table.set_fontsize(10)
    table.scale(1, 1.5)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    for item in table.get_celld():
        is_homework: table.get_celld()[item[0], 1].set_text_props(horizontalalignment='left')
        table.get_celld()[item].set_facecolor(facecolor)
        table.get_celld()[item].set_edgecolor(bordercolor)
        table.get_celld()[item].set_linewidth(0.8)
        table[item].get_text().set_color(textcolor)

    plt.subplots_adjust(left=0.5, right=0.6, top=0.9, bottom=0.1)

    # Save table as image in "assets" folder
    plt.savefig(f'{project_path}\\data\\assets\\user_{chat_id}\\{file}', bbox_inches='tight',
                facecolor=facecolor, dpi=150)
    # , pad_inches = 0.1
    plt.close()

