# Buena Vista: A Programmable Postgres Proxy Server

## SQLMesh Metric Layer Support

This branch adds support for querying a SQLMesh metric layer and a demo with duckdb and a sample project.

By default, SQLMesh config will be pulled from `./sqlmesh`, a sample SQLMesh project with some basic (contrived) metric definitions.

You might need to run `sqlmesh plan` to create the necessary tables.

To expose a pg server, start the server pointed at that same duckdb file: `python3 -m buenavista.examples.duckdb_postgres db.db`.

You should be able to connect to a server over the pg protocol and issue queries

```
nico=> SELECT 
          METRIC(total_orders)
       FROM __semantic.__table;

 total_orders 
--------------
            7
(1 row)


nico=> SELECT 
          event_date,
          METRIC(total_orders)
       FROM __semantic.__table
       GROUP BY 1
       ORDER BY 1 DESC;

 event_date | total_orders 
------------+--------------
 2020-01-07 |            1
 2020-01-06 |            1
 2020-01-05 |            1
 2020-01-04 |            1
 2020-01-03 |            1
 2020-01-01 |            2
(6 rows)
```
