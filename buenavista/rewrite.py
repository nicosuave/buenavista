from typing import Any, Callable, TypeVar
import os
import sqlglot
import sqlglot.expressions as exp
from sqlmesh.core.context import Context
from sqlmesh.core.config import load_configs

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])

class Rewriter:
    def __init__(self, read: sqlglot.Dialect, write: sqlglot.Dialect):
        self._relations = {}
        self._read = read
        self._write = write
        self._sqlmesh_context = None

        sqlmesh_config_path = os.environ.get('SQLMESH_CONFIG_PATH')
        if sqlmesh_config_path:
            paths = [sqlmesh_config_path]
            configs = load_configs(None, Context.CONFIG_TYPE, paths)
            self._sqlmesh_context = Context(paths=paths, config=configs)

    def relation(self, name: str) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self._relations[name] = func
            return func

        return decorator

    def rewrite(self, sql: str) -> str:
        try:
            if self._sqlmesh_context:
                rewritten_query = self._sqlmesh_context.rewrite(sql)
                sql = rewritten_query.sql(pretty=True, dialect=self._sqlmesh_context.config.dialect)

            stmts = self._read.parse(sql)
            ret = []
            for stmt in stmts:
                ret.append(self.rewrite_one(stmt))
            return ";\n".join(self._write.generate(s) for s in ret)
        except:
            # TODO: log this
            return sql

    def rewrite_one(self, expression: exp.Expression) -> exp.Expression:
        def _expand(node: exp.Expression):
            if isinstance(node, exp.Table):
                name = exp.table_name(node)
                if name in self._relations:
                    source = self._relations[name]
                    subquery = exp.paren(exp.maybe_parse(source()))
                    if node.alias:
                        subquery = exp.alias_(subquery, node.alias)
                    subquery.comments = [f"source: {name}"]
                    return subquery
            return node

        return expression.transform(_expand, copy=True)


if __name__ == "__main__":
    rewriter = Rewriter(sqlglot.dialects.Presto(), sqlglot.dialects.DuckDB())

    @rewriter.relation("schema.test")
    def test():
        return "SELECT 1 as a, 'foo' as b"

    print(rewriter.rewrite("SELECT * FROM schema.test"))
