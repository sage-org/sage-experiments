# gen_update.py
# Author: Thomas MINIER - MIT License 2017-2019
import click
from os.path import basename
from os import listdir, mkdir


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
        except FileExistsError as e:
            pass
        except Exception as e:
            raise e

        # transform each query in the workload
        for query_file in listdir("{}/{}".format(workloads_path, workload_folder)):
            with open("{}/{}/{}".format(workloads_path, workload_folder, query_file), 'r') as f:
                query = f.read()
            where_clause = query.split("SELECT * WHERE")[1].strip()
            update_query = """INSERT {{ GRAPH <http://172.16.8.50:8000/sparql/additionsgraph> {} }} WHERE {}""".format(where_clause, where_clause).strip()

            with open("{}/{}".format(output_workload, query_file), 'w+') as f:
                f.write(update_query)
                f.write("\n")


if __name__ == '__main__':
    gen_update_query()
