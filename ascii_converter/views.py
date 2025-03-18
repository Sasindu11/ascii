from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image


def home(request):
    return render(request, 'ascii_converter/home.html')


def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        # Convert the image to ASCII art
        ascii_art = convert_image_to_ascii(f'media/{filename}')

        return render(request, 'ascii_converter/home.html',
                      {'uploaded_file_url': uploaded_file_url, 'ascii_art': ascii_art})
    return render(request, 'ascii_converter/home.html')


def convert_image_to_ascii(image_path, new_width=100):
    # Load the image
    image = Image.open(image_path)

    # Resize image while maintaining aspect ratio
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    image = image.resize((new_width, new_height))

    # Convert the image to grayscale
    image = image.convert('L')

    # Define the ASCII characters for the conversion
    ascii_chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
    pixels = image.getdata()

    # Map pixels to ASCII characters
    ascii_str = ''.join([ascii_chars[pixel // 25] for pixel in pixels])

    # Break the string into lines
    ascii_str_len = len(ascii_str)
    ascii_art = [ascii_str[index: index + new_width] for index in range(0, ascii_str_len, new_width)]

    return "\n".join(ascii_art)
