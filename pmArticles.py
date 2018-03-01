import requests
import sqlite3
import os
import re
import xml.etree.ElementTree as ET
import urllib2

pm_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

converter_url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0'

pmc_url = 'https://www.ncbi.nlm.nih.gov/utils/oa/oa.fcgi?'
# pmc_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles'


abstracts = []

class PM:
    def __init__(self, path):
        db_file = os.path.join(path,'pm.db')
        if os.path.isfile(db_file):
            self.db = sqlite3.connect(db_file)
        else:
            # create table if it doesn't exist
            fp = open(db_file, 'w')
            fp.close()
            self.db = sqlite3.connect(db_file)
            self.populate_tables('pmIds.txt')

    def populate_tables(self, pm_ids_file):

        pm_ids = self.read_pm_ids(pm_ids_file)

        with self.db:
            cur = self.db.cursor()
            cur.execute("DROP TABLE IF EXISTS Pubmed")
            cur.execute("CREATE TABLE Pubmed(Id TEXT, PmcId TEXT, Abstract TEXT, Introduction TEXT, WholeText TEXT)")

            for id in pm_ids:
                pmc_id = self.send_converter_query(id[0])

                text = self.send_pmc_query(pmc_id[0].encode("utf8"))
                text = self._cleanhtml(text)



                abstract = self.send_pm_query(id, 'pubmed', 'abstract')
                cur.execute("INSERT INTO Pubmed VALUES(?, ?, ?, ?, ?)",
                            (id, pmc_id, abstract.decode('utf8'), "", text))


    def read_pm_ids(self, file):

        with open(file) as f:
            content = f.readlines()
            pm_ids = [x.strip() for x in content]
            return pm_ids


    def send_converter_query(self, pmc_id):

        # trim the PMCID part
        url = converter_url + "?ids=" + pmc_id[4:].encode("utf8")

        try:
            res = requests.get(url)
            s0 = res.content.find("pmcid=") + 7
            s1 = res.content[s0:].find("\"") + s0
            pmc_id = res.content[s0:s1]
            if "status" in pmc_id:
                pmc_id = ""

            return pmc_id
        except Exception as e:
            print e

    def send_pm_query(self, pm_id, db, type):

        url = pm_url + '?id=' + pm_id + '&db=' + db + '&retmode=text&rettype=' + type

        try:
            res = requests.get(url)
            return res.content

        except Exception as e:
            print e

    def send_pmc_query(self, pmc_id):
        url = pm_url + '?id=' + pmc_id + '&db=pmc&retmode=xml'

        try:
            res = requests.get(url)

            s0 = res.content.find("<body>")
            s1 = res.content.find("</body>")

            # tree = ET.XML(res.content)

            # print res.content[s0:s1]
            return res.content[s0:s1]

        except Exceptio as e:
            print e

    def _cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    # def update_table(self):
    #
    #     with self.db:
    #         cur = self.db.cursor()
    #         pmc_ids = cur.execute("SELECT PmcId FROM Pubmed").fetchall()
    #
    #         for pmc_id in pmc_ids:
    #             text = self.send_pmc_query(pmc_id[0].encode("utf8"))
    #             text = self._cleanhtml(text)
    #
    #             cur.execute("UPDATE Pubmed SET WholeText = ? WHERE PmcId = ?", (text, pmc_id[0].encode("utf8")))
    #             print text

# pm = PM('')

# pm.update_table()
# pm.send_pmc_query('PMC13901')
# pm_ids = pm.read_pm_ids('pmIds.txt')
# pm.populate_table_with_pmc_ids(pm_ids)
