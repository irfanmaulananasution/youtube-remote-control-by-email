import imaplib
from selenium import webdriver
import time

class email_checker(object):
    #fungsi untuk mengambil isi email, isi masih berantakan, dalam class byte
    def receive_email(self):
        #buka email
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
#!      #login, email dan password bisa dan sebaiknya diganti jika digunakan selain oleh programmer, password mungkin berubah
        mail.login(#YOUR EMAIL HERE, YOUR PASSWORD HERE)
        #listnya adalah inbox, draft send, dll
        mail.list()
        #memilih inbox dari list tadi
        mail.select("inbox")
        #dari inbox mengambil semua email
        result, data = mail.search(None, "ALL")
        #data adalah list, ids/data[0] bukan list
        ids = data[0] 
        #membuat list id email email (kata kunci)
        id_list = ids.split() 
        #mengambil katakunci email terbaru
        latest_email_id = id_list[-1]
        #dari inbox mengambil email terbaru
        result, data = mail.fetch(latest_email_id, "(RFC822)") 
        #mengambil isi email yang dimaksud(terbaru)
        raw_email = data[0][1] 
        return raw_email

    #mengambil bagian yang dibutuhkan dari receive_email yang masih berantakan, keluaran = list link youtube dari email
    def define_email(self):
        email = str(self.receive_email())
        #sistem pendetek link youtube didalam isi email
        start = email.find("https://www.youtube.com/")
        link = email[start:]
        end = link.find("--")
        link = link[:end]
        link = link.split("\\r\\n")
        link = link[0]  #link yang diambil hanya link youtube pertama
        #mendeteksi adanya perintah close and exit
        force_close = email.find("close and exit")
        #sistem untuk menentukan return
        if force_close != -1:
            return "close and exit"

        elif start != -1:
            return link


def main():
    check = email_checker()
    #sistem utama
    while True:
        try:
            email = check.define_email()
            #mencoba menutup browser sebelumnya jika ada,
            #agar suara youtube tidak tumpang tindih
            try:
                browser.close()
            except:
                pass

            #mengambil keputusan berdasarkan perintah email
            if email == "close and exit":
                break
            if email[:24] != "https://www.youtube.com/":
                time.sleep(30)
                continue

            #membuka youtube sesuai perintah email
            try:
                browser = webdriver.Chrome()
                browser.get(email)
            except:
                pass

            #sistem pendeteksi email baru setiap 30 detik
            while True:
                time.sleep(30)
                new_email = check.define_email()
                if new_email == email:
                    continue
                elif new_email != email:
                    break
        #jika terjadi exception, program akan tetap jalan,
        #dan menunggu perintah baru dari email
        except:
            time.sleep(30)
            continue
        
main()

