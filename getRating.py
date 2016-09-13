#-*- coding: UTF-8 -*- 
#--------------------------------------------------------

#--------------------------------------------------------
from math import sqrt

def loadTrain(fileName='train_sub_txt.txt'):

    
    prefer = {}
    for line in open(fileName,'r'):       # 打开指定文件
        (userid, movieid, rating) = line.split(' ')     # 数据集中每行有3项，以空格分割
        prefer.setdefault(userid, {})      # 设置字典的默认格式
        prefer[userid][movieid] = float(rating)
    

    return prefer     
def sim_cos(perfer, person1, person2):#计算余弦相似度
    sim={}

    for item in prefer[person1]:#查找两用户都评分过的项目
        if item in prefer[person2]:
            sin[item]=1
    n=len(sim)
    if len(sim) == 0:
        return -1
    sum1 = sum([prefer[person1][item] for item in sim])#用户1所有相关项目评分
    sum2 = sum([prefer[person2][item] for item in sim])
    sum1Sq=sum([pow(prefer[person1][item],2) for item in sim])#求平方和
    sum2Sq=sum([pow(prefer[person2][item],2) for item in sim])
    sumMulti=sum([prefer[person1][item]*prefer[person2][item] for item in sim])#求乘积和
    num1 = sumMulti
    num2=sqrt(sum1Sq*sum2Sq)
    if num2 == 0: #分母为0，返回0
        return 0
    result=num1/num2
    return result
def sim_coscorrect(prefer,person1,person2):#计算修正后余弦相似度
    sim={}
    for item in prefer[person1]:
        if item in prefer[person2]:
            sin[item]=1
    n=len(sim)
    if len(sim) == 0:
        return -1

    sum1 = sum([prefer[person1][item] for item in sim])  
    sum2 = sum([prefer[person2][item] for item in sim])  

    sum1Sq = sum( [pow(prefer[person1][item]-getAverage(prefer,person1) ,2) for item in sim] )
    sum2Sq = sum( [pow(prefer[person2][item]-getAverage(prefer,person1) ,2) for item in sim] )


    sumMulti = sum([(prefer[person1][item]-getAverage(prefer,person1))*(prefer[person2][item]-getAverage(prefer,person1)) for item in sim])

    num1 = sumMulti
    num2 = sqrt(sum1Sq*sum2Sq)         
    if num2==0:                                      
        return 0  

    result = num1/num2
    return result   
	

def sim_pearson1(prefer,person1,person2):#计算pearson相似度
    sim={}
    for item in prefer[person1]:
        if item in prefer[person2]:
            sin[item]=1
    n=len(sim)
    if len(sim) == 0:
        return -1

    sum1 = sum([prefer[person1][item] for item in sim])  
    sum2 = sum([prefer[person2][item] for item in sim])  

    sum1Sq = sum( [pow(prefer[person1][item]-getAverage(prefer,person1) ,2) for item in sim] )
    sum2Sq = sum( [pow(prefer[person2][item]-getAverage(prefer,person2) ,2) for item in sim] )


    sumMulti = sum([(prefer[person1][item]-getAverage(prefer,person1))*(prefer[person2][item]-getAverage(prefer,person2)) for item in sim])

    num1 = sumMulti
    num2 = sqrt(sum1Sq*sum2Sq)         
    if num2==0:                                      
        return 0  

    result = num1/num2
    return result   

def sim_pearson(prefer, person1, person2):#计算pearson相似度
    sim = {}

    for item in prefer[person1]:
        if item in prefer[person2]:
            sim[item] = 1         

    n = len(sim)
    if len(sim)==0:
        return -1

   
    sum1 = sum([prefer[person1][item] for item in sim])  
    sum2 = sum([prefer[person2][item] for item in sim])  


    sum1Sq = sum( [pow(prefer[person1][item] ,2) for item in sim] )
    sum2Sq = sum( [pow(prefer[person2][item] ,2) for item in sim] )

    sumMulti = sum([prefer[person1][item]*prefer[person2][item] for item in sim])

    num1 = sumMulti - (sum1*sum2/n)
    num2 = sqrt( (sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))  
    if num2==0:                                             
        return 0  

    result = num1/num2
    return result


### 获取对item评分的K个最相似用户（K默认10），默认使用pearson相似度
def topKMatches(prefer, person, itemId, k=10, sim = sim_pearson):
    userSet = []
    scores = []
    users = []
    #找出所有prefer中评价过Item的用户,存入userSet
    for user in prefer:
        if itemId in prefer[user]:
            userSet.append(user)
    #计算相似度
    scores = [(sim(prefer, person, other),other) for other in userSet if other!=person]

    #按相似度排序
    scores.sort()
    scores.reverse()

    if len(scores)<=k:       #如果小于k，只选择这些做推荐。
        for item in scores:
            users.append(item[1])  #提取每项的userId
        return users
    else:                   #如果>k,截取k个用户
        kscore = scores[0:k]
        for item in kscore:
            users.append(item[1])  #提取每项的userId
        return users               #返回K个最相似用户的ID


### 计算用户对所有物品平均评分
def getAverage(prefer, userId):
    count = 0
    sum = 0
    for item in prefer[userId]:
        sum = sum + prefer[userId][item]
        count = count+1
    return sum/count


### 根据基于用户的邻域算法公式，预测userId对itemId的评分
def getRating(prefer1, userId, itemId, knumber=10,similarity=sim_pearson):
    sim = 0.0
    averageOther =0.0
    jiaquanAverage = 0.0
    simSums = 0.0
    #获取K近邻用户(评过分的用户集)
    users = topKMatches(prefer1, userId, itemId, k=knumber, sim = sim_pearson)

    #获取userId 的平均值
    averageOfUser = getAverage(prefer1, userId)     

    for other in users:
        sim = similarity(prefer1, userId, other)    #计算比较其他用户的相似度
        averageOther = getAverage(prefer1, other)   #该用户的平均分
        # 累加
        simSums += abs(sim)    #取绝对值
        jiaquanAverage +=  (prefer1[other][itemId]-averageOther)*sim   #累加，一些值为负

    # simSums为0，即该项目尚未被其他用户评分，这里的处理方法：返回用户平均分
    if simSums==0:
        return averageOfUser
    else:
        return (averageOfUser + jiaquanAverage/simSums)  


##==================================================================
##     getAllUserRating(): 获取所有用户的预测评分，存放到fileResult中
##
## 参数:fileTrain,fileTest 是训练文件和对应的测试文件，fileResult为结果文件
##     similarity是相似度度量方法，默认是皮尔森。
##==================================================================
def getAllUserRating(fileTrain='train_sub_txt.txt', fileResult='result.txt', similarity=sim_pearson):
    prefer1 = loadTrain(fileTrain)         # 加载训练集 
    inAllnum = 0

    file = open(fileResult, 'w')
    c=[]
    for userid in range(1,10):             #test集中每个用户,共285个user，1682个item
        for item in range(1,10):   
            try:
                c.append(int(prefer1[str(userid)][str(item)]))
            except:
                c.append(0)
    print c
    

    
    
'''    
    for userid in range(1,286):             #test集中每个用户,共285个user，1682个item
        for item in range(1,1683):   
            try:
                r=prefer1[str(userid)][str(item)]
                file.write('%s %s %s\n'%(str(userid), str(item), int(r)))
            except:
                rating = getRating(prefer1, str(userid),str( item), 10)   #基于训练集预测用户评分
                file.write('%s %s %s\n'%(str(userid), str(item), int(round(rating))))
                inAllnum = inAllnum +1
    file.close()
'''


############    主程序   ##############
if __name__ == "__main__":
    print("\n--------------推荐系统 运行中-----------\n")
    getAllUserRating('train_sub_txt.txt','result.txt')










