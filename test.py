from datetime import datetime
data = [(1, 'Hoi', 'wqd', 'wd', '2022-10-15', 'qwsdwq'), (2, 'Dit is nog een post!', '<p>Ewa!</p>', 'Kelvin de Reus', '2022-10-13', 'Hardware'), (6, 'Nice gpu men', '<p>rtx5000</p>', 'Kelvin', '2023-01-06', None)]

lst_items = []
for item in data:
    lst_items.append(list(item))

print(lst_items)


for item in lst_items:
    item[0] = 1

print(lst_items)