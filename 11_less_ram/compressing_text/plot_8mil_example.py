import matplotlib.pyplot as plt

labels = ['list_bisect', 'set', 'Marisa Trie', 'DAWG', 'HAT Trie']
ram_used = [920, 1112, 293, 958, 244]
build_time = [47, 31, 55, 63, 44]
lookup_time = [0.02, 0.003, 0.01, 0.004, 0.005]

# make the build-time circles much larger
build_time = [bt * 5 for bt in build_time]

plt.figure(1)
plt.clf()
plt.scatter(ram_used, lookup_time, s=build_time)

for ram, lookup, label in zip(ram_used, lookup_time, labels):
    plt.annotate(label, (ram + 15, lookup + 0.0005))

plt.xlabel('RAM used (MB - lower is better)')
plt.ylabel("Look-up time (seconds - lower is better)")
plt.title(
    "Container behavior for 8,545,076 tokens\nsize represents build time (smaller is better)")
plt.xlim(xmin=0)
plt.tight_layout()
plt.savefig("less_ram_tries_dawg_text_8545076_tokens.png")
