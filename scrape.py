from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date

url_head = 'http://games.espn.com/ffl/scoreboard?leagueId=427004&scoringPeriodId=%s'
weeks = len(pd.date_range(date(2018,9,7), date.today(), freq='W'))+1

def get_scores(score_td, week_num):
    score = score_td.get_text()
    owner = score_td.parent()[0].find_all('span', {'class':'owners'})[0].get_text()
    winning = len(score_td['class']) > 1
    return owner, score, winning, week_num

x = []
for week in range(weeks):
    url = url_head % week
    r = requests.get(url)
    html = BeautifulSoup(r.text, 'html.parser')
    score_tds = html.find_all('td', {'class':'score'})
    week_len = ([week]*len(score_tds))
    x.extend(list(zip(week_len, score_tds)))
    

scores = pd.DataFrame([get_scores(td[1], td[0]) for td in x], columns=['name', 'score', 'win', 'week_num']).set_index(['name', 'week_num']).sort_index()
scores['score'] = scores.score.astype('float')
scores['expected_win'] = 0.0

uniq_owners = scores.index.get_level_values('name').unique()
for owner, week_num in scores.index:
    week_scores = scores.xs(week_num, level='week_num')
    expected_win = (float(week_scores.loc[owner, 'score']) > week_scores.loc[week_scores.index != owner, 'score']).mean()
    scores.loc[(owner,week_num), 'expected_win'] = expected_win
    
scores[['win', 'expected_win']].reset_index().groupby('name').sum().sort_values(by=['win', 'expected_win'],ascending=[False, False]).to_csv('week_%s_ew.csv' % (weeks-1))
