import pandas as pd  # Veri Analizi için Pandas kütüphanesi tanımlattım.
import matplotlib.pyplot as plt  # Grafiksel arayüz içinde Matplot kütüphanesini tanımlattım.
import os  # Dosya işlemlerini gerçekleştirmek için Os kütüphanesini tanımlattım.


# Önce dosya olup olmadığını doğrulayan bir fonksiyon yazdım.
def dosya_var_mi(dosya_adi):
    """
    Verilen dosya adının mevcut olup olmadığını kontrol eder.
    :param dosya_adi: Kontrol edilecek dosya adı (string)
    :return: Dosya varsa True, yoksa False
    """
    return os.path.isfile(dosya_adi)

# Sonra log dosyasını tanımlayıp okuyan fonksiyonu yazdım.
def log_dosyasi_oku(dosya_adi):
    """
    Ağ trafiği log dosyasını okur ve pandas DataFrame olarak döner.
    Beklenen format: IP, Port, Zaman, Veri Boyutu gibi sütunlar olabilir.
    :param dosya_adi: Okunacak log dosyasının adı (string)
    :return: pandas DataFrame
    """
    try:
        # Dosyayı pandas ile csv formatında okuyoruz, delimiter boşluk veya tab olabilir.
        df = pd.read_csv(dosya_adi, delim_whitespace=True, header=None)
        # Kolon isimlerini belirleyelim (örnek kolonlar).
        df.columns = ['Tarih', 'Saat', 'Kaynak_IP', 'Hedef_IP', 'Protokol', 'Port', 'Bayt'] # Sırasıyla sütunlara önemli detayları giriyoruz ki rahatça analiz yapalım.
        return df
    
    except FileNotFoundError: # Dosya yoksa kullanıcıya bilgi verir.
        print(f"Hata: '{dosya_adi}' dosyası bulunamadı.")
        return None
    
    except pd.errors.ParserError: # Dosyanın yapısı yanlışsa (örneğin düzgün ayrılmamışsa) hata mesajı verir.
        print("Hata: Dosya formatı beklenen şekilde değil.")
        return None
    
    except Exception as e: # Belirtilmeyen tüm diğer hatalarda devreye girer.
        print(f"Beklenmeyen hata: {e}") # Kısacası bilinmedik hatalarda ortaya çıkar.
        return None

# Okunmuş olan log dosyasındaki İp adreslerinin istatistik verilerinin fonksiyonunu yazdım.
def ip_adresleri_istatistik(df):
    """
    DataFrame'deki kaynak IP adreslerinin kaç kere geçtiğini sayar.
    :param df: pandas DataFrame
    :return: IP adresi ve sayısı içeren pandas Series
    """
    return df['Kaynak_IP'].value_counts() # Yukarıdaki sütunlarda tanımlattığımız Kaynak_IP ayrıştırarak düzene sokmamızı sağlıyor.

# Daha sonrasında ise, port istatistiklerinin fonksiyonunu yazdım.
def port_istatistik(df):
    """
    DataFrame'deki portların kullanım sıklığını hesaplar.
    :param df: pandas DataFrame
    :return: Port ve sayısı içeren pandas Series
    """
    return df['Port'].value_counts() # Yukarıdaki sütunlarda tanımlattığımız Port ayrıştırarak düzene sokmamızı sağlıyor.

# Veri boyutunu hesapladığımız istatiksel fonksiyonu yazdım.
def veri_boyutu_istatistik(df):
    """
    Gönderilen/verilen bayt toplamını ve ortalamasını hesaplar.
    :param df: pandas DataFrame
    :return: Toplam bayt, ortalama bayt (tuple)
    """
    toplam = df['Bayt'].sum()
    ortalama = df['Bayt'].mean()
    return toplam, ortalama

# Grafiği ipsini çizen fonksiyonu yazdım.
def grafik_ciz_ip(ip_serisi):
    """
    En çok kullanılan 10 IP adresini bar grafikte gösterir.
    :param ip_serisi: IP adresi ve sayısı pandas Series
    """
    en_cok_10 = ip_serisi.head(10) #
    plt.figure(figsize=(10,6)) # Boyutunu ayarladım.
    en_cok_10.plot(kind='bar', color='skyblue') # Grafiği çubuk türünde görselleştirdim ve "skyblue" da çubuklara verdiğim renk.
    plt.title('En Çok Trafik Yapan 10 Kaynak IP') 
    plt.xlabel('IP Adresi')
    plt.ylabel('Bağlantı Sayısı')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Grafiğin portunu çizen fonksiyonu yazdım.
def grafik_ciz_port(port_serisi):
    """
    En çok kullanılan 10 portu bar grafikte gösterir.
    :param port_serisi: Port ve sayısı pandas Series
    """
    en_cok_10 = port_serisi.head(10)
    plt.figure(figsize=(10,6))
    en_cok_10.plot(kind='bar', color='coral') # Grafiği çubuk türünde görselleştirdim ve "coral" da çubuklara verdiğim renk.
    plt.title('En Çok Kullanılan 10 Port')
    plt.xlabel('Port Numarası')
    plt.ylabel('Kullanım Sayısı')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Analiz Aracının ana menüsünün fonksiyonunu yazdım.
def ana_menu():
    """
    Kullanıcı ile etkileşim kuran ana menü fonksiyonudur.
    Kullanıcıdan log dosyasını alır, analiz yapar ve sonuçlarını gösterir.
    """
    print("=== Ağ Trafiği Log Analiz Aracı ===") # İlk program çalışında ekrana bastırılan başlık ve programın adı.
    dosya_adi = input("Lütfen analiz edilecek log dosyasının adını (örnek: log.txt) giriniz: ")

    # Dosya var mı kontrolü yapıyorum.
    if not dosya_var_mi(dosya_adi):  # Eğerki dosyayı bulamadıysa alttaki yazıyı terminale yazdırıyor.
        print("Dosya bulunamadı. Lütfen dosya adını ve konumunu kontrol edin.")
        return

    # Log dosyasını oku.
    df = log_dosyasi_oku(dosya_adi)
    if df is None:
        return  # Dosya okunamadıysa programı sonlandır.

    # Kullanıcıya analiz seçenekleri  - Menü Bölümü.
    while True:
        print("\nAnaliz seçenekleri:") # Menü Başlığı
        print("1 - En çok trafik yapan IP adresleri") # 1.Seçenek
        print("2 - En çok kullanılan portlar") # 2.Seçenek
        print("3 - Gönderilen toplam ve ortalama veri boyutu") # 3.Seçenek
        print("4 - Tüm analizleri göster") # 4.Seçenek
        print("5 - Çıkış") # 5.Seçenek

        secim = input("Seçiminizi yapınız (1-5): ") # Kullanıcıdan seçim yapmasını istiyoruz.

        if secim == '1': # 1.Seçimi yapınca ip adreslerinin istatiklerini getiriyor.
            ip_sayilari = ip_adresleri_istatistik(df)
            print("\nEn çok trafik yapan IP adresleri:")
            print(ip_sayilari.head(10))
            grafik_ciz_ip(ip_sayilari)

        elif secim == '2': # 2.Seçimi yapınca port istatiklerini getiriyor.
            port_sayilari = port_istatistik(df)
            print("\nEn çok kullanılan portlar:")
            print(port_sayilari.head(10))
            grafik_ciz_port(port_sayilari)

        elif secim == '3': # 3.Seçimi yapınca veri boyutu istatiklerini getiriyor. Bunları terminale yazdırıyor.
            toplam, ortalama = veri_boyutu_istatistik(df)
            print(f"\nToplam gönderilen veri boyutu: {toplam} bayt")
            print(f"Ortalama gönderilen veri boyutu: {ortalama:.2f} bayt")

        elif secim == '4': # 4.Seçimi yapınca tüm istatikleri analiz yapmamız için tüm fonksiyonları çağırıyoruz.
            ip_sayilari = ip_adresleri_istatistik(df) # Önce ip adreslerinin istatiklerini.
            port_sayilari = port_istatistik(df) # Sonrasında  port istatiklerini.
            toplam, ortalama = veri_boyutu_istatistik(df) # Son olarakta veri boyutu istatiklerini çağırıyor.

            print("\n--- En çok trafik yapan IP adresleri ---") # Bir tane title açıp önce İp istatik bölümünü yazdırıyor.
            print(ip_sayilari.head(10))
            grafik_ciz_ip(ip_sayilari)

            print("\n--- En çok kullanılan portlar ---") # Daha sonrasında portların title açıp port istatik bölümünü yazdırıyor.
            print(port_sayilari.head(10))
            grafik_ciz_port(port_sayilari)

            # Bu tarafta ise terminale toplam gönderilen veri boyutu ve ortalama gönderilen veri boyutunu gösteriyor.
            print(f"\nToplam gönderilen veri boyutu: {toplam} bayt") 
            print(f"Ortalama gönderilen veri boyutu: {ortalama:.2f} bayt")

        elif secim == '5': # 5.Seçimi de programdan rahatça çıkabilme imkanı sağladım.
            print("Programdan çıkılıyor...") # Çıkış yaparken terminale yazdırdığı metinde gözüküyor.
            break

        else: # Eğer ki geçersiz sayılar ve harfler girerse hata mesajı bastırıyor.
            print("Geçersiz seçim, lütfen 1 ile 5 arasında bir değer giriniz.")

if __name__ == "__main__":
    # Programın başlangıç noktası
    ana_menu()
