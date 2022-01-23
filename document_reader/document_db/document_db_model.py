import sqlite3
import logging

logger = logging.getLogger('__main__.document_db_model.py')


class DocumentDbModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def insert_document(self, document_record):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO document (file_blob, box_id) VALUES (?, ?)',
                       (document_record['file_blob'], document_record['box_id']))
        conn.commit()
        last_rowid = cursor.lastrowid
        logger.info(f'New Document with ID: {last_rowid} was successfully inserted into DB!')
        return last_rowid

    def insert_box(self, box_record):
        conn = self.get_db_connection()

        conn.execute('INSERT INTO box (id, warehouse_id) VALUES (?, ?)',
                     (box_record['box_id'], box_record['warehouse_id']))
        conn.commit()
        logger.info(f'New Box with ID: {box_record["box_id"]} was successfully inserted into DB!')

    def insert_warehouse(self, warehouse_record):
        conn = self.get_db_connection()

        conn.execute('INSERT INTO warehouse (id) VALUES (?)',
                     (warehouse_record['warehouse_id'], ))
        conn.commit()
        logger.info(f'New Warehouse with ID: {warehouse_record["warehouse_id"]} was successfully inserted into DB!')

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = dict_factory
        return conn

    def get_document(self, document_id):
        conn = self.get_db_connection()
        document = conn.execute('SELECT * FROM document WHERE id = ?',
                                (document_id,)).fetchone()
        conn.close()
        return document

    def get_warehouses(self):
        conn = self.get_db_connection()
        products = conn.execute('SELECT * '
                                'FROM warehouse ').fetchall()
        conn.close()

        return products

    def get_warehouse(self, warehouse_id):
        conn = self.get_db_connection()
        logger.info(f'New Warehouse with ID: {warehouse_id} was successfully inserted into DB!')
        fetched = conn.execute(f"SELECT EXISTS(SELECT 1 FROM warehouse WHERE ID=?)", (warehouse_id,)).fetchone()
        if fetched['EXISTS(SELECT 1 FROM warehouse WHERE ID=?)'] == 1:
            return True
        return False

    def get_box(self, box_id):
        conn = self.get_db_connection()
        fetched = conn.execute(f"SELECT EXISTS(SELECT 1 FROM box WHERE ID=?)", (box_id,)).fetchone()
        if fetched['EXISTS(SELECT 1 FROM box WHERE ID=?)'] == 1:
            return True
        return False

    def get_boxes(self):
        conn = self.get_db_connection()
        products = conn.execute('SELECT * '
                                'FROM box ').fetchall()
        conn.close()

        return products


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


if __name__ == '__main__':
    db_model = DocumentDbModel("./database.db")

    warehouse = db_model.get_warehouses()
    print(warehouse)
    print(db_model.get_warehouse(5))
    with open("data/converted.txt", 'r') as f:
        data = f.read()

    db_model.insert_document({'file_blob': data, 'box_id': 0})
    doc = db_model.get_document(1)
    print(doc)
