
import random
import math

# ================================
# PARAMETER GA
# ================================
JUMLAH_POPULASI = 30
PANJANG_KROMOSOM = 20  # 10 bit untuk x1 dan 10 bit untuk x2
MAKS_GENERASI = 100
PROBABILITAS_CROSSOVER = 0.8
PROBABILITAS_MUTASI = 0.05

# ================================
# INISIALISASI POPULASI
# ================================
def inisialisasi_populasi():
    populasi = []
    for _ in range(JUMLAH_POPULASI):
        kromosom = ''.join(random.choice('01') for _ in range(PANJANG_KROMOSOM))
        populasi.append(kromosom)
    return populasi

# ================================
# DEKODE KROMOSOM KE X1 DAN X2
# ================================
def decode_kromosom(kromosom):
    bagian_x1 = kromosom[:10]
    bagian_x2 = kromosom[10:]
    nilai_x1 = int(bagian_x1, 2)
    nilai_x2 = int(bagian_x2, 2)
    x1 = -10 + (nilai_x1 / 1023) * 20
    x2 = -10 + (nilai_x2 / 1023) * 20
    return x1, x2

# ================================
# HITUNG NILAI FITNESS
# ================================
def fungsi_objektif(x1, x2):
    try:
        return - (math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) +
                  0.75 * math.exp(1 - math.sqrt(x1**2)))
    except:
        return float('inf')

# ================================
# SELEKSI ORANGTUA: Turnamen
# ================================
def seleksi_turnamen(populasi, fitnesses):
    kandidat = random.sample(list(zip(populasi, fitnesses)), 2)
    kandidat.sort(key=lambda x: x[1])
    return kandidat[0][0]

# ================================
# CROSSOVER 1 TITIK
# ================================
def crossover(parent1, parent2):
    if random.random() < PROBABILITAS_CROSSOVER:
        titik = random.randint(1, PANJANG_KROMOSOM - 1)
        anak1 = parent1[:titik] + parent2[titik:]
        anak2 = parent2[:titik] + parent1[titik:]
        return anak1, anak2
    else:
        return parent1, parent2

# ================================
# MUTASI BIT FLIP
# ================================
def mutasi(kromosom):
    krom_baru = ''
    for bit in kromosom:
        if random.random() < PROBABILITAS_MUTASI:
            krom_baru += '0' if bit == '1' else '1'
        else:
            krom_baru += bit
    return krom_baru

# ================================
# GENERASI BARU DENGAN ELITISME
# ================================
def pergantian_generasi(populasi, fitnesses):
    populasi_baru = []
    indeks_terbaik = fitnesses.index(min(fitnesses))
    populasi_baru.append(populasi[indeks_terbaik])
    while len(populasi_baru) < JUMLAH_POPULASI:
        parent1 = seleksi_turnamen(populasi, fitnesses)
        parent2 = seleksi_turnamen(populasi, fitnesses)
        anak1, anak2 = crossover(parent1, parent2)
        anak1 = mutasi(anak1)
        anak2 = mutasi(anak2)
        populasi_baru.extend([anak1, anak2])
    return populasi_baru[:JUMLAH_POPULASI]

# ================================
# PROGRAM UTAMA
# ================================
if __name__ == "__main__":
    populasi = inisialisasi_populasi()
    for generasi in range(MAKS_GENERASI):
        fitnesses = [fungsi_objektif(*decode_kromosom(krom)) for krom in populasi]
        populasi = pergantian_generasi(populasi, fitnesses)

    fitnesses = [fungsi_objektif(*decode_kromosom(krom)) for krom in populasi]
    terbaik_idx = fitnesses.index(min(fitnesses))
    terbaik_kromosom = populasi[terbaik_idx]
    x1, x2 = decode_kromosom(terbaik_kromosom)
    nilai_fungsi = fungsi_objektif(x1, x2)

    print("Kromosom terbaik :", terbaik_kromosom)
    print("x1 =", x1)
    print("x2 =", x2)
    print("Nilai minimum fungsi =", nilai_fungsi)
