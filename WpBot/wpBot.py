from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from cleverbotfree import Cleverbot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
#gerekli import işlemleri

@Cleverbot.connect # cleverbot'un bağlantısını sağlamak
def chat(bot):
    driver = webdriver.Chrome(ChromeDriverManager().install()) #gerekli driverların kurulumu
    driver.get("https://web.whatsapp.com") #whatsapp sitesinin açılması

    # Kullanıcıdan QR kodunu okutmasını bekleyin
    input("QR kodu okutun ve devam etmek için Enter'a basın...")

    last_message_text = "" #son mesajı tutan bir değişken
    flag=False

    #ana döngü
    while True:

        try:
            message_area = driver.find_element(By.XPATH,
                                               '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p') #mesajın yazılacağı alanın html kodunu tutan XPATH türünde değişken
        except Exception as e:
            print(f"Message area not found: {e}")
            time.sleep(5)
            continue

        try:
            messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]') #son mesajı almak için
            if messages:
                last_message_element = messages[-1].find_element(By.XPATH,
                                                                 './/span[contains(@class, "selectable-text")]') #son mesaj
                last_message = last_message_element.text


                if last_message != last_message_text: #clever bot'un kendi kendine konuşmaması için son mesajın değişmesini bekleyen bir koşul
                    print(f"Received message: {last_message}")
                    last_message_text = last_message



                    if last_message.lower() == "quit" and flag==True:
                        #programdan çıkış yapmak için gereken kelime.
                        #Ayrıca aynı sohbette yapılacak konuşmada son cümle "quit" olursa diye bir flag eklendi
                        print("Quit command received. Exiting.")
                        break

                    response = bot.single_exchange(last_message) #cleverbot'un vereceği cevap
                    print(f"Response: {response}")

                    #mesajın girilmesi ve gönderilmesi
                    message_area.click()
                    message_area.send_keys(response)
                    message_area.send_keys(Keys.RETURN)
                else:
                    print("No messages found.")
                    flag=True




        except Exception as e:
            print(f"Error: {e}")

        time.sleep(5)  # Döngüde çok sık kontrol yapmamak için beklemek


if __name__ == "__main__":
    chat()
