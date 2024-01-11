from utils.utils import write_list_to_file
from mnemonic import Mnemonic
from utils.wallet import WalletHelp
from better_web3 import Wallet
from aptos_sdk.bcs import Serializer
from aptos_sdk.account import Account
from utils.sui_utils import SuiPublicKeyUtils
import base58
from solders.keypair import Keypair


def evm_generate(wallets_amount: int) -> None:
    data = []

    for i in range(wallets_amount):
        seed_phrase = Mnemonic('english').generate()
        wallet = Wallet.from_mnemonic(seed_phrase)
        data.append(f'{wallet.address}:{wallet.private_key}:{seed_phrase}')

    write_list_to_file(data, 'result/evm.txt')


def sui_generate(wallets_amount: int) -> None:
    data = []

    for i in range(wallets_amount):
        seed_phrase = Mnemonic('english').generate()
        pt_seed = SuiPublicKeyUtils(seed_phrase)
        keys = Account.load_key(pt_seed.private_key.hex())
        public_key = keys.public_key()

        serializer = Serializer()
        serializer.u8(0x00)
        serializer.fixed_bytes(public_key.key.encode())
        serialized_data = serializer.output()

        hashed = blake2b(serialized_data, digest_size=32)
        address = hashed.digest()
        private_key = pt_seed.mnemonic_to_private_key(mnemonic=seed_phrase).hex()
        data.append(f'{"0x" + address.hex()}:{private_key}:{seed_phrase}')

    write_list_to_file(data, 'result/sui.txt')


def aptos_generate(wallets_amount: int) -> None:
    data = []

    for i in range(wallets_amount):
        seed_phrase = Mnemonic('english').generate()
        wallet = WalletHelp(seed_phrase)
        keys = wallet.generate_aptos_keys()
        data.append(keys)

    write_list_to_file(data, 'result/aptos.txt')


def solana_generate(wallets_amount: int) -> None:
    data = []

    for x in range(wallets_amount):
        account = Keypair()
        private_key = base58.b58encode(account.secret() + base58.b58decode(str(account.pubkey()))).decode('utf-8')
        data.append(f'{account.pubkey()}:{private_key}')

    write_list_to_file(data, 'result/solana.txt')


if __name__ == '__main__':
    user_action: int = int(input('\n1. EVM'
                                 '\n2. SUI'
                                 '\n3. APTOS'
                                 '\n4. SOLANA'
                                 '\nВыберите ваше действие: '))
    wallets_amount: int = int(input('Количество кошельков: '))
    print('ФОРМАТ ВЫВОДА:'
          '\naddress:private_key\n')

    if user_action == 1:
        evm_generate(wallets_amount)

    elif user_action == 2:
        sui_generate(wallets_amount)

    elif user_action == 3:
        aptos_generate(wallets_amount)

    elif user_action == 4:
        solana_generate(wallets_amount)
