import sys  ##### argümanları almak için import edildi.
from PyQt5 import QtWidgets  ## PyQt5 in Widgetleri impport edildi.
from PyQt5.QtWidgets import *  ## uzun uzun QtWidget yazmamak için böyle yazıldı. değişkene de atanabilirdi
from Urun_Ekle import *  ##Ui.py deki tüm argümanlat import edildi.

uygulama = QApplication(
    sys.argv
)  # uygulama içindeki tüm argümanları al uygulama adı ver.
pencere = (
    QMainWindow()
)  # Mainwindow içindeki tüm fonksiyonları al. pencere değişkenine ata
ui = Ui_MainWindow()  # urun_ekle de bulunan tüm class içindekileri ui. diye adlandır.
ui.setupUi(pencere)  # ui. kodunun pencere olarak açılmasını sağlar.
pencere.show()  # pencereyi açar. ama kapatılması gerekir.

#########################################################
###### VERİTABANI İŞLEMLERİ ####################################
################################################################
import sqlite3  # veritabanı kütüphanesini yükler

baglanti = sqlite3.connect(
    "urunler.db"
)  # sqlite3 bağlan urunler.db veritabanını oluştur.
# adına da başlantı de.
islem = baglanti.cursor()  # bağlantıda mause gibi kullanır.
baglanti.commit()  # bağlantı da ne yaparsak veritabanına kaydeder.

table = islem.execute(
    "create table if not exists urun(urunKodu int, urunAdi text, birimFiyat int, stokMiktari int, urunAciklamasi text, marka text, kategori text)"
)  # burada create table if not exists urun aynı isimde varsa ekleme yoksa ekle , urunKodu int gibi kategori ekle
baglanti.commit()  # # bağlantı da ne yaparsak veritabanına kaydeder.


def tablo_ozellik():
    ui.tablowidget.clear()  # butona basıp veya fonksiyonu çağırdığımda önce tabloyu temizle.
    ui.tablowidget.setHorizontalHeaderLabels(
        (
            "Ürün\nKodu",
            "Ürün\nAdı",
            "Birim\nFiyatı",
            "Stok\nMiktarı",
            "Ürün\nAçıklaması",
            "Markası",
            "Kategori",
        )
    )
    # setHorizontalHeaderLabels yatay olan tablonun başlıklarını yaz. "xxx"
    ui.tablowidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


def kayit_ekle():  # Kayıt Ekleme işini bu fonksiyonda metod da yapacağız.
    UrunKodu = int(
        ui.lne_urunkodu.text()
    )  # urun kodu line editine ne yazdıysan o. int e çevirdim. veritabanında öyle
    UrunAdi = ui.lne_urunadi.text()  # aynısı string olduğu için .dp de çevirme yok
    BirimFiyat = int(ui.lne_birimfiyat.text())
    StokMiktari = int(ui.lne_stokmiktari.text())
    UrunAciklama = (
        ui.txt_urunaciklamas.toPlainText()
    )  # Qtext Edit te text değil bu kullanılır.
    Marka = ui.cmb_marka.currentText()  # şu an seçili olan text i seçiyorum demek.
    Kategori = ui.cmb_kategori.currentText()  # combobox da bu seçilir.

    try:
        ekle = "insert into urun(urunKodu, urunAdi, birimFiyat, stokMiktari, urunAciklamasi, marka, kategori)values (?,?,?,?,?,?,?) "
        # yukarıda insert into ekle demek. urun tablo ismi ve sırasıyla içindekilerde kategoriler.
        # values değerleri gir demek. soru işareti ise henüz gelmedi gelince gir demek.
        islem.execute(
            ekle,
            (UrunKodu, UrunAdi, BirimFiyat, StokMiktari, UrunAciklama, Marka, Kategori),
        )
        # ekle, de yukarıdaki kategorilere ekle demek. neti parantez içindekileri gelince demek
        baglanti.commit()  # bağlantıyı kur ve ekle.sqlite3.connect(urunler.db) :)
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 1000)
        ui.lne_urunkodu.clear()
        ui.lne_urunadi.clear()
        ui.lne_birimfiyat.clear()
        ui.lne_stokmiktari.clear()
        kayit_listele()
        # arayüzden statusbar aşağıdaki çağırır ve orada 1 saniye mesajı yazdır eklendikten sonra
    except Exception as hata:  # hata alırsan hata isminde bir hata çıkar ve
        ui.statusbar.showMessage(
            "Kayıt Eklenmedi Hata var. İşte Hata Kodu:" + str(hata)
        )


def kayit_listele():  # burada tüm kayıtları listeleteceğiz.
    tablo_ozellik()
    sorgu = "select * from urun"  # karışıklık olmasın komutu buraya yaz. komutları böyle kullanmak güzel
    islem.execute(sorgu)  # sorgu komutunu gönder.

    for indexSatir, KayitNumarasi in enumerate(
        islem
    ):  # islem içinde indexSatir indeksi KayitNumarasi kaydın değerini döndürür.
        for indexSutun, Kayit_Sutun in enumerate(
            KayitNumarasi
        ):  # döndürülen değerin kaydından sütunu ve sutun değerini döndürür
            ui.tablowidget.setItem(
                indexSatir, indexSutun, QTableWidgetItem(str(Kayit_Sutun))
            )
            # tabloya setItem komuru ile önce satır indeksi sonra sütun indeksi ve QTableWidgetItem(str(Kayit_Sutun) ile degerler girilir.
            # kayıtnumarası sürekli döndüğü için sütun girilir sadece. UNUTMA !!!


def kategoriyegorelistele():
    listelenecekKategori = ui.cmb_kategoriyegorelistele.currentText()
    # listelenecekKategori değişkenine dediğim ki bu listelenecek olan combobox un içinde seçili olan kategoridir.
    # bozdolabı ise buzdolabı , telefon ise telefondur.
    ui.tablowidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # tabloyu içindekilere sığdırır.
    ui.tablowidget.setHorizontalHeaderLabels(
        (
            "Ürün\nKodu",
            "Ürün\nAdı",
            "Birim\nFiyatı",
            "Stok\nMiktarı",
            "Ürün\nAçıklaması",
            "Markası",
            "Kategori",
        )
    )
    # Tablonun Başlıklarını oluşturur.
    sorgu = "select * from urun where kategori = ?"  # sorgu kodumuz tüm urun tablosundan kategorisi ? olanı listele
    islem.execute(sorgu, (listelenecekKategori,))
    # islem yap. önce sorgutu yaz. hangisi istelenecek yani soru işareini paranteze yazıyoruz.
    tablo_ozellik()
    for indexSatir, KayitNumarasi in enumerate(
        islem
    ):  # islem içinde indexSatir indeksi KayitNumarasi kaydın değerini döndürür.
        for indexSutun, Kayit_Sutun in enumerate(
            KayitNumarasi
        ):  # döndürülen değerin kaydından sütunu ve sutun değerini döndürür
            ui.tablowidget.setItem(
                indexSatir, indexSutun, QTableWidgetItem(str(Kayit_Sutun))
            )
            # tabloya setItem komuru ile önce satır indeksi sonra sütun indeksi ve QTableWidgetItem(str(Kayit_Sutun) ile degerler girilir.
            # kayıtnumarası sürekli döndüğü için sütun girilir sadece. UNUTMA !!!


def kayit_sil():
    sil_mesaj = QMessageBox.question(
        pencere,
        "Silme İşlemi",
        "Kaydı Silmek İstediğinize Emin Misiniz?",
        QMessageBox.Yes | QMessageBox.No,
    )
    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tablowidget.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()

        sorgu = "delete from urun where urunKodu = ?"
        try:
            islem.execute(sorgu, (silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla Silindi",2000)
            kayit_listele()

        except Exception as hata:
            ui.statusbar.showMessage("Kayıt Silinirken Hata Çıktı===" + str(hata),2000)
            print(hata)
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi",2000)

def kayit_guncelle():
    guncelle_mesaj = QMessageBox.question(
        pencere,
        "Güncelleme İşlemi",
        "Kaydı Güncellemek İstediğinizden Emin Misiniz?",
        QMessageBox.Yes | QMessageBox.No,
    )
    if guncelle_mesaj == QMessageBox.Yes:
        try:
            UrunKodu = int(ui.lne_urunkodu.text())  # urun kodu line editine ne yazdıysan o. int e çevirdim. veritabanında öyle
            UrunAdi = ui.lne_urunadi.text()  # aynısı string olduğu için .dp de çevirme yok
            BirimFiyat = ui.lne_birimfiyat.text()
            StokMiktari = ui.lne_stokmiktari.text()
            UrunAciklama = ui.txt_urunaciklamas.toPlainText()  # Qtext Edit te text değil bu kullanılır.
            Marka = ui.cmb_marka.currentText()  # şu an seçili olan text i seçiyorum demek.
            Kategori = ui.cmb_kategori.currentText()  # combobox da bu seçilir.
            
            if UrunAdi=="" and BirimFiyat=="" and StokMiktari=="" and UrunAciklama=="" and Marka=="":
                islem.execute("update urun set kategori = ? where urunKodu =?",(Kategori,UrunKodu))
                baglanti.commit()
                kayit_listele()

            elif UrunAdi=="" and BirimFiyat=="" and StokMiktari=="" and UrunAciklama==""  and Kategori=="":
                islem.execute("update urun set marka = ? where urunKodu =?",(Marka,UrunKodu))
                baglanti.commit()
                kayit_listele()

            elif UrunAdi=="" and BirimFiyat=="" and StokMiktari==""  and Marka=="" and Kategori=="":
                islem.execute("update urun set urunAciklamasi = ? where urunKodu =?",(UrunAciklama,UrunKodu))
                baglanti.commit()
                kayit_listele()

            elif UrunAdi=="" and BirimFiyat==""  and UrunAciklama=="" and Marka=="" and Kategori=="":
                islem.execute("update urun set stokMiktari = ? where urunKodu =?",(StokMiktari,UrunKodu))
                baglanti.commit()
                kayit_listele()
            elif UrunAdi==""  and StokMiktari=="" and UrunAciklama=="" and Marka=="" and Kategori=="":
                islem.execute("update urun set birimFiyat = ? where urunKodu =?",(BirimFiyat,UrunKodu))
                baglanti.commit()
                kayit_listele()
            elif  BirimFiyat=="" and StokMiktari=="" and UrunAciklama=="" and Marka=="" and Kategori=="":
                islem.execute("update urun set urunAdi = ? where urunKodu =?",(UrunAdi,UrunKodu))
                baglanti.commit()
                kayit_listele()
            else:
                islem.execute("update urun set urunAdi = ?,birimFiyat = ?, stokMiktari=?, urunAciklamasi =?, marka=?,kategori=? where urunKodu =?",(UrunAdi,BirimFiyat,StokMiktari,UrunAciklama,Marka,Kategori,UrunKodu)) 
                baglanti.commit()
                kayit_listele()
                ui.statusbar.showMessage("Kayıt Başarıyla Güncellendi",2000)
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Günncelemede Hata ==>"+str(error),2000)
            QMessageBox.information(pencere,"Dikkat","Ürün Kodu Boş Bırakılamaz")
            print(error)
    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi.",2000)


####################################################
####### BUTONLAR #########################
#################################################
kayit_ekle_butonu = ui.btn_urunEkle.clicked.connect(kayit_ekle)
### değişkene zevkine atadım. diyor ki urun ekle butonuna tıkladığında def kayit_ekle fonksiyonunu
## bul ona başlan ve oradaki işlemi yap.
kayit_listele_butonu = ui.btn_urun_listele.clicked.connect(kayit_listele)
# kayıt listele butonuna tıkladığında tabloyu listeler fonksiyonu çağırır.
kategoriyegorelistele_butonu = ui.btn_kategoriyegore_listele.clicked.connect(
    kategoriyegorelistele
)
# kategriye göre listeleyecek.
kayit_sil_butonu = ui.btn_urunsil.clicked.connect(kayit_sil)
kayit_guncelle_butonu =ui.btn_urunguncelle.clicked.connect(kayit_guncelle)
 

#########################################################┌
####### TABLO AYARLARI ###############
tablo_ozellik()


sys.exit(uygulama.exec_())  # arayüzü çarpıdan kapatır. bu olmazsa sürekli açılır sayfa
