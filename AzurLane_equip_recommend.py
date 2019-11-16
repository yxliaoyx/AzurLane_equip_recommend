from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import json


def equip_name():
    html_read = urllib.request.urlopen('http://wiki.joyme.com/blhx/%E8%A3%85%E5%A4%87').read()
    html_parser = BeautifulSoup(html_read, features='html.parser')

    equip_list = []
    for table_ShowEquipNavPannel in html_parser.find_all('table', {'class': 'table-ShowEquipNavPannel'}):
        for a in table_ShowEquipNavPannel.find_all('a'):
            equip_list.append(a.get('title'))

    return equip_list


def KAN_SEN_name():
    html_read = urllib.request.urlopen('http://wiki.joyme.com/blhx/%E8%88%B0%E5%A8%98').read()
    html_parser = BeautifulSoup(html_read, features='html.parser')

    name_list = []
    Flour_list = html_parser.find_all('div', {'class': 'Flour'})
    for Flour in Flour_list:
        name_list.append(Flour.find('a').get('title'))

    return name_list


def equip_recommend(KAN_SEN, retries=3):
    url = 'http://wiki.joyme.com/blhx/{}'.format(urllib.parse.quote(KAN_SEN))

    try:
        html_read = urllib.request.urlopen(url).read()
    except Exception as e:
        print(e)
        if retries > 0:
            print('retry')
            return equip_recommend(KAN_SEN, retries - 1)
        else:
            return

    html_parser = BeautifulSoup(html_read, features='html.parser')

    equip_list = []
    REt_list = html_parser.find_all('span', {'class': 'REt'})
    for REt in REt_list:
        equip_list.append(REt.find('a').get('title'))

    return equip_list


if __name__ == '__main__':
    equip_name_list = equip_name()
    with open('equip_name_list.txt', 'w', encoding='utf-8') as f:
        f.writelines([line + '\n' for line in equip_name_list])

    KAN_SEN_name_list = KAN_SEN_name()
    with open('KAN_SEN_name_list.txt', 'w', encoding='utf-8') as f:
        f.writelines([line + '\n' for line in KAN_SEN_name_list])

    equip_dict = dict.fromkeys(equip_name_list)
    for KAN_SEN in KAN_SEN_name_list:
        print(KAN_SEN)
        for equip in equip_recommend(KAN_SEN):
            try:
                equip_dict[equip[:-2]].add(KAN_SEN)
            except AttributeError:
                equip_dict[equip[:-2]] = {KAN_SEN}
            except KeyError:
                print('KeyError: {}'.format(equip))

    with open('equip_dict.txt', 'w', encoding='utf-8') as f:
        for k, v in equip_dict.items():
            print('{}\t{}'.format(k, v), file=f)
            try:
                equip_dict[k] = list(v)
            except TypeError:
                equip_dict[k] = []

    with open('equip_dict.json', 'w', encoding='utf-8') as f:
        json.dump(equip_dict, f, indent=2, ensure_ascii=False)
