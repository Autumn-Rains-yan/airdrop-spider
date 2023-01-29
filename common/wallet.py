import os
import time
from datetime import datetime
from threading import Thread

from mnemonic import Mnemonic
from web3 import Web3

from settings.ProjectSettings import BASE_DIR


class EthGenerateWallet:

    times = 0
    startTime = 0
    thousand = 0

    @staticmethod
    def createMetaMastAccount():
        filename = str(datetime.now())
        filenameNew = filename.replace('-', '').replace(':', '').replace(' ', '')
        contentStr = ''
        for i in range(0, 50):
            mnemo = Mnemonic('english')
            words = mnemo.generate(strength=128)
            w3 = Web3()
            w3.eth.account.enable_unaudited_hdwallet_features()
            account = w3.eth.account.from_mnemonic(words, account_path="m/44'/60'/0'/0/0")
            contentStr += f"{words};{str(account.privateKey.hex())};{str(account.address)};\n"

        file = open(BASE_DIR + '\\' + str(filenameNew) + '.txt', mode='a+')
        file.writelines(contentStr)
        file.close()

    @staticmethod
    def createAndGetBalance():
        print('开始刷eth')
        EthGenerateWallet.startTime = time.time()
        thread = {}
        for index in range(0, 3):
            thread[index] = Thread(target=EthGenerateWallet.createAndGetBalanceThread)
            thread[index].start()

    @staticmethod
    def createAndGetBalanceThread():
        for i in range(0, 5000000000):
            try:
                mumbai_rpc_url = "https://rpc-mumbai.maticvigil.com"
                mnemo = Mnemonic('english')
                words = mnemo.generate(strength=128)
                w3 = Web3(Web3.HTTPProvider(mumbai_rpc_url))
                w3.eth.account.enable_unaudited_hdwallet_features()
                account = w3.eth.account.from_mnemonic(words, account_path="m/44'/60'/0'/0/0")
                balance = w3.eth.getBalance(account.address)
                EthGenerateWallet.times = EthGenerateWallet.times + 1
                if EthGenerateWallet.times // 100 != EthGenerateWallet.thousand:
                    print(f"当前百次用时{time.time() - EthGenerateWallet.startTime}")
                    EthGenerateWallet.startTime = time.time()
                    EthGenerateWallet.thousand = EthGenerateWallet.times // 100
                if balance != 0:
                    print(f"{words}   {str(balance)}")
                    file = open(BASE_DIR + '/hasEth.txt', 'a+')
                    file.write(f"{words}   {str(balance)}\n")
                    file.close()
            except:
                pass

