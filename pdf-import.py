import sys
import re
import zlib
import sqlite3
from sqlite3 import Error
from locale import atof, setlocale, LC_NUMERIC

database = "test.db"

sql_create_agents_table = """CREATE TABLE IF NOT EXISTS "agents" (
                                "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                "agentno"	TEXT,
                                "agentname"	TEXT
                            );"""

# Functions and declarations


def slices(s, *args):
    position = 0
    for length in args:
        yield s[position:position + length]
        position += length


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
            sql = '''SELECT MAX(id) AS id, agentno, agentname FROM agents WHERE trim(agentno)=trim(?) GROUP BY agentno, agentname '''
            cur = conn.cursor()
            cur.execute(sql, (agent_no,))
            agents = cur.fetchone()

            if not agents:
                sql = '''INSERT INTO agents(agentno, agentname) VALUES(?,?)'''
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

            setlocale(LC_NUMERIC, "nb_NO.UTF-8")

            agent_no = ""
            agent_name = ""
            new_agent = False
            new_agent_saved = False
            commission_settlemenmt = False
            commission_settlemenmt_amount = 0.0
            commission_settlemenmt_name = ""
            commission_settlemenmt_periode = ""
            commission_settlemenmt_items = []

            for element in elements:
                if element[53:59] == "AGENT:":
                    agent_name = element[60:]
                    continue
                
                if element[40:48] == "AGENTNR:":
                    if element[50:60] != agent_no:
                        new_agent = True
                        new_agent_saved = False
                        agent_no = element[50:60]
                    continue                

                if element[10:33] == "PROVISJONSAVREGNING FRA":
                    print("PROVISJONSAVREGNING START")
                    commission_settlemenmt = True
                    commission_settlemenmt_amount = 0
                    commission_settlemenmt_name = element[34:68]
                    commission_settlemenmt_periode = element[77:]
                    continue

                if commission_settlemenmt and (element[5:14] != "PROVISJON") and (element[5:11] != "TOTALT") and (element[0:] != "### END ###"):
                    print("PROVISJONSAVREGNING COLLECTION")
                    commission_settlemenmt = True
                    commission_settlemenmt_amount += atof(element[50:])
                    commission_settlemenmt_items.append(element[5:40]+";"+element[50:])
                    continue
                
                if commission_settlemenmt and element[5:11] == "TOTALT":
                    print("PROVISJONSAVREGNING END")
                    commission_settlemenmt = False
                    continue
                
                if element[32:] == "*** STYKKPROVISJON ***":
                    print("Found!")
                    continue
                
                if element[27:] == "*** STYKKPROVISJON NÆRINGSLIV ***":
                    print("Found!")
                    continue
                
                if element[5:] == "AVTALENR         NAVN                           PRODUKT                      DATO   SJON":
                    print("Found!")
                    continue
                
                if element[5:] == "AVTALE-NR               NAVN         KJENNMRK N T    DATO      PREMIE    PROVISJON":
                    print("Found!")
                    continue
                
                if element[5:] == "AVTALENR  KUNDENAVN       PRODUKT         K  K  DATO         FORV.INNBET  PROVISJON":
                    print("Found!")
                    continue

                if new_agent and not new_agent_saved:
                    db_add_agent(database, agent_no, agent_name)
                    agent_no = ""
                    agent_name = ""
                    new_agent = False
                    new_agent_saved = True

                print(element)

            break


if __name__ == '__main__':
    main()
