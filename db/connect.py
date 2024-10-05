"""To load the DB"""

import os
from datetime import datetime
from typing import Optional

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor


def connect_db(db_config):
    """Connect to the PostgreSQL database server"""
    try:
        with psycopg2.connect(**db_config) as conn:
            print("Connected to the PostgreSQL server.")
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"ERROR: While establishing database connection: {error}")
        raise error


def connect_db_env():
    """Connect to the PostgreSQL database server"""
    try:
        with psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
            port=5432,
        ) as conn:
            print("Connected to the PostgreSQL server.")
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"ERROR: While establishing database connection: {error}")
        raise error


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
        print(f"ERROR: While getting business units: {error}")


def save_doc_db(bu_id, jd_file, doc_content):
    """Saving the doc to DB"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = """INSERT INTO jobdescription(title, doc, bu_id, job_posted)
             VALUES(%s, %s, %s, %s);"""

            cursor.execute(sql, (jd_file, doc_content, bu_id, datetime.now()))
            db_connection.commit()

            db_connection.close()

    except Exception as error:
        print(f"ERROR: While saving JDs in DB: {error}")


def get_jds_for_bu_db(bu_id: int):  # -> Any | None:
    """Retrieve all JDs for the specific business units from the database"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = "SELECT jd.id as jd_id, title, bu.id as bu_id, job_posted FROM jobdescription jd JOIN businessunit bu on jd.bu_id = bu.id and bu.id = %s"

            cursor.execute(sql, (bu_id))
            results = cursor.fetchall()

            db_connection.close()
            return results

    except Exception as error:
        print(f"ERROR: While getting JDs for a specific business unit: {error}")


def get_jd_from_db(jd_id: int, bu_id: int):
    """Retrieve the specific JD from business units from the database"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = "SELECT title, doc FROM jobdescription jd WHERE jd.id = %s and jd.bu_id = %s"

            cursor.execute(sql, (jd_id, bu_id))
            results = cursor.fetchone()

            db_connection.close()
            return results

    except Exception as error:
        print(
            f"ERROR: While getting a specific JD from a specific business unit: {error}"
        )


# Query Data
def query_data(query):
    """Querying via Pandas"""
    db_connection = connect_db_env()
    return pd.read_sql(query, db_connection)


def get_total_applications_count():
    """Getting applications count"""

    total_applications_query = """
    SELECT COUNT(application_id) AS total_applications 
    FROM applications;
    """

    return query_data(total_applications_query).iloc[0]["total_applications"]


def get_screening_efficiency():
    """Getting screening efficiency"""

    ai_screening_efficiency_query = """
        SELECT COUNT(*) * 100.0 / (SELECT COUNT(*) FROM applications) AS ai_efficiency
        FROM applications WHERE screening_score > 70;
    """
    return query_data(ai_screening_efficiency_query).iloc[0]["ai_efficiency"]


def get_candidates_pipeline():
    """Getting candidates pipeline"""

    pipeline_query = """
        SELECT stage, COUNT(*) AS candidates
        FROM applications
        GROUP BY stage;
    """
    return query_data(pipeline_query)


def get_time_to_hire():
    """Getting time to hire"""

    time_to_hire_query = """
        SELECT job_id, AVG(DATE_PART('day', date_updated - date_applied)) AS avg_time_to_hire
        FROM applications
        WHERE status = 'Hired'
        GROUP BY job_id;
    """
    return query_data(time_to_hire_query)


def get_max_time_to_hire():
    """Getting maximum time to hire"""

    max_time_to_hire_query = """
       SELECT MAX(avg_time_to_hire) AS max_time
       FROM (
           SELECT job_id, AVG(DATE_PART('day', date_updated - date_applied)) AS avg_time_to_hire
           FROM applications
           WHERE status = 'Hired'
           GROUP BY job_id
       ) AS subquery;
    """
    return query_data(max_time_to_hire_query)


def get_entire_job_openings_count():
    """Getting entire job openings count"""

    total_jobopenings_query = """
    SELECT COUNT(job_id) AS total_openings 
    FROM job_openings;
    """

    return query_data(total_jobopenings_query).iloc[0]["total_openings"]


def save_candidate_details(jd_id, bu_id, candidate_details_list):
    """Saving the candidate details"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """INSERT INTO candidates(name, email, phone, resume, bu_id, jd_id, status, status_updated_date)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""

            for candidate in candidate_details_list:
                cursor.execute(
                    sql,
                    (
                        candidate.name,
                        candidate.email,
                        candidate.phone,
                        candidate.resume,
                        bu_id,
                        jd_id,
                        "Applied",
                        datetime.now(),
                    ),
                )
                data = cursor.fetchone()
                candidate.id = data.get("id")
            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While saving candidates when screening: {error}")

    return candidate_details_list


def get_screened_candidates(jd_id: int, bu_id: int, interview: str):
    """Getting only selected candidates"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = "SELECT id, name, email, phone FROM selected_candidates WHERE interview = %s and jd_id = %s and bu_id = %s"

            cursor.execute(sql, (interview, jd_id, bu_id))
            results = cursor.fetchall()

            db_connection.close()
            return results

    except Exception as error:
        print(
            f"ERROR: While getting screened candidates for a specific JD in a specific business unit: {error}"
        )


def save_candidate_scores(candidate_results):
    """Saving the candidate scores"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """UPDATE candidates SET fit_score = %s where id = %s"""

            data = [(candidate.score, candidate.id) for candidate in candidate_results]
            cursor.executemany(sql, data)
            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While saving candidate scores: {error}")


def update_candidate_interview_status(jd_id, bu_id, candidate_status):
    """Updating interview status"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """UPDATE candidates SET status = %s where id = %s and bu_id = %s and jd_id = %s"""

            data = [
                (candidate.interview_status, candidate.id, bu_id, jd_id)
                for candidate in candidate_status
            ]
            cursor.executemany(sql, data)
            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While saving candidate scores: {error}")
    pass


if __name__ == "__main__":
    connect_db_env()
