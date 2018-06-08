import pandas as pd
import ast
import os
import math
os.chdir('D:/Dropbox/FreelancerDataMining')

bidders = pd.read_excel('userinfo2017/bidder1Data.xlsx')
bidders2 = pd.read_excel('userinfo2017/bidder1Data_Nojson.xlsx')
bidders3 = pd.read_excel('userinfo2017/boss1Data.xlsx')
bidders4 = pd.read_excel('userinfo2017/boss1Data_Nojson.xlsx')

bidders = pd.concat([bidders, bidders2, bidders3, bidders4])

def parseTimeZone(row):
    bid = row['about.id']
    timezone = ast.literal_eval(row['about.timezone'])
    if timezone and 'offset' in timezone:
        return {'bid':bid, 'country':timezone['country'],'offset':timezone['offset'],'timezone':timezone['timezone']}
    else: 
        return {'bid':bid, 'country':None,'offset':None,'timezone':None}

res = [parseTimeZone(row) for index, row in bidders.iterrows() if type(row['about.timezone']) is str]    
res = pd.DataFrame(res)    
res.to_csv('userinfo2017/users_timezone.csv',index=False)

print('Done!')