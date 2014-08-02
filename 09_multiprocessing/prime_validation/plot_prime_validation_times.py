import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Project description')
parser.add_argument(
    '--slow',
    action="store_true",
    default=False,
    help='if present then draw slow result, if not then fast results')
args = parser.parse_args()

labels = ["small non-prime", "large non-prime 1",
          "large non-prime 2", "prime 1", "prime 2"]

times_primes = [0.000002, 3.54, 6.35, 11.72, 11.74]
times_primes_pool_per_number1 = [0.09, 2.93, 2.97, 3.09, 2.98]
times_primes_pool_per_number2 = [0.000002, 2.95, 2.94, 2.99, 3.01]
times_primes_pool_per_number_redis = [0.00007, 1.48, 1.2, 8.05, 7.84]

times_primes_pool_per_number_manager = [0.00003, 1.32, 1.09, 6.5, 6.5]
times_primes_pool_per_number_value = [0.000002, 0.94, 0.78, 4.69, 4.68]
times_primes_pool_per_number_mmap = [0.000003, 0.92, 0.77, 4.59, 4.59]
times_primes_pool_per_number_mmap3 = [0.000003, 0.61, 0.50, 3.03, 3.04]

# , "Manager flag", "Value flag", "MMap flag"]
method_labels_slower = [
    "Serial (No IPC)", "Less naive Pool", "Redis flag", "Manager flag"]
all_times_slower = [times_primes,
                    times_primes_pool_per_number2,
                    times_primes_pool_per_number_redis,
                    times_primes_pool_per_number_manager]

method_labels_faster = [
    "Less naive Pool", "RawValue flag", "MMap flag", "MMap Redux flag"]
all_times_faster = [times_primes_pool_per_number2,
                    times_primes_pool_per_number_value,
                    times_primes_pool_per_number_mmap,
                    times_primes_pool_per_number_mmap3]

if args.slow:
    png_filename = "multiprocessing_plot_prime_validation_times_slower_results.png"
    print "Writing to", png_filename
    symbols = ["o", "v", "s", "^", "*", "+", "x"]
    linestyles = ["-", "--", "-.", ":", "-"]
    all_times = all_times_slower
    method_labels = method_labels_slower
    title = "Slower IPC methods"
    ymax = 12
else:
    png_filename = "multiprocessing_plot_prime_validation_times_faster_results.png"
    symbols = ["v", "o", "s", "^", "*", "+", "x"]
    linestyles = ["--", "-", "-.", ":", "-"]
    all_times = all_times_faster
    method_labels = method_labels_faster
    title = "Faster IPC methods"
    ymax = 5

f = plt.figure(1)
plt.clf()

for times, label, symbol, linestyle in zip(all_times, method_labels, symbols, linestyles):
    #plt.scatter(range(len(labels)), times, label=label, marker=symbol)
    plt.plot(range(len(labels)), times, label=label,
             marker=symbol, linestyle=linestyle)

plt.title(title)
plt.legend(loc="upper left")
plt.ylabel("Time in seconds (smaller is better)")
plt.xticks(range(len(labels)), labels, rotation=45, ha="right")
plt.xlim(xmin=-0.1, xmax=len(labels) - 0.9)
plt.ylim(ymin=-0.1, ymax=ymax)
plt.tight_layout()
plt.savefig(png_filename)
