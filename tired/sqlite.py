import sqlite3
import dataclasses


@dataclasses.dataclass
class InfoField:
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
    def get_name(self):
        return "id"

    def generate_sql_create(self):
        return f'{self.get_name()} integer primary key autoincrement'


@dataclasses.dataclass
class ForeignIdField:
    parent_table: object

    def get_name(self):
        return self.parent_table.get_name() + "_" + "id"

    def generate_sql_create(self):
        return f'{self.get_name()} integer not null'


@dataclasses.dataclass
class Table:
    """
    Table w/ mandatory ID
    """
    name: str

    def get_name(self):
        return self.name

    def __post_init__(self):
        self._fields = list()
        self._fields.append(IdField())

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
    table: object
    """
    Child table
    """

    def __post_init__(self):
        self._table_fields = list()
        self._joined_tables = list()

    def add_field(self, table, field):
        """
        Will automatically detect whether the table is different, and will
        generate appropriate join queries.

        Will not check upon correctness of the join. The `table` MUST be a
        parent, i.e. must provide a foreign key to the "child" table.
        """
        self._table_fields.append(TableFieldPair(table, field))

        if table.get_name() != self.table.get_name():
            self._joined_tables.append(table)

    def _generate_sql_field_query_iter(self):
        yield from map(lambda i: i.generate_sql_select(), self._table_fields)

    def _generate_sql_inner_join_iter(self):
        for table in self._joined_tables:
            yield f'inner join {table.get_name()} on {self.table.get_name()}.id = {table.get_name()}.id'

    def _generate_sql_select_iter(self):
        yield "select"
        yield ', '.join(self._generate_sql_field_query_iter())
        yield 'from'
        yield self.table.get_name()
        yield from self._generate_sql_inner_join_iter()
        yield ';'

    def generate_sql_select(self):
        return ' '.join(self._generate_sql_select_iter())

    def generate_sql(self):
        return ' '.join(self._generate_sql_select_iter())


@dataclasses.dataclass
class InsertQuery:
    table: object

    def __post_init__(self):
        self._field_names = list()
        self._values = list()

    def add_value(self, field, value):
        if type(value) is str:
            value = f'"{value}"'
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
    def __init__(self, tables: list = None):
        self._tables = tables

    def execute(self, query):
        cur = self._conn.cursor()
        cur.execute(query.generate_sql())
        self._conn.commit()

        return cur.fetchall()

    def execute_script(self, script):
        self._conn.cursor().executescript(script.generate_sql_script())
        self._conn.commit()

    def connect(self, filename):
        self._conn = sqlite3.connect(filename)

    def generate_sql_create(self):
        return '\n'.join([
            'pragma foreign_keys = ON;',
            *list(map(lambda i: i.generate_sql_create(), self._tables))
        ])

