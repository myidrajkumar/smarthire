"""To load the DB"""
import os
from typing import Optional
import psycopg2
# from config.dbconfig import load_config


from psycopg2.extras import RealDictCursor


def connect_db(db_config):
    """Connect to the PostgreSQL database server"""
    try:
        with psycopg2.connect(**db_config) as conn:
            print("Connected to the PostgreSQL server.")
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def connect_db_env():
    """Connect to the PostgreSQL database server"""
    try:
        with psycopg2.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"),
                              password=os.getenv("DB_PASSWORD"), 
                              dbname=os.getenv("DB_NAME"), port=5432) as conn:
            print("Connected to the PostgreSQL server.")
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        

# config = load_config()


def get_business_units(bu_id: Optional[int] = None):
    """Retrieve the business units from the database"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = "SELECT * FROM businessunit"
            if bu_id:
                sql += f" WHERE id = {bu_id}"

            cursor.execute(sql)
            results = cursor.fetchall()

            db_connection.close()
            return results

    except Exception as error:
        print(error)


def save_doc_db(bu_id, jd_file, doc_content):
    """Saving the doc to DB"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = """INSERT INTO jobdescription(title, doc, bu_id)
             VALUES(%s, %s, %s);"""

            cursor.execute(sql, (jd_file, doc_content, bu_id))
            db_connection.commit()

            db_connection.close()

    except Exception as error:
        print(error)


def get_jds_for_bu_db(bu_id: int):  # -> Any | None:
    """Retrieve the business units from the database"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = "SELECT jd.id as jd_id, title, bu.id as bu_id FROM jobdescription jd JOIN businessunit bu on jd.bu_id = bu.id and bu.id = %s"

            cursor.execute(sql, (bu_id))
            results = cursor.fetchall()

            db_connection.close()
            return results

    except Exception as error:
        print(error)


def get_jd_from_db(jd_id: int, bu_id: int):
    """Retrieve the business units from the database"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = "SELECT title, doc FROM jobdescription jd WHERE jd.id = %s and jd.bu_id = %s"

            cursor.execute(sql, (jd_id, bu_id))
            results = cursor.fetchone()

            db_connection.close()
            return results

    except Exception as error:
        print(error)


if __name__ == "__main__":
    config = load_config()
    connect_db(config)
