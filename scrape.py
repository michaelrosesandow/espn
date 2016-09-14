from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'http://games.espn.com/ffl/scoreboard?leagueId=427004&scoringPeriodId=1'
r = requests.get(url)
html = BeautifulSoup(r.text, 'html.parser')

score_tds = html.find_all('td', {'class':'score'})

def get_scores(score_td):
    score = score_td.get_text()
    owner = score_td.parent()[0].find_all('span', {'class':'owners'})[0].get_text()
    winning = len(score_td['class']) > 1
    return owner, score, winning

scores = pd.DataFrame([get_scores(td) for td in score_tds], columns=['name', 'score', 'win']).set_index('name')
scores['score'] = scores.score.astype('float')
scores['expected_win'] = 0.0

for owner in scores.index:
    scores.loc[owner, 'expected_win'] = (scores.loc[owner, 'score'] > scores[~scores.index.isin([owner])]).score.mean()

scores.sort_values(by='expected_win', ascending=False).to_csv('week_1_ew.csv')
