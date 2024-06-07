import re

def parse_and_update_sales(lines, items, vip_sales, member_sales, total_sales):
  pattern = re.compile(r'(\[VIP\])?\s*([\w]+)\s+buys\s+(\w+)\s+for\s+\$(\d+)')

  for line in lines:
    match = pattern.match(line.strip())
    if match:
      is_vip = match.group(1) is not None
      name = match.group(2)
      item = match.group(3)
      price = int(match.group(4))

      if item not in items:
        items.append(item)
        total_sales[item] = 0

        for user_sales in vip_sales.values():
           user_sales[item] = 0
        for user_sales in member_sales.values():
           user_sales[item] = 0

      if is_vip:
        if name not in vip_sales:
          vip_sales[name] = {item_name: 0 for item_name in items}
        vip_sales[name][item] += price
      else:
        if name not in member_sales:
          member_sales[name] = {item_name: 0 for item_name in items}
        member_sales[name][item] += price

      total_sales[item] += price

def format_sales(sales_dict):
  result = []
  for name, items in sales_dict.items():
    sales = ", ".join([f"{item}: {amount}" for item, amount in items.items() if amount > 0])
    result.append(f"{name} buys {sales}")
  return result

def print_sales(vip_result, member_result, total_sales):
  print("[VIP]")
  for line in vip_result:
    print(line)
  print("\n[Member]")
  for line in member_result:
    print(line)
  print("\nTotal sales")
  for item, total in total_sales.items():
    print(f"{item}: {total}")

def main():
  with open('./log.txt', 'r') as file:
    lines = file.readlines()
  items, vip_sales, member_sales, total_sales = [], {}, {}, {}
  parse_and_update_sales(lines, items, vip_sales, member_sales, total_sales)
  vip_result = format_sales(vip_sales)
  member_result = format_sales(member_sales)
  print_sales(vip_result, member_result, total_sales)

main()