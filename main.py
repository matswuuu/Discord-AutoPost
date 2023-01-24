from discum import Client
from random import SystemRandom, randint
from json import loads
from time import sleep
from configparser import ConfigParser
from art import tprint

tprint('AutoPost      v0.0.2')
config = ConfigParser()

def check_answer(name):
    if name == 'да':
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
    advertisements = input('Введите текст (можно добавить несколько вариантов, разделяя их с помощью ;): ')
    advertisements = advertisements.split(';')
    
    global delete
    delete = input('Удалять сообщения? (да/нет): ')
    delete = check_answer(save)
        
    global random_delete
    random_delete = input('Всегда удалять сообщения? (да/нет): ')
    random_delete = check_answer(random_delete)
        
    global MIN_delay
    MIN_delay = input('Введите минимальный промежуток между сообщениями (в минутах): ')
    MIN_delay = int(MIN_delay) * 60
    
    global MAX_delay
    MAX_delay = input('Введите максимальный промежуток между сообщениями (в минутах): ')
    MAX_delay = int(MAX_delay) * 60

    if save:
        config['Config']['save'] = str(save)
        config['Config']['discord_token'] = discord_token
        config['Config']['channel_ID'] = channel_ID
        config['Config']['advertisements'] = str(advertisements)
        config['Config']['delete'] = str(delete)
        config['Config']['random_delete'] = str(random_delete)
        config['Config']['MIN_delay'] = str(MIN_delay)
        config['Config']['MAX_delay'] = str(MAX_delay)
               
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
        advertisements = advertisements.replace('\'', '')
        advertisements = advertisements.strip('][').split(', ')
        delete = eval(config.get('Config', 'delete'))
        random_delete = eval(config.get('Config', 'random_delete'))
        MIN_delay = int(config.get('Config', 'MIN_delay'))
        MAX_delay = int(config.get('Config', 'MAX_delay'))
    else:
        new_config()
else:
    new_config()

bot = Client(token=discord_token)
while True:   
    sended_message = bot.sendMessage(channelID=channel_ID, message=SystemRandom().choice(advertisements))
    sended_message = sended_message.text.encode().decode('unicode-escape')
    sended_message_json = loads(sended_message.replace('\\', ''))

    sleep(5)
    if delete:
        if not random_delete:
            if randint(0, 1) == 0:
                bot.deleteMessage(channelID=channel_ID, messageID=sended_message_json['id'])
        else:
            bot.deleteMessage(channelID=channel_ID, messageID=sended_message_json['id'])

    sleep(randint(MIN_delay, MAX_delay))