import re

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_data(data):
    pattern = re.compile(r'\[VIP\] (.*?) buys (.*?) for \$(\d+)|(\S+?) buys (.*?) for \$(\d+)')
    return pattern.findall(data)

def process_purchases(matches):
    vip_purchases = {}
    member_purchases = {}

    for match in matches:
        if match[0]: 
            name, item, price = match[0], match[1], int(match[2])
            if name not in vip_purchases:
                vip_purchases[name] = {}
            if item not in vip_purchases[name]:
                vip_purchases[name][item] = 0
            vip_purchases[name][item] += price
        else:  
            name, item, price = match[3], match[4], int(match[5])
            if name not in member_purchases:
                member_purchases[name] = {}
            if item not in member_purchases[name]:
                member_purchases[name][item] = 0
            member_purchases[name][item] += price

    return vip_purchases, member_purchases

def calculate_total_sales(vip_purchases, member_purchases):
    total_sales = {'Computer': 0, 'Notebook': 0, 'Paper': 0, 'Book': 0}

    for purchases in [vip_purchases, member_purchases]:
        for items in purchases.values():
            for item, price in items.items():
                if item in total_sales:
                    total_sales[item] += price

    return total_sales

def generate_report(group_name, purchases):
    report = f'[{group_name}]\n'
    for name, items in purchases.items():
        item_str = ', '.join([f'{item}: {price}' for item, price in items.items()])
        report += f'{name} buys {item_str}\n'
    return report

def generate_total_report(total_sales):
    return (
        f'Total Computer sales: {total_sales["Computer"]}\n'
        f'Total NoteBook sales: {total_sales["Notebook"]}\n'
        f'Total Paper sales: {total_sales["Paper"]}\n'
        f'Total Book sales: {total_sales["Book"]}\n'
    )

def main():
    data = read_file('./log.txt')
    matches = parse_data(data)
    vip_purchases, member_purchases = process_purchases(matches)
    total_sales = calculate_total_sales(vip_purchases, member_purchases)
    
    vip_report = generate_report('VIP', vip_purchases)
    member_report = generate_report('Member', member_purchases)
    total_report = generate_total_report(total_sales)

    final_report = f'=== Analysis_result.txt ===\n\n{vip_report}\n{member_report}\n{total_report}'
    print(final_report)

if __name__ == "__main__":
    main()
