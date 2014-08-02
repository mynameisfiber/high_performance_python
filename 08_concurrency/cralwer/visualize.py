import pylab as py
import ujson as json

if __name__ == "__main__":
    raw_data = json.load(open("metric_data.json"))

    for name, values in raw_data.iteritems():
        print(name)
        py.figure()
        py.title("Call timeline for {}".format(name))
        min_t = values[0]['start']
        for i, data in enumerate(values):
            py.plot([data["start"] - min_t, data["end"] - min_t], [i, i])
        py.xlabel("Time")
        py.ylabel("Reuqest Number")
        py.savefig("images/{}.png".format(name))
