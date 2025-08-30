import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime
import tkinter as tk


# Global değişkenlerimiz 
gelen_urunler = [] # Kişiselleştirilebilir sevkiyat sistemi.
stok = {}  
log_kayitlari = [] 
calisanlar = []
current_user_role = None  
btn_tatli_panel = None  


#Kullanıcı JSON
KULLANICI_DOSYA = "kullanicilar.json"

KULLANICILAR = {
    "mudur": {"sifre": "1234", "rol": "mudur"},
    "calisan1": {"sifre": "1234", "rol": "calisan"},
    "gmudur": {"sifre": "1234", "rol": "mudur"},
    "calisan2": {"sifre": "0000", "rol": "calisan"} 
    }

def get_default_data():
    return {
        "tables": {str(i): {"adisyon_acik": False, "siparisler": [], "toplam": 0} for i in range(1, 21)},
        "gunluk_ciro": 0,
        "stok": {},
        "log_kayitlari": [],
        "last_save": datetime.now().isoformat()
    }

def load_data():
    global tables, gunluk_ciro, stok, log_kayitlari
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            tables = {int(k): v for k, v in data.get("tables", {}).items()}
            gunluk_ciro = data.get("gunluk_ciro", 0)
            stok = data.get("stok", {})
            log_kayitlari = data.get("log_kayitlari", [])
            
            print(f"Veriler başarıyla yüklendi. Son kayıt: {data.get('last_save', 'Bilinmiyor')}")
            return True
        else:
            default_data = get_default_data()
            tables = {int(k): v for k, v in default_data["tables"].items()}
            gunluk_ciro = default_data["gunluk_ciro"]
            stok = default_data["stok"]
            log_kayitlari = default_data["log_kayitlari"]
            print("İlk çalıştırma - varsayılan veriler yüklendi.")
            return False
    except Exception as e:
        print(f"Veri yükleme hatası: {e}")
        default_data = get_default_data()
        tables = {int(k): v for k, v in default_data["tables"].items()}
        gunluk_ciro = default_data["gunluk_ciro"]
        stok = default_data["stok"]
        log_kayitlari = default_data["log_kayitlari"]
        return False

def save_data():
    try:
        tables_for_json = {str(k): v for k, v in tables.items()}
        
        data = {
            "tables": tables_for_json,
            "gunluk_ciro": gunluk_ciro,
            "stok": stok,
            "log_kayitlari": log_kayitlari,
            "last_save": datetime.now().isoformat()
        }
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("Veriler başarıyla kaydedildi.")
        return True
    except Exception as e:
        print(f"Veri kaydetme hatası: {e}")
        messagebox.showerror("Hata", f"Veriler kaydedilemedi: {e}")
        return False



# Uygulama açıldığında dosyadan yükle
if os.path.exists(KULLANICI_DOSYA):
    with open(KULLANICI_DOSYA, "r", encoding="utf-8") as f:
        KULLANICILAR = json.load(f)
else:
    # Dosya yoksa varsayılanı kaydet
    with open(KULLANICI_DOSYA, "w", encoding="utf-8") as f:
        json.dump(KULLANICILAR, f, ensure_ascii=False, indent=4)


def kullanicilari_kaydet():
    """JSON dosyasına kullanıcıları kaydeder"""
    with open(KULLANICI_DOSYA, "w", encoding="utf-8") as f:
        json.dump(KULLANICILAR, f, ensure_ascii=False, indent=4)

def kullanici_dogrula():
    """Profesyonel ve düzenli kullanıcı giriş ekranı"""
    global current_user_role, btn_tatli_panel
    
    # Ana pencere
    giris_penceresi = tk.Tk()
    giris_penceresi.title("TRITAT - Kullanıcı Girişi")
    giris_penceresi.geometry("500x600")
    giris_penceresi.configure(bg="#1a252f")
    giris_penceresi.resizable(False, False)

    # Pencereyi merkeze al
    giris_penceresi.update_idletasks()
    x = (giris_penceresi.winfo_screenwidth() // 2) - (500 // 2)
    y = (giris_penceresi.winfo_screenheight() // 2) - (600 // 2)
    giris_penceresi.geometry(f"500x600+{x}+{y}")
    
    # ÜST BAŞLIK
    title_container = tk.Frame(giris_penceresi, bg="#1a252f")
    title_container.pack(pady=20)
    tk.Label(title_container, text="🍽️ TRITAT", font=("Arial", 28, "bold"),
             bg="#1a252f", fg="#ecf0f1").pack()
    tk.Label(title_container, text="Restoran Yönetim Sistemi", font=("Arial", 14),
             bg="#1a252f", fg="#95a5a6").pack()

    # ANA FORM ALANI
    main_container = tk.Frame(giris_penceresi, bg="#2c3e50", bd=3, relief="ridge")
    main_container.pack(pady=20, padx=30, fill="both", expand=True)

    tk.Label(main_container, text="🔐 Kullanıcı Girişi", font=("Arial", 18, "bold"),
             bg="#2c3e50", fg="#ecf0f1").pack(pady=(20,10))

    # KULLANICI ADI
    tk.Label(main_container, text="👤 Kullanıcı Adı", font=("Arial", 14),
            bg="#2c3e50", fg="#bdc3c7").pack(anchor="w", padx=40, pady=(10,5))
    kullanici_entry = tk.Entry(main_container, font=("Arial", 16),
                                bg="white", fg="#2c3e50", justify="center", relief="solid", bd=2)
    kullanici_entry.pack(fill="x", padx=40, ipady=12)

    # ŞİFRE
    tk.Label(main_container, text="🔒 Şifre", font=("Arial", 14),
            bg="#2c3e50", fg="#bdc3c7").pack(anchor="w", padx=40, pady=(20,5))
    sifre_entry = tk.Entry(main_container, font=("Arial", 16),
                            bg="white", fg="#2c3e50", show="*", justify="center", relief="solid", bd=2)
    sifre_entry.pack(fill="x", padx=40, ipady=12)

    # Şifreyi Göster
    show_password = tk.BooleanVar()
    def toggle_password():
        sifre_entry.config(show="" if show_password.get() else "*")

    check_frame = tk.Frame(main_container, bg="#2c3e50")
    check_frame.pack(pady=10)
    tk.Checkbutton(check_frame, text="Şifreyi Göster", variable=show_password,
                command=toggle_password, font=("Arial", 12),
                bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e").pack()

    status_label = tk.Label(main_container, text="Bilgilerinizi girin", 
                            font=("Arial", 12), bg="#2c3e50", fg="#95a5a6")
    status_label.pack(pady=10)

    # Giriş fonksiyonu
    def attempt_login():
        global current_user_role, btn_tatli_panel
        username = kullanici_entry.get().strip().lower()
        password = sifre_entry.get().strip()

        if not username or not password:
            status_label.config(text="❌ Lütfen tüm alanları doldurun!", fg="#e74c3c")
            return

        # Kullanıcı adı ve şifre kontrolü
        if username in KULLANICILAR and KULLANICILAR[username]["sifre"] == password:
            status_label.config(text="✅ Giriş Başarılı!", fg="#27ae60")
            current_user_role = KULLANICILAR[username]["rol"]
            
            # Giriş başarılı mesajından sonra pencereyi kapat
            giris_penceresi.after(500, giris_penceresi.destroy)

        else:
            status_label.config(text="❌ Kullanıcı adı veya şifre hatalı!", fg="#e74c3c")
            sifre_entry.delete(0, tk.END)
            kullanici_entry.focus()

    def clear_fields():
        kullanici_entry.delete(0, tk.END)
        sifre_entry.delete(0, tk.END)
        status_label.config(text="Bilgilerinizi girin", fg="#95a5a6")
        kullanici_entry.focus()

    def exit_app():
        giris_penceresi.destroy()
        import sys
        sys.exit()

    # BUTONLAR
    button_frame = tk.Frame(main_container, bg="#2c3e50")
    button_frame.pack(pady=20)
    tk.Button(button_frame, text="🚀 Giriş Yap", font=("Arial", 14, "bold"),
              bg="#27ae60", fg="white", width=12, height=2,
              relief="raised", bd=2, cursor="hand2", command=attempt_login).pack(side="left", padx=5)
    tk.Button(button_frame, text="🗑️ Temizle", font=("Arial", 14, "bold"),
              bg="#f39c12", fg="white", width=10, height=2,
              relief="raised", bd=2, cursor="hand2", command=clear_fields).pack(side="left", padx=5)
    tk.Button(button_frame, text="❌ Çıkış", font=("Arial", 14, "bold"),
              bg="#e74c3c", fg="white", width=8, height=2,
              relief="raised", bd=2, cursor="hand2", command=exit_app).pack(side="left", padx=5)

    # ALT BİLGİ
    info_frame = tk.Frame(giris_penceresi, bg="#1a252f")
    info_frame.pack(pady=10)
    tk.Label(info_frame, text="💡 Test Kullanıcıları:", font=("Arial", 11, "bold"),
             bg="#1a252f", fg="#f39c12").pack()
    tk.Label(info_frame, text="admin/1234  •  calisan/5678  •  mudur/admin  •  garson/0000",
             font=("Arial", 10), bg="#1a252f", fg="#95a5a6").pack()

    # Enter tuşu ile giriş
    giris_penceresi.bind('<Return>', lambda e: attempt_login())
    kullanici_entry.focus()

    # Başlangıç focus
    kullanici_entry.focus()

    giris_penceresi.mainloop()

    return current_user_role is not None

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# LOG Kayıt fonksiyonu fakat ÇALIŞMIYOR ŞUANLIK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def log_ekle(mesaj):
    """Log listesine zaman damgası ile yeni bir kayıt ekler."""
    global log_kayitlari
    zaman_damgasi = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    log_kayitlari.append({"zaman": zaman_damgasi, "mesaj": mesaj})
    save_data() # Her log kaydından sonra otomatik kaydet
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def update_admin_button():
    """Admin panel butonunu kullanıcı rolüne göre güncelle"""
    global btn_tatli_panel, current_user_role
    
    if btn_tatli_panel is None:
        return
        
    if current_user_role == "mudur":
        # Müdür için yeşil ve aktif
        btn_tatli_panel.config(
            state="normal",
            bg="#27ae60",  # Yeşil
            text="🍰 Admin Paneli (Aktif)",
            activebackground="#1e8449"
        )
    else:
        # Çalışan için kırmızı ve pasif
        btn_tatli_panel.config(
            state="disabled",
            bg="#e74c3c",  # Kırmızı
            text="🍰 Admin Paneli (Erişim Yok)",
            activebackground="#c0392b"
        )

# VERİ DOSYASI YOLU
DATA_FILE = "tritat_data.json"

# VARSAYILAN VERİ YAPISI
def get_default_data():
    return {
        "tables": {str(i): {"adisyon_acik": False, "siparisler": [], "toplam": 0} for i in range(1, 21)},
        "gunluk_ciro": 0,
        "last_save": datetime.now().isoformat()
    }

# VERİYİ YÜKLEME
def load_data():
    global tables, gunluk_ciro
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Masa verilerini yükle (string key'leri int'e çevir)
            tables = {}
            for key, value in data.get("tables", {}).items():
                tables[int(key)] = value
            
            gunluk_ciro = data.get("gunluk_ciro", 0)
            
            print(f"Veriler başarıyla yüklendi. Son kayıt: {data.get('last_save', 'Bilinmiyor')}")
            return True
        else:
            # İlk çalıştırma - varsayılan verileri kullan
            default_data = get_default_data()
            tables = {int(k): v for k, v in default_data["tables"].items()}
            gunluk_ciro = default_data["gunluk_ciro"]
            print("İlk çalıştırma - varsayılan veriler yüklendi.")
            return False
    except Exception as e:
        print(f"Veri yükleme hatası: {e}")
        # Hata durumunda varsayılan verileri kullan
        default_data = get_default_data()
        tables = {int(k): v for k, v in default_data["tables"].items()}
        gunluk_ciro = default_data["gunluk_ciro"]
        return False

# VERİYİ KAYDETME
def save_data():
    try:
        # Masa key'lerini string'e çevir (JSON için)
        tables_for_json = {str(k): v for k, v in tables.items()}
        
        data = {
            "tables": tables_for_json,
            "gunluk_ciro": gunluk_ciro,
            "last_save": datetime.now().isoformat()
        }
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("Veriler başarıyla kaydedildi.")
        return True
    except Exception as e:
        print(f"Veri kaydetme hatası: {e}")
        messagebox.showerror("Hata", f"Veriler kaydedilemedi: {e}")
        return False

# OTOMATİK KAYDETME
def auto_save():
    """Her 30 saniyede bir otomatik kaydet"""
    save_data()
    root.after(30000, auto_save)  # 30 saniye = 30000 ms

# PROGRAM KAPATILIRKEN KAYDET
def on_closing():
    if messagebox.askokcancel("Çıkış", "Programdan çıkmak istediğinizden emin misiniz?\nTüm veriler kaydedilecek."):
        save_data()
        root.destroy()

# VERİLERİ SIFIRLA
def reset_data():
    global tables, gunluk_ciro
    result = messagebox.askyesno(
        "Verileri Sıfırla", 
        "UYARI: Bu işlem tüm masa durumlarını ve günlük ciroyu sıfırlayacak!\n\nDevam etmek istediğinizden emin misiniz?"
    )
    if result:
        # Onay için ikinci bir dialog
        confirm = messagebox.askyesno(
            "Son Onay", 
            "SON UYARI: Bu işlem geri alınamaz!\n\nTüm veriler silinecek ve program yeniden başlayacak."
        )
        if confirm:
            default_data = get_default_data()
            tables = {int(k): v for k, v in default_data["tables"].items()}
            gunluk_ciro = default_data["gunluk_ciro"]
            
            # Dosyayı sil
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            
            save_data()
            update_buttons()
            guncelle_durum_bilgileri()
            guncelle_secili_masa_bilgisi()
            temizle_orta_panel()
            
            messagebox.showinfo("Başarılı", "Tüm veriler sıfırlandı!")

# Verileri yükle
load_data()

menu = {
    # Dilim Tatlılar
    "Dark Velvet": 80,
    "Red Velvet": 80,
    "Frambuazlı Trileçe": 80,
    "Çikolatalı Trileçe": 80,
    "Karamelli Trileçe": 80,
    "Soğuk Kadayıf": 80,
    "Tiramisu": 80,
    
    # Kap Tatlılar
    "Antep Fıstıklı M.": 80,
    "Lotuslu M.": 80,
    "Muzlu M.": 80,
    "Çilekli M.":80,
    "İtalyan Karamelli M.": 80,
    "Profiterol": 80,
    "Supangle": 80,
    "Sütlaç": 80,
    
    # İçecekler
    "Soda": 25,
    "Meyveli Soda": 30,
    "Su": 10
}

# Kullanıcı girişi ekranı göster
if not kullanici_dogrula():
    exit()


# Ana pencere oluştur
root = tk.Tk()
root.title("Çalışan Paneli - TRITAT")
root.geometry("1200x700")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

update_admin_button()  # Buraya ekle

secilen_masa = tk.IntVar()
secilen_masa.set(0)

# RENKLER
soft_red = "#f28b82"
soft_green = "#81c995"
soft_blue = "#a0c4ff"
soft_orange = "#ffb77d"
soft_purple = "#c59aff"
soft_gray = "#d3d3d3"
highlight_color = "#ffd966"
soft_white = "#ffffff"

# ÜST BİLGİ PANELİ
ust_panel = tk.Frame(root, bg="#2c3e50", height=70)
ust_panel.pack(fill="x")
ust_panel.pack_propagate(False)

# Logo/Başlık
baslik_frame = tk.Frame(ust_panel, bg="#2c3e50")
baslik_frame.pack(side="left", padx=15, pady=10)

tk.Label(baslik_frame, text="TRITAT", font=("Arial", 18, "bold"),
        bg="#2c3e50", fg="#ecf0f1").pack()
tk.Label(baslik_frame, text="Restoran Yönetim Sistemi", font=("Arial", 8), 
        bg="#2c3e50", fg="#bdc3c7").pack()

# Ortada buton için frame
orta_frame = tk.Frame(ust_panel, bg="#2c3e50")
orta_frame.pack(side="left", expand=True)

# Modern Tasarımlı Tatlı Paneli Butonu
btn_tatli_panel = tk.Button(
    orta_frame,
    text="🍰 Admin Paneli",
    font=("Arial", 14, "bold"),
    bg="#95a5a6",  # Başlangıçta gri
    fg="white",
    activebackground="#7f8c8d",
    activeforeground="white",
    relief="flat",
    width=25,
    height=3,
    cursor="hand2",
    state="disabled",  # Başlangıçta kilitli
    command=lambda: tatli_sayfasi() if current_user_role == "mudur" else messagebox.showwarning("Erişim Reddedildi", "Bu özelliğe sadece müdürler erişebilir!")
)
btn_tatli_panel.pack(expand=True)

# Hover efekti için event binding
def on_enter(e):
    if current_user_role == "mudur":
        btn_tatli_panel.config(bg="#1e8449")  # Koyu yeşil
    elif current_user_role == "calisan":
        btn_tatli_panel.config(bg="#c0392b")  # Koyu kırmızı

def on_leave(e):
    if current_user_role == "mudur":
        btn_tatli_panel.config(bg="#27ae60")  # Açık yeşil
    elif current_user_role == "calisan":
        btn_tatli_panel.config(bg="#e74c3c")  # Açık kırmızı

btn_tatli_panel.bind("<Enter>", on_enter)
btn_tatli_panel.bind("<Leave>", on_leave)

update_admin_button()


def tatli_sayfasi():
    # Sadece müdürler erişebilir
    if current_user_role != "mudur":
        messagebox.showwarning("Erişim Reddedildi", "Bu özelliğe sadece müdürler erişebilir!")
        return
        
    temizle_orta_panel()

    tk.Label(
        orta_panel, text="Kontrol Paneli", font=("Arial", 16, "bold"),
        bg="#fafafa", fg="#2c3e50"
    ).pack(pady=15)

    # Üst Butonlar
    buton_frame = tk.Frame(orta_panel, bg="#fafafa")
    buton_frame.pack(pady=10)

    # Çalışan Ekle
    tk.Button(
        buton_frame, text="Çalışan Ekle", font=("Arial", 10, "bold"),
        bg="#27ae60", fg="white", width=15, height=2,
        command=lambda: calisan_ekle()
    ).grid(row=0, column=0, padx=10)

    # Çalışanları Göster
    tk.Button(
        buton_frame, text="Çalışanları Göster", font=("Arial", 10, "bold"),
        bg="#8e44ad", fg="white", width=18, height=2,
        command=lambda: calisanlari_goster()
    ).grid(row=0, column=1, padx=10)

    # Gelen Tatlı Sayısı
    tk.Button(
        buton_frame, text="Gelen Tatlı Sayısı", font=("Arial", 10, "bold"),
        bg="#f39c12", fg="white", width=18, height=2,
        command=lambda: gelen_urun_formu()
    ).grid(row=0, column=2, padx=10)

    # Gelen Ürünler Listesi
    tk.Button(
        buton_frame, text="Gelen Ürünler Listesi", font=("Arial", 10, "bold"),
        bg="#2980b9", fg="white", width=20, height=2,
        command=lambda: gelen_urunler_listesi()
    ).grid(row=0, column=3, padx=10)

    # Günlük Ciro
    tk.Label(
        orta_panel, text=f"Günlük Ciro: {gunluk_ciro} TL",
        font=("Arial", 14, "bold"), bg="#fafafa", fg="#27ae60"
    ).pack(pady=10)

    # Satışlar
    tk.Label(
        orta_panel, text="Yapılan Satışlar", font=("Arial", 14, "bold"),
        bg="#fafafa", fg="#2c3e50"
    ).pack(pady=10)

    # Liste Alanı
    liste_frame = tk.Frame(orta_panel, bg="#fafafa")
    liste_frame.pack(fill="both", expand=True, padx=15, pady=10)

    canvas = tk.Canvas(liste_frame, bg="#fafafa")
    scrollbar = tk.Scrollbar(liste_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#fafafa")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def tatli_listesini_guncelle():
        for w in scroll_frame.winfo_children():
            w.destroy()
        
        # Günlük ciro ve toplam satış bilgisini göster
        toplam_satis = sum(sip['tutar'] for masa in tables.values() for sip in masa['siparisler'])
        tk.Label(
            scroll_frame,
            text=f"Güncel Ciro: {gunluk_ciro} TL | Toplam Satış: {toplam_satis} TL",
            font=("Arial", 11, "bold"),
            bg="#fafafa", fg="#e74c3c"
        ).pack(pady=8)
        
        # Stok durumunu göster
        stok_frame = tk.Frame(scroll_frame, bg="#fafafa")
        stok_frame.pack(fill="x", pady=5)
        for urun, adet in stok.items():
            tk.Label(
                stok_frame,
                text=f"{urun}: {adet} adet stokta",
                font=("Arial", 9),
                bg="#fafafa", fg="#2c3e50"
            ).pack(side="left", padx=5)

        tk.Label(
            scroll_frame,
            text="--- Uygulama Logları ---",
            font=("Arial", 12, "bold"),
            bg="#fafafa", fg="#34495e"
        ).pack(pady=10)

        # Log kayıtlarını tersten listele (en yeni en üstte)
        if not log_kayitlari:
            tk.Label(scroll_frame, text="Henüz log kaydı yok.", font=("Arial", 10), bg="#fafafa").pack()
        else:
            for log in reversed(log_kayitlari):
                tk.Label(
                    scroll_frame,
                    text=f"{log['zaman']} - {log['mesaj']}",
                    font=("Arial", 10),
                    bg="#fafafa", fg="#2c3e50", anchor="w"
                ).pack(fill="x", pady=2)

# ===================== İÇ FONKSİYONLAR =====================
def calisan_ekle():
    win = tk.Toplevel(root)
    win.title("Çalışan Ekle")
    win.geometry("350x350")
    win.configure(bg="#f0f2f5")
    win.resizable(False, False)

    tk.Label(win, text="Yeni Çalışan Ekle", font=("Helvetica", 14, "bold"),
             bg="#f0f2f5", fg="#34495e").pack(pady=15)

    tk.Label(win, text="Kullanıcı Adı", font=("Arial", 11),
             bg="#f0f2f5").pack(pady=5)
    ad_var = tk.StringVar()
    tk.Entry(win, textvariable=ad_var, font=("Arial", 11),
             bd=2, relief="groove").pack(pady=5, ipadx=5, ipady=5)

    tk.Label(win, text="Şifre", font=("Arial", 11),
             bg="#f0f2f5").pack(pady=5)
    sifre_var = tk.StringVar()
    tk.Entry(win, textvariable=sifre_var, font=("Arial", 11),
             bd=2, relief="groove", show="*").pack(pady=5, ipadx=5, ipady=5)

    tk.Label(win, text="Görev", font=("Arial", 11),
             bg="#f0f2f5").pack(pady=5)
    gorev_var = tk.StringVar(value="calisan")
    ttk.Combobox(win, textvariable=gorev_var,
                 values=["calisan", "mudur"], state="readonly",
                 font=("Arial", 11)).pack(pady=5, ipadx=5, ipady=5)

    # Kaydet butonu için frame
    frame_btn = tk.Frame(win, bg="#f0f2f5")
    frame_btn.pack(pady=20, fill="x")

    def kaydet():
        ad = ad_var.get().strip()
        sifre = sifre_var.get().strip()
        gorev = gorev_var.get().strip()
        if not ad or not sifre:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return
        if ad in KULLANICILAR:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten var!")
            return
        KULLANICILAR[ad] = {"sifre": sifre, "rol": gorev}
        kullanicilari_kaydet()
        messagebox.showinfo("Başarılı", f"{ad} ({gorev}) eklendi!")
        win.destroy()

    btn_kaydet = tk.Button(frame_btn, text="Kaydet", bg="#2ecc71", fg="white",
                           font=("Arial", 12, "bold"), bd=0, command=kaydet)
    btn_kaydet.pack(ipadx=10, ipady=5)

    # Hover efekti
    def on_enter(e):
        btn_kaydet['bg'] = '#27ae60'
    def on_leave(e):
        btn_kaydet['bg'] = '#2ecc71'
    btn_kaydet.bind("<Enter>", on_enter)
    btn_kaydet.bind("<Leave>", on_leave)


def calisanlari_goster():
    win = tk.Toplevel(root)
    win.title("Çalışanlar")
    win.geometry("400x400")
    win.configure(bg="#f0f2f5")

    tk.Label(win, text="Çalışan Listesi", font=("Helvetica", 14, "bold"),
             bg="#f0f2f5", fg="#34495e").pack(pady=15)

    frame_liste = tk.Frame(win, bg="#f0f2f5")
    frame_liste.pack(fill="both", expand=True, padx=20)

    if not KULLANICILAR:
        tk.Label(frame_liste, text="Henüz kullanıcı yok", font=("Arial", 11),
                 bg="#f0f2f5").pack(pady=10)
    else:
        for ad, bilgiler in KULLANICILAR.items():
            tk.Label(frame_liste, text=f"{ad} - {bilgiler['rol']}",
                     font=("Arial", 11), bg="#ecf0f1", fg="#2c3e50",
                     anchor="w", bd=1, relief="solid").pack(fill="x", pady=3, ipady=5)
            



def gelen_urun_formu():
    win = tk.Toplevel(root)
    win.title("Gelen Ürün Miktarları")
    win.geometry("450x500")
    win.configure(bg="#f5f6fa")
    win.resizable(False, False)

    # Başlık
    tk.Label(
        win, text="Gelen Ürün Miktarları",
        font=("Helvetica", 14, "bold"),
        bg="#f5f6fa", fg="#2f3640"
    ).pack(pady=20)

    urunler = [
        "Dilim Tatlı", "Kap Tatlı", "Su", "Soda",
        "Meyveli Soda", "Limonata", "Boronice",
        "Craft", "Kaşık", "Mendil", "Islak Mendil"
    ]

    entries = {}
    form_frame = tk.Frame(win, bg="#f5f6fa")
    form_frame.pack(pady=10)

    for i, urun in enumerate(urunler):
        row = i // 2
        col = (i % 2) * 2

        tk.Label(
            form_frame, text=urun,
            font=("Helvetica", 11),
            bg="#f5f6fa", fg="#2f3640"
        ).grid(row=row, column=col, padx=10, pady=8, sticky="w")

        var = tk.IntVar()
        entry = tk.Entry(
            form_frame, textvariable=var,
            width=8, font=("Helvetica", 11),
            justify="center", bd=2, relief="groove"
        )
        entry.grid(row=row, column=col+1, padx=5, pady=8)
        entries[urun] = var

    # Hover efektli buton
    def on_enter(e):
        kaydet_btn['background'] = "#2980b9"

    def on_leave(e):
        kaydet_btn['background'] = "#3498db"
    
    def kaydet():
        zaman = datetime.now().strftime("%H:%M")
        toplam_eklenen = 0
        for urun, var in entries.items():
            adet = var.get()
            if adet > 0:
                gelen_urunler.append({"urun": urun, "adet": adet, "zaman": zaman})
                toplam_eklenen += adet

        if toplam_eklenen == 0:
            messagebox.showerror("Hata", "Hiçbir ürün girmediniz!")
            return

        messagebox.showinfo("Başarılı", f"{toplam_eklenen} ürün kaydedildi!")
        win.destroy()

    kaydet_btn = tk.Button(
        win, text="Kaydet",
        bg="#3498db", fg="white",
        font=("Helvetica", 12, "bold"),
        activebackground="#2980b9",
        activeforeground="white",
        padx=20, pady=8,
        command=kaydet
    )
    kaydet_btn.pack(pady=25)
    kaydet_btn.bind("<Enter>", on_enter)
    kaydet_btn.bind("<Leave>", on_leave)

def gelen_urunler_listesi():
    """Gelen ürünlerin listesi - estetik versiyon"""
    win = tk.Toplevel(root)
    win.title("Gelen Ürünler Listesi")
    win.geometry("450x450")
    win.configure(bg="#f5f6fa")
    win.resizable(False, False)

    # Başlık
    header = tk.Label(
        win, text="Gelen Ürünler",
        font=("Helvetica", 14, "bold"),
        bg="#f5f6fa", fg="#2f3640"
    )
    header.pack(pady=15)

    # Çerçeve
    frame = tk.Frame(win, bg="#ffffff", bd=2, relief="groove")
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    if not gelen_urunler:
        tk.Label(frame, text="Henüz veri yok", font=("Helvetica", 11),
                 bg="#ffffff", fg="#7f8c8d").pack(pady=20)
    else:
        # Scrollbar ve Listbox
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            frame, font=("Helvetica", 11),
            bg="#ecf0f1", fg="#2c3e50",
            yscrollcommand=scrollbar.set,
            selectbackground="#3498db",
            selectforeground="white",
            activestyle="none",
            bd=0, highlightthickness=0
        )
        listbox.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.config(command=listbox.yview)

        for g in gelen_urunler:
            listbox.insert("end", f"{g['zaman']} - {g['urun']} : {g['adet']} adet")


# Durum bilgileri
durum_frame = tk.Frame(ust_panel, bg="#2c3e50")
durum_frame.pack(side="left", padx=30, pady=10)  # Padding küçültüldü

def temizle_orta_panel():
    for widget in orta_panel.winfo_children():
        widget.destroy()

def guncelle_durum_bilgileri():
    for widget in durum_frame.winfo_children():
        widget.destroy()
    
    acik_masa_sayisi = sum(1 for masa in tables.values() if masa["adisyon_acik"])
    
    bilgi_frame1 = tk.Frame(durum_frame, bg="#2c3e50")
    bilgi_frame1.pack(side="top", fill="x")
    
    tk.Label(bilgi_frame1, text="Açık Masalar:", font=("Arial", 9), 
            bg="#2c3e50", fg="#bdc3c7").pack(side="left")
    tk.Label(bilgi_frame1, text=f"{acik_masa_sayisi}/20", font=("Arial", 10, "bold"), 
            bg="#2c3e50", fg="#e74c3c").pack(side="left", padx=(5,0))
    
    bilgi_frame2 = tk.Frame(durum_frame, bg="#2c3e50")
    bilgi_frame2.pack(side="top", fill="x")
    
    tk.Label(bilgi_frame2, text="Günlük Ciro:", font=("Arial", 9), 
            bg="#2c3e50", fg="#bdc3c7").pack(side="left")
    tk.Label(bilgi_frame2, text=f"{gunluk_ciro} TL", font=("Arial", 10, "bold"), 
            bg="#2c3e50", fg="#27ae60").pack(side="left", padx=(5,0))
    
    


guncelle_durum_bilgileri()

# Seçili masa bilgisi
secili_masa_frame = tk.Frame(ust_panel, bg="#2c3e50")
secili_masa_frame.pack(side="right", padx=15, pady=8)

secili_masa_label = tk.Label(secili_masa_frame, text="Masa Seçilmedi", 
                            font=("Arial", 10, "bold"), bg="#2c3e50", fg="#f39c12")
secili_masa_label.pack()

masa_siparis_label = tk.Label(secili_masa_frame, text="", 
                            font=("Arial", 8), bg="#2c3e50", fg="#ecf0f1")
masa_siparis_label.pack()


def guncelle_secili_masa_bilgisi():
    masa_no = secilen_masa.get()
    if masa_no == 0:
        secili_masa_label.config(text="Masa seçilmedi")
        masa_siparis_label.config(text="")
        return

    masa = tables[masa_no]
    if masa["adisyon_acik"]:
        siparis_sayisi = len(masa["siparisler"])
        toplam_adet = sum(s['adet'] for s in masa["siparisler"])
        secili_masa_label.config(text=f"Masa {masa_no} | Adisyon AÇIK")
        masa_siparis_label.config(text=f"{siparis_sayisi} Sipariş - {toplam_adet} adet - {masa['toplam']} TL")
    else:
        secili_masa_label.config(text=f"Masa {masa_no} | Adisyon Kapalı")
        masa_siparis_label.config(text="")

# ANA CONTAINER
main_container = tk.Frame(root, bg="#f5f5f5")
main_container.pack(fill="both", expand=True, padx=8, pady=8)

# SOL PANEL - MASALAR
sol_panel = tk.Frame(main_container, bg="#f5f5f5", width=450)  # Genişlik küçültüldü
sol_panel.pack(side="left", fill="y", padx=(0,8))
sol_panel.pack_propagate(False)

# SAĞ PANEL - İŞLEMLER VE ORTA ALAN
sag_panel = tk.Frame(main_container, bg="#f5f5f5")
sag_panel.pack(side="right", fill="both", expand=True)

# ORTA PANEL
orta_panel = tk.Frame(sag_panel, bg="#fafafa", relief="ridge", bd=1)
orta_panel.pack(fill="both", expand=True, pady=(0,8))

def temizle_orta_panel():
    for widget in orta_panel.winfo_children():
        widget.destroy()

def siparisleri_goster():
    temizle_orta_panel()
    masa_no = secilen_masa.get()
    if masa_no == 0:
        tk.Label(orta_panel, text="Lütfen bir masa seçin", font=("Arial", 14), bg="#fafafa", fg="gray").pack(pady=50)
        return

    masa = tables[masa_no]
    if not masa["siparisler"]:
        tk.Label(orta_panel, text="Henüz sipariş yok", font=("Arial", 14), bg="#fafafa", fg="gray").pack(pady=50)
        return

    # Başlık
    baslik_frame = tk.Frame(orta_panel, bg="#fafafa")
    baslik_frame.pack(pady=8, fill="x", padx=15)
    
    tk.Label(baslik_frame, text=f"Masa {masa_no} Siparişleri", 
            font=("Arial", 14, "bold"), bg="#fafafa", fg="#2c3e50").pack(side="left")
    
    # Toplam tutar
    if masa["toplam"] > 0:
        tk.Label(baslik_frame, text=f"Toplam: {masa['toplam']} TL", 
                font=("Arial", 12, "bold"), bg="#fafafa", fg="#e74c3c").pack(side="right")

    # Siparişler listesi
    siparis_frame = tk.Frame(orta_panel, bg="#fafafa")
    siparis_frame.pack(pady=8, fill="both", expand=True, padx=15)
    
    # Başlık satırı
    baslik_kutu = tk.Frame(siparis_frame, bg="#34495e", height=35)
    baslik_kutu.pack(fill="x", pady=(0,3))
    baslik_kutu.pack_propagate(False)
    
    tk.Label(baslik_kutu, text="Adet", font=("Arial", 9, "bold"), 
            bg="#34495e", fg="white", width=6).pack(side="left", padx=8, pady=6)
    tk.Label(baslik_kutu, text="Ürün", font=("Arial", 9, "bold"), 
            bg="#34495e", fg="white", width=22).pack(side="left", padx=8, pady=6)
    tk.Label(baslik_kutu, text="Birim Fiyat", font=("Arial", 9, "bold"), 
            bg="#34495e", fg="white", width=10).pack(side="left", padx=8, pady=6)
    tk.Label(baslik_kutu, text="Toplam", font=("Arial", 9, "bold"), 
            bg="#34495e", fg="white", width=8).pack(side="left", padx=8, pady=6)

    for idx, sip in enumerate(masa["siparisler"]):
        kutu = tk.Frame(siparis_frame, bg=soft_white, bd=1, relief="ridge", height=30)
        kutu.pack(fill="x", pady=1)
        kutu.pack_propagate(False)
        
        # Adet
        tk.Label(kutu, text=f"{sip['adet']}", width=6, font=("Arial", 10), 
                 bg=soft_white, fg="#2c3e50").pack(side="left", padx=8, pady=4)
        
        # Ürün adı
        tk.Label(kutu, text=sip['urun'], width=22, font=("Arial", 10), 
                 bg=soft_white, fg="#2c3e50", anchor="w").pack(side="left", padx=8, pady=4)
        
        # Birim fiyat
        birim_fiyat = sip['tutar'] // sip['adet']
        tk.Label(kutu, text=f"{birim_fiyat} TL", width=10, font=("Arial", 10), 
                 bg=soft_white, fg="#7f8c8d").pack(side="left", padx=8, pady=4)
        
        # Toplam tutar
        tk.Label(kutu, text=f"{sip['tutar']} TL", width=8, font=("Arial", 10, "bold"), 
                 bg=soft_white, fg="#e74c3c").pack(side="left", padx=8, pady=4)


def siparis_ekle():
    """Sipariş ekleme ekranı - geliştirilmiş versiyon"""
    temizle_orta_panel()
    masa_no = secilen_masa.get()
    if masa_no == 0:
        tk.Label(orta_panel, text="Lütfen bir masa seçin", font=("Arial", 14), bg="#fafafa", fg="gray").pack(pady=50)
        return
    
    masa = tables[masa_no]
    if not masa["adisyon_acik"]:
        masa["adisyon_acik"] = True
        masa["siparisler"] = []
        masa["toplam"] = 0
        update_buttons()
        guncelle_secili_masa_bilgisi()
        guncelle_durum_bilgileri()

    # Başlık
    tk.Label(orta_panel, text=f"Masa {masa_no} - Sipariş Ekle", font=("Arial", 14, "bold"), bg="#fafafa", fg="#2c3e50").pack(pady=10)

    # Ana container
    main_siparis_frame = tk.Frame(orta_panel, bg="#fafafa")
    main_siparis_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Sol taraf - menü butonları
    menu_frame = tk.Frame(main_siparis_frame, bg="#fafafa")
    menu_frame.pack(side="left", fill="both", expand=True)
    
    # Sağ taraf - adet kontrolü ve ekleme
    kontrol_frame = tk.Frame(main_siparis_frame, bg="#e8f4fd", bd=2, relief="ridge", width=200)
    kontrol_frame.pack(side="right", fill="y", padx=(20,0))
    kontrol_frame.pack_propagate(False)

    # Seçili ürün ve adet kontrolü
    tk.Label(kontrol_frame, text="Seçili Ürün:", font=("Arial", 11, "bold"), bg="#e8f4fd", fg="#2c3e50").pack(pady=(10,5))
    secili_urun_label = tk.Label(kontrol_frame, text="Ürün seçiniz", font=("Arial", 10), bg="#e8f4fd", fg="#7f8c8d")
    secili_urun_label.pack(pady=5)

    # Adet kontrolü
    tk.Label(kontrol_frame, text="Adet:", font=("Arial", 11, "bold"), bg="#e8f4fd", fg="#2c3e50").pack(pady=(15,5))
    adet_frame = tk.Frame(kontrol_frame, bg="#e8f4fd")
    adet_frame.pack(pady=5)
    adet_var = tk.IntVar(value=1)
    
    def adet_azalt():
        if adet_var.get() > 1:
            adet_var.set(adet_var.get() - 1)
            
    def adet_arttir():
        adet_var.set(adet_var.get() + 1)
    
    btn_azalt = tk.Button(adet_frame, text="-", width=3, height=1, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), command=adet_azalt)
    btn_azalt.pack(side="left", padx=5)
    
    adet_entry = tk.Entry(adet_frame, textvariable=adet_var, width=5, font=("Arial", 12), justify="center", bd=2, relief="groove")
    adet_entry.pack(side="left", ipady=5)
    
    btn_arttir = tk.Button(adet_frame, text="+", width=3, height=1, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), command=adet_arttir)
    btn_arttir.pack(side="left", padx=5)
    
    secilen_urun = None

    def urun_sec(urun_adi):
        nonlocal secilen_urun
        secilen_urun = urun_adi
        secili_urun_label.config(text=urun_adi)
        adet_var.set(1)

    def siparis_ekle_komut():
        nonlocal secilen_urun
        if not secilen_urun:
            messagebox.showerror("Hata", "Lütfen bir ürün seçin!")
            return
        
        adet = adet_var.get()
        if adet <= 0:
            messagebox.showerror("Hata", "Adet 0'dan büyük olmalı!")
            return
        
        urun_fiyati = menu[secilen_urun]
        toplam_tutar = urun_fiyati * adet
        
        # Sipariş listesinde ürün var mı kontrol et
        found = False
        for siparis in masa["siparisler"]:
            if siparis["urun"] == secilen_urun:
                siparis["adet"] += adet
                siparis["tutar"] += toplam_tutar
                found = True
                break
        if not found:
            masa["siparisler"].append({"urun": secilen_urun, "adet": adet, "tutar": toplam_tutar})
            
        masa["toplam"] += toplam_tutar
        
        # Günlük ciroya ekle
        global gunluk_ciro
        gunluk_ciro += toplam_tutar
        
        # Loga ekle
        log_ekle(f"Masa {masa_no} için {adet} adet {secilen_urun} eklendi. ({toplam_tutar} TL)")
        
        messagebox.showinfo("Başarılı", f"{adet} adet {secilen_urun} masaya eklendi.")
        guncelle_secili_masa_bilgisi()
        guncelle_durum_bilgileri()
        save_data()
        siparisleri_goster()
        
    btn_siparis_ekle = tk.Button(
        kontrol_frame, text="Siparişe Ekle",
        font=("Arial", 12, "bold"),
        bg="#3498db", fg="white",
        activebackground="#2980b9",
        activeforeground="white",
        command=siparis_ekle_komut
    )
    btn_siparis_ekle.pack(pady=20, ipadx=10, ipady=5)

    # --- Kategoriye göre düzenleme ---
    kategoriler = {
        "Dilim Tatlıları": ["Dark Velvet", "Red Velvet", "Frambuazlı Trileçe", "Çikolatalı Trileçe", "Karamelli Trileçe", "Soğuk Kadayıf", "Tiramisu"],
        "Kap Tatlıları": ["Antep Fıstıklı M.", "Lotuslu M.", "Muzlu M.", "Çilekli M.", "İtalyan Karamelli M.", "Profiterol", "Supangle", "Sütlaç"],
        "İçecekler": ["Soda", "Meyveli Soda", "Su", "Türk Kahvesi", "Filtre Kahve"]
    }
    
    # "menu" sözlüğünü güncelle
    global menu
    menu.pop("Dilim Tatlı", None)
    menu.pop("Kap Tatlı", None)
    menu["Türk Kahvesi"] = 35 # Örnek fiyat
    menu["Filtre Kahve"] = 40 # Örnek fiyat

    # Her kategori için ayrı bir frame ve başlık oluştur
    for kategori_adi, urun_listesi in kategoriler.items():
        kategori_frame = tk.Frame(menu_frame, bg="#fafafa")
        kategori_frame.pack(fill="x", pady=5)
        
        # Kategori başlığı
        tk.Label(
            kategori_frame, text=f"--- {kategori_adi} ---",
            font=("Arial", 11, "bold"),
            bg="#fafafa", fg="#34495e"
        ).pack(anchor="w", padx=10)
        
        # Ürün butonları için alt frame
        urun_frame = tk.Frame(kategori_frame, bg="#fafafa")
        urun_frame.pack(fill="x", padx=10)
        
        # Butonları oluştur
        for urun in urun_listesi:
            btn = tk.Button(
                urun_frame, text=urun,
                font=("Arial", 10),
                bg="#ffffff", fg="#2c3e50",
                activebackground="#f0f0f0",
                width=18,
                command=lambda u=urun: urun_sec(u)
            )
            btn.pack(side="left", padx=5, pady=5)

def masa_degistir():
    """Masa değiştirme fonksiyonu - iyileştirilmiş"""
    temizle_orta_panel()
    eski_masa_no = secilen_masa.get()
    if eski_masa_no == 0:
        tk.Label(orta_panel, text="Önce masa seçiniz!", font=("Arial", 14), bg="#fafafa", fg="red").pack(pady=50)
        return
    
    eski_masa = tables[eski_masa_no]
    if not eski_masa["adisyon_acik"]:
        tk.Label(orta_panel, text="Seçili masada açık adisyon yok!", font=("Arial", 14), bg="#fafafa", fg="red").pack(pady=50)
        return
    
    if not eski_masa["siparisler"]:
        tk.Label(orta_panel, text="Seçili masada sipariş yok, masa değiştirilmez!", font=("Arial", 14), bg="#fafafa", fg="red").pack(pady=50)
        return

    # Başlık
    tk.Label(orta_panel, text=f"Masa {eski_masa_no} - Masa Değiştir", 
             font=("Arial", 14, "bold"), bg="#fafafa", fg="#2c3e50").pack(pady=10)

    # Ana container
    main_degistir_frame = tk.Frame(orta_panel, bg="#fafafa")
    main_degistir_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Sol taraf - mevcut masa bilgileri
    bilgi_frame = tk.Frame(main_degistir_frame, bg="#e8f4fd", bd=2, relief="ridge")
    bilgi_frame.pack(side="left", fill="both", expand=True, padx=(0,10))

    tk.Label(bilgi_frame, text=f"Masa {eski_masa_no} Bilgileri", 
             font=("Arial", 12, "bold"), bg="#e8f4fd", fg="#2c3e50").pack(pady=10)

    siparis_sayisi = len(eski_masa["siparisler"])
    toplam_adet = sum(s['adet'] for s in eski_masa["siparisler"])
    
    tk.Label(bilgi_frame, text=f"Sipariş Sayısı: {siparis_sayisi}", 
             font=("Arial", 10), bg="#e8f4fd", fg="#2c3e50").pack(pady=2)
    tk.Label(bilgi_frame, text=f"Toplam Adet: {toplam_adet}", 
             font=("Arial", 10), bg="#e8f4fd", fg="#2c3e50").pack(pady=2)
    tk.Label(bilgi_frame, text=f"Toplam Tutar: {eski_masa['toplam']} TL", 
             font=("Arial", 10, "bold"), bg="#e8f4fd", fg="#e74c3c").pack(pady=5)

    # Siparişler detayı
    tk.Label(bilgi_frame, text="Siparişler:", 
             font=("Arial", 10, "bold"), bg="#e8f4fd", fg="#2c3e50").pack(pady=(10,5))
    
    siparis_detay_frame = tk.Frame(bilgi_frame, bg="#e8f4fd")
    siparis_detay_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    for sip in eski_masa["siparisler"]:
        tk.Label(siparis_detay_frame, text=f"• {sip['adet']} x {sip['urun']} - {sip['tutar']} TL", 
                 font=("Arial", 9), bg="#e8f4fd", fg="#2c3e50", anchor="w").pack(fill="x")

    # Sağ taraf - masa seçimi
    secim_frame = tk.Frame(main_degistir_frame, bg="#fff0f0", bd=2, relief="ridge", width=300)
    secim_frame.pack(side="right", fill="y")
    secim_frame.pack_propagate(False)

    tk.Label(secim_frame, text="Yeni Masa Seç", 
             font=("Arial", 12, "bold"), bg="#fff0f0", fg="#2c3e50").pack(pady=10)

    # Seçili masa göstergesi
    secili_yeni_masa = tk.IntVar(value=0)
    secili_masa_label = tk.Label(secim_frame, text="Masa seçilmedi", 
                                font=("Arial", 10), bg="#fff0f0", fg="#7f8c8d")
    secili_masa_label.pack(pady=5)

    def yeni_masa_sec(masa_no):
        if tables[masa_no]["adisyon_acik"]:
            secili_masa_label.config(text=f"Masa {masa_no} - DOLU!", fg="red")
            degistir_btn.config(state="disabled")
            secili_yeni_masa.set(0)
        else:
            secili_masa_label.config(text=f"Masa {masa_no} - Uygun", fg="green")
            degistir_btn.config(state="normal")
            secili_yeni_masa.set(masa_no)
        
        # Tüm butonları sıfırla
        for btn in masa_btn_list:
            if btn.winfo_exists():
                btn.config(relief="raised", bd=2)
        
        # Seçili butonu vurgula
        for btn in masa_btn_list:
            if btn.winfo_exists() and btn["text"] == f"Masa {masa_no}":
                btn.config(relief="sunken", bd=3)

    # Masa butonları
    masa_btn_frame = tk.Frame(secim_frame, bg="#fff0f0")
    masa_btn_frame.pack(fill="both", expand=True, padx=10, pady=10)

    masa_btn_list = []
    for i in range(1, 21):
        if i == eski_masa_no:
            continue
        
        row = (i-1) // 4
        col = (i-1) % 4
        
        # Masa durumuna göre renk
        if tables[i]["adisyon_acik"]:
            btn_color = "#ffcccb"  # Açık kırmızı (dolu)
            btn_text_color = "#8b0000"
        else:
            btn_color = "#c8e6c9"  # Açık yeşil (boş)
            btn_text_color = "#2e7d32"
        
        btn = tk.Button(masa_btn_frame, text=f"Masa {i}", 
                       width=8, height=1, font=("Arial", 8),
                       bg=btn_color, fg=btn_text_color,
                       relief="raised", bd=2, cursor="hand2",
                       command=lambda m=i: yeni_masa_sec(m))
        btn.grid(row=row, column=col, padx=2, pady=2)
        masa_btn_list.append(btn)

    # Değiştir butonu
    degistir_btn = tk.Button(secim_frame, text="Masa Değiştir", width=20, height=2,
                            bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                            state="disabled", cursor="hand2")
    degistir_btn.pack(pady=15)

    def masa_degistir_onayli():
        yeni_masa_no = secili_yeni_masa.get()
        if yeni_masa_no == 0:
            return
        
        yeni_masa = tables[yeni_masa_no]
        
        # Masa değiştirme işlemi
        yeni_masa["adisyon_acik"] = True
        yeni_masa["siparisler"] = eski_masa["siparisler"].copy()
        yeni_masa["toplam"] = eski_masa["toplam"]
        
        # Eski masayı temizle
        eski_masa["adisyon_acik"] = False
        eski_masa["siparisler"] = []
        eski_masa["toplam"] = 0
        
        # Yeni masayı seç
        secilen_masa.set(yeni_masa_no)
        
        save_data()
        
        update_buttons()
        guncelle_secili_masa_bilgisi()
        guncelle_durum_bilgileri()
        siparisleri_goster()
        
        # Başarı mesajı göster
        temizle_orta_panel()
        tk.Label(orta_panel, text="✓ Masa Değiştirme Başarılı!", 
                 font=("Arial", 16, "bold"), bg="#fafafa", fg="green").pack(pady=30)
        tk.Label(orta_panel, text=f"Masa {eski_masa_no} → Masa {yeni_masa_no}", 
                 font=("Arial", 14), bg="#fafafa", fg="#2c3e50").pack(pady=10)
        tk.Label(orta_panel, text=f"Toplam: {yeni_masa['toplam']} TL", 
                 font=("Arial", 12), bg="#fafafa", fg="#e74c3c").pack(pady=5)

    degistir_btn.configure(command=masa_degistir_onayli)

def adisyon_ac():
    masa_no = secilen_masa.get()
    if masa_no == 0:
        messagebox.showwarning("Uyarı", "Önce masa seçiniz!")
        return
    masa = tables[masa_no]
    if masa["adisyon_acik"]:
        messagebox.showinfo("Bilgi", "Bu masada zaten açık bir adisyon var.")
        return
    masa["adisyon_acik"] = True
    masa["siparisler"] = []
    masa["toplam"] = 0
    save_data()  # EKLENEN SATIR
    update_buttons()
    guncelle_secili_masa_bilgisi()
    guncelle_durum_bilgileri()
    siparisleri_goster()
    messagebox.showinfo("Başarılı", f"Masa {masa_no} için yeni adisyon açıldı.")

def siparis_ekle():
    """Sipariş ekleme ekranı - geliştirilmiş versiyon"""
    temizle_orta_panel()
    masa_no = secilen_masa.get()
    if masa_no == 0:
        tk.Label(orta_panel, text="Lütfen bir masa seçin", font=("Arial", 14), bg="#fafafa", fg="gray").pack(pady=50)
        return

    masa = tables[masa_no]
    if not masa["adisyon_acik"]:
        masa["adisyon_acik"] = True
        masa["siparisler"] = []
        masa["toplam"] = 0
        update_buttons()
        guncelle_secili_masa_bilgisi()
        guncelle_durum_bilgileri()

    # Başlık
    tk.Label(orta_panel, text=f"Masa {masa_no} - Sipariş Ekle", 
             font=("Arial", 14, "bold"), bg="#fafafa", fg="#2c3e50").pack(pady=10)

    # Ana container
    main_siparis_frame = tk.Frame(orta_panel, bg="#fafafa")
    main_siparis_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Sol taraf - menü butonları
    menu_frame = tk.Frame(main_siparis_frame, bg="#fafafa")
    menu_frame.pack(side="left", fill="both", expand=True)

    # Sağ taraf - adet kontrolü ve ekleme
    kontrol_frame = tk.Frame(main_siparis_frame, bg="#e8f4fd", bd=2, relief="ridge", width=200)
    kontrol_frame.pack(side="right", fill="y", padx=(20,0))
    kontrol_frame.pack_propagate(False)

    # Seçili ürün ve adet kontrolü
    tk.Label(kontrol_frame, text="Seçili Ürün:", font=("Arial", 11, "bold"), 
             bg="#e8f4fd", fg="#2c3e50").pack(pady=(10,5))
    
    secili_urun_label = tk.Label(kontrol_frame, text="Ürün seçiniz", 
                                font=("Arial", 10), bg="#e8f4fd", fg="#7f8c8d")
    secili_urun_label.pack(pady=5)

    # Adet kontrolü
    tk.Label(kontrol_frame, text="Adet:", font=("Arial", 11, "bold"), 
             bg="#e8f4fd", fg="#2c3e50").pack(pady=(15,5))

    adet_frame = tk.Frame(kontrol_frame, bg="#e8f4fd")
    adet_frame.pack(pady=5)

    adet_var = tk.IntVar(value=1)
    
    def adet_azalt():
        if adet_var.get() > 1:
            adet_var.set(adet_var.get() - 1)
    
    def adet_arttir():
        if adet_var.get() < 50:
            adet_var.set(adet_var.get() + 1)

    btn_azalt = tk.Button(adet_frame, text="-", width=3, height=1,
                         bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                         command=adet_azalt)
    btn_azalt.pack(side="left", padx=2)

    adet_entry = tk.Entry(adet_frame, textvariable=adet_var, width=5, justify="center",
                         font=("Arial", 12))
    adet_entry.pack(side="left", padx=2)

    btn_arttir = tk.Button(adet_frame, text="+", width=3, height=1,
                          bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                          command=adet_arttir)
    btn_arttir.pack(side="left", padx=2)

    # Toplam tutar
    toplam_label = tk.Label(kontrol_frame, text="Toplam: 0 TL", 
                           font=("Arial", 11, "bold"), bg="#e8f4fd", fg="#e74c3c")
    toplam_label.pack(pady=(15,10))

    # Ekle butonu
    ekle_btn = tk.Button(kontrol_frame, text="Sepete Ekle", width=15, height=2,
                        bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                        state="disabled", cursor="hand2")
    ekle_btn.pack(pady=10)

    # Değişkenler
    secili_urun = {"urun": None, "fiyat": 0}

    def urun_sec(urun, fiyat):
        secili_urun["urun"] = urun
        secili_urun["fiyat"] = fiyat
        secili_urun_label.config(text=f"{urun} - {fiyat} TL")
        ekle_btn.config(state="normal")
        toplam_guncelle()
        
        # Tüm menü butonlarının rengini sıfırla
        for btn in menu_buttons:
            btn.config(relief="raised", bd=2)
        
        # Seçili butonun rengini değiştir
        for btn in menu_buttons:
            if btn["text"].split("\n")[0] == urun:
                btn.config(relief="sunken", bd=3)

    def toplam_guncelle():
        if secili_urun["urun"]:
            toplam = secili_urun["fiyat"] * adet_var.get()
            toplam_label.config(text=f"Toplam: {toplam} TL")

    def siparis_ekle_sepete():
        if not secili_urun["urun"]:
            return
        
        urun = secili_urun["urun"]
        adet = adet_var.get()
        tutar = secili_urun["fiyat"] * adet
        
        masa["siparisler"].append({"urun": urun, "adet": adet, "tutar": tutar})
        masa["toplam"] += tutar
        
        save_data()
        
        # Başarı mesajı (kısa süre göster)
        mesaj_label = tk.Label(kontrol_frame, text=f"✓ {adet} {urun} eklendi!", 
                              font=("Arial", 9), bg="#e8f4fd", fg="#27ae60")
        mesaj_label.pack(pady=5)
        kontrol_frame.after(2000, mesaj_label.destroy)  # 2 saniye sonra sil
        
        # Adet sıfırla
        adet_var.set(1)
        toplam_guncelle()
        guncelle_durum_bilgileri()
        guncelle_secili_masa_bilgisi()
        update_buttons()

    # Adet değiştiğinde toplam güncelle
    adet_var.trace("w", lambda *args: toplam_guncelle())
    ekle_btn.configure(command=siparis_ekle_sepete)

    # Menü butonları
    colors = [soft_blue, soft_green, soft_orange, soft_purple, "#ff9999", "#99ccff"]
    menu_buttons = []
    
    for i, (urun, fiyat) in enumerate(menu.items()):
        btn = tk.Button(menu_frame, text=f"{urun}\n{fiyat} TL", 
                       width=13, height=2, font=("Arial", 9, "bold"),
                       command=lambda u=urun, f=fiyat: urun_sec(u, f), 
                       bg=colors[i % len(colors)], fg="white",
                       relief="raised", bd=2, cursor="hand2")
        btn.grid(row=i//3, column=i%3, padx=8, pady=8)
        menu_buttons.append(btn)
        
def siparis_sil():
    """Sipariş silme - geliştirilmiş versiyon"""
    temizle_orta_panel()
    masa_no = secilen_masa.get()
    if masa_no == 0:
        tk.Label(orta_panel, text="Lütfen bir masa seçin", font=("Arial", 12), bg="#fafafa", fg="gray").pack(pady=40)
        return
    
    masa = tables[masa_no]
    if not masa["adisyon_acik"]:
        tk.Label(orta_panel, text="Bu masada açık adisyon yok", font=("Arial", 12), bg="#fafafa", fg="gray").pack(pady=40)
        return

    # Başlık
    tk.Label(orta_panel, text=f"Masa {masa_no} - Sipariş Sil", 
             font=("Arial", 14, "bold"), bg="#fafafa", fg="#e74c3c").pack(pady=10)

    if not masa["siparisler"]:
        tk.Label(orta_panel, text="Bu masada silinecek sipariş bulunmuyor.", 
                 bg="#fafafa", font=("Arial", 11), fg="gray").pack(pady=25)
        return

    # Ana container
    main_sil_frame = tk.Frame(orta_panel, bg="#fafafa")
    main_sil_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Sol taraf - siparişler listesi
    siparis_frame = tk.Frame(main_sil_frame, bg="#fafafa")
    siparis_frame.pack(side="left", fill="both", expand=True)

    # Sağ taraf - silme kontrolü
    kontrol_frame = tk.Frame(main_sil_frame, bg="#ffe6e6", bd=2, relief="ridge", width=200)
    kontrol_frame.pack(side="right", fill="y", padx=(20,0))
    kontrol_frame.pack_propagate(False)

    tk.Label(kontrol_frame, text="Seçili Sipariş:", font=("Arial", 11, "bold"), 
             bg="#ffe6e6", fg="#2c3e50").pack(pady=(10,5))
    
    secili_siparis_label = tk.Label(kontrol_frame, text="Sipariş seçiniz", 
                                   font=("Arial", 9), bg="#ffe6e6", fg="#7f8c8d")
    secili_siparis_label.pack(pady=5)

    # Adet kontrolü
    tk.Label(kontrol_frame, text="Silinecek Adet:", font=("Arial", 11, "bold"), 
             bg="#ffe6e6", fg="#2c3e50").pack(pady=(15,5))

    adet_frame = tk.Frame(kontrol_frame, bg="#ffe6e6")
    adet_frame.pack(pady=5)

    silinecek_adet_var = tk.IntVar(value=1)
    
    def adet_azalt():
        if silinecek_adet_var.get() > 1:
            silinecek_adet_var.set(silinecek_adet_var.get() - 1)
    
    def adet_arttir():
        max_adet = secili_siparis.get("max_adet", 1)
        if silinecek_adet_var.get() < max_adet:
            silinecek_adet_var.set(silinecek_adet_var.get() + 1)

    btn_azalt = tk.Button(adet_frame, text="-", width=3, height=1,
                         bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                         command=adet_azalt)
    btn_azalt.pack(side="left", padx=2)

    adet_entry = tk.Entry(adet_frame, textvariable=silinecek_adet_var, width=5, justify="center",
                         font=("Arial", 12))
    adet_entry.pack(side="left", padx=2)

    btn_arttir = tk.Button(adet_frame, text="+", width=3, height=1,
                          bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                          command=adet_arttir)
    btn_arttir.pack(side="left", padx=2)

    # Silinecek tutar
    silinecek_tutar_label = tk.Label(kontrol_frame, text="Silinecek: 0 TL", 
                                    font=("Arial", 11, "bold"), bg="#ffe6e6", fg="#e74c3c")
    silinecek_tutar_label.pack(pady=(15,10))

    # Sil butonu
    sil_btn = tk.Button(kontrol_frame, text="Seçili Adeti Sil", width=15, height=2,
                       bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                       state="disabled", cursor="hand2")
    sil_btn.pack(pady=10)

    # Değişkenler
    secili_siparis = {"idx": -1, "max_adet": 1, "birim_fiyat": 0}

    def siparis_sec(idx):
        if idx >= len(masa["siparisler"]):
            return
            
        siparis = masa["siparisler"][idx]
        secili_siparis["idx"] = idx
        secili_siparis["max_adet"] = siparis["adet"]
        secili_siparis["birim_fiyat"] = siparis["tutar"] // siparis["adet"]
        
        secili_siparis_label.config(text=f"{siparis['urun']}\n{siparis['adet']} adet mevcut")
        silinecek_adet_var.set(1)
        sil_btn.config(state="normal")
        silinecek_tutar_guncelle()
        
        # Tüm sipariş butonlarının rengini sıfırla
        for btn in siparis_buttons:
            btn.config(relief="raised", bd=2)
        
        # Seçili butonun rengini değiştir
        siparis_buttons[idx].config(relief="sunken", bd=3)

    def silinecek_tutar_guncelle():
        if secili_siparis["idx"] >= 0:
            tutar = secili_siparis["birim_fiyat"] * silinecek_adet_var.get()
            silinecek_tutar_label.config(text=f"Silinecek: {tutar} TL")

    def siparis_sil_onayli():
        idx = secili_siparis["idx"]
        if idx < 0 or idx >= len(masa["siparisler"]):
            return
        
        siparis = masa["siparisler"][idx]
        silinecek_adet = silinecek_adet_var.get()
        birim_fiyat = siparis["tutar"] // siparis["adet"]
        silinen_tutar = birim_fiyat * silinecek_adet
        
        if silinecek_adet == siparis["adet"]:
            # Tüm ürün siliniyor
            masa["siparisler"].pop(idx)
            mesaj = f"'{siparis['urun']}' tamamen silindi."
        else:
            # Kısmi silme
            masa["siparisler"][idx]["adet"] -= silinecek_adet
            masa["siparisler"][idx]["tutar"] -= silinen_tutar
            mesaj = f"'{siparis['urun']}' ürününden {silinecek_adet} adet silindi."
        
        masa["toplam"] -= silinen_tutar
        
        save_data()
        
        # Başarı mesajı (kısa süre göster)
        mesaj_label = tk.Label(kontrol_frame, text=f"✓ {mesaj}", 
                              font=("Arial", 8), bg="#ffe6e6", fg="#27ae60", wraplength=180)
        mesaj_label.pack(pady=5)
        kontrol_frame.after(3000, mesaj_label.destroy)  # 3 saniye sonra sil
        
        guncelle_secili_masa_bilgisi()
        guncelle_durum_bilgileri()
        update_buttons()
        siparis_sil()  # Sayfayı yenile

    # Adet değiştiğinde silinecek tutar güncelle
    silinecek_adet_var.trace("w", lambda *args: silinecek_tutar_guncelle())
    sil_btn.configure(command=siparis_sil_onayli)

    # Siparişler listesi
    tk.Label(siparis_frame, text="Silmek istediğiniz siparişe tıklayın:", 
             font=("Arial", 11), bg="#fafafa", fg="#2c3e50").pack(pady=5)

    siparis_buttons = []
    for idx, sip in enumerate(masa["siparisler"]):
        kutu = tk.Frame(siparis_frame, bg=soft_white, bd=1, relief="ridge", height=35)
        kutu.pack(fill="x", pady=2)
        kutu.pack_propagate(False)
        
        # Sipariş bilgisi
        bilgi = f"{sip['adet']} x {sip['urun']} - {sip['tutar']} TL"
        
        # Tıklanabilir buton olarak sipariş
        btn = tk.Button(kutu, text=bilgi, font=("Arial", 10), 
                       bg=soft_white, fg="#2c3e50", anchor="w",
                       relief="raised", bd=2, cursor="hand2",
                       command=lambda i=idx: siparis_sec(i))
        btn.pack(fill="both", expand=True, padx=5, pady=2)
        siparis_buttons.append(btn)

def hesap_kapat():
    masa_no = secilen_masa.get()
    if masa_no == 0:
        messagebox.showerror("Hata", "Lütfen bir masa seçin!")
        return

    masa = tables[masa_no]
    if not masa["adisyon_acik"]:
        messagebox.showerror("Hata", "Bu masa için açık bir adisyon yok.")
        return

    # Siparişleri stoktan düş ve log kaydı oluştur
    for siparis in masa["siparisler"]:
        urun = siparis["urun"]
        adet = siparis["adet"]
        if urun in stok:
            stok[urun] -= adet
            if stok[urun] < 0:
                stok[urun] = 0 # Negatif stoku önle

        log_ekle(f"Masa {masa_no} için {adet} adet {urun} satıldı ve stoktan düşüldü.")

    toplam_tutar = masa["toplam"]
    if toplam_tutar == 0:
        messagebox.showinfo("Bilgi", "Hesapta sipariş yok.")
        masa["adisyon_acik"] = False
        masa["siparisler"] = []
        masa["toplam"] = 0
        update_buttons()
        guncelle_secili_masa_bilgisi()
        guncelle_durum_bilgileri()
        save_data()
        temizle_orta_panel()
        return

    messagebox.showinfo("Hesap Kapatma", f"Masa {masa_no}'nun adisyonu kapatıldı.\nToplam: {toplam_tutar} TL")
    log_ekle(f"Masa {masa_no} adisyonu kapatıldı. Toplam satış: {toplam_tutar} TL")
    
    # Masayı sıfırla
    masa["adisyon_acik"] = False
    masa["siparisler"] = []
    masa["toplam"] = 0
    
    update_buttons()
    guncelle_secili_masa_bilgisi()
    guncelle_durum_bilgileri()
    save_data()
    temizle_orta_panel()

    # Başlık
    tk.Label(orta_panel, text=f"Masa {masa_no} - Hesap Kapat", 
             font=("Arial", 14, "bold"), bg="#fafafa", fg="#e74c3c").pack(pady=10)

    # Ana container
    main_hesap_frame = tk.Frame(orta_panel, bg="#fafafa")
    main_hesap_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Sol taraf - hesap detayları
    hesap_frame = tk.Frame(main_hesap_frame, bg="#e8f4fd", bd=2, relief="ridge")
    hesap_frame.pack(side="left", fill="both", expand=True, padx=(0,10))

    tk.Label(hesap_frame, text=f"Masa {masa_no} Hesap Detayı", 
             font=("Arial", 12, "bold"), bg="#e8f4fd", fg="#2c3e50").pack(pady=10)

    siparis_sayisi = len(masa["siparisler"])
    toplam_adet = sum(s['adet'] for s in masa["siparisler"])
    
    tk.Label(hesap_frame, text=f"Sipariş Sayısı: {siparis_sayisi}", 
             font=("Arial", 10), bg="#e8f4fd", fg="#2c3e50").pack(pady=2)
    tk.Label(hesap_frame, text=f"Toplam Adet: {toplam_adet}", 
             font=("Arial", 10), bg="#e8f4fd", fg="#2c3e50").pack(pady=2)
    
    # Toplam tutar - büyük ve belirgin
    tk.Label(hesap_frame, text=f"TOPLAM TUTAR", 
             font=("Arial", 12, "bold"), bg="#e8f4fd", fg="#2c3e50").pack(pady=(15,5))
    tk.Label(hesap_frame, text=f"{toplam} TL", 
             font=("Arial", 20, "bold"), bg="#e8f4fd", fg="#e74c3c").pack(pady=5)

    # Siparişler detayı
    tk.Label(hesap_frame, text="Siparişler:", 
             font=("Arial", 10, "bold"), bg="#e8f4fd", fg="#2c3e50").pack(pady=(15,5))
    
    # Siparişler listesi için frame
    siparis_detay_frame = tk.Frame(hesap_frame, bg="#e8f4fd")
    siparis_detay_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Scrollable frame için
    canvas = tk.Canvas(siparis_detay_frame, bg="#e8f4fd", height=200)
    scrollbar = tk.Scrollbar(siparis_detay_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#e8f4fd")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    for sip in masa["siparisler"]:
        tk.Label(scrollable_frame, text=f"• {sip['adet']} x {sip['urun']} - {sip['tutar']} TL", 
                 font=("Arial", 9), bg="#e8f4fd", fg="#2c3e50", anchor="w").pack(fill="x", pady=1)

    # Sağ taraf - ödeme seçimi
    odeme_frame = tk.Frame(main_hesap_frame, bg="#fff0f0", bd=2, relief="ridge", width=280)
    odeme_frame.pack(side="right", fill="y")
    odeme_frame.pack_propagate(False)

    tk.Label(odeme_frame, text="Ödeme Türü Seçin", 
             font=("Arial", 12, "bold"), bg="#fff0f0", fg="#2c3e50").pack(pady=15)

    # Seçili ödeme türü
    secili_odeme = tk.StringVar(value="")
    
    # Ödeme türü butonları
    odeme_turleri = [
        ("NAKİT", "#27ae60", "💵"),
        ("KART", "#3498db", "💳"),
        ("KARIŞIK", "#f39c12", "💳💵")
    ]
    
    odeme_buttons = []
    
    def odeme_sec(tur):
        secili_odeme.set(tur)
        secili_odeme_label.config(text=f"Seçili: {tur}")
        hesap_kapat_btn.config(state="normal")
        
        # Tüm butonları normal renge çevir
        for btn in odeme_buttons:
            btn.config(relief="raised", bd=2)
        
        # Seçili butonu vurgula
        for btn in odeme_buttons:
            if btn["text"].split("\n")[0] == tur:
                btn.config(relief="sunken", bd=3)

    for tur, renk, emoji in odeme_turleri:
        btn = tk.Button(odeme_frame, text=f"{tur}\n{emoji}", 
                       width=15, height=3, font=("Arial", 11, "bold"),
                       bg=renk, fg="white", relief="raised", bd=2, cursor="hand2",
                       command=lambda t=tur: odeme_sec(t))
        btn.pack(pady=8)
        odeme_buttons.append(btn)

    # Seçili ödeme göstergesi
    secili_odeme_label = tk.Label(odeme_frame, text="Ödeme türü seçiniz", 
                                 font=("Arial", 10), bg="#fff0f0", fg="#7f8c8d")
    secili_odeme_label.pack(pady=15)

    # Karışık ödeme için detay frame (başlangıçta gizli)
    karisik_frame = tk.Frame(odeme_frame, bg="#fff0f0")
    
    tk.Label(karisik_frame, text="Nakit:", font=("Arial", 9), bg="#fff0f0").pack()
    nakit_var = tk.DoubleVar()
    nakit_entry = tk.Entry(karisik_frame, textvariable=nakit_var, width=10, justify="center")
    nakit_entry.pack(pady=2)
    
    tk.Label(karisik_frame, text="Kart:", font=("Arial", 9), bg="#fff0f0").pack(pady=(5,0))
    kart_var = tk.DoubleVar()
    kart_entry = tk.Entry(karisik_frame, textvariable=kart_var, width=10, justify="center")
    kart_entry.pack(pady=2)
    
    def hesapla_karisik():
        if nakit_var.get() + kart_var.get() == toplam:
            hesap_kapat_btn.config(state="normal")
            toplam_kontrol_label.config(text="✓ Toplam doğru", fg="green")
        else:
            hesap_kapat_btn.config(state="disabled")
            toplam_kontrol_label.config(text=f"Toplam: {nakit_var.get() + kart_var.get():.2f} TL", fg="red")
    
    toplam_kontrol_label = tk.Label(karisik_frame, text="", font=("Arial", 8), bg="#fff0f0")
    toplam_kontrol_label.pack(pady=5)
    
    nakit_var.trace("w", lambda *args: hesapla_karisik())
    kart_var.trace("w", lambda *args: hesapla_karisik())
    
    # Karışık ödeme seçildiğinde frame'i göster/gizle
    def odeme_sec_updated(tur):
        secili_odeme.set(tur)
        secili_odeme_label.config(text=f"Seçili: {tur}")
        
        if tur == "KARIŞIK":
            karisik_frame.pack(pady=10)
            nakit_var.set(0)
            kart_var.set(0)
            hesap_kapat_btn.config(state="disabled")
        else:
            karisik_frame.pack_forget()
            hesap_kapat_btn.config(state="normal")
        
        # Buton vurguları
        for btn in odeme_buttons:
            btn.config(relief="raised", bd=2)
        for btn in odeme_buttons:
            if btn["text"].split("\n")[0] == tur:
                btn.config(relief="sunken", bd=3)
    
    # Buton komutlarını güncelle
    for i, (tur, renk, emoji) in enumerate(odeme_turleri):
        odeme_buttons[i].configure(command=lambda t=tur: odeme_sec_updated(t))

    # Hesap kapat butonu
    hesap_kapat_btn = tk.Button(odeme_frame, text="HESABI KAPAT", width=18, height=2,
                               bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                               state="disabled", cursor="hand2")
    hesap_kapat_btn.pack(pady=20)

    def hesap_kapat_onayli():
        global gunluk_ciro  # EKLENEN SATIR
        odeme_turu = secili_odeme.get()
        if not odeme_turu:
            return
        
        # Karışık ödeme kontrolü
        if odeme_turu == "KARIŞIK":
            nakit_miktar = nakit_var.get()
            kart_miktar = kart_var.get()
            if nakit_miktar + kart_miktar != toplam:
                messagebox.showerror("Hata", "Nakit + Kart toplamı hesap tutarına eşit değil!")
                return
            odeme_detay = f"Nakit: {nakit_miktar} TL, Kart: {kart_miktar} TL"
        else:
            odeme_detay = odeme_turu
        
        # Son onay
        result = messagebox.askyesno("Hesap Kapat", 
                                   f"Masa {masa_no} hesabını kapatmak istediğinizden emin misiniz?\n\n" +
                                   f"Toplam Tutar: {toplam} TL\n" +
                                   f"Ödeme Türü: {odeme_detay}")
        if result:
            # Ciroya ekle
            gunluk_ciro += toplam
            
            # Masayı temizle
            masa["adisyon_acik"] = False
            masa["siparisler"] = []
            masa["toplam"] = 0
            
            save_data()
            update_buttons()
            guncelle_secili_masa_bilgisi()
            guncelle_durum_bilgileri()
            temizle_orta_panel()
            
            # Başarı mesajı
            tk.Label(orta_panel, text="✓ Hesap Başarıyla Kapatıldı!", 
                     font=("Arial", 16, "bold"), bg="#fafafa", fg="green").pack(pady=30)
            tk.Label(orta_panel, text=f"Masa {masa_no}", 
                     font=("Arial", 14), bg="#fafafa", fg="#2c3e50").pack(pady=5)
            tk.Label(orta_panel, text=f"Toplam: {toplam} TL", 
                     font=("Arial", 12), bg="#fafafa", fg="#e74c3c").pack(pady=5)
            tk.Label(orta_panel, text=f"Ödeme: {odeme_detay}", 
                     font=("Arial", 12), bg="#fafafa", fg="#2c3e50").pack(pady=5)
            tk.Label(orta_panel, text=f"Günlük Ciro: {gunluk_ciro} TL", 
                     font=("Arial", 12, "bold"), bg="#fafafa", fg="#27ae60").pack(pady=10)
            
            messagebox.showinfo("Hesap Kapatıldı", 
                              f"Masa {masa_no} hesabı kapatıldı.\n" +
                              f"Toplam: {toplam} TL\n" +
                              f"Ödeme: {odeme_detay}\n" +
                              f"Günlük Ciro: {gunluk_ciro} TL")

    hesap_kapat_btn.configure(command=hesap_kapat_onayli)

# MASA GRUPLARI
masa_groups = {
    "Ön Bahçe": [1,2,3,4],
    "Ön": [5,6,7],
    "Arka": [8,9,10,11,12,13,14],
    "Arka Bahçe": [15,16,17,18,19,20]
}

masa_buttons = {}
for group_name, masalar in masa_groups.items():
    frame = tk.LabelFrame(sol_panel, text=group_name, bg="#ecf0f1", fg="#2c3e50", 
                         font=("Arial", 10, "bold"), padx=4, pady=4)
    frame.pack(pady=6, fill="x")
    
    # Masa butonlarını grid ile düzenle
    for i, m in enumerate(masalar):
        btn = tk.Button(frame, text=f"Masa {m}", width=9, height=2,  # Boyut küçültüldü
                        bg=soft_green, fg="white", font=("Arial", 8, "bold"),
                        relief="raised", bd=2, cursor="hand2",
                        command=lambda m=m: [secilen_masa.set(m), update_buttons(), 
                                           guncelle_secili_masa_bilgisi(), siparisleri_goster()])
        
        # Grup başına düzenleme
        if group_name == "Ön Bahçe":
            btn.grid(row=0, column=i, padx=2, pady=2)
        elif group_name == "Ön":
            btn.grid(row=0, column=i, padx=2, pady=2)
        elif group_name == "Arka":
            btn.grid(row=i//4, column=i%4, padx=2, pady=2)
        else:  # Arka Bahçe
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
        
        masa_buttons[m] = btn

# ALT PANEL - İŞLEM BUTONLARI
alt_panel = tk.Frame(sag_panel, bg="#ecf0f1", relief="ridge", bd=1, height=80)  # Yükseklik küçültüldü
alt_panel.pack(fill="x")
alt_panel.pack_propagate(False)

alt_colors = {
    "Adisyon Aç": soft_blue,
    "Sipariş Ekle": soft_green,
    "Sipariş Sil": soft_red,
    "Siparişleri Göster": soft_orange,
    "Hesabı Kapat": soft_purple,
    "Masa Değiştir": "#ff6b9d"
}

alt_buttons = []
button_specs = [
    ("Adisyon Aç", adisyon_ac),
    ("Sipariş Ekle", siparis_ekle),
    ("Sipariş Sil", siparis_sil),
    ("Siparişleri Göster", siparisleri_goster),
    ("Hesabı Kapat", hesap_kapat),
    ("Masa Değiştir", masa_degistir)
]

for i, (text, func) in enumerate(button_specs):
    btn = tk.Button(alt_panel, text=text, width=15, height=2,  # Boyut küçültüldü
                    bg=soft_gray, fg="white", font=("Arial", 9, "bold"),  # Font küçültüldü
                    relief="raised", bd=2, state="disabled", cursor="hand2")
    btn.grid(row=0, column=i, padx=6, pady=15)  # Padding küçültüldü
    btn.configure(command=func)
    alt_buttons.append(btn)

def update_buttons():
    masa_no = secilen_masa.get()
    
    # Alt panel butonları
    for btn in alt_buttons:
        btn_text = btn["text"]
        if btn_text == "Adisyon Aç":
            if masa_no != 0:
                btn.configure(state="normal", bg=alt_colors[btn_text])
            else:
                btn.configure(state="disabled", bg=soft_gray)
        elif btn_text == "Siparişleri Göster":
            # Siparişleri göster butonu masa seçildiğinde aktif olsun
            if masa_no != 0:
                btn.configure(state="normal", bg=alt_colors[btn_text])
            else:
                btn.configure(state="disabled", bg=soft_gray)
        else:
            # Diğer butonlar için adisyon açık olması gerekli
            if masa_no != 0 and tables[masa_no]["adisyon_acik"]:
                btn.configure(state="normal", bg=alt_colors[btn_text])
            else:
                btn.configure(state="disabled", bg=soft_gray)
    
    # Masa butonları
    for m_no, btn in masa_buttons.items():
        if masa_no == m_no:
            btn.configure(bg=highlight_color, fg="black")
        else:
            if tables[m_no]["adisyon_acik"]:
                btn.configure(bg=soft_red, fg="white")
            else:
                btn.configure(bg=soft_green, fg="white")
                

update_buttons()
auto_save()


if __name__ == "__main__":
    auto_save()
    root.mainloop()

print("Kullanıcı girişi başarılı - Ana program başlatılıyor...")