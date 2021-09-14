# app.py
# Author: Jerrad Flores
import colorama
import block
import blockchain
import socket
import time



class UI():
  def __init__(self):
    self.name = "" #changes once user types in name
    self.cm_blockchain = blockchain.Blockchain("CM Blockchain")
    self.cm_blockchain.create_node(socket.gethostname())
    self.on_app = True
    self.dollar_balance = 1 #initlialized to 1 dollar, can generate more upon request.
    self.balances = {}


  def select_coin(self):
    coin = ""
    while coin not in self.balances.keys():
      coin_names = ""
      for name in self.balances.keys():
        coin_names += name
        coin_names += ", "

      coin = input(f'Please select a coin: {coin_names}:')
      if coin not in self.balances.keys():
        print(f'Please select a valid coin (one of the following): {coin_names}: ')
    return coin


  def view_balances(self):
    print("\tDollar Balance is:", self.dollar_balance)
    coin = self.select_coin()
    print("\tCurrent Balance for", coin, "is:", self.balances[coin], "currenly valued at:", self.cm_blockchain.value(coin), "per coin.")

  
  def add_money(self):
    quantity = ""
    while type(quantity) != int:
      try:
        quantity = int(input("Please type in how many DOLLARS you want to add: "))
      except ValueError:
        print("Must be a numerical value! Try again.")
    print("Currently adding", quantity, "dollars to your dollar balance...")
    time.sleep(quantity) # simulates the time to generate or "earn" the dollars.
    self.dollar_balance += quantity
    print("Successfully added", quantity, "dollars to your balance. Current DOLLARS balance:", self.dollar_balance)


  def sell_or_buy(self):
    sb = ""
    while sb != "Buy" and sb != "Sell":
      sb = input("Buy or Sell?: ")
      if sb != "Buy" and sb != "Sell":
        print("\nPlease select \"Buy\" or \"Sell\"")
    return sb


  def buy(self, coin):
    print("\nCurrent buying power (dollars)", "is", self.dollar_balance)
    if self.dollar_balance == 0:
      print("You currently have no", self.dollar_balance, "to use for buying coins.")
      return 0
    dollar_quantity = 1237123091203971203917209371093
    while (type(dollar_quantity) != int) or (dollar_quantity > self.dollar_balance):
      try:
        dollar_quantity = int(input("Please type the quantity of DOLLARS that you want to trade: "))
      except ValueError:
        print("Must be a numerical value! Try again.")
      if dollar_quantity > self.dollar_balance:
        print("You don't have that much dollars in your balance.")
    coin_quantity = dollar_quantity/self.cm_blockchain.value(coin)
    
    print("Currently buying", coin_quantity, coin, "valued at:", self.cm_blockchain.value(coin), "...")
    self.cm_blockchain.buy("CM_TRADING", self.name, coin_quantity, dollar_quantity, coin)
    self.balances[coin] += coin_quantity
    self.dollar_balance -= dollar_quantity


  def sell(self, coin):
    print("Current balance for", coin, "is", self.balances[coin])
    if self.balances[coin] == 0:
      print("You currently have no", coin, "to sell.")
      return 0
    coin_quantity = ""
    while (type(coin_quantity) != int) or (coin_quantity > self.balances[coin]):
      try:
        coin_quantity = int(input(f"\nPlease type the quantity of COIN that you want to sell (balance is currently {self.balances[coin]}): "))
      except ValueError:
        print("Must be a numerical Value! Try again.")
      if coin_quantity > self.balances[coin]:
        print("You don't have that much coin to sell.")
    dollar_quantity = coin_quantity * self.cm_blockchain.value(coin)
    print("Currently selling", coin_quantity, coin, "valued at:", self.cm_blockchain.value(coin))
    self.cm_blockchain.sell("CM_TRADING", self.name, dollar_quantity, coin_quantity, coin)
    self.balances[coin] -= coin_quantity
    self.dollar_balance += dollar_quantity


  def trade(self):
    coin = self.select_coin()
    sb = self.sell_or_buy()
    if sb == "Buy":
      self.buy(coin)
    elif sb == "Sell":
      self.sell(coin)
    print("SUCESSFULLY EXECUTED TRADE.")


  def mine(self):
    coin = self.select_coin()
    quantity = ""
    while type(quantity) != int:
      try:
        quantity = int(input(f"Please type the quantity of desired coin (more coins = more time taken to mine) valued currently at {self.cm_blockchain.value(coin)}: "))
      except ValueError:
        print("Must be a numerical value! Try again.")
    print("Currently Mining", quantity, coin, "...")
    block_mined = self.cm_blockchain.mine(quantity, coin, self.name)
    if block_mined != None:
      print("Successfully mined", quantity, coin)
      self.balances[coin] += quantity


  def intro(self):
    '''
    Welcomes user to app, and allows them to enter their name.
    '''
    print("Welcome to CM_TRADING!")
    self.name = input("Please enter your name: ")
    print("Welcome,", self.name, '\n\n')
    # Mine for 0 coin for all the coins that are going to be in the CM_TRADING system (that way we have them displayed in the app)

    # Why are the bought and sold values being initialized to 1?
    # In order to get the value of a coin, we need to be able to divide by a divisible greater than 0 (if not, we get an error). So, anything greater than 1 for a given coin indicates that the base value will be changed for that particular coin.
    self.balances["Butter Coin"] = 0
    self.cm_blockchain.bought["Butter Coin"] = 1
    self.cm_blockchain.sold["Butter Coin"] = 1
    self.balances["Official Coin"] = 0
    self.cm_blockchain.bought["Official Coin"] = 1
    self.cm_blockchain.sold["Official Coin"] = 1
    self.balances["Simple Coin"] = 0
    self.cm_blockchain.bought["Simple Coin"] = 1
    self.cm_blockchain.sold["Simple Coin"] = 1


  def choose_options(self):
    options = ""
    while options not in [0,1,2,3,4]:
      while type(options) != int:
        try:
          print("0 - Quit\n1 - Trade\n2 - Mine\n3 - View Balances\n4 - Add Money")
          options = int(input())
          if options == 1:
            self.trade()
          elif options == 2:
            self.mine()
          elif options == 3:
            self.view_balances()
          elif options == 4:
            self.add_money()
          elif options == 0:
            self.on_app = False
            return 0
        except ValueError:
          print("Please type in an integer ranging from 0-4")
      else:
        print("\nPlease select either \"Trade\" or \"Mine\" or \"View Balances\"")


  def main(self):
    self.intro()
    while self.on_app:
      print(colorama.Fore.GREEN + "---------------------Main Menu---------------------\n"+ colorama.Fore.WHITE + "Please select from the following options:")
      self.choose_options()
    print("\n\n\n-------------Thank you for using CM_TRADING! Have a great day.-------------")
      