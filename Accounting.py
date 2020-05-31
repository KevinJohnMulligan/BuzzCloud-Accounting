# -----------------------------------------------------------
# runs double entry checks on banking transactions
# written by Kevin Mulligan and Roger Lewis
#
# -----------------------------------------------------------

import pandas as pd; import numpy as np; import time; import os; import argparse; import shortuuid
from forex_python.converter import get_rate, get_rates
import datetime

#HSBC_HK = "csv/hsbchk.csv"
#ICBC = "csv/icbc.csv"
#Halifax = "halifax.csv"

np.random.seed(0)   # set random seed

class Accounting():
    """ get chart of accounts into memory
    with open('csv/chart.csv', 'ra') as csv_file:
    reader = csv.reader(csv_file);"""
    #now establish logger
    #setup_logging(self, default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG')

    def __init__(self):
        self.main_account = "main"
    def run(self):
        """Begin by initalising Xero Chart"""
        self.chart = []
        self.chart = pd.read_csv('csv/chart-xero.csv')
        self.chart = self.chart.fillna(0)

        # attempt to get valid FX rates for a small set of currencies, keep them in dated csv files
        getFxRates()
        # read in the CSV created by AirTable for transactions and chart of accounts
        getTransactions()
        # build new df for primary ledger and each required account. Place each transaction into both
        buildDoubleEntryLedger()
        # read CSV showing bank input and output transactions
        #getBank()
        # go thru every double entry ledger entry not reconciled and get user to mark as reconciled
        promptReconciled()
        return


def getFxRates():
    """Retrieve the current foreign exchange rates for USD and GBP"""
    forex = []
    forex = get_rates('USD')
    forex = pd.DataFrame([forex], columns=forex.keys())
    #self.forex.loc[:, 'GBP']
    GBPUSD = forex['GBP'].values
    date_obj = datetime.datetime(2020, 5, 17)
    print("date"+ date_obj)
    test = get_rate('USD', 'GBP', date_obj)
    print(test)
    return GBPUSD

def getTransactions():
    return

def buildDoubleEntryLedger():
    return

class BankAccount:
    """create a bank account from a csv file and put it in a dataframe"""
    #this "self" is the instance/object of the BankAccount class.
    #Example:      <__main__.BankAccount object at 0x0000019777A06C88>

    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.bank_csv_file = 'csv/'+ bank_name + '.csv'
        print("bankacc init")
        print(self)
        # read csv in from file and store it as a dataframe
        self.bank_dataframe = pd.read_csv('csv/' + self.bank_name + '.csv')
        # fill empty cells with 0
        self.bank_dataframe = self.bank_dataframe.fillna(0)
        # remove duplicates, keep the first instance of a row
        self.bank_dataframe = self.bank_dataframe.drop_duplicates(subset=None,
                                                                  keep='first',
                                                                  inplace=False)
        # change the date column from string to datetime format
        self.bank_dataframe['Date'] = pd.to_datetime(self.bank_dataframe['Date'])
        # self.bank_dataframe['random_ID_all'] = np.random.permutation(self.bank_dataframe.shape[0])
        self.bank_dataframe['unique_ID'] = np.random.randint(low=100000,
                                                             high=999999,
                                                             size=len(self.bank_dataframe))
        return

    def sortDataframe(self):
        # order the entire list by date
        self.bank_dataframe = self.bank_dataframe .sort_values(['Date'])
        # reset the indexes and delete(drop) the old indexes
        self.bank_dataframe = self.bank_dataframe.reset_index(drop=True)
        return
    def getFirstTransactionDate(self):
        """get the second row (the first row 0 contains the titles), and return the only the date as a string (not its type)"""
        return str(self.bank_dataframe.head(1)['Date'])[4:14]

    def getLastTransactionDate(self):
        """get the second row and return the only the date as a string (not its type)"""
        return str(self.bank_dataframe.tail(1)['Date'])[4:14]

    def assignUniqueID(self):
        shortuuid.set_alphabet("0123456789")
        return shortuuid.random(length=10)


def promptReconciled():
    return


accts = Accounting()
#self = accts
accts.run()

halifax_obj = BankAccount("halifax")
halifax_obj.sortDataframe()

hsbc_hk_obj = BankAccount("hsbchk")
hsbc_hk_obj.sortDataframe()

print(halifax_obj.bank_dataframe.tail(5))
print(hsbc_hk_obj.bank_dataframe.tail(5))
print("\nfirst transaction date")
print(hsbc_hk_obj.getFirstTransactionDate())
print("last transaction date")
print(hsbc_hk_obj.getLastTransactionDate())

print(hsbc_hk_obj.assignUniqueID())
#
#
