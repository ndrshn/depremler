# 2003-2022 Arasında Olan Depremler

Bu küçük uygulama Kandilli Rasathanesi'nin sitesindeki deprem arşivini (XML dosyalarını) çekip (yıllara göre ayırarak) JSON dosyalarına dönüştürür.

### Veri Formatı

```json
{
  "01": [
    {
      "date": "2003.01.01 22:15:31",
      "location": "EGE DENiZi",
      "lat": 38.5515,
      "lng": 25.4177,
      "mag": 3.4,
      "depth": 7.8
    },
    ...
  ],
  "02": [...]
}
```

### Amaç

Var olan bilgileri eğitimsel ve akademik çalışmalar için daha kolay kullanılabilir şekile dönüştürmek.

### Lisans

Tüm bilgiler T.C. Boğaziçi Üniversitesi Kandilli Rasathanesi ve Deprem Araştırma Enstitüsü'ne aittir.

[Kaynak](http://www.koeri.boun.edu.tr/scripts/lst9.asp)

# Earhquakes Between 2003-2022 in Türkiye

This small application pulls the earthquake data (XML files) from the web site of Kandilli Observatory and converts them into JSON files.

### Data Format

```json
{
  "01": [
    {
      "date": "2003.01.01 22:15:31",
      "location": "EGE DENiZi",
      "lat": 38.5515,
      "lng": 25.4177,
      "mag": 3.4,
      "depth": 7.8
    },
    ...
  ],
  "02": [...]
}
```

### Purpose

To convert existing information to more easily available ways for educational and academic studies.

### Licence

All Information belongs to Kandilli Observatory and Earthquake Research Institute of Boğaziçi University.

[Source](http://www.koeri.boun.edu.tr/scripts/lasteq.asp)
