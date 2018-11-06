from hdt import HDTDocument
import os
import csv

black_list = ["query_10020.rq", "query_10025.rq", "query_10039.rq", "query_10044.rq", "query_10061.rq", "query_10069.rq", "query_10078.rq", "query_10082.rq", "query_10083.rq", "query_10091.rq", "query_10122.rq", "query_10150.rq", "query_10168.rq", "query_10169.rq"]

path = "watdiv_queries/watdiv_queries_0/"
dest = "watdiv_one_triple/"
card_file = "results/optionals/cardinalities.csv"

document = HDTDocument('/Users/minier-t/Documents/hdt-files/watdiv.10M.hdt')

cardinalities = list()
final_queries = list()


def get_triples(query):
    start = query.index('WHERE {')
    end = query.index('}')
    return query[start+7:end].strip().split(" . ")


def cardinality(triple):
    terms = triple.split(" ")
    subj = terms[0].strip()[1:-1] if not terms[0].startswith('?') else ""
    pred = terms[1].strip()[1:-1] if not terms[1].startswith('?') else ""
    obj = terms[2].strip()[1:-1] if not terms[2].startswith('?') else ""
    iter, card = document.search_triples(subj, pred, obj)
    return (triple, card)


for filename in os.listdir(path):
    if filename not in black_list:
        with open(path + filename) as f:
            query = f.read()
        triples = get_triples(query)
        cards = [cardinality(t) for t in triples]
        sorted(cards, key=lambda t: t[1])
        (max_triple, max_card) = cards[0]
        # save cardinality
        cardinalities.append((filename, max_card))
        # generate query
        # with open(dest + filename, 'w') as out:
        #     out.write("SELECT * WHERE { " + max_triple + " }")

# save cardinalities in CSV file
field_names = ['query', 'cardinality']
with open(card_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    for (query, card) in cardinalities:
        writer.writerow({'query': query[:-3], 'cardinality': card})
