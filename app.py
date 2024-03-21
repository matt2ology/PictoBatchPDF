import os
import PIL
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(image_folder, output_pdf):
    try:
        images = []
        for filename in sorted(os.listdir(image_folder), key=lambda x: os.path.getctime(os.path.join(image_folder, x))):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                images.append(os.path.join(image_folder, filename))

        if not images:
            raise ValueError("No image files found in the specified folder.")

        # Define size for each image in PDF
        page_width, page_height = letter
        margin = 20
        num_images_per_row = 3
        num_images_per_col = 2
        img_width = int((page_width - (2 * margin)) / num_images_per_row)
        img_height = int((page_height - (2 * margin)) / num_images_per_col)

        # Initialize PDF canvas
        c = canvas.Canvas(output_pdf, pagesize=letter)

        x_offset = margin
        y_offset = page_height - margin

        for i, img_path in enumerate(images):
            if i % (num_images_per_row * num_images_per_col) == 0 and i != 0:
                c.showPage()
                x_offset = margin
                y_offset = page_height - margin

            img = PIL.Image.open(img_path)
            # Inside the loop where images are processed
            resized_img = img.copy()  # Create a copy of the image object
            # Resize the copied image
            resized_img.thumbnail((img_width, img_height),
                                  PIL.Image.Resampling.LANCZOS)
            c.drawInlineImage(resized_img, x_offset, y_offset - img_height,
                              resized_img.width, resized_img.height,
                              preserveAspectRatio=True)

            x_offset += img_width
            if x_offset + img_width > page_width - margin:
                x_offset = margin
                y_offset -= img_height

        c.save()
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    # Provide the path to the image folder and output PDF file
    # image_folder = "path_to_image_folder"
    image_folder = "test_images"
    output_pdf = "output.pdf"
    create_pdf(image_folder, output_pdf)
