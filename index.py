# 银行家算法
import re


class CommonError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class BankerAlgorithm(object):
    def __init__(self, n=4, m=3):
        self.n = n  # 进程数量
        self.m = m  # 资源有多少类

        self.Available = []  # 可用资源向量

        self.Max = {}  # 最大需求矩阵
        for i in range(0, self.n):
            self.Max["P{}".format(i)] = []
        self.Allocation = {}  # 分配矩阵
        for i in range(0, self.n):
            self.Allocation["P{}".format(i)] = []
        self.Need = {}  # 需求矩阵
        for i in range(0, self.n):
            self.Need["P{}".format(i)] = []
        self.Request = {}
        for i in range(0, self.n):
            self.Request["P{}".format(i)] = []

    def getInit(self):
        self.getMax()
        self.getAvailable()
        self.getNeed()

    def getAvailable(self):
        self.Available = []
        # self.Available = [1, 1, 2]
        for i in range(0, self.m):
            j = input(">")
            self.Available.append(int(j))

    def getMax(self):
        for i in range(0, self.n):
            # self.Max["P{}".format(i)] = []
            for j in range(0, self.m):
                k = input("P{}[{}]>>".format(i, j))
                self.Max["P{}".format(i)].append(k)

    def getAllocation(self):
        for i in range(0, self.n):
            # self.Allocation["P{}".format(i)] = []
            for j in range(0, self.m):
                k = input("P{}[{}]>>".format(i, j))
                self.Allocation["P{}".format(i)].append(k)

    def getNeed(self):
        for i in range(0, self.n):
            # self.Need["P{}".format(i)] = []
            for j in range(0, self.m):
                self.Need["P{}".format(i)].append(
                    self.Max["P{}".format(i)][j] - self.Allocation["P{}".format(i)][j]
                )
                if self.Need["P{}".format(i)][j] < 0:
                    print("[-] P{}Need Matrix{} Error".format(i, j))

    def getRequest(self):
        for i in range(0, self.n):
            self.Request["P{}".format(i)] = []

    def deBug(self):
        # output = ""
        print("n = {}".format(self.n))
        print("m = {}".format(self.m))
        print("Available = \n")
        print(self.Available)
        print("Max = \n")
        print(self.Max)
        print("Allocation = \n")
        print(self.Allocation)
        print("Need = \n")
        print(self.Need)

    def initRequest(self):
        self.Request = {}
        for i in range(0, self.n):
            self.Request["P{}".format(i)] = []

    def exampleInit1(self):
        # 9 3 6
        self.Available = [1, 1, 2]
        self.Max = {
            "P0": [3, 2, 2],
            "P1": [6, 1, 3],
            "P2": [3, 1, 4],
            "P3": [4, 2, 2]
        }
        self.Allocation = {
            "P0": [1, 0, 0],
            "P1": [5, 1, 1],
            "P2": [2, 1, 1],
            "P3": [0, 0, 2]
        }
        self.getNeed()
        # self.deBug()

    def exampleInit2(self):
        # 10 3 7
        self.Available = [1, 1, 2]
        self.Max = {
            "P0": [3, 2, 2],
            "P1": [6, 1, 3],
            "P2": [3, 1, 4],
            "P3": [4, 2, 2]
        }
        self.Allocation = {
            "P0": [1, 0, 0],
            "P1": [6, 1, 2],
            "P2": [2, 1, 1],
            "P3": [0, 0, 2]
        }
        self.getNeed()
        # self.deBug()

    def exmapleInit3(self):
        # 10 3 7
        self.Available = [1, 1, 2]
        self.Max = {
            "P0": [6, 2, 2],
            "P1": [6, 1, 3],
            "P2": [3, 1, 4],
            "P3": [4, 2, 2]
        }
        self.Allocation = {
            "P0": [1, 0, 0],
            "P1": [6, 1, 2],
            "P2": [2, 1, 1],
            "P3": [0, 0, 2]
        }
        self.getNeed()
        # self.deBug()

    def sendRequest(self, Px, vector):
        '''

        :param Px: 字符串...P0-P4
        :param vector: 请求向量，为一个列表
        :return:
        '''
        process_num = Px[1]
        self.checkRequestInputValid()
        self.Request[Px] = vector
        print(self.Request)
        for i in range(0, self.m):
            if self.Request[Px][i] > self.Need[Px][i]:
                raise CommonError("{}申请的资源数目Available[{}]不应该超过它的需求数目".format(Px, i))
            if self.Request[Px][i] > self.Available[i]:
                raise CommonError("{}需要等待，因为目前可用资源 Available[{}] 不够".format(Px, i))

        tmp_Available = self.Available
        tmp_Allocation = self.Allocation
        tmp_Need = self.Need

        for i in range(0, self.m):
            tmp_Available[i] = tmp_Available[i] - self.Request[Px][i]
            tmp_Allocation[Px][i] = tmp_Allocation[Px][i] + self.Request[Px][i]
            tmp_Need[Px][i] = tmp_Need[Px][i] - self.Request[Px][i]

        if self.checkTmpMatrixSafe(tmp_Available, tmp_Allocation, tmp_Need) is True:
            print("[+] Check safe ; Format changed")
            self.Allocation = tmp_Allocation
            self.Available = tmp_Available
            self.Need = tmp_Need

        else:
            print("[-] Not safe ; Format not changed")

    def checkTmpMatrixSafe(self, tmp_Available, tmp_Allocation, tmp_Need):
        '''

        :return:
        '''
        Work = tmp_Available
        Finish = [False] * self.n

        # finding valid i

        def helperChecker(tmp_Need_Px, Work, m):
            tag = True
            for i in range(0, m):
                if tmp_Need_Px[i] > Work[i]:
                    tag = False
            return tag

        for i in range(0, self.n):
            if Finish[i] is True:
                continue
            if Finish[i] is False and helperChecker(tmp_Need["P{}".format(i)], Work, self.m):
                print("[*] Finding P{} safe".format(i))
                for j in range(0, self.m):
                    Work[j] = Work[j] + tmp_Allocation["P{}".format(i)][j]
                Finish[i] = True
                # print(Finish)
                print(Work)

                for x in range(0, i):
                    if Finish[x] is True:
                        continue
                    if Finish[x] is False and helperChecker(tmp_Need["P{}".format(x)], Work, self.m):
                        print("[*] Finding P{} safe".format(x))
                        for y in range(0, self.m):
                            Work[y] += + tmp_Allocation["P{}".format(x)][y]
                        Finish[x] = True
                        # print(Finish)
                        print(Work)

        if Finish == [True] * self.n:
            # tmp_Available = __tmp_Available
            return True
        else:
            return False

    # Work = Work + tmp_Allocation["P{}".format(i)]

    def checkRequestInputValid(self):
        '''
        TODO
        :return:
        '''
        pass


def example2():
    try:
        Bancker = BankerAlgorithm()
        Bancker.exampleInit2()
        Bancker.sendRequest("P0", [1, 0, 1])
    except Exception as e:
        print(e)


def example1():
    try:
        Bancker = BankerAlgorithm()
        Bancker.exampleInit1()
        Bancker.sendRequest("P1", [1, 0, 1])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    example1()
    example2()
