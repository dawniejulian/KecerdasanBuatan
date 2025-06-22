# main.py

import pandas as pd

df = pd.read_excel('restoran.xlsx') 
# Fungsi Membership Segitiga
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    else:
        return 0

# Fuzzifikasi kualitas servis
def fuzzify_service(service):
    buruk = triangular(service, 1, 25, 50)
    sedang = triangular(service, 30, 55, 80)
    bagus = triangular(service, 60, 80, 100)
    return {'buruk': buruk, 'sedang': sedang, 'bagus': bagus}

# Fuzzifikasi harga
def fuzzify_price(price):
    murah = triangular(price, 25000, 30000, 35000)
    sedang = triangular(price, 30000, 37500, 45000)
    mahal = triangular(price, 40000, 47500, 55000)
    return {'murah': murah, 'sedang': sedang, 'mahal': mahal}

# Inferensi berdasarkan aturan
# Return: dictionary {"layak": derajat, "tidak_layak": derajat}
def inference(service_fuzzy, price_fuzzy):
    rules = []

    # Definisi aturan
    rules.append(('tidak_layak', min(service_fuzzy['buruk'], price_fuzzy['murah'])))
    rules.append(('tidak_layak', min(service_fuzzy['buruk'], price_fuzzy['sedang'])))
    rules.append(('tidak_layak', min(service_fuzzy['buruk'], price_fuzzy['mahal'])))

    rules.append(('layak', min(service_fuzzy['sedang'], price_fuzzy['murah'])))
    rules.append(('layak', min(service_fuzzy['sedang'], price_fuzzy['sedang'])))
    rules.append(('tidak_layak', min(service_fuzzy['sedang'], price_fuzzy['mahal'])))

    rules.append(('layak', min(service_fuzzy['bagus'], price_fuzzy['murah'])))
    rules.append(('layak', min(service_fuzzy['bagus'], price_fuzzy['sedang'])))
    rules.append(('layak', min(service_fuzzy['bagus'], price_fuzzy['mahal'])))

    # Agregasi maksimal
    layak = max([value for label, value in rules if label == 'layak'])
    tidak_layak = max([value for label, value in rules if label == 'tidak_layak'])

    return {'layak': layak, 'tidak_layak': tidak_layak}

# Defuzzifikasi dengan metode centroid sederhana
def defuzzify(inference_result):
    # Layak: pusat di 75, Tidak Layak: pusat di 25
    numerator = (inference_result['layak'] * 75) + (inference_result['tidak_layak'] * 25)
    denominator = inference_result['layak'] + inference_result['tidak_layak']
    if denominator == 0:
        return 0
    return numerator / denominator

# Program utama
def main():
    # Membaca data restoran.xlsx
    df = pd.read_excel('restoran.xlsx')

    results = []

    # Proses semua data
    for index, row in df.iterrows():
        service = row['Pelayanan']
        price = row['harga']
        
        service_fuzzy = fuzzify_service(service)
        price_fuzzy = fuzzify_price(price)
        inference_result = inference(service_fuzzy, price_fuzzy)
        score = defuzzify(inference_result)

        results.append({
            'ID': index + 1,
            'Pelayanan': service,
            'harga': price,
            'Skor': score
        })

    # Membuat DataFrame hasil
    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values(by='Skor', ascending=False).drop_duplicates(subset=['Skor'], keep='first')

    #memilih 5 restoran terbaik setelah penghapusan duplikas
    result_df = result_df.head(4)
    # Menyimpan ke file Excel
    result_df.to_excel('peringkat.xlsx', index=False)
    print("Proses selesai! Hasil disimpan di 'peringkat.xlsx'")

if __name__ == '__main__':
    main()
