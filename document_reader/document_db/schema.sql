DROP TABLE IF EXISTS warehouse;
DROP TABLE IF EXISTS box;
DROP TABLE IF EXISTS document;

CREATE TABLE warehouse (
    id int NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

CREATE TABLE box (
    id int NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    warehouse_id int NOT NULL,
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(id),
    PRIMARY KEY(id)
);


CREATE TABLE document (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    file_blob text NOT NULL,
    box_id int NOT NULL,
    FOREIGN KEY (box_id) REFERENCES box(id)
);