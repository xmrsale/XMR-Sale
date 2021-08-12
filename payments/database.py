import sqlite3


def create_database(name="database.db"):
    with sqlite3.connect("database.db") as conn:
        print("Creating new database.db...")
        conn.execute(
            "CREATE TABLE payments (uuid TEXT, dollar_value DECIMAL, xmr_value DECIMAL, method TEXT, address TEXT, time DECIMAL, webhook TEXT, payment_id TEXT)"
        )
    return


def write_to_database(invoice, name="database.db"):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO payments (uuid,dollar_value,xmr_value,method,address,time,webhook,payment_id) VALUES (?,?,?,?,?,?,?,?)",
            (
                invoice["uuid"],
                invoice["dollar_value"],
                invoice["xmr_value"],
                invoice["method"],
                invoice["address"],
                invoice["time"],
                invoice["webhook"],
                invoice["payment_id"],
            ),
        )
    return


def load_invoice_from_db(uuid):
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        rows = cur.execute(
            "select * from payments where uuid='{}'".format(uuid)
        ).fetchall()
    if len(rows) > 0:
        return [dict(ix) for ix in rows][0]
    else:
        return None
