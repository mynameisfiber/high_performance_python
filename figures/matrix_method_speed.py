#!/usr/bin/env python2.7

import csv
import numpy as np
import pylab as py

from itertools import cycle

markers = cycle('h*o>Dxsp8')
linestyles = cycle(['-', ':', '--', '-.'])

if __name__ == "__main__":
    data_raw = csv.DictReader(open("matrix_method_speed.csv"))
    data = []
    for item in data_raw:
        name = item.pop("method")
        if name != 'python':
            values = sorted((int(k), float(v)) for k, v in item.iteritems())
            data.append((name, np.asarray(values)))

    py.figure()
    for name, values in data:
        py.plot(values[:, 0], values[:, 1], linestyle=linestyles.next(),
                marker=markers.next(), label=name, linewidth=4)

    py.ylim(ymin=0, ymax=90)
    py.legend(loc='upper center', ncol=3, mode="expand", borderaxespad=0.,
              labelspacing=0.2, fontsize=12, handlelength=5)

    ax = py.gca()
    ticks = data[0][1][:, 0]
    ax.set_xticks(ticks)
    ax.set_xticklabels(["%dx%d" % (x, x)
                        for x in ticks], rotation=25, ha='right')
    py.xlim(xmin=ticks.min(), xmax=ticks.max())

    py.title("Summary of code performance")
    py.ylabel("Speedup from pure python (larger is better)")
    py.xlabel("Grid Size")
    py.tight_layout()

    py.savefig("images/matrix_method_speed.png")
    py.show()
