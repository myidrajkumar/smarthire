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
    except Exception as error:
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
    except Exception as error:
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
        raise error


def save_doc_db(bu_id, jd_file, doc_content):
    """Saving the doc to DB"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = """INSERT INTO jobdescription(title, doc, bu_id, job_posted)
             VALUES(%s, %s, %s, %s)  RETURNING id;"""

            cursor.execute(sql, (jd_file, doc_content, bu_id, datetime.now()))
            data = cursor.fetchone()

            db_connection.commit()
            db_connection.close()

            return data.get("id")

    except Exception as error:
        print(f"ERROR: While saving JDs in DB: {error}")


def get_jds_for_bu_db(bu_id: int):  # -> Any | None:
    """Retrieve all JDs for the specific business units from the database"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = """SELECT jd.id as jd_id, title, bu.id as bu_id, job_posted
            FROM jobdescription jd JOIN businessunit bu on jd.bu_id = bu.id and bu.id = %s
            ORDER BY job_posted DESC"""

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
        raise error


# Query Data
# def query_data(query):
#     """Querying via Pandas"""
#     db_connection = connect_db_env()
#     return pd.read_sql(query, db_connection)


# def get_total_applications_count():
#     """Getting applications count"""

#     total_applications_query = """
#     SELECT COUNT(application_id) AS total_applications
#     FROM applications;
#     """

#     return query_data(total_applications_query).iloc[0]["total_applications"]


# def get_screening_efficiency():
#     """Getting screening efficiency"""

#     ai_screening_efficiency_query = """
#         SELECT COUNT(*) * 100.0 / (SELECT COUNT(*) FROM applications) AS ai_efficiency
#         FROM applications WHERE screening_score > 70;
#     """
#     return query_data(ai_screening_efficiency_query).iloc[0]["ai_efficiency"]


# def get_candidates_pipeline():
#     """Getting candidates pipeline"""

#     pipeline_query = """
#         SELECT stage, COUNT(*) AS candidates
#         FROM applications
#         GROUP BY stage;
#     """
#     return query_data(pipeline_query)


# def get_time_to_hire():
#     """Getting time to hire"""

#     time_to_hire_query = """
#         SELECT job_id, AVG(DATE_PART('day', date_updated - date_applied)) AS avg_time_to_hire
#         FROM applications
#         WHERE status = 'Hired'
#         GROUP BY job_id;
#     """
#     return query_data(time_to_hire_query)


# def get_max_time_to_hire():
#     """Getting maximum time to hire"""

#     max_time_to_hire_query = """
#        SELECT MAX(avg_time_to_hire) AS max_time
#        FROM (
#            SELECT job_id, AVG(DATE_PART('day', date_updated - date_applied)) AS avg_time_to_hire
#            FROM applications
#            WHERE status = 'Hired'
#            GROUP BY job_id
#        ) AS subquery;
#     """
#     return query_data(max_time_to_hire_query)


# def get_entire_job_openings_count():
#     """Getting entire job openings count"""

#     total_jobopenings_query = """
#     SELECT COUNT(job_id) AS total_openings
#     FROM job_openings;
#     """

#     return query_data(total_jobopenings_query).iloc[0]["total_openings"]


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


def get_screened_candidates(jd_id: int, bu_id: int, status: str):
    """Getting only selected candidates"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = f"SELECT id, name, email, phone, status, fit_score as screen_score, prelim_score, status_updated_date as last_update_date FROM candidates WHERE jd_id = {jd_id} and bu_id = {bu_id}"
            if status:
                sql += f" and status = '{status}'"

            cursor.execute(sql)
            results = cursor.fetchall()

            db_connection.close()
            return results

    except Exception as error:
        print(
            f"ERROR: While getting screened candidates for a specific JD in a specific business unit: {error}"
        )
        raise error


def save_all_candidates_scores_with_status(candidate_results, status):
    """Saving the candidate scores"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """UPDATE candidates SET fit_score = %s, status = %s, status_updated_date = %s where id = %s"""

            data = [
                (candidate.score, status, datetime.now(), candidate.id)
                for candidate in candidate_results
            ]
            cursor.executemany(sql, data)
            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While saving candidate scores: {error}")


def save_candidate_score_with_status(candidate_id, score, status):
    """Saving the candidate score with status"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """UPDATE candidates SET prelim_score = %s , status = %s, status_updated_date = %s where id = %s"""

            cursor.execute(sql, (score, status, datetime.now(), candidate_id))
            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While saving candidate scores: {error}")


def update_candidate_interview_status(jd_id, bu_id, candidate_status):
    """Updating interview status"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """UPDATE candidates SET status = %s, status_updated_date = %s where id = %s and bu_id = %s and jd_id = %s"""

            data = [
                (candidate.interview_status, datetime.now(), candidate.id, bu_id, jd_id)
                for candidate in candidate_status
            ]
            cursor.executemany(sql, data)
            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")


def save_question_answers_to_db(candidate_list, jd_id, bu_id, response):
    """Inserting correct answers"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """
            INSERT INTO candidate_questions_answers(
            candidate_id, jd_id, bu_id, question,
            option1, option2, option3, option4, answer
            ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            data = []
            for candidate_id in candidate_list:
                data.extend(
                    [
                        (
                            candidate_id,
                            jd_id,
                            bu_id,
                            question_info.question,
                            question_info.options[0],
                            question_info.options[1],
                            question_info.options[2],
                            question_info.options[3],
                            question_info.correct_answer,
                        )
                        for candidate_info in response.candidates_set
                        for question_info in candidate_info.questions_set
                    ]
                )

            cursor.executemany(sql, data)

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While saving question answers: {error}")


def save_candidate_credentials(candidateid, username, password):
    """Saving the candidate credentials"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """
            INSERT INTO candidate_credentials(
            candidate_id, username, password) VALUES(%s, %s, %s)
            """

            cursor.execute(sql, (candidateid, username, password))
            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While saving candidate credentials: {error}")


def get_interview_questions_from_db(jd_id, bu_id, candidate_id):
    """Get Interview Questions from DB"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = """SELECT question, option1, option2, option3, option4
            FROM candidate_questions_answers WHERE candidate_id = %s
            AND jd_id = %s AND bu_id = %s"""

            cursor.execute(sql, (candidate_id, jd_id, bu_id))
            results = cursor.fetchall()

            db_connection.close()
            return results

    except Exception as error:
        print(f"ERROR: While getting interview questions: {error}")


def get_candidate_from_db(candidate_id: int):
    """Get Candidate from DB"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = f"""SELECT name, email, phone
            FROM candidates WHERE id = {candidate_id}"""

            cursor.execute(sql)
            results = cursor.fetchone()

            db_connection.close()
            return results

    except Exception as error:
        print(f"ERROR: While getting candidates: {error}")


def validate_user_credentials(username, password):
    """Validate user credentials"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:

            sql = """SELECT id as candidate_id, name, email, phone, bu_id, jd_id
            FROM candidates WHERE id = (
                SELECT candidate_id FROM candidate_credentials 
                WHERE username = %s AND password = %s)"""

            cursor.execute(sql, (username, password))
            results = cursor.fetchone()

            db_connection.close()
            return results

    except Exception as error:
        print(f"ERROR: While getting candidates: {error}")


def get_answers_from_db(candidate_id, jd_id, bu_id):
    """Getting answers from the database"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """SELECT answer FROM candidate_questions_answers WHERE candidate_id = %s
            AND jd_id = %s and bu_id = %s"""

            cursor.execute(sql, (candidate_id, jd_id, bu_id))
            results = cursor.fetchall()

            db_connection.close()
            return results

    except Exception as error:
        print(f"ERROR: While getting business units: {error}")
        raise error


def update_candidate_preliminary_interview_status_db(
    jd_id, bu_id, candidate_list, status
):
    """Update candidate status"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = """UPDATE candidates SET status = %s, status_updated_date = %s where id = %s and bu_id = %s and jd_id = %s"""

            data = [
                (status, datetime.now(), candidate_id, bu_id, jd_id)
                for candidate_id in candidate_list
            ]
            cursor.executemany(sql, data)
            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")


def get_kpis_from_db():
    """Getting kpis from DB"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:
            # Query for total open positions
            cursor.execute(
                "SELECT COUNT(*) FROM visualization_jobs WHERE status = 'open'"
            )
            total_open_positions = cursor.fetchone()[0]

            # Query for total candidates sourced
            cursor.execute("SELECT COUNT(*) FROM visualization_candidates")
            total_candidates_sourced = cursor.fetchone()[0]

            # Query for offer acceptance rate
            cursor.execute(
                "SELECT COUNT(*) FROM visualization_offers WHERE accepted = TRUE"
            )
            offers_accepted = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM visualization_offers")
            total_offers = cursor.fetchone()[0]

            offer_acceptance_rate = (
                (offers_accepted / total_offers) * 100 if total_offers > 0 else 0
            )

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {
        "total_open_positions": total_open_positions,
        "total_candidates_sourced": total_candidates_sourced,
        "offer_acceptance_rate": offer_acceptance_rate,
    }


def get_job_analytics_from_db(job_id: int):
    """Getting analytics for a given job"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:
            # Query for application volume per job
            cursor.execute(
                "SELECT COUNT(*) FROM visualization_applications WHERE job_id = %s",
                (job_id,),
            )
            application_volume = cursor.fetchone()[0]

            # Query for pipeline health (candidates at different stages)
            cursor.execute(
                """
                SELECT 
                    application_status, COUNT(*)
                FROM visualization_applications
                WHERE job_id = %s
                GROUP BY application_status
            """,
                (job_id,),
            )
            pipeline_health = cursor.fetchall()

            # Query for job description effectiveness (application click-through rate, if tracked)
            # This assumes a table where job view data is stored (job_views)
            cursor.execute(
                """
                SELECT views, applications
                FROM visualization_job_views
                WHERE job_id = %s
            """,
                (job_id,),
            )
            job_views = cursor.fetchone()
            if job_views:
                views, applications = job_views
                job_description_effectiveness = (
                    (applications / views) * 100 if views > 0 else 0
                )
            else:
                job_description_effectiveness = 0

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {
        "application_volume": application_volume,
        "pipeline_health": dict(pipeline_health),
        "job_description_effectiveness": job_description_effectiveness,
    }


def get_sourcing_analytics_from_db():
    """Getting source analytics from database"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:
            # Query for source breakdown
            cursor.execute(
                """
                SELECT source, COUNT(*)
                FROM visualization_applications applications
                JOIN visualization_candidates candidates ON applications.candidate_id = candidates.candidate_id
                GROUP BY source
            """
            )
            source_breakdown = cursor.fetchall()

            # Query for geographical sourcing
            cursor.execute(
                """
                SELECT location, COUNT(*)
                FROM visualization_candidates
                GROUP BY location
            """
            )
            geographical_sourcing = cursor.fetchall()

            # Query for cost per source (assuming cost data exists in sourcing_costs table)
            cursor.execute(
                """
                SELECT source, SUM(cost)
                FROM visualization_sourcing_costs
                GROUP BY source
            """
            )
            cost_per_source = cursor.fetchall()

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {
        "source_breakdown": dict(source_breakdown),
        "geographical_sourcing": dict(geographical_sourcing),
        "cost_per_source": dict(cost_per_source),
    }


def get_screening_interview_analytics_from_db():
    """Getting screening analytics"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:
            # Query for screening progress (candidates passed screening)
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM visualization_screening_results
                WHERE pass = TRUE
            """
            )
            passed_screening = cursor.fetchone()[0]

            # Query for interview conversion rate (candidates who passed interview / total interviewed)
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM visualization_interviews
                WHERE result = 'pass'
            """
            )
            passed_interviews = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM visualization_interviews")
            total_interviews = cursor.fetchone()[0]

            interview_conversion_rate = (
                (passed_interviews / total_interviews) * 100
                if total_interviews > 0
                else 0
            )

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {
        "passed_screening": passed_screening,
        "interview_conversion_rate": interview_conversion_rate,
    }


def get_offer_hiring_analytics_from_db():
    """Getting offere analytics"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:
            # Query for offer to hire ratio (offers accepted / total offers)
            cursor.execute(
                "SELECT COUNT(*) FROM visualization_offers WHERE accepted = TRUE"
            )
            accepted_offers = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM visualization_offers")
            total_offers = cursor.fetchone()[0]

            offer_to_hire_ratio = (
                (accepted_offers / total_offers) * 100 if total_offers > 0 else 0
            )

            # Query for candidate drop-off rate (candidates who applied but did not get hired)
            cursor.execute(
                """
                SELECT 
                    COUNT(*) 
                FROM visualization_applications 
                WHERE application_status IN ('rejected', 'withdrawn')
            """
            )
            dropped_candidates = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM visualization_applications")
            total_candidates = cursor.fetchone()[0]

            drop_off_rate = (
                (dropped_candidates / total_candidates) * 100
                if total_candidates > 0
                else 0
            )

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {
        "offer_to_hire_ratio": offer_to_hire_ratio,
        "candidate_drop_off_rate": drop_off_rate,
    }


def get_diversity_metrics_from_db():
    """Getting Diversity Metrics"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:
            # Query for gender diversity
            cursor.execute(
                """
                SELECT gender, COUNT(*)
                FROM visualization_candidates
                GROUP BY gender
            """
            )
            gender_diversity = cursor.fetchall()

            # Query for ethnicity diversity
            cursor.execute(
                """
                SELECT ethnicity, COUNT(*)
                FROM visualization_candidates
                GROUP BY ethnicity
            """
            )
            ethnicity_diversity = cursor.fetchall()

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {
        "gender_diversity": dict(gender_diversity),
        "ethnicity_diversity": dict(ethnicity_diversity),
    }


def get_candidate_experience_from_db():
    """Candidates Experience"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:
            # Query for average candidate NPS (assuming a table candidate_feedback with NPS scores)
            cursor.execute(
                """
                SELECT AVG(nps_score)
                FROM visualization_candidate_feedback
            """
            )
            average_nps = cursor.fetchone()[0]

            # Query for the average time candidates spend in the hiring process (from application to offer/rejection)
            cursor.execute(
                """
                SELECT AVG(last_updated - date_applied) 
                FROM visualization_applications
            """
            )
            average_time_in_process = int(cursor.fetchone()[0])

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {
        "average_nps": average_nps,
        "average_time_in_process": average_time_in_process,
    }


def get_recruitment_efficiency_from_db():
    """Recruitment Efficiency"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:
            # Query for recruiter performance (applications handled by each recruiter)
            cursor.execute(
                """
                SELECT recruiter_name, COUNT(*) 
                FROM visualization_applications applications
                JOIN visualization_recruiters recruiters ON applications.recruiter_id = recruiters.recruiter_id
                GROUP BY recruiter_name
            """
            )
            recruiter_performance = cursor.fetchall()

            # Query for task completion rate (assuming a tasks table)
            cursor.execute(
                """
            SELECT r.recruiter_name, 
                   COUNT(*) FILTER (WHERE t.status = 'completed')::float / COUNT(*) * 100 AS completion_rate
            FROM visualization_recruiters r
            LEFT JOIN visualization_tasks t ON r.recruiter_id = t.recruiter_id
            GROUP BY r.recruiter_name
            """
            )
            task_completion_rate = cursor.fetchall()

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {
        "recruiter_performance": dict(recruiter_performance),
        "task_completion_rate": dict(task_completion_rate),
    }


def get_compliance_metrics_from_db():
    """Get the compliance metrics"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:
            # Query for Equal Employment Opportunity (EEO) compliance (e.g., distribution by gender or ethnicity)
            cursor.execute(
                """
                SELECT gender, COUNT(*)
                FROM visualization_candidates
                GROUP BY gender
            """
            )
            gender_distribution = cursor.fetchall()

            cursor.execute(
                """
                SELECT ethnicity, COUNT(*)
                FROM visualization_candidates
                GROUP BY ethnicity
            """
            )
            ethnicity_distribution = cursor.fetchall()

            # Query for GDPR compliance (assuming a column tracking GDPR consent in candidates table)
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM visualization_candidates
                WHERE gdpr_consent = TRUE
            """
            )
            gdpr_compliant_candidates = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM visualization_candidates
            """
            )
            total_candidates = cursor.fetchone()[0]

            gdpr_compliance_rate = (
                (gdpr_compliant_candidates / total_candidates) * 100
                if total_candidates > 0
                else 0
            )

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {
        "gender_distribution": dict(gender_distribution),
        "ethnicity_distribution": dict(ethnicity_distribution),
        "gdpr_compliance_rate": gdpr_compliance_rate,
    }


def get_jobs_from_db():
    """Getting Jobs"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT job_id, job_title FROM visualization_jobs")
            jobs = cursor.fetchall()

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")

    return {"jobs": jobs}


def remove_candidate_questions_from_db(candidate_id: int, jd_id: int, bu_id: int):
    """Removing Candidate Questions"""

    db_connection = connect_db_env()
    try:
        with db_connection.cursor() as cursor:

            sql = f"""DELETE FROM candidate_questions_answers WHERE
            candidate_id = {candidate_id} AND jd_id = {jd_id} AND bu_id = {bu_id}"""

            cursor.execute(sql)

            db_connection.commit()
            db_connection.close()

    except Exception as error:
        print(f"ERROR: While updating interview status: {error}")


if __name__ == "__main__":
    connect_db_env()
