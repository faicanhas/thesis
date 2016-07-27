import pprint
import telepot
import ast
from time import sleep



def handle(msg):
    # pprint.pprint(msg)
    # Do your stuff here ...
    content_type, chat_type, chat_id = telepot.glance(msg)
    print (content_type, chat_type, chat_id)

    command = msg['text']

    if chat_id == 148554570:
        chat_id_admin = chat_id

    if chat_id_admin:
        bot.sendMessage(chat_id_admin, "Halo Admin!")

    if command == '/mulai':
        # Mengirim pesan
        bot.sendMessage('@aferentalmobil1',
                        "Halo pengguna mobil 1! Selamat berkendara menggunakan mobil rental kami!")

        bot.sendMessage('@aferentalmobil1',
                        "Mengemudilah dengan baik ya. Patuhi rambu-rambu lalu lintas demi keselamatan bersama.")

        bot.sendMessage('@aferentalmobil1',
                        "Secara otomatis saya akan mengirimkan pemberitahuan untuk keperluan supervisi mengemudi Anda.\n"
                        "Jika Anda melanggar batas-batas aturan tertentu yang telah ditetapkan pihak rental, "
                        "maka akan muncul pemberitahuan dan supervisi.")

        bot.sendMessage('@aferentalmobil1',
                        "Ikuti supvervisi yang diberikan demi terciptanya perilaku pengemudi yang baik.\n"
                        "Karena cara mengemudi Anda juga berperan penting dalam keselamatan selama berkendara.")

        bot.sendMessage('@aferentalmobil1',
                        "Selamat berkendara dan selamat selalu bersama AFE Rental Car : Your One Stop Solution Rental Car Service!")

        global status_mulai
        status_mulai = True


TOKEN = '213285961:AAHbSxe5vs7JugX8Euq2SXt3dWVsUNb7CMo'

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

status_mulai = False

print ('Listening ...')


# Keep the program running.
while 1:
    print "status_mulai = ", status_mulai
    if status_mulai:
        file = open('statusdata.txt', 'r')
        bacadata = file.read()                  # masih dalam bentuk string
        data = ast.literal_eval(bacadata)       # sudah dalam bentuk dict

        # print type(data)
        rpm = data["rpm"]
        kecepatan = data["kecepatan"]
        # throttlepos = data["throttlepos"]
        engineload = data["engineload"]
        coolanttemp = data["coolanttemp"]

        print "kecepatan = ", kecepatan, "km/h"
        print "putaran mesin = ", rpm, "rpm"
        # print "throttlepos = ", throttlepos, "%"
        print "engineload = ", engineload, "%"
        print "coolanttemp = ", coolanttemp, "C"
        print "\n"

        # nilai default alert selalu di-set ke False
        alert_kecepatan = False
        alert_rpm = False
        alert_engineload = False
        alert_coolanttemp1 = False
        alert_coolanttemp2 = False

        # blok kondisi
        if kecepatan > 80:
            print "Kecepatan Anda melebihi 60 km/jam. Segera kurangi kecepatan!"
            alert_kecepatan = True
        if rpm > 2500:
            print "Putaran mesin melebihi 2500 rpm. Segera turunkan kecepatan atau ganti gigi ke gigi yang lebih tinggi!"
            alert_rpm = True
        if  engineload > 50:
            print "Jangan tancap gas mendadak. Injaklah pedal gas secara perlahan!"
            alert_engineload = True
        if 80 <= coolanttemp <= 90:
            print "Suhu mobil meningkat pada suhu optimal (80-90", "C" + ")", "Jaga agar suhu mesin tidak " \
                                                                                    "melebihi 90", "C" + "!"
            alert_coolanttemp1 = True
        if coolanttemp > 90:
            print "Mesin mulai mengalami OVERHEAT. Segera berhenti, matikan mesin, lalu cek kondisi pendingin mesin!"
            alert_coolanttemp2 = True

        # logging
        if alert_kecepatan:
            bot.sendMessage('@aferentalmobil1',
                            "Kecepatan Anda melebihi 80 km/jam.")
            bot.sendMessage('@aferentalmobil1,'
                            'Segera kurangi kecepatan!')
        if alert_rpm:
            bot.sendMessage('@aferentalmobil1',
                            "Putaran mesin melebihi 2500 rpm.")
            bot.sendMessage('@aferentalmobil1',
                            "Segera turunkan kecepatan atau ganti gigi ke gigi yang lebih tinggi!")
        if alert_engineload:
            bot.sendMessage('@aferentalmobil1',
                            "Jangan injak pedal gas secara mendadak! ")
            bot.sendMessage('@aferentalmobil1',
                            "Injaklah pedal gas secara perlahan-lahan!")
        if alert_coolanttemp1:
            bot.sendMessage('@aferentalmobil1',
                            "Suhu pendingin mobil mulai meningkat di atas 80 derajat Celcius.")
            bot.sendMessage('@aferentalmobil1',
                            "Jaga agar suhu mesin tidak melebihi 90 derajat Celcius!")
        if alert_coolanttemp2:
            bot.sendMessage('@aferentalmobil1',
                            "Mesin mulai mengalami OVERHEAT. ")
            bot.sendMessage('@aferentalmobil1',
                            "Segera berhenti, matikan mesin, lalu cek kondisi pendingin mesin!")



    sleep(15)

