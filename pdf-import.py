from enum import Enum, auto
import re
import sqlite3
from sqlite3 import Error
from locale import atof, setlocale, LC_NUMERIC
from typing import Optional

database = "test.db"

sql_create_agents_table = """CREATE TABLE IF NOT EXISTS "agents" (
                                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                "agent_no" TEXT,
                                "agent_name" TEXT
                            );"""

sql_create_commission_settlements_table = """CREATE TABLE IF NOT EXISTS "commission_settlements" (
                                            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                            "agent_no" TEXT NOT NULL,
                                            "periode" TEXT,
                                            "description" TEXT
                                        );"""

sql_create_commission_settlement_items_table = """CREATE TABLE IF NOT EXISTS "commission_settlement_items" (
                                                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                "commission_settlement_id" NUMERIC,
                                                "agent_no" TEXT NOT NULL,
                                                "description" TEXT,
                                                "amount" NUMERIC
                                            );"""

sql_create_commission_reports_table = """CREATE TABLE IF NOT EXISTS "commission_reports" (
                                            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                            "agent_no" TEXT NOT NULL,
                                            "periode" TEXT,
                                            "total_amount" NUMERIC,
                                            "description" TEXT,
                                            "type" TEXT
                                        );"""

sql_create_commission_report_items_table = """CREATE TABLE IF NOT EXISTS "commission_report_items" (
                                                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                "commission_report_id" NUMERIC,
                                                "agent_no" TEXT NOT NULL,
                                                "contract_no" TEXT,
                                                "name" TEXT,
                                                "product" TEXT,
                                                "rn" TEXT,
                                                "akt" TEXT,
                                                "from_date" TEXT,
                                                "premium" NUMBER,
                                                "commission" NUMBER
                                            );"""

# Functions and declarations


def slices(s, *args):
    position = 0
    for length in args:
        yield s[position:position + length]
        position += length


class ProcessingStep(Enum):
    Default = auto()
    Header = auto()
    Details = auto()


def get_str(data: any):
    return str(data).strip()


def get_float(data: any):
    return atof(str(data).replace(".", "").replace(",", "."))


def texist(source, start, substr):
    txt_length = len(substr)
    if not substr:
        return False
    if start < 0 or start > len(source)-1 or start+txt_length > len(source):
        return False
    if source[start:(start+txt_length)] == substr:
        return True

    return False


def ss(source, start, length=None):
    if length == None:
        return source[start:]

    return source[start:start+length]


def db_create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def db_create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def db_add_agent(database, agent_no, agentName):
    """ Save agent to database """
    conn = None
    try:
        conn = db_create_connection(database)
        if conn is not None:
            db_create_table(conn, sql_create_agents_table)
            sql = """SELECT MAX(id) AS id, agent_no, agent_name FROM agents WHERE trim(agent_no)=trim(?) GROUP BY agent_no, agent_name """
            cur = conn.cursor()
            cur.execute(sql, (agent_no,))
            agents = cur.fetchone()

            if not agents:
                sql = """INSERT INTO agents(agent_no, agent_name) VALUES(?,?)"""
                cur = conn.cursor()
                cur.execute(sql, (agent_no, agentName))
                conn.commit()
                return cur.lastrowid
            else:
                return agents[0]
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def db_save_commission_settlement(description, periode, agent_no, items):
    """ Save Commission settlement to the database """
    conn = None
    try:
        conn = db_create_connection(database)
        if conn is not None:
            db_create_table(conn, sql_create_commission_settlements_table)
            db_create_table(conn, sql_create_commission_settlement_items_table)
            sql1 = """INSERT INTO commission_settlements(agent_no, periode, description) VALUES(?,?,?)"""
            sql2 = """INSERT INTO commission_settlement_items(commission_settlement_id, agent_no, description, amount) VALUES(?,?,?,?)"""
            cur = conn.cursor()
            cur.execute(sql1, (agent_no, periode, description))
            commission_settlement_id = cur.lastrowid
            for item in items:
                cur.execute(sql2, (commission_settlement_id, agent_no, ss(item, 5, 39), ss(item, 44)))
            conn.commit()
            return cur.lastrowid
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return


def db_save_commission_report_1(agent_no, name, periode, type, total_amount, items):
    """ Save Commission report 1 to the database """
    conn = None
    try:
        conn = db_create_connection(database)
        if conn is not None:
            db_create_table(conn, sql_create_commission_reports_table)
            db_create_table(conn, sql_create_commission_report_items_table)
            sql1 = """INSERT INTO commission_reports(agent_no, periode, total_amount, type, description) VALUES(?,?,?,?,?)"""
            sql2 = """INSERT INTO commission_report_items(commission_report_id, agent_no, contract_no, name, product, rn, akt, from_date, premium, commission) VALUES(?,?,?,?,?,?,?,?,?,?)"""
            cur = conn.cursor()
            cur.execute(sql1, (agent_no, periode, total_amount, type, name))
            commission_report_id = cur.lastrowid
            for item in items:
                cur.execute(sql2, (commission_report_id, agent_no, ss(item, 5, 13), ss(item, 18, 24), ss(item, 42, 9), ss(item, 51, 1), ss(item, 53, 4), ss(item, 57, 6), get_float(ss(item, 63, 12)), get_float(ss(item, 75, 14))))
            conn.commit()
            return cur.lastrowid
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return


def db_save_commission_report_2(agent_no, name, periode, type, total_amount, items):
    """ Save Commission report 2 to the database """
    return


def db_save_commission_report_3(agent_no, name, periode, type, total_amount, items):
    """ Save Commission report 2 to the database """
    return

def main():

    # Testing purposes only
    data = slices('Dette er en test', 6, 3, 3, 10)

    for d in data:
        print(d)

    # Main program
    encodings = ["utf-8", "ISO-8859-1", "windows-1250", "windows-1252"]
    regex_page = r"((.?)stream(.|\n)BT(?P<page>.*?)ET(.|\n)endstream)|(\/Title(?P<title>.*?)\n)"
    regex_objects = r"(?P<object>[0-9]+\s+[0-9]+\s+obj\s.+?endobj)"
    regex_text = r"\((?P<text>.*)\)\s*?Tj"

    for e in encodings:
        try:
            with open("test.pdf", "r", encoding=e) as strm:
                pdf = strm.read()
                strm.close()

        except UnicodeDecodeError:
            print('got unicode error with %s , trying different encoding' % e)
        else:
            print('opening the file with encoding:  %s ' % e)

            matches = re.finditer(regex_page, pdf, re.DOTALL)
            matches_enum = enumerate(matches, start=1)
            elements = []

            for matchNum, match in matches_enum:
                page = match.group("page")
                pageTitle = match.group("title")
                if not page:
                    continue
                sub_matches = re.finditer(regex_text, page, re.MULTILINE | re.IGNORECASE)
                sub_matches_enum = enumerate(sub_matches, start=1)

                for subMatchNum, sub_match in sub_matches_enum:
                    sub_group_text = sub_match.group("text")
                    elements.append(sub_group_text)

                elements.append("### END ###")

            with open("test.txt", "w") as strm:
                strm.writelines('\n'.join(elements) + '\n')

            # TODO: Convert these variable to appropriate classes.
            agent_no = ""
            agent_name = ""
            processing_step: ProcessingStep = ProcessingStep.Default

            commission_settlemenmt = False
            commission_settlemenmt_name = ""
            commission_settlemenmt_periode = ""
            commission_settlemenmt_items = []

            commission_report = False
            commission_report_name = ""
            commission_report_periode = ""
            commission_report_type = ""
            commission_report_items = []

            for element in elements:
                if texist(element, 53, "AGENT:"):
                    agent_name = get_str(ss(element, 60))
                    continue

                if texist(element, 40, "AGENTNR:"):
                    if get_str(ss(element, 50, 10)) != agent_no:
                        agent_no = get_str(ss(element, 50, 10))
                        db_add_agent(database, agent_no, agent_name)
                    continue

                # Commission settlement
                if texist(element, 10, "PROVISJONSAVREGNING FRA"):
                    commission_settlemenmt = True
                    commission_settlemenmt_name = get_str(ss(element, 10, 58))
                    commission_settlemenmt_periode = get_str(ss(element, 76))
                    commission_settlemenmt_items.clear()
                    continue

                if commission_settlemenmt and not texist(element, 5, "PROVISJON") and not texist(element, 5, "TOTALT"):
                    commission_settlemenmt_items.append(element)
                    continue

                if commission_settlemenmt and texist(element, 5, "PROVISJON"):
                    commission_amount = get_float(ss(element, 31))
                    continue

                if commission_settlemenmt and texist(element, 5, "TOTALT"):
                    commission_settlemenmt = False
                    total_amount = get_float(ss(element, 31))
                    db_save_commission_settlement(commission_settlemenmt_name, commission_settlemenmt_periode, agent_no, commission_settlemenmt_items)
                    continue

                # Commission report
                if texist(element, 10, "PROVISJONSOPPGAVE FRA"):
                    commission_report = True
                    commission_report_name = get_str(ss(element, 10, 56))
                    commission_report_periode = get_str(ss(element, 75))
                    commission_report_items.clear()
                    commission_report_type = ""
                    processing_step = ProcessingStep.Default
                    continue

                if commission_report and not texist(element, 50, "TOTALT") and not texist(element, 76, "TOTALT:"):
                    if processing_step == ProcessingStep.Default:
                        commission_report_type = get_str(element).strip("* ")
                        processing_step = ProcessingStep.Header
                        continue
                    if processing_step == ProcessingStep.Header and texist(element, 5, "AVTALE-NR               NAVN"):
                        processing_step = ProcessingStep.Details
                        continue
                    if processing_step == ProcessingStep.Header and texist(element, 5, "AVTALENR         NAVN"):
                        processing_step = ProcessingStep.Details
                        continue
                    if processing_step == ProcessingStep.Header and texist(element, 5, "AVTALENR  KUNDENAVN"):
                        processing_step = ProcessingStep.Details
                        continue
                    if processing_step == ProcessingStep.Details and texist(element, 0, "### END ###"):
                        processing_step = ProcessingStep.Header
                        continue
                    if processing_step == ProcessingStep.Details:
                        commission_report_items.append(element)

                    continue

                if commission_report and texist(element, 50, "TOTALT"):
                    commission_report = False
                    processing_step = ProcessingStep.Default
                    total_amount = get_float(ss(element, 70, 15))
                    db_save_commission_report_1(agent_no, commission_report_name, commission_report_periode, commission_report_type, total_amount, commission_report_items)
                    continue

                if commission_report and texist(element, 76, "TOTALT"):
                    commission_report = False
                    processing_step = ProcessingStep.Default
                    total_amount = get_float(ss(element, 83))
                    db_save_commission_report_2(agent_no, commission_report_name, commission_report_periode, commission_report_type, total_amount, commission_report_items)
                    continue

                if commission_report and texist(element, 53, "TOTALT"):
                    commission_report = False
                    processing_step = ProcessingStep.Default
                    total_amount = get_float(ss(element, 83))
                    db_save_commission_report_3(agent_no, commission_report_name, commission_report_periode, commission_report_type, total_amount, commission_report_items)
                    continue

            break


if __name__ == '__main__':
    main()
