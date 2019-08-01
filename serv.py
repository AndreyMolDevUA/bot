import telebot
import requests
import os.path
import os
import datetime
import sqlite3
from googletrans import Translator
#from cryptography.fernet import Fernet
#токен телеграмм
TOKEN = '673246695:AAG4S3999R_tgvWYXfpbR-7oCAjjVlA-dZo'

city_name='Одесса'
temp_sity='698740'
def listener(messages):
    try:
        """
        When new messages arrive TeleBot will call this function.
        """
        
        #path='C:/Users/Andrey/Desktop/Bot/ChatID/'
        global cr

        global city_name
        global temp_sity
        for m in messages:
            chatid = m.chat.id
            if m.content_type == 'text':
                    #print(s_city)
                #Обработчик команды старт
                if m.text == '/start':
                    tb.send_message(chatid, 'Вы подключили бота для получения информации напишите /help')
                #Обработчик каомнды хелп 
                elif m.text == '/help':
                    tb.send_message(chatid,'Для получения информации о погоде надо написать город можно воспользоваться функцией /last для вывода погоды в последнем введеном городпри. Для получения курса валют напишите /val. Новости спорта - /f1news, новости спорта - /sportnews, новоти IT тематики - /tehnonews. Для получения номера такси и отеля напишите областной центр. При возникновении проблемы написать на почту mitep999@gmail.com. Ясной погоды и теплых температур.')
                elif m.text == '/val':
                    val = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=usd&json")
                    data = val.json()
                    dol = '_Доллар США_' + '\n*' + data[0]['cc'] + "*: " + str("%.2f" % data[0]['rate'])
                    val = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&json")
                    data = val.json()
                    eur = '_Евро_' + '\n*' + data[0]['cc'] + "*: " + str("%.2f" % data[0]['rate'])
                    val = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=RUB&json")
                    data = val.json()
                    rub = '_Рубль_' + '\n*' + data[0]['cc'] + "*: " + str("%.2f" % data[0]['rate'])
                    tb.send_message(chatid,dol+"\n"+eur+"\n"+rub,parse_mode='Markdown')
                    #tb.send_message(chatid, t, parse_mode='Markdown')
                elif m.text == '/last':
                    #Читаем город к данному чат ид
                    try:
                        f = open("ChatID/"+str(chatid)+'.txt')
                        city_id = f.read()
                        #print (a)
                        f.close
                    except Exception as e:
                        tb.send_message(chatid, "Вы не вводили город")
                        print("Exception (weather):", e)
                    pass
                    appid = "949efb3c52636e70f50f4d7d399222ba"
                    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                    params={'q': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                    data = res.json()
                    #Переводим градусы в сторону света
                    try:
                        t = data['wind']['deg']
                        if (t > 330) or (t <= 30):
                            w = 'С(' + str(t) + "\xB0) "
                        elif (t > 30) and (t <= 60):
                            w = 'СВ(' + str(t) + "\xB0) "
                        elif (t > 60) and (t <= 120):
                            w = 'В(' + str(t) + "\xB0) "
                        elif (t > 120) and (t <= 150):
                            w = 'ЮВ(' + str(t) + "\xB0) "
                        elif (t > 150) and (t <= 210):
                            w = 'Ю(' + str(t) + "\xB0) "
                        elif (t > 210) and (t <= 240):
                            w = 'ЮЗ(' + str(t) + "\xB0) "
                        elif (t > 240) and (t <= 300):
                            w = 'З(' + str(t) + "\xB0) "
                        elif (t > 300) and (t <= 330):
                            w = 'СЗ(' + str(t) + "\xB0) "
                    except Exception as e:
                        w = 'не известно'
                    from time import gmtime, strftime
                    H=int((strftime("%H", gmtime())))+3
                    M=(strftime("%M", gmtime()))
                    #Делаем строку текста с указанием времени
                    if (H < 12):
                        con = "_" + data['name'] + "_" + "\n*Сейчас:* " + str(H) + ":" + M + " утра. \n*На улице:* " + str(data['weather'][0]['description']) + " " + str(data['main']['temp']) + "\xB0 \n*Влажность:* " + str(data['main']['humidity']) + "%\n*Ветер:* " + w + str(data['wind']['speed']) + " м/с \n/last"
                    elif (H < 20):
                        con = "_" + data['name'] + "_" + "\n*Сейчас:* " + str(H) + ":" + M + " утра. \n*На улице:* " + str(data['weather'][0]['description']) + " " + str(data['main']['temp']) + "\xB0 \n*Влажность:* " + str(data['main']['humidity']) + "%\n*Ветер:* " + w + str(data['wind']['speed']) + " м/с \n/last"
                    else:
                        con = "_" + data['name'] + "_" + "\n*Сейчас:* " + str(H) + ":" + M + " утра. \n*На улице:* " + str(data['weather'][0]['description']) + " " + str(data['main']['temp']) + "\xB0 \n*Влажность:* " + str(data['main']['humidity']) + "%\n*Ветер:* " + w + str(data['wind']['speed']) + " м/с \n/last"
                    tb.send_message(chatid, con, parse_mode='Markdown')
                    print (chatid)
                    print (city_id)
                    print ('==============================================================================')
                    #print ("city:",m.text)
                    #print("temp:", data['main']['temp'])    
                else:

                    city_name = m.text
                    city_id = 0
                    # token open whether
                    # s_city = m.text
                    appid = "949efb3c52636e70f50f4d7d399222ba"
                    try:
                        rus_text = m.text
                        eng_text = Translator().translate(text=rus_text, dest='en').text
                        # Ïåðåâîä÷èê äîñòàòî÷íî ãëóï
                        s_city = eng_text
                        conn = sqlite3.connect("DB")
                        cur = conn.cursor()
                        cur.execute("SELECT CG FROM City WHERE CB = '"+s_city+"'")
                        rows = cur.fetchone()
                        conn.commit()
                        city = rows
                        print (city)
                        if rows ==None:
                            s_city = s_city + ",ua"
                        else:
                            s_city = rows[0]
                        #if (s_city == 'Ishmael'):
                        #    s_city = 'Izmail'
                        #elif (s_city == 'Izmail'):
                        #    s_city = 'Izmail'
                        #elif (s_city == 'Lions'):
                        #    s_city = 'Lviv'
                        #elif (s_city == 'Dawn'):
                        #    s_city = 'Zarya'
                        #elif (s_city == 'Chabot'):
                        #    s_city = 'Shabo'
                        #elif (s_city == 'Black'):
                        #    s_city = 'Illichivsk'
                        #elif (s_city == 'Kharkov'):
                        #    s_city = 'Kharkiv'
                        #elif (s_city == 'Khmelnitsky'):
                        #    s_city = 'Khmelnytskyy'

                        # Ïîëó÷àåì ñèòè àéäè
                        file = os.path.isfile("ChatID/" + str(chatid) + '.txt')
                        if (file != True):
                            f = open('chatid.txt', 'a')
                            f.write(str(chatid) + '\n')
                            f.close
                        # print(os.path.isfile('C:/Users/Àíäðåé/Desktop/Áîò/ChatID/'+str(chatid)+'.txt'))
                        f = open("ChatID/" + str(chatid) + '.txt', 'w')
                        f.write(str(s_city))
                        # f.write(str(m.text))
                        f.close()
                        # Ïîëó÷àåì ïîãîäó ïî óêàçàííîìó ñèòè àéäè
                        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                           params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                        data = res.json()
                        # print (data)
                        try:
                            t = data['wind']['deg']
                            if (t > 330) or (t <= 30):
                                w = 'С('+str(t)+"\xB0) "
                            elif (t > 30) and (t <= 60):
                                w = 'СВ('+str(t)+"\xB0) "
                            elif (t > 60) and (t <= 120):
                                w = 'В('+str(t)+"\xB0) "
                            elif (t > 120) and (t <= 150):
                                w = 'ЮВ('+str(t)+"\xB0) "
                            elif (t > 150) and (t <= 210):
                                w = 'Ю('+str(t)+"\xB0) "
                            elif (t > 210) and (t <= 240):
                                w = 'ЮЗ('+str(t)+"\xB0) "
                            elif (t > 240) and (t <= 300):
                                w = 'З('+str(t)+"\xB0) "
                            elif (t > 300) and (t <= 330):
                                w = 'СЗ('+str(t)+"\xB0) "
                        except Exception as e:
                            w='не известно'
                        from time import gmtime, strftime
                        H = int((strftime("%H", gmtime()))) + 3
                        M = (strftime("%M", gmtime()))
                        if (H < 12):
                            con = "_" + city_name + "_" + "\n*Сейчас:* " + str(H) + ":" + M + " утра. \n*На улице:* " + str(data['weather'][0]['description']) + " " + str(data['main']['temp']) + "\xB0 \n*Влажность:* " + str(data['main']['humidity']) + "%\n*Ветер:* " + w  + str(data['wind']['speed']) + " м/с \n/last"
                        elif (H < 20):
                            con = "_" + city_name + "_" + "\n*Сейчас:* " + str(H) + ":" + M + " дня. \n*На улице:* " + str(data['weather'][0]['description']) + " " + str(data['main']['temp']) + "\xB0 \n*Влажность:* " + str(data['main']['humidity']) + "%\n*Ветер:* " + w +  str(data['wind']['speed']) + " м/с \n/last"
                        else:
                            con = "_" + city_name + "_" + "\n*Сейчас:* " + str(H) + ":" + M + " вечера. \n*На улице:* " + str(data['weather'][0]['description']) + " " + str(data['main']['temp']) + "\xB0 \n*Влажность:* " + str(data['main']['humidity']) + "%\n*Ветер:* " + w + str(data['wind']['speed']) + " м/с \n/last"
                        # con="Ñåé÷àñ:"+str(data['weather'][0]['description'])+" "+str(data['main']['temp'])+"\xB0 Âåòåð: "+str(data['wind']['speed'])+" ì/ñ"
                        conn = sqlite3.connect("DB")
                        cur = conn.cursor()
                        cur.execute("SELECT Taxi FROM taxi WHERE City = '" + city_name + "'")
                        rows = cur.fetchone()
                        cur.execute("SELECT TaxiNom FROM taxi WHERE City = '" + city_name + "'")
                        nom = cur.fetchone()
                        cur.execute("SELECT Hotel FROM hotel WHERE City = '" + city_name + "'")
                        hot=cur.fetchone()
                        cur.execute("SELECT HotelNom FROM hotel WHERE City = '" + city_name + "'")
                        hotnom=cur.fetchone()
                        print (hot)
                        conn.commit()
                        if hot == None:
                            tb.send_message(chatid, con, parse_mode='Markdown')
                        else:
                            tb.send_message(chatid, "*"+str(hot[0])+"*\n_"+str(hotnom[0])+"_", parse_mode='Markdown')
                            tb.send_message(chatid, "*"+str(rows[0])+"*\n_"+str(nom[0])+"_", parse_mode='Markdown')
                            tb.send_message(chatid, con, parse_mode='Markdown')
                        #print ("city:",m.text)
                        #print("temp:", data['main']['temp'])
                        print (chatid)
                        print (file)
                        print (s_city)
                        print ('==============================================================================')
                        pass
                    except Exception as e:
                        print("Exception (weather):", e)
                        tb.send_message(chatid,'Город '+s_city+' не найден')
                    pass
    except Exception as e:
                    print('Exception (weather):',e)
try:
        tb = telebot.TeleBot(TOKEN)
        tb.set_update_listener(listener) #register listener
        tb.polling()
    #Use none_stop flag let polling will not stop when get new message occur error.
        tb.polling(none_stop=True)
    # Interval setup. Sleep 3 secs between request new message.
        tb.polling(interval=3)
except Exception as e:
        print('Ошибка потеря содинения ')
        #os.chdir('C:/Users/Андрей/Desktop/Бот/rest.bat')
        #os.startfile("rest.bat")

while True: # Don't let the main Thread end.
    pass