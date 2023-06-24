import sys
from graphql.utils import schema_printer

from modules.schema import schema

fp = open("schema.graphql", "w")
fp.write(schema_printer.print_schema(schema))
fp.close()
