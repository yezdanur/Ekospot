import streamlit as st
import pandas as pd
import os

DOSYA_ADI = "ekospot_kayit.xlsx"

st.set_page_config(page_title="Ekospot Teknisyen Kaydı", layout="centered")
st.title("Ekospot Yarışması Teknisyen Kaydı")

if not os.path.exists(DOSYA_ADI):
    bos_tablo = pd.DataFrame(columns=["Grup Adı", "Ad", "Soyad", "Telefon"])
    bos_tablo.to_excel(DOSYA_ADI, index=False)

df = pd.read_excel(DOSYA_ADI, dtype=str)
df = df.fillna("")

# 1. KAYIT FORMU
st.write("### Lütfen Teknisyen Bilgilerinizi Girin")
with st.form("kayit_formu", clear_on_submit=True):
    grup_adi = st.text_input("Grup Adınız")
    ad = st.text_input("Teknisyenin Adı")
    soyad = st.text_input("Teknisyenin Soyadı")
    telefon = st.text_input("Teknisyenin Telefon Numarası")
    
    kaydet = st.form_submit_button("Bilgilerimi Kaydet")
    
    if kaydet:
        if grup_adi and ad and soyad and telefon:
            yeni_veri = pd.DataFrame({
                "Grup Adı": [grup_adi], 
                "Ad": [ad], 
                "Soyad": [soyad], 
                "Telefon": [telefon]
            })
            
            df = pd.concat([df, yeni_veri], ignore_index=True)
            df.to_excel(DOSYA_ADI, index=False)
            
            st.success("Teknisyen bilgileri başarıyla kaydedildi!")
        else:
            st.error("Lütfen Grup Adı, Ad, Soyad ve Telefon alanlarının hepsini doldurun!")

# 2. YÖNETİCİ PANELİ (İndirme ve Geri Yükleme)
st.divider()
st.caption("Yönetici Girişi")
sifre = st.text_input("Yönetici panelini açmak için şifreyi girin:", type="password")

if sifre == "Yezda123":
    st.success("Şifre doğru! Yönetici paneline hoş geldiniz.")
    
    # İndirme Butonu
    with open(DOSYA_ADI, "rb") as file:
        st.download_button(
            label="📥 Güncel Teknisyen Tablosunu İndir",
            data=file,
            file_name="ekospot_teknisyenler.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    st.write("---")
    st.write("#### 📤 Düzenlenmiş Excel'i Geri Yükle")
    st.info("Eğer bilgisayarınıza indirdiğiniz dosyada değişiklik yaptıysanız, yeni halini buraya yükleyerek sitedeki verileri güncelleyebilirsiniz.")
    
    # Yükleme Alanı
    yuklenen_dosya = st.file_uploader("Değiştirilmiş Excel dosyasını seçin", type=["xlsx"])
    
    if yuklenen_dosya is not None:
        # Yüklenen dosyayı eski dosyanın üzerine yaz
        with open(DOSYA_ADI, "wb") as f:
            f.write(yuklenen_dosya.getbuffer())
        st.success("Yeni Excel dosyası başarıyla sisteme yüklendi! Lütfen sayfayı yenileyin.")
