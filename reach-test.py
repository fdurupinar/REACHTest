import requests
import json
import time
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from pmArticles import PM
import urllib



reach_text_url = 'http://localhost:8080/api/textBody'
# reach_text_url = 'http://agathon.sista.arizona.edu:8080/odinweb/api/text'
performances = []

pm = PM('')

def send_reach_query(msg):

    url = reach_text_url

    data = {'text': msg.encode('utf-8'), 'output':'indexcard'}

    # data = urllib.urlencode(data)


    try:
        ts0 = time.time()
        res = requests.post(url, data=data)
        ts1 = time.time()

        json_str = res.content
        card_len = 0
        json_obj = json.loads(json_str)


        if(json_obj and 'cards' in json_obj):
            card_len = len(json_obj['cards'])

        return {'textSize': len(msg), 'cardLength': card_len, 'runTime': ts1-ts0}

    except requests.exceptions.RequestException as e:
        print('Could not connect to REACH service:')
        print(e)




def send_reach_queries_for_text(file, text_type, max_cnt):

    with pm.db:
        cur = pm.db.cursor()
        query = "SELECT " + text_type + " FROM Pubmed"
        fields = cur.execute(query).fetchall()
        i = 0
        for field in fields:
            if len(field[0]) > 1:
                perf = send_reach_query(field[0])
                performances.append(perf)
            i += 1
            if i >= max_cnt:
                break

    with open(file, "w") as f:
        f.write('Text size\t#Index cards\tTime(secs)\n')

        for perf in performances:
            f.write(str(perf['textSize']) + "\t" + str(perf['cardLength']) + "\t" + str(perf['runTime']) + '\n')



def plot_performance(file):

    performances = []
    with open(file) as f:
        lines = f.readlines()

        for i in range(1, len(lines)):

            words = lines[i].split('\t')
            performances.append({'textSize': float(words[0])*0.001, 'cardLength': int(words[1].strip()), 'runTime': float(words[2])})

    print performances
    ax = plt.axes(projection='3d')
    ax.set_xlabel('Text size (kb)')
    ax.set_ylabel('# index cards')
    ax.set_zlabel('Run time (sec)')
    for perf in performances:
        ax.scatter3D(perf['textSize'],perf['cardLength'],  perf['runTime'],   c = 'red', cmap='Greens');

    plt.show()

# plot_performance('performance.txt')
plot_performance('performancePapers.txt')
# send_reach_queries_for_abstracts('performance.txt', 500)
# send_reach_queries_for_text('performance.txt', "Abstract", 500)
# send_reach_queries_for_text('performancePapers.txt', "WholeText", 500)
# plot_performance()





# print get_pm_abstracts('pmIds.txt', 'abstracts.txt')
# send_reach_query('AKT1 phosphorylates MAPK1')

# send_pmc_query('PMC2797771', 'pmc')