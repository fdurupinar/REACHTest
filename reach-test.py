import requests
import json
import time
import matplotlib.pyplot as plt
from pmArticles import PM



reach_text_url = 'http://localhost:8080/api/text'
# reach_text_url = 'http://agathon.sista.arizona.edu:8080/odinweb/api/text'
performances = []

pm = PM('')

def send_reach_query(msg):

    url = reach_text_url + '?text= ' + msg.encode('utf-8') + '&output=indexcard'

    # data = {'text': msg.encode('utf-8'), 'output':'indexcard'}
    # print(json.dumps(data))
    # print(data)

    try:
        ts0 = time.time()
        res = requests.post(url)
        ts1 = time.time()

        json_str = res.content
        card_len = 0
        try:
            json_obj = json.loads(json_str)


            if(json_obj and 'cards' in json_obj):
                card_len = len(json_obj['cards'])

            return {'length': card_len, 'time': ts1-ts0}
        except:
            return {'length': 0, 'time': ts1-ts0}

    except requests.exceptions.RequestException as e:
        print('Could not connect to REACH service:')
        print(e)




def send_reach_queries_for_abstracts(file, max_cnt):

    with pm.db:
        cur = pm.db.cursor()
        abstracts = cur.execute("SELECT Abstract FROM Pubmed").fetchall()
        i = 0
        for abstract in abstracts:
            perf = send_reach_query(abstract[0])
            performances.append(perf)
            i += 1
            if i >= max_cnt:
                break

    with open(file, "w") as f:
        for perf in performances:
            f.write(str(perf['length']) + "\t" + str(perf['time']) + '\n')


def plot_performance():

    for perf in performances:
        plt.plot(perf['length'], perf['time'] , 'o', label='Fitted line')
    plt.show()


send_reach_queries_for_abstracts('performance.txt', 200)
# plot_performance()





# print get_pm_abstracts('pmIds.txt', 'abstracts.txt')
# send_reach_query('AKT1 phosphorylates MAPK1')

# send_pmc_query('PMC2797771', 'pmc')