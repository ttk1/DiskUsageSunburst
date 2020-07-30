#!/bin/env python

import os
import time

from plotly import graph_objects as go


labels = []
parents = []
values = []


def f(current, parent):
    total = 0
    if os.path.islink(current):
        return 0
    elif os.path.isfile(current):
        total = os.path.getsize(current)
    else:
        try:
            children = os.scandir(current)
        except:
            return 0
        for child in children:
            total += f(child.path, current)

    # 数が多いと激重なので、100 MiB以下のファイル・フォルダは表示しない
    if total > 100 * 1024 ** 2:
        labels.append(current)
        parents.append(parent)
        values.append(total / 1024 ** 3)

    return total


if __name__ == '__main__':
    start = time.time()

    # calc size
    f('c:\\', '')

    trace = go.Sunburst(
        name='',
        labels=labels,
        parents=parents,
        values=values,
        hovertemplate=(
            '<b>%{label}</b><br>'
            'size: %{value:.2f} GiB<br>'
        ),
        branchvalues='total'
    )

    figure = go.Figure(
        data=trace
    )
    figure.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    figure.write_html('out.html')

    print('elapsed_time:{0:.2f} sec'.format(time.time() - start))
