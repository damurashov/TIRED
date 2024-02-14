import tired.sqlite


if __name__ == "__main__":
    f1 = tired.sqlite.InfoField("quantity", int)
    f2 = tired.sqlite.InfoField("name", str)

    parent = tired.sqlite.Table("parent")
    child = tired.sqlite.Table("child")

    parent.add_field(f1)
    parent.add_field(f2)
    child_parent_field = tired.sqlite.ForeignIdField(parent)
    child.add_field(child_parent_field)
    child.add_field(f1)

    generate_db = tired.sqlite.GenerateDbScript()
    generate_db.add_table(parent)
    generate_db.add_table(child)
    print(generate_db.generate_sql_script())

    db = tired.sqlite.Db([parent, child])
    db.connect("/tmp/db.db")
    print(db.execute_script(generate_db))

    insert = tired.sqlite.InsertQuery(parent)
    insert.add_value(f1, "12")
    insert.add_value(f2, "some string")
    print(insert.generate_sql())
    print(db.execute(insert))

    insert = tired.sqlite.InsertQuery(child)
    insert.add_value(f1, "someone")
    insert.add_value(child_parent_field, 1)
    print(insert.generate_sql())
    print(db.execute(insert))

    query = tired.sqlite.InnerJoinSelectQuery(child)
    query.add_field(parent, f1)
    query.add_field(child, f1)
    print(query.generate_sql())
    print(db.execute(query))

    query = tired.sqlite.InnerJoinSelectQuery(parent)
    query.add_field(parent, f1)
    query.add_field(parent, f2)
    print(query.generate_sql())
    print(db.execute(query))

    query = tired.sqlite.UpdateQuery(parent)
    query.add_field(f1, "its been changed")
    query.add_eq_constraint(parent.get_id_field(), 1)
    print(query.generate_sql())
    print(db.execute(query))

    query = tired.sqlite.InnerJoinSelectQuery(parent)
    query.add_field(parent, f1)
    query.add_field(parent, f2)
    print(query.generate_sql())
    print(db.execute(query))
