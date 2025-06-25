# Program Naive Bayes sederhana untuk prediksi kelulusan mahasiswa
# Dibuat oleh: Dawnie Julian Nugroho & Mohammad Fathurrohman
# Tidak menggunakan library ML seperti sklearn (sesuai aturan tugas)

# Data training: [IPK, Kehadiran, MK_Tidak_Lulus, Label]
data = [
    [3.2, 90, 0, 'Ya'],
    [2.4, 75, 2, 'Tidak'],
    [3.5, 95, 0, 'Ya'],
    [2.8, 60, 3, 'Tidak'],
    [3.7, 85, 0, 'Ya'],
    [2.5, 70, 2, 'Tidak'],
    [3.0, 80, 1, 'Ya'],
    [2.2, 65, 3, 'Tidak']
]

# Fungsi untuk menghitung mean dari fitur
def mean(numbers):
    return sum(numbers) / float(len(numbers))

# Fungsi untuk menghitung variance (diperlukan untuk distribusi Gaussian)
def variance(numbers, mean_val):
    return sum([(x - mean_val)**2 for x in numbers]) / float(len(numbers))

# Fungsi untuk menghitung probabilitas Gaussian
def gaussian_prob(x, mean, var):
    import math
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * var)))
    return (1 / (math.sqrt(2 * math.pi * var))) * exponent

# Fungsi untuk memisahkan data berdasarkan kelas
def separate_by_class(dataset):
    separated = {}
    for row in dataset:
        vector = row[:-1]  # fitur
        class_value = row[-1]
        if class_value not in separated:
            separated[class_value] = []
        separated[class_value].append(vector)
    return separated

# Fungsi untuk menghitung statistik (mean dan var) untuk tiap fitur per kelas
def summarize_by_class(dataset):
    separated = separate_by_class(dataset)
    summaries = {}
    for class_value, rows in separated.items():
        summaries[class_value] = [(mean(col), variance(col, mean(col)))
                                  for col in zip(*rows)]
    return summaries

# Fungsi untuk menghitung probabilitas dari input terhadap setiap kelas
def calculate_class_probabilities(summaries, input_vector):
    probabilities = {}
    for class_value, class_summaries in summaries.items():
        probabilities[class_value] = 1
        for i in range(len(class_summaries)):
            mean_val, var_val = class_summaries[i]
            x = input_vector[i]
            probabilities[class_value] *= gaussian_prob(x, mean_val, var_val)
    return probabilities

# Fungsi prediksi kelas dari input baru
def predict(summaries, input_vector):
    probs = calculate_class_probabilities(summaries, input_vector)
    return max(probs, key=probs.get)

# Training model
summaries = summarize_by_class(data)

# Input baru untuk prediksi
# Format: [IPK, Kehadiran, MK_Tidak_Lulus]
new_data = [
    [3.1, 88, 0],
    [2.3, 60, 3]
]

# Prediksi dan output
print("=== Hasil Prediksi ===")
for i, item in enumerate(new_data):
    result = predict(summaries, item)
    print(f"Data {i+1}: {item} => Prediksi: {result}")
