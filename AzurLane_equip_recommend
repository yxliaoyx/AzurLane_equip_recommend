from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


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
    KAN_SEN_name_list = KAN_SEN_name()
    with open('KAN_SEN_name_list.txt', 'w', encoding='utf-8') as f:
        f.writelines([line + '\n' for line in KAN_SEN_name_list])

    equip_dict = {}
    for name in KAN_SEN_name_list:
        print(name)
        for equip in equip_recommend(name):
            try:
                equip_dict[equip].add(name)
            except KeyError:
                equip_dict[equip] = {name}

    with open('equip_dict.txt', 'w', encoding='utf-8') as f:
        for k, v in equip_dict.items():
            print('{}\t{}'.format(k, v), file=f)
