from flask import Flask
from flask import request
import ast

from IPython.display import HTML


import pandas as pd
from sklearn.preprocessing import LabelEncoder

dpool=['A000', 'A001', 'A009', 'A0100', 'A0101', 'A0102', 'A0103',
       'A0104', 'A0105', 'A0109', 'A011', 'A012', 'A013', 'A014', 'A020',
       'A021', 'A0220', 'A0221', 'A0222', 'A0223']

ppool=['04B00ZZ', '04B04ZZ', '04R007Z', '04R00JZ', '04R00KZ', '04R047Z',
       '04R04JZ', '04R04KZ', '0X600ZZ', '0X610ZZ', '0X620ZZ', '0X630ZZ',
       '0X680Z1', '0X680Z2', '0X680Z3', '0X690Z1', '0X690Z2', '0X690Z3',
       '0X6B0ZZ', '0X6C0ZZ', '0X6D0Z1', '0X6D0Z2', '0X6D0Z3', '0X6F0Z1',
       '0X6F0Z2', '0X6F0Z3', '0X6J0Z0', '0X6J0Z4', '0X6J0Z5', '0X6J0Z6',
       '0X6J0Z7', '0X6J0Z8', '0X6J0Z9', '0X6J0ZB', '0X6J0ZC', '0X6J0ZD',
       '0X6J0ZF', '0X6K0Z0', '0X6K0Z4', '0X6K0Z5', '0X6K0Z6', '0X6K0Z7',
       '0X6K0Z8', '0X6K0Z9', '0X6K0ZB', '0X6K0ZC', '0X6K0ZD', '0X6K0ZF',
       '0X6L0Z0', '0X6L0Z1', '0X6L0Z2', '0X6L0Z3', '0X6M0Z0', '0X6M0Z1',
       '0X6M0Z2', '0X6M0Z3', '0X6N0Z0', '0X6N0Z1', '0X6N0Z2', '0X6N0Z3',
       '0X6P0Z0', '0X6P0Z1', '0X6P0Z2', '0X6P0Z3', '0X6Q0Z0', '0X6Q0Z1',
       '0X6Q0Z2', '0X6Q0Z3', '0X6R0Z0', '0X6R0Z1', '0X6R0Z2', '0X6R0Z3',
       '0X6S0Z0', '0X6S0Z1', '0X6S0Z2', '0X6S0Z3', '0X6T0Z0', '0X6T0Z1',
       '0X6T0Z2', '0X6T0Z3', '0X6V0Z0', '0X6V0Z1', '0X6V0Z2', '0X6V0Z3',
       '0X6W0Z0', '0X6W0Z1', '0X6W0Z2', '0X6W0Z3', '0Y620ZZ', '0Y630ZZ',
       '0Y640ZZ', '0Y670ZZ', '0Y680ZZ', '0Y6C0Z1', '0Y6C0Z2', '0Y6C0Z3',
       '0Y6D0Z1', '0Y6D0Z2', '0Y6D0Z3', '0Y6F0ZZ']


def HTML_with_style(df, style=None, random_id=None):
    import numpy as np
    import re

    df_html = df.to_html()

    if random_id is None:
        random_id = 'id%d' % np.random.choice(np.arange(1000000))

    if style is None:
        style = """
        <style>
            table#{random_id} {{color: blue}}
        </style>
        """.format(random_id=random_id)
    else:
        new_style = []
        s = re.sub(r'</?style>', '', style).strip()
        for line in s.split('\n'):
                line = line.strip()
                if not re.match(r'^table', line):
                    line = re.sub(r'^', 'table ', line)
                new_style.append(line)
        new_style = ['<style>'] + new_style + ['</style>']

        style = re.sub(r'table(#\S+)?', 'table#%s' % random_id, '\n'.join(new_style))

    df_html = re.sub(r'<table', r'<table id=%s ' % random_id, df_html)

    return style + df_html



from numpy import random
import numpy as np
random.seed(7)

sele = list(dpool)+list(ppool)

#testcode=random.choice(sele, size=random.randint(3,15))

#dic=request.args
dic=[]




import os
import pandas as pd
import math
import findspark

findspark.init('/usr/hdp/2.6.0.3-8/spark')

from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from pyspark import rdd, SparkContext, SparkFiles

sc=SparkContext()


from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType, FloatType

from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

schema = StructType([StructField('userID', IntegerType(), True), 
                     StructField('codeID', IntegerType(), True), 
                     StructField('valid_prob', FloatType(), True)])



app = Flask(__name__)

@app.route('/')
def hello_world():
    global dic
    
    def newcode_helper(ID):
        result=[]
        for i in testcode:
            result.append([ID,i,1.0])
        return result

    def genOneClaim():
        rd =  random.choice(dpool, 1)
        # print rd

        rp = random.choice(dpool, random.randint(3,15))
        # print rp

        pool = np.concatenate([rd, rp])
        return pool    
    
    dic=request.args
    
    s=''
    for i in dic:
        s=s+str(i)
        
    print dic, 'len dic',len(dic)
    testcode= [str(i) for i in dic]    
    
    
    print 'test:', testcode, type(testcode), len(testcode)
    
    testcode=[str(i) for i in testcode[0].split(',')]
    
    print testcode
    
    for t in testcode:print t
    
    mock=[]
    
    for i in range(1000):
        mock.append(genOneClaim())
    
    print len(mock)
    
    
    mock.append(testcode)
    #print mock
    df = pd.DataFrame([{i:1 for i in j} for j in mock]).fillna(0)
    
    print df.shape
    df['index']=df.index+1
    
    dfm = df.melt(id_vars=['index'])
    
    le = LabelEncoder()
    
    le.fit(dfm['variable'].unique())
    
    
        
        
    dfm['code']=le.transform(dfm['variable'])
    exist_code = dfm['code'].unique()
    
    
    testcode=le.transform(testcode)
    print testcode

    
    new = sc.parallelize(newcode_helper(999))
    
    print new
    
    dfm2 = dfm[['index','code','value']]
    table = sc.parallelize(dfm2.values)
    table = table.map(lambda x: [int(x[0]), int(x[1]), x[2]])
    
    data = sc.union([table ,new])
    ratings = data.map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))
    rank = 10
    numIterations = 10
    
    print 'start fitting matrix'
    model = ALS.train(ratings, rank, numIterations)
    print 'model done'
    
    print model.predict(1,2)

    
    
    results1 = model.predictAll(sc.parallelize([(999,i) for i in exist_code]))
    results2 = model.predictAll(sc.parallelize([(999,i) for i in testcode]))
    
    
    df1 = sqlContext.createDataFrame(results1, schema)
    df2 = sqlContext.createDataFrame(results2, schema)
    
    df=pd.concat([df2.toPandas(), df1.toPandas()])
    df = df.reset_index()
    
       
    
    from sklearn.preprocessing import MinMaxScaler
    df['valid_prob'] = MinMaxScaler().fit_transform(df['valid_prob'].values.reshape(-1,1))
    
    df['codeID']=le.inverse_transform(df['codeID'])
    df = df[['codeID', 'valid_prob']]
    
    df['valid_prob'] =df['valid_prob'].apply(lambda x: round(x, 4))
    
    print df
    
    import pprint
    SS = dict(zip(df['codeID'], df['valid_prob']))
    #S = pprint.pformat(SS)



    
    
    return df.to_html()



