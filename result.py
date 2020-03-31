import matplotlib.pyplot as plt
import numpy as np

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def affiche_result(logs, total):
    print(total)
    # Graphique
    plt.figure(1)
    immu = []
    clean = []
    dead = []
    days = []
    bad = []
    good = []

    for i in range(len(logs)) :
        immu.append(logs[i][2])
        clean.append(logs[i][1])
        dead.append(logs[i][3])
        days.append(logs[i][0])
        bad.append(logs[i][4])
        good.append(total-logs[i][3])

    plt.title("Recapitulatif par jour")
    plt.plot(days, immu, "b--", label="Immu")
    plt.plot(days, clean, "g--", label="Clean")
    plt.plot(days, dead, "k", label="Morts")
    plt.plot(days, bad, "r", label="Malade")
    plt.plot(days, good, "c", label="Vivant")
    plt.ylabel('Results')
    plt.xlabel('days')
    plt.legend()

    # Fromage
    plt.figure(2)

    name = [str(logs[len(logs)-1][2]), str(logs[len(logs)-1][3]), str(logs[len(logs)-1][1])]
    data = [logs[len(logs)-1][2], logs[len(logs)-1][3], logs[len(logs)-1][1]]
    labels = ['Immu', 'Mort', 'Clean']
    color = ['b', 'k', 'g']
    explode = (0, 0.15, 0)

    plt.pie(data, colors=color, explode=explode, labels=name,
            autopct=lambda pct: func(pct, data), shadow=True, textprops={'color':"w"})
    plt.legend(labels)
    plt.title("Bilan de la simulation ("+str(total)+")")
    plt.show()

    #Clear
    logs.clear()
    good.clear()
