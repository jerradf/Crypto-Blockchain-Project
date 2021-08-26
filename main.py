# main.py
# Author: Jerrad Flores

import block
import blockchain


bc = blockchain.Blockchain('\033[95m'+"John Doe's Blockchain")

print('\033[95m'+"Currently mining JohnCoin....")
bc.mine("JohnCoin", "Yu Sun")


print('\033[92m'+"Successfully mined JohnCoin!")
print('\033[95m'+"")
print(bc.last_block)