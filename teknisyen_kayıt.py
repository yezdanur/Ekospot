import streamlit as st
import pandas as pd
import os

# Sunucu üzerinde çalışacağı için sadece dosya adını yazıyoruz
DOSYA_ADI = "ekospot_kayit.xlsx"

# 1. DEĞİŞİKLİK: Sekme adı "Teknisyen Kaydı" oldu
st.set_page_config(page_title="Ekospot Teknisyen Kaydı", layout="centered")

# 2. DEĞİŞİKLİK: Sayfa ana başlığı "Teknisyen Kaydı" oldu
st.title("Ekospot Yarışması Teknisyenleri")

if not os.path.exists(DOSYA_ADI):
    bos_tablo = pd.DataFrame(columns=["Grup Adı", "Ad", "Soyad", "Telefon"])
    bos_tablo.to_excel(DOSYA_ADI, index=False)

df = pd.read_excel(DOSYA_ADI, dtype=str)
df = df.fillna("")

# 3. DEĞİŞİKLİK: Alt başlık teknisyene uyarlandı
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

# YÖNETİCİ GİRİŞİ (Sadece Senin Göreceğin Gizli İndirme Butonu)
st.divider()
st.caption("Yönetici Girişi")
# Buraya girilen karakterler *** şeklinde gizli görünür
sifre = st.text_input("Excel tablosunu indirmek için şifreyi girin:", type="password")

# Şifreyi buradan istediğin gibi değiştirebilirsin
if sifre == "Ekospotseslendirme2026":
    st.success("Şifre doğru! Excel dosyasını aşağıdan indirebilirsiniz.")
    with open(DOSYA_ADI, "rb") as file:
        st.download_button(
            label="📥 Güncel Teknisyen Tablosunu İndir",
            data=file,
            file_name="ekospot_teknisyenler.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
