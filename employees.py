import matplotlib.pyplot as plt
import numpy as np
import time
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

txtfile = 'employees_dataset.csv'




class Candidate:
    def __init__(self, degree, education, skills, experience, position):
        self.degree = degree
        self.education = education
        self.skills = skills
        self.experience = experience
        self.position = position

    def printInfo(self):
        print("This candidate has degree of ", self.degree, ", from ", self.education, "and has skills ", self.skills,
              "\n has been worked for ", self.experience, " as ", self.position)


def readFromFile(txtfile):
    f = open(txtfile, 'r')
    lines = f.readlines()
    candidates = []
    for i in range(len(lines)):
        if i == 0:
            continue
        text = lines[i].split(',')
        degree = text[0]
        education = text[1]
        skills = text[2].split(';')
        experience = text[3].split(';')
        position = text[4].split('\n')
        candidates.append(Candidate(degree, education, skills, experience, position[0]))
    return candidates
    # candidates[0].printInfo()

if __name__ == "__main__":
    candidates=readFromFile(txtfile)
    skillsets=[]
    companysets=[]
    positionsets=[]
    degreesets=[]
    skillsets.append([candidates[0].skills[0],0,0,0])
    companysets.append([candidates[0].experience[0],0,0,0])
    positionsets.append(candidates[0].position)
    degreesets.append([candidates[0].degree,0,0,0])
    labelset=[]
    for i in range(len(candidates)):
        for j in range(len(candidates[i].skills)):
            for k in range(len(skillsets)):
                if candidates[i].skills[j] == skillsets[k][0]:
                    break
                if k==len(skillsets)-1:
                    skillsets.append([candidates[i].skills[j],0,0,0])
        for j in range(len(candidates[i].experience)):
            for k in range(len(companysets)):
                if candidates[i].experience[j] == companysets[k][0]:
                    break
                if k==len(companysets)-1:
                    companysets.append([candidates[i].experience[j],0,0,0])
        for j in range(len(positionsets)):
            if candidates[i].position == positionsets[j]:
                break
            if j==len(positionsets)-1:
                positionsets.append(candidates[i].position)
        for j in range(len(degreesets)):
            if candidates[i].degree == degreesets[j][0]:
                break
            if j==len(degreesets)-1:
                degreesets.append([candidates[i].degree,0,0,0])
        labelset.append(candidates[i].position)
    # print(len(skillsets))
    # print(positionsets)
    # print(degreesets)
    X_train, X_test, y_train, y_test = train_test_split(candidates, labelset, random_state=int(time.time()))
    print(len(X_test),len(y_test))
    # X_train[0].printInfo()
    for i in range(len(X_train)):
        for j in range(len(positionsets)):
            if X_train[i].position == positionsets[j]:
                for k in range(len(X_train[i].skills)):
                    for index in range(len(skillsets)):
                        if X_train[i].skills[k] == skillsets[index][0]:
                            skillsets[index][j+1] += 1
                for index in range(len(degreesets)):
                    if X_train[i].degree == degreesets[index][0]:
                        degreesets[index][j+1]+=1
    dev_predict=0
    dev_count=0
    dev_fn=0
    manager_predict=0
    manager_count=0
    manager_fn=0
    qa_predict=0
    qa_count=0
    qa_fn=0
    for k in range(len(X_test)):
        # id=int(time.time())%len(X_train)
        # X_train[id].printInfo()
        degree_pre=0;
        targetpersion=X_test[k]
        for i in range(len(degreesets)):
            if degreesets[i][0]==targetpersion.degree:
                degree_pre=i
                break
        # print(degree_pre)
        dev_pre=0
        manager_pre=0
        qa_pre=0
        for i in range(len(targetpersion.skills)):
            for j in range(len(skillsets)):
                if(targetpersion.skills[i]==skillsets[j][0]):
                    max=skillsets[j][1]
                    maxpos=1
                    if skillsets[j][2]>max:
                        max=skillsets[j][2]
                        maxpos=2
                    if skillsets[j][3]>max:
                        max=skillsets[j][3]
                        maxpos=3
                    if maxpos==1:
                        dev_pre+=1
                    if maxpos==2:
                        manager_pre+=1
                    if maxpos==3:
                        qa_pre+=1
        x=[dev_pre,manager_pre,qa_pre]
        predict=np.where(x==np.max(x))
        # print("predict=",predict[0][0])
        result=0
        if predict[0][0]==0:
            result='dev'
        if predict[0][0]==1:
            result='manager'
        if predict[0][0]==2:
            result='qa'
        print(result, y_test[k])
        if y_test[k]=='dev':
            if y_test[k]!=result:
                dev_fn+=1
        if y_test[k]=='manager':
            if y_test[k]!=result:
                manager_fn+=1
        if y_test[k]=='qa':
            if y_test[k]!=result:
                qa_fn+=1
        if result=='dev':
            dev_predict+=1
            if result==y_test[k]:
                dev_count+=1
        if result=='manager':
            manager_predict+=1
            if result==y_test[k]:
                manager_count+=1
        if result=='qa':
            qa_predict+=1
            if result==y_test[k]:
                qa_count+=1
    dev_precision=dev_count/dev_predict
    dev_recall=dev_count/(dev_count+dev_fn)
    dev_F1score=2*(dev_precision*dev_recall)/(dev_precision+dev_recall)
    print("dev:",dev_precision,dev_recall,dev_F1score)
    manager_precision = manager_count / manager_predict
    manager_recall = manager_count / (manager_count + manager_fn)
    manager_F1score = 2 * (manager_precision * manager_recall) / (manager_precision + manager_recall)
    print("manager:",manager_precision,manager_recall,manager_F1score)
    if qa_predict!=0:
        qa_precision = qa_count / qa_predict
        qa_recall = qa_count / (qa_count + qa_fn)
        qa_F1score = 2 * (qa_precision * qa_recall) / (qa_precision + qa_recall)
        print("qa:",qa_precision,qa_recall,qa_F1score)

    # print(count/len(X_test))
