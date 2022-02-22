import requests
from faker import Faker

txt = '''
简体中文:zh_CN
繁体中文:zh_TW
美国英文:en_US
英国英文:en_GB
'''

url = 'https://mk.dustess.com/qw-scrm-svc/action/customer-manage/company/add'
headers = {'Authorization': 'qw.74e5deb4-90cc-11ec-a7c4-b22dc7044521'}
total = 0
success = 0
fail = 0
while True:
    for line in txt.split('\n'):
        if line:
            language = line.split(':')[-1]
            faker = Faker(language)
            data = {
                "name": faker.company(),
                "fullName": faker.company(),
                "tel": "pZXXvIqFD/WuJqKe6rcXTQ==",
                "industry": "",
                "web": "",
                "prov_city": "",
                "address": faker.address(),
                "peoples": "",
                "level": "",
                "source": "",
                "businessID": "",
                "map_user_opt_id": "",
                "province": 0,
                "city": 0,
                "district": 0,
                "tags": [],
                "custom_fields": [
                    {
                        "id": "field0",
                        "type": "date",
                        "string_value": ""
                    },
                    {
                        "id": "field8",
                        "type": "files",
                        "files_value": []
                    }
                ]
            }

            print(data)
            response = requests.post(url=url, headers=headers, json=data).json()
            print(response)
            total += 1
            if response.get('success') == True:
                success += 1
            else:
                fail += 1
    print(f'total: {total}, success: {success}, fail: {fail}')
