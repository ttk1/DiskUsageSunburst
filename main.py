#!/bin/env python

import os
import time

from plotly import graph_objects as go


values = []
labels = []
parents = []


def f(current, parent):
    total = 0

    try:
        children = os.scandir(current)
    except:
        return 0

    for child in children:
        if child.is_file(follow_symlinks=False):
            try:
                total += os.path.getsize(child.path)
            except:
                pass
        elif child.is_dir(follow_symlinks=False):
            total += f(child.path, current)

    # 数が多いと激重なので、100 MiB以下のフォルダは表示しない
    if total > 100 * 1024 ** 2:
        values.append(total / 1024 ** 3)
        labels.append(current)
        parents.append(parent)

    return total


if __name__ == '__main__':
    start = time.time()

    # calc size
    f('c:\\', '')

    trace = go.Sunburst(
        name='',
        values=values,
        labels=labels,
        parents=parents,
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