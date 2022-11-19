import arweave
from arweave.arweave_lib import Transaction


wallet_file_path = "/some/folder/on/your/system"
wallet = arweave.Wallet(wallet_file_path)


balance =  wallet.balance
print('Balance before uploading='+balance)

with open('myfile.pdf', 'r') as mypdf:
    pdf_string_data = mypdf.read()

    transaction = Transaction(wallet, data=pdf_string_data)
    transaction.sign()
    transaction.send()

last_transaction = wallet.get_last_transaction_id()
balance =  wallet.balance
print('Balance after uploading='+balance)
