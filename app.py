# app.py
# Author: Jerrad Flores
import colored_text
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
    self.coins = []
    self.balances = {}


  def select_coin(self):
    coin = 9999
    while coin > len(self.balances.keys()):
      coin_names = ""
      for num, name in enumerate(self.balances.keys()):
        coin_names += "{} - {}\n".format(num, name)

      coin = int(input("Please select a coin:\n{}".format(coin_names)))
      if coin > len(self.balances.keys()):
        colored_text.print_white("Please select a valid coin (one of the following):\n {}".format(coin_names))
    return self.coins[coin] #The integer index of the coin


  def view_balances(self):
    colored_text.print_white("\tDollar Balance is: {}".format(self.dollar_balance))
    coin = self.select_coin()
    colored_text.print_white("\tCurrent Balance for {} is: {} currenly valued at: {} per coin.".format(coin, self.balances[coin], self.cm_blockchain.value(coin)))

  
  def add_money(self):
    quantity = ""
    while type(quantity) != int:
      try:
        quantity = int(input("Please type in how many DOLLARS you want to add: "))
      except ValueError:
        colored_text.print_white("Must be a numerical value! Try again.")
    colored_text.print_white("Currently adding {} dollars to your dollar balance...".format(quantity))
    time.sleep(quantity) # simulates the time to generate or "earn" the dollars.
    self.dollar_balance += quantity
    colored_text.print_white("Successfully added {}dollars to your balance. Current DOLLARS balance: {}".format(quantity, self.dollar_balance))


  def sell_or_buy(self):
    sb = -1
    while sb not in [0,1]:
      sb = int(input("0 - Buy\n1 - Sell\n"))
      if sb not in [0,1]:
        colored_text.print_white("\nPlease select \"Buy\" or \"Sell\"")
    if sb == 0:
      return "Buy"
    return "Sell"


  def buy(self, coin):
    colored_text.print_white("\nCurrent buying power (dollars) is {}".format(self.dollar_balance))
    if self.dollar_balance == 0:
      colored_text.print_white("You currently have no DOLLARS to use for buying coins.")
      return 0
    dollar_quantity = 1237123091203971203917209371093
    while (type(dollar_quantity) != int) or (dollar_quantity > self.dollar_balance):
      try:
        dollar_quantity = int(input("Please type the quantity of DOLLARS that you want to trade: "))
      except ValueError:
        colored_text.print_white("Must be a numerical value! Try again.")
      if dollar_quantity > self.dollar_balance:
        colored_text.print_white("You don't have that much dollars in your balance.")
        return 0
    coin_quantity = dollar_quantity/self.cm_blockchain.value(coin)
    
    colored_text.print_white("Currently buying {} {} valued at: {}...".format(coin_quantity, coin, self.cm_blockchain.value(coin)))
    self.cm_blockchain.buy("CM_TRADING", self.name, coin_quantity, dollar_quantity, coin)
    self.balances[coin] += coin_quantity
    self.dollar_balance -= dollar_quantity


  def sell(self, coin):
    colored_text.print_white("Current balance for {} is {}".format(coin, self.balances[coin]))
    if self.balances[coin] == 0:
      colored_text.print_white("You currently have no {} to sell.".format(coin))
      return 0
    coin_quantity = ""
    while (type(coin_quantity) != int) or (coin_quantity > self.balances[coin]):
      try:
        coin_quantity = int(input("\nPlease type the quantity of COIN that you want to sell (balance is currently {}): ".format(self.balances[coin])))
      except ValueError:
        colored_text.print_white("Must be a numerical Value! Try again.")
      if coin_quantity > self.balances[coin]:
        colored_text.print_white("You don't have that much coin to sell.")
    dollar_quantity = coin_quantity * self.cm_blockchain.value(coin)
    colored_text.print_white("Currently selling {} {} value at: {}...".format(coin_quantity, coin, self.cm_blockchain.value(coin)))
    self.cm_blockchain.sell("CM_TRADING", self.name, dollar_quantity, coin_quantity, coin)
    self.balances[coin] -= coin_quantity
    self.dollar_balance += dollar_quantity


  def trade(self):
    coin = self.select_coin()
    sb = self.sell_or_buy()
    action = -1
    if sb == "Buy":
      action = self.buy(coin)
    elif sb == "Sell":
      action = self.sell(coin)
    if action != 0:
      colored_text.print_white("SUCESSFULLY EXECUTED TRADE.")


  def mine(self):
    coin = self.select_coin()
    quantity = ""
    while type(quantity) != int:
      try:
        quantity = int(input("Please type the quantity of desired coin (more coins = more time taken to mine) valued currently at {}: ".format(self.cm_blockchain.value(coin))))
      except ValueError:
        colored_text.print_white("Must be a numerical value! Try again.")
    colored_text.print_white("Currently Mining {} {}...".format(quantity, coin))
    block_mined = self.cm_blockchain.mine(quantity, coin, self.name)
    if block_mined != None:
      colored_text.print_white("Successfully mined {} {}".format(quantity, coin))
      self.balances[coin] += quantity
    else:
      colored_text.print_white("Error mining")


  def initialize_trading_coins(self):
    # Mine for 0 coin for all the coins that are going to be in the CM_TRADING system (that way we have them displayed in the app)

    # Why are the bought and sold values being initialized to 1?
    # In order to get the value of a coin, we need to be able to divide by a divisible greater than 0 (if not, we get an error). So, anything greater than 1 for a given coin indicates that the base value will be changed for that particular coin.
    self.coins = ["Butter Coin", "Official Coin", "Simple Coin"]

    self.cm_blockchain.in_circulation = {
      "Butter Coin" : 0,
      "Official Coin" : 0,
      "Simple Coin" : 0
    }

    self.balances["Butter Coin"] = 0
    self.cm_blockchain.bought["Butter Coin"] = 1
    self.cm_blockchain.sold["Butter Coin"] = 1
    self.balances["Official Coin"] = 0
    self.cm_blockchain.bought["Official Coin"] = 1
    self.cm_blockchain.sold["Official Coin"] = 1
    self.balances["Simple Coin"] = 0
    self.cm_blockchain.bought["Simple Coin"] = 1
    self.cm_blockchain.sold["Simple Coin"] = 1


  def intro(self):
    '''
    Welcomes user to app, and allows them to enter their name.
    '''
    colored_text.print_white("Welcome to CM_TRADING!")
    self.name = input("Please enter your name: ")
    colored_text.print_white("Welcome, {}! \n\n".format(self.name))
    self.initialize_trading_coins()


  def choose_options(self):
    options = ""
    while options not in [0,1,2,3,4]:
      while type(options) != int:
        try:
          colored_text.print_white("0 - Quit\n1 - Trade\n2 - Mine\n3 - View Balances\n4 - Add Money")
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
          colored_text.print_white("Please type in an integer ranging from 0-4")
      else:
        colored_text.print_white("\nPlease select either \"Trade\" or \"Mine\" or \"View Balances\"")


  def main(self):
    self.intro()
    while self.on_app:
      colored_text.print_green("---------------------Main Menu---------------------")
      colored_text.print_white("Please select from the following options:")
      self.choose_options()
    colored_text.print_white("\n\n\n-------------Thank you for using CM_TRADING! Have a great day.-------------")
      