z1 = 0 + 0j
z2 = -0.82 + 0j
c = -0.62772 - 0.42193j

# may never diverge
zs1 = []
z = z1
zs1.append(abs(z))
for n in range(50):
    z = z * z + c
    az = abs(z)
    assert az < 2
    zs1.append(az)

# diverges quickly
zs2 = []
z = z2
zs2.append(abs(z))
for n in range(30):
    z = z * z + c
    az = abs(z)
    #assert az < 2
    zs2.append(az)


print zs2[:20]


from matplotlib import pyplot as plt
f = plt.figure(1)
plt.clf()
plt.plot(zs1, 'o-', linewidth=4, label="z=" + str(z1))
plt.plot(zs2, 'd:', linewidth=4, label="z=" + str(z2))

plt.annotate("cutoff", (25, 1.9), fontsize="large")
plt.hlines(2, 0, 50, colors='k', linewidth=4, linestyles="dashed")

plt.ylim(ymax=2.1)

plt.legend(loc="center right")
plt.title("Two examples of the evolution of\nabs(z) with c=-0.62772-0.42193j")
plt.xlabel('Iteration')
plt.xlim((0, 50))
plt.tight_layout()

plt.savefig("julia_nonconvergence.png")
