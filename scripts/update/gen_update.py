# gen_update.py
# Author: Thomas MINIER - MIT License 2017-2019
import click
from os.path import basename
from os import listdir, mkdir

mappings_prefixes = {
    'http://purl.org/dc/terms/': 'http://sage.univ-nantes.fr/dc/terms/',
    'http://xmlns.com/foaf/': 'http://sage.univ-nantes.fr/foaf/',
    'http://purl.org/goodrelations/': 'http://sage.univ-nantes.fr/goodrelations/',
    'http://www.geonames.org/ontology#': 'http://sage.univ-nantes.fr/geonames#',
    'http://purl.org/ontology/mo/': 'http://sage.univ-nantes.fr/mo/',
    'http://ogp.me/ns#': 'http://sage.univ-nantes.fr/ogp#',
    'http://purl.org/stuff/rev#': 'http://sage.univ-nantes.fr/stuff/rev#',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'http://sage.univ-nantes.fr/rdf-syntax-ns#',
    'http://www.w3.org/2000/01/rdf-schema#': 'http://sage.univ-nantes.fr/rdf-schema#',
    'http://schema.org/': 'http://sage.univ-nantes.fr/schema/',
    'http://db.uwaterloo.ca/~galuc/wsdbm/': 'http://sage.univ-nantes.fr/wsdbm/'
}


@click.command()
@click.argument("workloads_path")
@click.argument("output_path")
def gen_update_query(workloads_path, output_path):
    """Generate workloads of SPARQL UPDATE queries from a set of workloads"""
    # load template queries
    for workload_folder in listdir(workloads_path):
        workload_name = basename(workload_folder)
        output_workload = "{}/{}".format(output_path, workload_name)
        try:
            mkdir(output_workload)
            mkdir("{}/inserts/".format(output_workload))
            mkdir("{}/deletes/".format(output_workload))
        except FileExistsError as e:
            pass
        except Exception as e:
            raise e

        # transform each query in the workload
        for query_file in listdir("{}/{}".format(workloads_path, workload_folder)):
            insert_qname = "ins_{}".format(query_file)
            delete_qname = "del_{}".format(query_file)
            with open("{}/{}/{}".format(workloads_path, workload_folder, query_file), 'r') as f:
                query = f.read()
            where_clause = query.split("SELECT * WHERE")[1].strip()
            # create the insert_clause from the where clause
            insert_clause = where_clause
            for old_v, new_v in mappings_prefixes.items():
                insert_clause = insert_clause.replace(old_v, new_v)
            insert_query = """INSERT {} WHERE {}""".format(insert_clause, where_clause).strip()
            delete_query = """DELETE {} WHERE {}""".format(insert_clause, insert_clause).strip()

            with open("{}/inserts/{}".format(output_workload, insert_qname), 'w+') as f:
                f.write(insert_query)
                f.write("\n")
            with open("{}/deletes/{}".format(output_workload, delete_qname), 'w+') as f:
                f.write(delete_query)
                f.write("\n")


if __name__ == '__main__':
    gen_update_query()
