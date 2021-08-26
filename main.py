# main.py
# Author: Jerrad Flores

import block
import blockchain


bc = blockchain.Blockchain("John Doe's Blockchain")

print('\033[95m'+"Currently mining JohnCoin....")
bc.mine("JohnCoin", "Yu Sun")


print('\033[92m'+"Successfully mined JohnCoin!")
print('\033[95m'+"")
print(bc.last_block)

# I can also mine for other coins as well!
#.....................
print()
print()
print()

print('\033[95m'+"Currently mining JaneCoin....")
bc.mine("JaneCoin", "Yu Sun")


print('\033[92m'+"Successfully mined JaneCoin!")
print('\033[95m'+"")
print(bc.last_block)