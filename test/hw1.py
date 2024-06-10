import re

with open('./log.txt', 'r') as file:
    logs = file.readlines()

# 初始化字典來存儲VIP和普通會員的信息
vip_members = {}
members = {}

# 初始化字典來存儲每種商品的總銷售額
total_sales = {}

# 解析每一行記錄
for log in logs:
    match = re.match(r'(\[VIP\] )?(\w+) buys (\w+) for \$(\d+)', log.strip())
    if match:
        vip, name, item, amount = match.groups()
        amount = int(amount)
        
        # 更新商品總銷售額
        if item not in total_sales:
            total_sales[item] = 0
        total_sales[item] += amount
        
        # 更新會員購物信息
        if vip:
            if name not in vip_members:
                vip_members[name] = {}
            if item not in vip_members[name]:
                vip_members[name][item] = 0
            vip_members[name][item] += amount
        else:
            if name not in members:
                members[name] = {}
            if item not in members[name]:
                members[name][item] = 0
            members[name][item] += amount

# 輸出分析結果到Analysis_result.txt
with open('./Analysis_result.txt', 'w') as file:
    file.write('[VIP]\n')
    for name, purchases in vip_members.items():
        file.write(f'{name} buys ')
        file.write(' '.join([f'{item}: {amount}' for item, amount in purchases.items()]))
        file.write('\n')
    
    file.write('\n[Member]\n')
    for name, purchases in members.items():
        file.write(f'{name} buys ')
        file.write(' '.join([f'{item}: {amount}' for item, amount in purchases.items()]))
        file.write('\n')
    
    file.write('\n')
    for item, amount in total_sales.items():
        file.write(f'Total {item} sales: {amount}\n')
