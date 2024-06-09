import re

def analysis_string(string):
    pattern = re.compile(r'(\[VIP\] )?(\w+) buys (\w+) for \$(\d+)')
    vip_purchases = {}
    member_purchases = {}
    total_sales = {}

    for vip_status, name, item, price in pattern.findall(string):
        price = int(price)
        if vip_status:
            if name not in vip_purchases:
                vip_purchases[name] = {}
            if item not in vip_purchases[name]:
                vip_purchases[name][item] = 0
            vip_purchases[name][item] += price
        else:
            if name not in member_purchases:
                member_purchases[name] = {}
            if item not in member_purchases[name]:
                member_purchases[name][item] = 0
            member_purchases[name][item] += price
        if item not in total_sales:
            total_sales[item] = 0
        total_sales[item] += price

    content = "[VIP]\n"
    for name, items in vip_purchases.items():
        items_str = ', '.join([f"{item}: {price}" for item, price in items.items()])
        content += f"{name} buys {items_str}\n"

    content += "\n[Member]\n"
    for name, items in member_purchases.items():
        items_str = ', '.join([f"{item}: {price}" for item, price in items.items()])
        content += f"{name} buys {items_str}\n"

    content += "\n"
    for item, total in total_sales.items():
        content += f"Total {item} sales: {total}\n"
    return content

def open_file(path):
    with open(path, 'r') as file:
        log_data = file.read()
    return log_data

def save_file(path, string):
    with open(path, 'w') as file:
        file.write(string)

if __name__ == '__main__':
    log_data=open_file(r'H:\PY\week15\test\log.txt')
    content=analysis_string(log_data)
    print(content)
    save_file(r'H:\PY\week15\test\Analysis_result.txt', content)