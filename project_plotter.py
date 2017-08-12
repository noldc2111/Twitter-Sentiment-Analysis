import matplotlib.pyplot as plt
import numpy as np
import operator


def makeList(file):
    label = []
    false = []
    true = []

    for each in file:
        y = each.split(";")
        #print(y[1])
        fl,fv = y[1].split(",")
        tr = y[2].strip('\n')
        tr,tv  = tr.split(",")
        tv = tv.lstrip(" ")
        nm = int(tv)/(int(fv)+int(tv))
        nm = nm*1000
        label.append(y[0])
        false.append(y[1])
#        true.append(tv)
        true.append(nm)

    return true, false, label

def econ_data(file):
    labels = []
    data = []
    for each in file:
        item = each.split(";")
        labels.append(item[0])
        dat = item[1].strip('\n')
        data.append(dat)
    return data, labels


econ = open("/Users/caseynold/Desktop/CS624/Project/economy.txt")
stock = open("/Users/caseynold/Desktop/CS624/Project/stock.txt")
positive = open("/Users/caseynold/Desktop/CS624/Project/positive.txt")
negative = open("/Users/caseynold/Desktop/CS624/Project/negative.txt")
dija = open("/Users/caseynold/Desktop/CS624/Project/djia.txt")

econ_file = econ.readlines()
stock_file = stock.readlines()
positive_file = positive.readlines()
negative_file = negative.readlines()
dija_file = dija.readlines()



true_s, false_s, label_s = makeList(stock_file)
true_e, false_e, label_e = makeList(econ_file)
true_p, false_p, label_p = makeList(positive_file)
true_n, false_n, label_n = makeList(negative_file)

econ_data, econ_labels = econ_data(dija_file)

plt.figure(1)
plt.subplot(211)
plt.title("Frequency of Positive & Negative Opinion Words")
#plt.plot(label_p, true_p, "g-")
pn= plt.plot(label_p, true_p, "g-", label_n,true_n,"c-")
plt.ylabel("Frequency of Occurrence")
plt.xlabel("November")
plt.axis([0,31,0,30])
plt.legend(pn,["Positive","Negative"])

plt.subplot(212)
plt.title("Dow Jones Industrial Average")
plt.plot(econ_labels, econ_data, "r-")
plt.axis([0,31,12000,15000])
plt.ylabel("Points")
plt.xlabel("November")
#plt.legend()

plt.figure(2)
plt.subplot(211)
plt.title("Frequency of 'Economy'")
#plt.plot(label_e,true_e,"g-",label_s,true_s,"r--")
plt.plot(label_e,true_e,"b-")
plt.axis([0,30,0,1])
plt.ylabel("Frequency of Occurrence")
plt.xlabel("November")
#plt.legend()


plt.subplot(212)
plt.title("Dow Jones Industrial Average")
plt.plot(econ_labels, econ_data, "r-")
plt.axis([0,31,12000,15000])
plt.ylabel("Points")
plt.xlabel("November\n\n")
#plt.legend()

plt.figure(3)
plt.subplot(211)
plt.title("Frequency of 'Stock Market'")
plt.plot(label_s,true_s,"m-")
plt.axis([0,30,0,0.1])
plt.ylabel("Frequency of Occurrence")
plt.xlabel("November")
#plt.legend()

plt.subplot(212)
plt.title("Dow Jones Industrial Average")
plt.plot(econ_labels, econ_data, "r-")
plt.axis([0,31,12000,15000])
plt.ylabel("Points")
plt.xlabel("November")
#plt.legend()

plt.show()

