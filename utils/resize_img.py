import os
from PIL import Image
from constants import *

def resize_images_in_folder(input_folder, output_folder, new_size):
    # Sprawdź, czy folder wyjściowy istnieje, jeśli nie, utwórz go
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iteruj przez pliki w folderze wejściowym
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Pomijaj, jeśli to nie jest plik graficzny
        if not os.path.isfile(input_path) or not any(input_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
            continue

        # Wczytaj obraz i zmniejsz do kwadratu
        resize_to_square(input_path, output_path, new_size)

def resize_to_square(input_path, output_path, new_size):
    # Wczytaj obraz
    original_image = Image.open(input_path)

    # Ustal długość najkrótszego boku
    min_side = min(original_image.size)

    # Stwórz kwadratowy obraz
    square_image = original_image.crop((0, 0, min_side, min_side))

    # Zmień rozmiar obrazu
    resized_image = square_image.resize((new_size, new_size))

    # Zapisz zmniejszony obraz
    resized_image.save(output_path)

if __name__ == "__main__":
    input_folder = "C:/Users/Darek/Desktop/Studia/TO/PacBraun/assets/images"
    output_folder = "C:/Users/Darek/Desktop/Studia/TO/PacBraun/assets/images_cropped"
    new_size = GRID_SIZE

    resize_images_in_folder(input_folder, output_folder, new_size)

    print(f"Wszystkie obrazy zostały zmniejszone do rozmiarów: {new_size}x{new_size}")
