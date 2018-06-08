import pandas as pd
import matplotlib.pyplot as plt

def showpic(df):
    print len(df)
    print 'viewing ',len(df), 'pics'
    
    f=0
    for i in range(df.shape[0]):
        f+=1
        if f%2==1:
            print f, '-', f+1
            plt.figure(figsize=((10,7)))
            ax = plt.subplot(1,2,1)
            score=df.iloc[i,2]
            if df.iloc[i,1]=='M':
                ax.set_title("Male "+str(score), color='b',size=20)
            else:
                ax.set_title("Female "+str(score), color='r',size=20)
            plt.imshow(plt.imread(df.iloc[i,0]))
        else:
            score=df.iloc[i,2]

            ax = plt.subplot(1,2,2)
            if df.iloc[i,1]=='M':
                ax.set_title("Male "+str(score), color='b',size=20)
            else:
                ax.set_title("Female "+str(score), color='r',size=20)
            plt.imshow(plt.imread(df.iloc[i,0]))
            plt.show()