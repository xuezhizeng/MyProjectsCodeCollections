import csv
import numpy as np

attributes = []
states = []

with open('data.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    rowno = 0
    for row in spamreader:
        rowno += 1
        if rowno == 1:
            for i in range(len(row)):
                attributes.append(row[i])
            continue
        if row[4] not in states:
            states.append(row[4])

    population = np.zeros(len(states))
    leases = np.zeros(len(states))

    csvfile.seek(0)
    flag = 0
    for row in spamreader:
        flag += 1
        if flag ==1:
            continue
        leases[states.index(row[4])]+= 1
        population[states.index(row[4])] += float(row[attributes.index('Population')])
    avgpop = np.divide(population,leases)
    for i in range(len(states)):
        print 'State '+states[i]+' has '+str(int(leases[i]))+' leases, '+'average population: '+str(avgpop[i])
