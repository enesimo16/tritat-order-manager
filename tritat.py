users=[]
tables = {i: {"adisyon_acik": False, "siparisler": [], "toplam": 0} for i in range(1, 21)}
payment_history = []

menu = {
    1: {"ad": "Dilim Tatlı", "fiyat": 80},
    2: {"ad": "Kap Tatlı", "fiyat": 80},
    3: {"ad": "Makaron", "fiyat": 120},
    4: {"ad": "Soda", "fiyat": 25},
    5: {"ad": "Meyveli Soda", "fiyat": 30},
    6: {"ad": "Su", "fiyat": 10}
}

slice_d = 0
bowl_d = 0
macaroon = 0
soda = 0
f_soda = 0
water = 0

def admin_panel():
    global slice_d, bowl_d, macaroon, soda, f_soda, water
    
    name_a = input("İsim: ")
    password_a = input("Şifre: ")
    
    if name_a == "admin" and password_a == "123456789":
        print("Giriş yapıldı.")
        
        while True:
            print("\n--- ADMIN PANEL ---")
            print("1- Ödeme al")
            print("2- Ciro")
            print("3- Gelen tatlılar")
            print("4- İşlem geçmişi")
            print("0- Çıkış")
            
            secim = input("Yapmak istediğiniz seçim: ")
            
            if secim == "1":
                masa_no = int(input("Ödeme alınacak masa numarası (1-20): "))
                if 1 <= masa_no <= 20:
                    admin_pay(masa_no)
                else:
                    print("Geçersiz masa numarası!")
            
            elif secim == "2":
                # Ciro = tüm payment_history toplamı
                toplam_ciro = sum(p["toplam"] for p in payment_history)
                print(f"\nToplam Ciro: {toplam_ciro} TL")
            
            elif secim == "3":
                stok()
            
            elif secim == "4":
                payment_gecmisi()
            
            elif secim == "0":
                print("Admin panelinden çıkılıyor...")
                break
            
            else:
                print("Geçersiz seçim!")
    
    else:
        print("Yanlış girildi.")

def payment_gecmisi():
    """
    Ödenmiş tüm masaları ve toplamları göster
    """
    print("\n--- Ödeme Geçmişi ---")
    if not payment_history:
        print("Henüz ödeme yapılmadı.")
        return
    
    for p in payment_history:
        print(f"Masa {p['masa']} - Toplam: {p['toplam']} TL")

def admin_pay(masa_no):
    """
    Admin kasada ödeme alır ve masayı sıfırlar
    """
    if not tables[masa_no]["siparisler"]:
        print(f"{masa_no}. masa zaten boş.")
        return
    
    toplam = tables[masa_no]["toplam"]
    print(f"\n{masa_no}. MASA ÖDEME İŞLEMİ")
    print(f"Ödenecek Tutar: {toplam} TL")
    
    # Ödeme kaydı
    payment_history.append({
        "masa": masa_no,
        "toplam": toplam,
        "detay": tables[masa_no]["siparisler"]
    })
    
    # Masayı sıfırla
    tables[masa_no] = {"siparisler": [], "toplam": 0}
    print("Ödeme alındı, masa sıfırlandı!")
    
    tables[masa_no]["adisyon_acik"] = False

def user_register():
    name_k = input("Kullanıcı Adı: ")
    password_k = input("Şifre: ")
    password_ktekrar = input("Tekrar Şifre: ")

    if password_k != password_ktekrar:
        print("Şifreler eşleşmiyor! Kayıt başarısız.")
        return

    for user in users:
        if user["name"] == name_k:
            print("Bu kullanıcı adı zaten kayıtlı!")
            return

    users.append({"name": name_k, "password": password_k})
    print("Kayıt yapıldı!!")

def stok():
    global slice_d, bowl_d, macaroon, soda, f_soda, water
    slice_d = int(input("Sabah gelen dilim tatlı sayısı: "))
    bowl_d = int(input("Sabah gelen kap tatlı sayısı: "))
    macaroon = int(input("Sabah gelen makaron sayısı: "))
    soda = int(input("Sabah gelen soda sayısı: "))
    f_soda = int(input("Sabah gelen meyveli soda sayısı: "))
    water = int(input("Sabah gelen su sayısı: "))
    print("Stok bilgileri güncellendi!")

def opening():
    print("TRITAT-TERMINAL")

def authentication():
    if len(users) == 0:
        print("Herhangi bir çalışan bulunamadı, kasadan kayıt açtırın veya başka birinin hesabı ile devam ediniz.")
        return False
    else:
        name = input("Kullanıcı Adı: ")
        password = input("Şifre: ")

        for user in users:
            if user["name"] == name and user["password"] == password:
                print(f"Hoş geldin, {name}!")
                return True

        print("Hatalı kullanıcı adı veya şifre!")
        return False





def user_panel(masa_no):
    while True:
        print(f"\n--- {masa_no}. MASA ---")
        print("1- Yeni Adisyon")
        print("2- Adisyon")
        print("3- Ürün ekle")
        print("4- Ürün sil")
        print("5- Hesap")
        print("6- Hesabı Kapat")
        print("0- Geri Dön")

        secim = input("Seçiminiz: ")
        if secim == "1":
            adisyon1 = False
            new_adisyon(masa_no)
        elif secim == "2":
            adisyon(masa_no)
        elif secim == "3":
            siparis_ekle(masa_no)
        elif secim == "4":
            siparis_sil(masa_no)
        elif secim == "5":
            hesap(masa_no)
        elif secim == "6":
            hesabi_kapat(masa_no)
            break
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim!")
            
    else:
        print("Geçersiz ürün!")

def new_adisyon(masa_no):
    if tables[masa_no]["adisyon_acik"]:
        print(f"{masa_no}. masada zaten açık bir adisyon var.")
    else:
        tables[masa_no]["adisyon_acik"] = True
        tables[masa_no]["siparisler"] = []
        tables[masa_no]["toplam"] = 0
        print(f"{masa_no}. masa için yeni adisyon açıldı.")
    
def adisyon(masa_no):
    print(f"\n{masa_no}. MASA SİPARİŞLERİ:")
    if not tables[masa_no]["siparisler"]:
        print("Henüz sipariş yok.")
    else:
        for siparis in tables[masa_no]["siparisler"]:
            print(f"{siparis['urun']} - {siparis['adet']} adet - {siparis['tutar']} TL")
        print(f"Toplam: {tables[masa_no]['toplam']} TL")

def siparis_ekle(masa_no):
    if not tables[masa_no]["adisyon_acik"]:
        print("Önce yeni adisyon açmalısınız!")
        return

    print("\n--- Menü ---")
    for k, v in menu.items():
        print(f"{k}. {v['ad']} - {v['fiyat']} TL")

    secim = int(input("Ürün numarası: "))
    adet = int(input("Adet: "))

    if secim in menu:
        urun = menu[secim]
        toplam_fiyat = urun["fiyat"] * adet
        tables[masa_no]["siparisler"].append({"urun": urun["ad"], "adet": adet, "tutar": toplam_fiyat})
        tables[masa_no]["toplam"] += toplam_fiyat
        print(f"{adet} adet {urun['ad']} eklendi. Toplam: {tables[masa_no]['toplam']} TL")
    else:
        print("Geçersiz ürün!")

def siparis_sil(masa_no):
    siparisler = tables[masa_no]["siparisler"]
    if not siparisler:
        print("Bu masada sipariş yok.")
        return
    
    print("\n--- Mevcut Siparişler ---")
    for i, siparis in enumerate(siparisler, start=1):
        print(f"{i}. {siparis['urun']} x{siparis['adet']} - {siparis['tutar']} TL")
    
    secim = int(input("Silmek istediğiniz sipariş numarası: "))
    
    if 1 <= secim <= len(siparisler):
        silinen = siparisler.pop(secim - 1)
        tables[masa_no]["toplam"] -= silinen["tutar"]
        print(f"{silinen['urun']} silindi. Yeni toplam: {tables[masa_no]['toplam']} TL")
    else:
        print("Geçersiz seçim!")

def hesap(masa_no):
    print(f"\n{masa_no}. MASA SİPARİŞ DURUMU:")
    if not tables[masa_no]["siparisler"]:
        print("Henüz sipariş yok.")
    else:
        for siparis in tables[masa_no]["siparisler"]:
            print(f"{siparis['urun']} - {siparis['adet']} adet - {siparis['tutar']} TL")
        print(f"TOPLAM: {tables[masa_no]['toplam']} TL")

def hesabi_kapat(masa_no):
    toplam = tables[masa_no]['toplam']
    print(f"\n{masa_no}. MASA HESABI KAPATILIYOR...")
    print(f"Toplam Hesap: {toplam} TL")
    
    # Ödeme kaydı
    payment_history.append({
        "masa": masa_no,
        "toplam": toplam,
        "detay": tables[masa_no]["siparisler"]
    })
    
    # Masayı sıfırla
    tables[masa_no] = {"siparisler": [], "toplam": 0}
    print("Masa sıfırlandı!")
    
    tables[masa_no]["adisyon_acik"] = False
    
    

def main():
    opening()  # TRITAT-TERMINAL yazısı
    while True:
        print("\n--- ANA MENÜ ---")
        print("1- Çalışan Girişi")
        print("2- Çalışan Kaydı")
        print("3- Admin Girişi")
        print("0- Çıkış")

        secim = input("Seçiminiz: ")

        if secim == "1":
            if authentication():
                masa_no = int(input("Çalıştığınız masa numarası (1-20): "))
                if 1 <= masa_no <= 20:
                    user_panel(masa_no)
                else:
                    print("Geçersiz masa numarası!")
        elif secim == "2":
            user_register()
        elif secim == "3":
            admin_panel()
        elif secim == "0":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim!")

# Programı başlat
if __name__ == "__main__":
    main()

