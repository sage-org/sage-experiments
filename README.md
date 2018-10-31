# SaGe: Web Preemption for Public SPARQL Query Services

## Abstract

To preserve the availability of SPARQL query services, data providers enforce quotas on server usage. Queries which exceed these quotas are interrupted and delivers partial results. Such interruption is not an issue if it is possible to resume the query execution afterwards. Unfortunately, there is no preemption model for the web that allows to suspend and resume SPARQL queries.
In this paper, we present a model for Web preemption and SaGe, a SPARQL query service that supports such preemption. SPARQL queries are suspended by the web server after a fixed quantum of time and resumed upon client request. Web preemption is tractable only if its cost in time is negligible compared to the time quantum. Thus, the challenge is to support full SPARQL query language while keeping the cost of preemption negligible. Extensive experimentations demonstrate that SaGe outperforms existing approaches by several order of magnitude in term of average total query execution time, time for first results and data transferred per query.

## Online demo

AN online demonstration is available at []()

## Softwares used

* [SaGe python server](https://github.com/sage-org/sage-engine)
* [SaGe java client](https://github.com/sage-org/sage-jena)
* [Virtuoso]() v7.2.4
* [TPF server](https://www.npmjs.com/package/ldf-server) v2.2.3
* [TPF client](https://www.npmjs.com/package/ldf-client) v2.0.5
* [BrTPF client + server](http://olafhartig.de/brTPF-ODBASE2016/)

## Dataset and queries

We used the WatDiv RDF dataset and query workloads from BrTPF exper- iments [14]. The dataset contains 107 triples 11, and the queries used are conjunctive SPARQL queries with STAR, PATH and SNOWFLAKE shapes. These queries vary in complexity, with very high and very low selectivity.
