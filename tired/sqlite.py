import dataclasses
import sqlite3
import tired.logging

######################################################################
#           First order entities
######################################################################

@dataclasses.dataclass
class InfoField:
    """
    Regular field of either `int`, or `text` type
    """
    name: str
    field_type: object

    def __post_init__(self):
        assert self.field_type in [int, str]

    def field_type_as_name(self):
        if self.field_type is int:
            return "integer"
        elif self.field_type is str:
            return "text"

    def get_name(self):
        return self.name

    def generate_sql_create(self):
        return f'{self.name} {self.field_type_as_name()}'


class IdField:
    """
    An autoincremented id field. SHOULD NOT be used directly, as each table has
    it by default.
    """
    def get_name(self):
        return "id"

    def generate_sql_create(self):
        return f'{self.get_name()} integer primary key autoincrement'


@dataclasses.dataclass
class ForeignIdField:
    """
    Represents a foreign "id" field from some other table.
    """
    parent_table: object

    def get_name(self):
        return self.parent_table.get_name() + "_" + "id"

    def generate_sql_create(self):
        return f'{self.get_name()} integer not null'


@dataclasses.dataclass
class Table:
    """
    Representation of a table. By default (and this cannot be changed), each
    table DOES hold an autoincremented integer "id" field.
    """
    name: str

    def get_name(self):
        return self.name

    def get_id_field(self):
        return self._id_field

    def __post_init__(self):
        self._fields = list()
        self._id_field = IdField()
        self._fields.append(self._id_field)

    def add_field(self, field):
        self._fields.append(field)

    def _generate_foreign_key_create_iter(self):
        for field in self._fields:
            if type(field) is ForeignIdField:
                yield f'foreign key ({field.get_name()}) references {field.parent_table.get_name()}(id) on update cascade on delete cascade'

    def generate_sql_create(self):
        fields = list(map(lambda i: i.generate_sql_create(), self._fields))
        foreign_keys = list(self._generate_foreign_key_create_iter())

        return '\n'.join([
            f"create table if not exists {self.name} (",
            ',\n'.join([*fields, *foreign_keys]),
            ');',
        ])


@dataclasses.dataclass
class TableFieldPair:
    table: object
    field: object

    def generate_sql_select(self):
        return f'{self.table.get_name()}.{self.field.get_name()} as {self.table.get_name()}_{self.field.get_name()}'


@dataclasses.dataclass
class InnerJoinSelectQuery:
    """
    Queries a set of rows from the table in the exact order as they have been
    added (see "add_field"). If fields from parent tables are queried too, an
    "inner join" statement WILL BE generated automatically.

    WARNING: As of yet, the implementation DOES NOT check the relation b/w 2
    tables, so if `self.table` does not pull foreign keys from some parent
    table, this error WILL NOT be caught, and the behaviour IS undefined.
    """

    table: object
    """
    The table that is being queried
    """

    def __post_init__(self):
        self._table_fields = list()
        self._eq_constraints = list()
        self._inner_joins = list()

    def add_parent_table_field(self, parent_table, parent_table_field, child_table):
        """
        The parent table might be a few tables away from the table the query
        is made for
        """
        # Make inner join query
        child_id_field_name = ForeignIdField(parent_table).get_name()
        child_table_name = child_table.get_name()
        parent_table_name = parent_table.get_name()
        join_query = f'inner join {parent_table.get_name()} on {parent_table_name}.id = {child_table_name}.{child_id_field_name}'

        if join_query not in self._inner_joins:
            self._inner_joins += [join_query]

        # Add field
        self._table_fields.append(TableFieldPair(parent_table, parent_table_field))

    def add_field(self, field):
        """
        Will automatically detect whether the table is different, and will
        generate appropriate join queries.

        Will not check upon correctness of the join. The `table` MUST be a
        parent, i.e. must provide a foreign key to the "child" table.
        """
        self._table_fields.append(TableFieldPair(self.table, field))

    def add_eq_constraint(self, table1, field1, value):
        self._eq_constraints.append((table1, field1, value))

    def _generate_sql_field_query_iter(self):
        yield from map(lambda i: i.generate_sql_select(), self._table_fields)

    def _generate_sql_inner_join_iter(self):
        for join in self._inner_joins:
            yield join

    def _generate_sql_eq_constraints(self):
            for t1, f1, v in self._eq_constraints:
                yield f'{t1.get_name()}.{f1.get_name()} = "{v}"'

    def _generate_sql_select_iter(self):
        yield "select"
        yield ', '.join(self._generate_sql_field_query_iter())
        yield 'from'
        yield self.table.get_name()
        yield from self._generate_sql_inner_join_iter()
        if len(self._eq_constraints):
            yield 'where'
            yield ' AND '.join(self._generate_sql_eq_constraints())
        yield ';'

    def generate_sql_select(self):
        return ' '.join(self._generate_sql_select_iter())

    def generate_sql(self):
        return ' '.join(self._generate_sql_select_iter())


@dataclasses.dataclass
class UpdateQuery:
    table: object

    def __post_init__(self):
        self._eq_constraints = list()
        self._value_mappings = list()

    def add_field(self, field, value):
        self._value_mappings += [(field.get_name(), value)]

    def add_eq_constraint(self, field, value):
        self._eq_constraints += [(field.get_name(), value)]

    def generate_sql(self):
        out = ' '.join([
            'UPDATE',
            self.table.get_name(),
            'SET',
            ','.join([f"{f}='{v}'" for f, v in self._value_mappings]),
            'WHERE',
            ' AND '.join([f'{f}={v}' for f, v in self._eq_constraints]),
            ';'
        ])

        return out


@dataclasses.dataclass
class DeleteQuery:
    table: object
    identifier: int

    def generate_sql(self):
        out = f'DELETE FROM {self.table.get_name()} where {self.table.get_name()}.id = {self.identifier}'

        return out


@dataclasses.dataclass
class InsertQuery:
    """
    Encapsulates an SQL "insert" query.
    """

    table: object
    """ The table that is being inserted into """

    def __post_init__(self):
        self._field_names = list()
        self._values = list()

    def add_value(self, field, value):
        """
        Adds a (field, value) pair into the query.

        WARNING: please note that if a field does not have a default value, all
        of its fields MUST BE added in the query.

        WARNING: The "id" field MUST NOT be included.
        """

        if type(value) is str:
            value = f"'{value}'"
        elif type(value) is int:
            value = str(value)

        self._field_names.append(field.get_name())
        self._values.append(value)

    def generate_sql_insert(self):
        columns = ', '.join(self._field_names)
        values = ', '.join(self._values)
        return f'insert into {self.table.get_name()} ({columns}) values({values});'

    def generate_sql(self):
        return self.generate_sql_insert()


class GenerateDbScript:
    """
    Creates a script for generating a stub for the database. Usually, it is
    being used at the beginning, after the connection w/ the database is
    established.
    """

    def __init__(self):
        self._tables = list()

    def add_table(self, table):
        self._tables.append(table)

    def generate_sql_script(self):
        return '\n'.join([
            'pragma foreign_keys = ON;',
            *list(map(lambda i: i.generate_sql_create(), self._tables))
        ])


class Db:
    """
    Opens/creates a database file, and provides an API for executing *Queries*
    and *Scripts*. The difference b/w the two is that queries MAY return
    resulting fields, and CAN contain ONLY one SQL sentence.
    """
    def __init__(self, tables: list = None):
        self._tables = tables

    def execute(self, query):
        cur = self._conn.cursor()
        sql = query.generate_sql()
        try:
            cur.execute(query.generate_sql())
            self._conn.commit()
        except sqlite3.OperationalError as e:
            tired.logging.error(f"Failed to execute query: {sql}: {e}")
            raise e

        return cur.fetchall()

    def execute_query(self, query):
        return self.execute(query)

    def execute_script(self, script):
        self._conn.cursor().executescript(script.generate_sql_script())
        self._conn.commit()

    def connect(self, filename):
        tired.logging.info(f'Trying to connect w/ the database "{filename}"')
        self._conn = sqlite3.connect(filename)
