import csv
import dateutil

import pylab as py
import matplotlib.dates as mdates

if __name__ == "__main__":
    data = list(csv.DictReader(open("processor.csv")))
    dates = [dateutil.parser.parse(x['date']) for x in data if x['date']]
    clock = [x['clock'] for x in data if x['date']]

    ax = py.gca()
    fig = py.gcf()

    ax.scatter(mdates.date2num(dates), clock, alpha=0.5)
    ax.set_xticklabels([d.strftime("%Y") for d in mdates.num2date(
        ax.get_xticks())], rotation=15, ha='right')
    ax.set_yscale('log')

    ax.set_ylabel("Clock speed (MHz)")
    ax.set_xlabel("Date of CPU Release")
    ax.set_title("Historical growth of CPU clock speed")

    py.savefig("images/processor_clock.png")
    py.show()
