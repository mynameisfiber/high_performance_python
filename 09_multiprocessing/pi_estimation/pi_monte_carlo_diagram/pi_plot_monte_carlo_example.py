import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    np.random.seed(0)  # force repeatable plt
    nbr_items = 1E4
    xs = np.random.uniform(0, 1, nbr_items)
    ys = np.random.uniform(0, 1, nbr_items)
    estimate_inside_quarter_unit_circle = (xs * xs + ys * ys) <= 1
    nbr_trials_in_quarter_unit_circle = np.sum(
        estimate_inside_quarter_unit_circle)
    # estimate for the full circle
    pi = (nbr_trials_in_quarter_unit_circle * 4) / nbr_items

    plt.figure(1, figsize=(8, 8))
    plt.clf()
    plt.plot(xs[estimate_inside_quarter_unit_circle],
             ys[estimate_inside_quarter_unit_circle], 'bx')
    plt.plot(xs[estimate_inside_quarter_unit_circle == False],
             ys[estimate_inside_quarter_unit_circle == False], 'g.')

    unit_circle_xs = np.arange(0, 1, 0.001)
    unit_circle_ys = np.sin(np.arccos(unit_circle_xs))
    plt.plot(unit_circle_xs, unit_circle_ys, linewidth=2, c="k")
    plt.xticks([0.0, 1.0])
    plt.yticks([0.0, 1.0])
    plt.title("Pi estimated as {} using \n{:,} Monte Carlo dart throws".format(
        pi, int(nbr_items)))
    # plt.show()
    plt.tight_layout()
    plt.savefig("08_pi_plot_monte_carlo_example.png")
