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
        return f'{self.get_name()} integer primary key'


@dataclasses.dataclass
class ForeignIdField:
    parent_table: object

    def get_name(self):
        return self.parent_table.get_name() + "_" + "id"

    def generate_sql_create(self):
        return ',\n'.join([
            f'{self.get_name()} integer not null',
            f'foreign key ({self.get_name()}) references {self.parent_table.get_name()}(id) on update cascade on delete cascade'
        ])


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

    def add_field(self, field: InfoField or ForeignIdField):
        self._fields.append(field)

    def generate_sql_create(self):
        return '\n'.join([
            f"create table if not exists {self.name} (",
            ',\n'.join(map(lambda i: i.generate_sql_create(), self._fields)),
            ');',
        ])


class Db:
    def __init__(self, tables: list):
        self._tables = tables

    def connect(self, filename):
        self.conn = sqlite3.connect(filename)
        self.conn.cursor().executescript(self.generate_sql_create())
        self.conn.commit()

    def generate_sql_create(self):
        return '\n'.join([
            'pragma foreign_keys = ON;',
            *list(map(lambda i: i.generate_sql_create(), self._tables))
        ])

