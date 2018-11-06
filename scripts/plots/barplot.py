import numpy as np

black_list = [106, 114, 117, 120, 12, 130, 134, 136, 138, 142, 153, 158, 170, 174, 20, 26, 2, 33, 40, 41, 42, 43, 44, 54, 58, 5, 63, 65, 6, 74, 86, 89, 94, 98]
black_list = list(map(lambda x: "query_{}".format(x), black_list))


def compute_overhead(suffix, metric=4):

    def predicate(df):
        return df["httpCalls"] > 1

    def mapper(df):
        return df[metric]

    df_1 = np.genfromtxt("results/overhead/watdiv_{}_1.csv".format(suffix), delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    df_2 = np.genfromtxt("results/overhead/watdiv_{}_2.csv".format(suffix), delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    df_3 = np.genfromtxt("results/overhead/watdiv_{}_3.csv".format(suffix), delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    all = list(map(mapper, filter(predicate, df_1))) + list(map(mapper, filter(predicate, df_2))) + list(map(mapper, filter(predicate, df_3)))
    return all


def compute_space(suffix, metric=3):

    def predicate(df):
        return df["httpCalls"] > 1

    def mapper(df):
        return df[metric]

    df_1 = np.genfromtxt("results/overhead/watdiv_{}_space_1.csv".format(suffix), delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    return list(map(mapper, filter(predicate, df_1)))


def compute_http_watdiv(path, suffix):

    df_1 = np.genfromtxt("results/{}/run1/1clients/mix_watdiv_queries_0/execution_times_{}.csv".format(path, suffix), delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    df_2 = np.genfromtxt("results/{}/run2/1clients/mix_watdiv_queries_0/execution_times_{}.csv".format(path, suffix), delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    df_3 = np.genfromtxt("results/{}/run2/1clients/mix_watdiv_queries_0/execution_times_{}.csv".format(path, suffix), delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    return np.mean([np.sum(df_1["httpCalls"]), np.sum(df_2["httpCalls"]), np.sum(df_3["httpCalls"])])


def feasible(path):

    def predicate(df):
        return df["query"] not in black_list

    def mapper(df):
        return df[2]

    df = np.genfromtxt("results/feasible/{}".format(path), delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    return np.sum(list(map(mapper, filter(predicate, df))))


def optional(join_times, triples_times, cardinalities):
    df_joins = np.genfromtxt(join_times, delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    df_triples = np.genfromtxt(triples_times, delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
    df_card = np.genfromtxt(cardinalities, delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)

    # load all times by query
    triples = dict()
    cards = dict()
    for row in df_triples:
        triples[row['query']] = row['httpCalls']
    for row in df_card:
        cards[row['query']] = row['cardinality']

    # compute results for bind joins
    bind_join = list()
    for row in df_joins:
        if row['query'] in triples:
            v = triples[row['query']] + (cards[row['query']] / 15)
            bind_join.append(v)
    # compute results for optimized
    optimized = list()
    for row in df_joins:
        if row['query'] in triples:
            v = row['httpCalls'] + triples[row['query']] - 1
            optimized.append(v)

    return (np.sum(bind_join), np.sum(optimized))


# 1M
sage_1M_import = compute_overhead('1M')
sage_1M_export = compute_overhead('1M', metric=5)

# 10M
sage_10M_import = compute_overhead('10M')
sage_10M_export = compute_overhead('10M', metric=5)
sage_10M_space = compute_space('10M')

# 100M
sage_100M_import = compute_overhead('100M')
sage_100M_export = compute_overhead('100M', metric="exportTime")

print('Overhead')
print('WatDiv 1M')
print('import', np.mean(sage_1M_import))
print('export', np.mean(sage_1M_export))
print('WatDiv 10M')
print('import', np.mean(sage_10M_import))
print('export', np.mean(sage_10M_export))
print('space min', np.min(sage_10M_space) / 1000, 'kb')
print('space max', np.max(sage_10M_space) / 1000, 'kb')
print('space avg', np.mean(sage_10M_space) / 1000, 'kb')
print('space std', np.std(sage_10M_space) / 1000, 'kb')
print('WatDiv 100M')
print('import', np.mean(sage_100M_import))
print('export', np.mean(sage_100M_export))


print('----------------------')

bj_75, opt_75 = optional('results/watdiv-sage-75ms/run1/1clients/mix_watdiv_queries_0/execution_times_sage.csv', 'results/optionals/1triple_75ms.csv', 'results/optionals/cardinalities.csv')

bj_1s, opt_1s = optional('results/watdiv-sage-1s/run1/1clients/mix_watdiv_queries_0/execution_times_sage.csv', 'results/optionals/1triple_1s.csv', 'results/optionals/cardinalities.csv')

print('Sage-75ms')
print('Sage bind join')
print(bj_75)
print('Sage optimized')
print(opt_75)
print('Sage-1s')
print('Sage bind join')
print(bj_1s)
print('Sage optimized')
print(opt_1s)

print('----------------------')

# http requests
print("HTTP requests WatDiv")
sage_1s = compute_http_watdiv("watdiv-sage-1s", "sage")
sage_75ms = compute_http_watdiv("watdiv-sage-75ms", "sage")
brtpf = np.genfromtxt("results/watdiv-brtpf/run1/1clients/mix_watdiv_queries_0/execution_times_brtpf.csv", delimiter=',', names=True, dtype=None, encoding='utf-8', invalid_raise=False)
brtpf = np.sum(brtpf['httpCalls'])
tpf = compute_http_watdiv("watdiv-tpf", "tpf")
print("sage 1s")
print(sage_1s)
print("sage 75ms")
print(sage_75ms)
print('BrTPF')
print(brtpf)
print("TPF")
print(tpf)

print('----------------------')

print("HTTP requests FEASIBLE")
sage_1s = feasible("sage_1s.csv")
sage_75ms = feasible("sage_75.csv")
brtpf = feasible('brtpf.csv')
tpf = feasible("tpf.csv")
print("sage 1s")
print(sage_1s)
print("sage 75ms")
print(sage_75ms)
print('BrTPF')
print(brtpf)
print("TPF")
print(tpf)

# plt.rc('text', usetex=True)
# ax = plt.axes(yscale='linear')
# ax.yaxis.grid(color='lightgrey')
# plt.xlabel('WatDiv dataset size (nb triples)', fontsize=17)
# plt.ylabel('Avg. time overhead (ms)', fontsize=17)
# plt.tick_params(axis='both', which='major', labelsize=15)
# plt.tight_layout()
# plt.boxplot([sage_107_import, sage_107_export], positions=[1, 2], vert=True, labels=['\\texttt{Resume}', '\\texttt{Suspend}'])
# plt.boxplot([sage_108_import, sage_108_export], positions=[3, 4], vert=True, labels=['\\texttt{Resume}', '\\texttt{Suspend}'])
# plt.show()
