# gen_update.py
# Author: Thomas MINIER - MIT License 2017-2019
from hdt import HDTDocument
import click
from os.path import basename, splitext

prefixes = {
    'wsdbm': 'http://db.uwaterloo.ca/~galuc/wsdbm/'
}


@click.command()
@click.argument("template_file")
@click.argument("hdt_file")
@click.option("-o", "--out", type=str,
              default=None, help="Directory where generated SPARQL queries will be stored. If not used, output all queries in the standard output")
def gen_update_query(template_file, hdt_file, out):
    """Generate a set of SPARQL UPDATE queries from a template query and a HDT file which contains the RDF dataset"""
    # load template query
    template_name = splitext(basename(template_file))[0]
    with open(template_file, 'r') as f:
        lines = f.read().splitlines()

    template_query = ''
    mappings = dict()

    # parse template
    for line in lines:
        # extract mapping information
        if line.startswith('#mapping'):
            (op, variable, base_entity, law) = line.split(' ')
            # expand possible prefixes
            if base_entity.startswith('wsdbm:'):
                base_entity = prefixes['wsdbm'] + base_entity[6:]
            mappings[variable] = base_entity
        elif line.strip().startswith('#'):
            # ignore comments.
            # The SaGe java client coalesce the input query on a single line,
            # thus any comment may also comment out the entier query...
            pass
        else:
            template_query += line + '\n'
    template_query = template_query.strip()

    # load HDT dataset
    document = HDTDocument(hdt_file)

    # instanciate mappings by lloking for matching entities
    entities = dict()
    for variable, base_entity in mappings.items():
        done = False
        current = 0
        all_entites = list()
        while not done:
            entity = "{}{}".format(base_entity, current)
            # search for ?s ?p <entity> first
            iterator, card = document.search_triples('', '', entity)
            if card > 0:
                all_entites.append(entity)
            else:
                # otherwise, search for <entity> ?p ?o
                iterator, card = document.search_triples(entity, '', '')
                if card > 0:
                    all_entites.append(entity)
                else:
                    done = True
            current += 1
        # save all entities found
        entities[variable] = all_entites

    # build template queries
    all_queries = list()
    for variable, entities in entities.items():
        v = "%{}%".format(variable)
        for entity in entities:
            all_queries.append(template_query.replace(v, "<{}>".format(entity)))

    # write results to the standard output or to the disk
    if out is None:
        print(len(all_queries))
        # for query in all_queries:
        #     print(query)
    else:
        cpt = 1
        for query in all_queries:
            file_name = "{}/Q{}_{}.sparql".format(out, cpt, template_name)
            with open(file_name, 'w+') as out_file:
                out_file.write(query)
                # print("Query Q{}_{}.sparql saved in {}".format(cpt, template_name, out))
            cpt += 1


if __name__ == '__main__':
    gen_update_query()
