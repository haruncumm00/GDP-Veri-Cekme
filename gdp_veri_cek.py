import pandas as pd
import wbgapi as wb

ulkeler = ['TUR', 'USA', 'DEU', 'IND']
gostergeler = {'NY.GDP.MKTP.CD': 'GDP (USD)', 'IS.AIR.PSGR': 'Air Passengers Carried'}

print("Dünya Bankası'ndan veriler çekiliyor, lütfen bekleyin...")
df = wb.data.DataFrame(list(gostergeler.keys()), ulkeler, time=range(1960, 2023), numericTimeKeys=True)

# 1. AŞAMA: Yatay gelen yılları dikey formata (melt) çeviriyoruz
df = df.reset_index()
df = df.melt(id_vars=['economy', 'series'], var_name='Year', value_name='Value')

# 2. AŞAMA: GDP ve Yolcu verilerini ayrı sütunlara (pivot) ayırıyoruz
df = df.pivot(index=['economy', 'Year'], columns='series', values='Value').reset_index()

# 3. AŞAMA: İsimleri ve sütunları senin tablonun yapısına uyduruyoruz
ulke_isimleri = {'TUR': 'Turkiye', 'USA': 'United States', 'DEU': 'Germany', 'IND': 'India'}
df['economy'] = df['economy'].map(ulke_isimleri)

df = df.rename(columns={
    'economy': 'Country',
    'NY.GDP.MKTP.CD': 'GDP (USD)',
    'IS.AIR.PSGR': 'Air Passengers Carried'
})

df = df[['Country', 'Year', 'GDP (USD)', 'Air Passengers Carried']]
df = df.sort_values(by=['Country', 'Year']).reset_index(drop=True)

# İstatistikleri ekrana yazdırma
print("\n--- Veri Seti İstatistiksel Özeti ---")
print(df[['GDP (USD)', 'Air Passengers Carried']].describe())
print(f"\nSkewness (Çarpıklık):\n{df[['GDP (USD)', 'Air Passengers Carried']].skew()}")
print(f"\nKurtosis (Basıklık):\n{df[['GDP (USD)', 'Air Passengers Carried']].kurtosis()}\n")

# Senin istediğin gibi formatlama (1,359,123.77 şeklinde)
df['GDP (USD)'] = df['GDP (USD)'].apply(lambda x: f"{x:,.2f}" if pd.notnull(x) else x)
df['Air Passengers Carried'] = df['Air Passengers Carried'].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else x)

# --- DEĞİŞEN KISIM: CSV YERİNE DOĞRUDAN EXCEL OLARAK KAYDEDİYORUZ ---
dosya_adi = "math202_project_kusursuz_tablo.xlsx"
df.to_excel(dosya_adi, index=False)

print(f"İşlem tamamlandı! Veriler sütunlara ayrılmış saf Excel formatında '{dosya_adi}' olarak kaydedildi.")
# Veri çekme işlemleri eklendi