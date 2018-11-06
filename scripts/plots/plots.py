import matplotlib.pyplot as plt
from utils import DrawPlot, compute_total_time, compute_tffr, compute_tpf_ttfr
from brtpf import compute_brtpf_time, compute_brtpf_ttfr


def add_latency(http_calls):
    LATENCY = 0.050  # in seconds
    return http_calls * LATENCY


clients = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
quotas = [50, 60, 70, 75, 77, 80, 100, 150, 200]

# query distribution
# distribution = list(np.genfromtxt('results/distributions.csv', delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)['time'])
# distribution.sort(reverse=True)
# print(min(distribution))
#
# with DrawPlot('distribution', plt, 'Query', 'Execution time (s)', yscale='log', save_png=False) as figure:
#     figure.bar(np.arange(1, len(distribution)+1), distribution)
#     fig = figure.gcf()
#     fig.set_size_inches(5, 3)

# Average completion time 1W
virtuo_inf = compute_total_time('results/watdiv-virtuoso', clients, 3, suffix="virtuoso")
sage_75ms = compute_total_time('results/watdiv-sage-75ms', clients, 3, add_latency=True)
sage_1s = compute_total_time('results/watdiv-sage-1s', clients, 1, add_latency=True)
brtpf = compute_brtpf_time()
tpf = compute_total_time('results/watdiv-tpf', clients, 3, suffix="tpf")

with DrawPlot('total_time', plt, 'Number of clients', 'Avg. workload completion time (s)', save_png=True) as figure:
    figure.plot(clients, virtuo_inf, linestyle='-', marker='o', color='r', label='Virtuoso')
    figure.plot(clients, brtpf, linestyle='--', marker='x', color='k', label='BrTPF')
    figure.plot(clients, sage_1s, linestyle='--', marker='P', color='c', label='SaGe-1s')
    figure.plot(clients, tpf, linestyle='-', marker='s', color='g', label='TPF')
    figure.plot(clients, sage_75ms, linestyle='-', marker='D', color='b', label='SaGe-75ms')
    figure.legend(ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.23), fontsize=13, fancybox=False)
    fig = figure.gcf()
    fig.set_size_inches(7, 5)


# # Average completion time 4W
# virtuo_4w = compute_total_time('results/watdiv-virtuoso-4w', clients, 1, suffix="virtuoso")
# sage_75ms_4w = compute_total_time('results/watdiv-sage-75ms-4w', clients, 1, add_latency=True)
#
# with DrawPlot('total_time_4w', plt, 'Number of clients', 'Avg. workload completion time (s)', save_png=True) as figure:
#     figure.plot(clients, virtuo_4w, linestyle='-', marker='o', color='r', label='Virtuoso 1 worker')
#     figure.plot(clients, virtuo_inf, linestyle='--', marker='o', color='r', label='Virtuoso 4 workers')
#     figure.plot(clients, sage_75ms, linestyle='-', marker='D', color='b', label='SaGe-75ms 1 worker')
#     figure.plot(clients, sage_75ms_4w, linestyle='--', marker='D', color='b', label='SaGe-75ms 4 workers')
#     figure.legend(ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1.2), fontsize=13, fancybox=False)
#
# # Time for first results
# virtuo_inf = compute_tffr('results/watdiv-virtuoso', clients, 3, suffix="virtuoso")
# sage_1s = compute_tffr('results/watdiv-sage-1s', clients, 1)
# sage_75ms = compute_tffr('results/watdiv-sage-75ms', clients, 3)
# brtpf = compute_brtpf_ttfr()
# tpf = compute_tpf_ttfr('results/watdiv-tpf', clients, 3)
#
# with DrawPlot('time_first_results', plt, 'Number of clients', 'Avg. time for First results (s)', yscale='linear', save_png=True) as figure:
#     figure.plot(clients, virtuo_inf, linestyle='-', marker='o', color='r', label='Virtuoso')
#     figure.plot(clients, brtpf, linestyle='--', marker='x', color='k', label='BrTPF')
#     figure.plot(clients, sage_1s, linestyle='--', marker='P', color='c', label='SaGe-1s')
#     figure.plot(clients, tpf, linestyle='-', marker='s', color='g', label='TPF')
#     figure.plot(clients, sage_75ms, linestyle='-', marker='D', color='b', label='SaGe-75ms')
#     figure.legend(ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.23), fontsize=13, fancybox=False)
