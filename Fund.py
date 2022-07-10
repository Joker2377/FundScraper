class Fund:
    def __init__(self, *args):
        if len(args) == 2:
            self.id = args[0]
            self.name = args[1]
        elif len(args) == 1:
            self.id = args[0]
            self.name = None
        self.infoList = []
        self.valueList = []
        self.confList = []
        self.dataList = []
        self.earnList = []
        self.risk = None
        self.dividend = None

    def show(self):
        print(self.id + ' ' + self.name )
        print("Info:")
        for x in self.infoList:
            print(x)
        print('\n\n')
        print("Value List:")
        for x in self.valueList:
            print(x)
        print('\n\n')
        print("Earn List:")
        for x in self.earnList:
            print(x)
        print('\n\n')
        print("Configure List:")
        for x in self.confList:
            print(x)
        print('\n\n')
        print("Data List:")
        for x in self.dataList:
            print(x)
        print('\n\n')
        print("Risk:")
        print(self.risk)
        print('\n\n')
        print("Dividend:")
        if isinstance(self.dividend, str):
            print(self.dividend)
        else:
            for x in self.dividend:
                print(x)
        print('-----------------------------------------------------------')

    def addInfo(self, *args):
        for x in args:
            self.infoList.append(x)

    def setName(self, name):
        self.name = name

    def setValueList(self, listOfValue: list):
        self.valueList = listOfValue

    def setConfList(self, confList):
        self.confList = confList

    def setDataList(self, dataList):
        self.dataList = dataList

    def setRisk(self, risk):
        self.risk = risk

    def setDividend(self, dividend):
        self.dividend = dividend

    def setEarnList(self, earnList):
        self.earnList = earnList

    def getId(self):
        return self.id
