from web3 import Web3
import csv
import os

# Infura 配置
INFURA_URL = "https://mainnet.infura.io/v3/062d70b6c7d14186a37ae2aa9119cf96"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# 检查连接
if not web3.is_connected():
    print("无法连接到以太坊网络，请检查 Infura URL 或网络连接")
    exit()
else:
    print("成功连接到以太坊网络")

# 定义区块范围
START_BLOCK = 17000000  # 起始区块号
END_BLOCK = 17000002    # 结束区块号

# 定义输出的 CSV 文件路径
OUTPUT_FILE = "ethereum_transactions_infura.csv"

# 清理旧文件
if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

# 写入 CSV 文件
with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入表头
    writer.writerow(["block_number", "tx_hash", "from", "to", "value", "gas", "gas_price", "input"])

    # 遍历指定区块范围
    for block_number in range(START_BLOCK, END_BLOCK + 1):
        print(f"正在处理区块 {block_number}...")
        
        # 获取区块信息
        block = web3.eth.get_block(block_number, full_transactions=True)
        print(f"区块 {block_number} 包含交易数：{len(block.transactions)}")

        # 遍历区块中的每笔交易
        for tx in block.transactions:
            print(f"处理交易: {tx.hash.hex()}")
            writer.writerow([
                str(block_number),                  # 确保区块号是字符串
                tx.hash.hex(),                      # 交易哈希
                tx['from'],                         # 发送方
                tx['to'],                           # 接收方
                web3.from_wei(tx.value, 'ether'),   # 转账金额
                tx.gas,                             # Gas 消耗
                web3.from_wei(tx.gasPrice, 'gwei'),# Gas 价格
                tx.input                            # 交易输入数据
            ])

print(f"交易数据已保存到 {OUTPUT_FILE}")
