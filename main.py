import requests
import json
import random
import time
from configparser import ConfigParser
from art import tprint
import plyer

tprint('AutoPost')
config = ConfigParser()
api_version = '9'

def check_answer(name):
    if name == 'да' or 'lf':
        return True
    else:
        return False

def new_config():
    save = input('Сохранить конфигурацию? (да/нет): ')
    save = check_answer(save)
        
    global discord_token
    discord_token = input('Введите Ваш Discord-token: ')
    
    global channel_ID
    channel_ID = input('Введите ID канала, в который будут отсылаться сообщения: ')
    
    global advertisements
    advertisements = input('Введите текст (можно добавить несколько вариантов, разделяя их с помощью ; ): ')

    global delete
    delete = input('Удалять сообщения? (да/нет): ')
    delete = check_answer(delete)
        
    global random_delete
    random_delete = input('Всегда удалять сообщения? (да/нет): ')
    random_delete = check_answer(random_delete)
        
    global notification
    notification = input('Уведомлять о отправке сообщения? (да/нет): ')
    notification = check_answer(notification)
        
    global MIN_delay
    MIN_delay = input('Введите минимальный промежуток между сообщениями (в минутах): ')
    
    global MAX_delay
    MAX_delay = input('Введите максимальный промежуток между сообщениями (в минутах): ')

    if save:
        config['Config']['save'] = str(save)
        config['Config']['discord_token'] = discord_token
        config['Config']['channel_ID'] = channel_ID
        config['Config']['advertisements'] = str(advertisements)
        config['Config']['delete'] = str(delete)
        config['Config']['random_delete'] = str(random_delete)
        config['Config']['MIN_delay'] = MIN_delay
        config['Config']['MAX_delay'] = MAX_delay
        config['Config']['notification'] = str(notification)
               
        with open('config.ini', 'w') as config_file:
            config.write(config_file)


config.read_file(open(r'config.ini'))
save = eval(config.get('Config', 'save'))      
if save:  
    print('Последняя конфигурация: ')
    for x in config['Config']:
        print(x + ' = ' + config['Config'][x])
        
    choice = input('Загрузить прошлую конфигурацию? (да/нет): ')
    choice = check_answer(choice)
    if choice:
        discord_token = config.get('Config', 'discord_token')
        channel_ID = config.get('Config', 'channel_ID')
        advertisements = config.get('Config', 'advertisements')
        delete = eval(config.get('Config', 'delete'))
        random_delete = eval(config.get('Config', 'random_delete'))
        notification = eval(config.get('Config', 'notification'))
        MIN_delay = config.get('Config', 'MIN_delay')
        MAX_delay = config.get('Config', 'MAX_delay')
    else:
        new_config()
else:
    new_config()

headers = {
    'authorization': discord_token
}

advertisements = advertisements.split(';')
MIN_delay = int(MIN_delay) * 60
MAX_delay = int(MAX_delay) * 60

while True:   
    content = {
        'content': random.SystemRandom().choice(advertisements)
    }
    sended_message = requests.post(f'https://discord.com/api/v{api_version}/channels/{channel_ID}/messages', headers=headers, data=content)
    sended_message = sended_message.text.encode().decode('unicode-escape')
    sended_message_json = json.loads(sended_message.replace('\\', ''))
    message_id = sended_message_json['id']
    
    if delete:
        if random_delete:
            if random.randint(0, 1) == 0:
                requests.delete(f'https://discord.com/api/v{api_version}/channels/{channel_ID}/messages/{message_id}', headers=headers)
        else:
            requests.delete(f'https://discord.com/api/v{api_version}/channels/{channel_ID}/messages/{message_id}', headers=headers)

    if notification:
        plyer.notification.notify(title='AutoPost', message='Сообщение было успешно отправлено.')
        
    random_time = random.randint(MIN_delay, MAX_delay)
    print('До следующего сообщения: ' + str(random_time) + ' сек.')
    time.sleep(random_time)