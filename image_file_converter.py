"""
- Converts image to specific file format.
- Convert size is optional.
- Converted image file name is added with converted size
"""
import json
from dataclasses import dataclass
from PIL import Image

@dataclass
class ConvertImage:
    """image converter"""
    file_path: str
    convert_format: str
    convert_sizes: list = []
    image_destination: str = ''


    def image_file_name(self, width, height):
        """changes file extension for new image extension"""
        file_name = self.file_path.split('/')[-1]
        split_file_name = file_name.split('.')
        join_name = '.'.join(split_file_name[:-1])
        if width:
            file_name = f"{join_name}-{width}x{height}.{self.convert_format}"
            return file_name

        file_name = f"{join_name}.{self.convert_format}"
        print(f"filename: {file_name}")
        return file_name


    def saved_file_destination(self, file_name):
        """build saved file destination"""
        image_dest = self.image_destination
        if image_dest:
            if image_dest[-1] != '/':
                image_dest = image_dest + '/'
        destination = image_dest + file_name
        print(f"save path: {destination}")
        return destination


    def resize_image(self, image):
        """
        - Resize image
        - Image resized by its longest side. The shortest side is based
          on the percentage of the resized image.
           - math
                - ex. original size = width, height = 1260 x 720
                - convert_sizes = [200]
                - if width > height
                    - width = 200
                    - height = (200 / 1260) x 100
                    - height = 15.87%
                    - height = 15.87% x 720 or 0.1587 x 720
                    - height = 114.264  # for simplification we will round of the result
                    - height = 114
                    widht, height = 200 x 114
                - if width < heigh just reverse the process
        """
        orig_width, orig_height = image.size
        print(orig_width, orig_height)
        image_resizes = self.convert_sizes
        for size in image_resizes:
            print(f"resize image to {size}...")
            if orig_width > orig_height:
                resize_height_percentage = size / orig_width
                resize_height = round(resize_height_percentage * orig_height)
                resized_image = image.resize((size, resize_height))
                file_name_with_size = self.image_file_name(size, resize_height)
            else:
                resize_width_percentage = size / orig_height
                resize_width = round(resize_width_percentage * orig_width)
                resized_image = image.resize((resize_width, size))
                file_name_with_size = self.image_file_name(resize_width, size)

            print(file_name_with_size)
            save_converted_image = self.saved_file_destination(file_name_with_size)
            self.save_image(resized_image, save_converted_image)


    def save_image(self, image, save_path):
        """save image"""
        image_format = f'{self.convert_format.upper()}'
        image.save(save_path, image_format)

        print("file saved...")
        message = {}
        message["success"] = True
        message["message"] = f"Image converted to {self.convert_format.upper()}"
        print(" ")
        return json.dumps(message)


    def convert_image(self):
        """convert image"""
        print("open image...")
        image = Image.open(self.file_path).convert("RGB")
        if self.convert_sizes:
            return self.resize_image(image)

        print("convert image to {}...".format(self.convert_format))
        file_name = self.image_file_name('', '')
        save_path = self.saved_file_destination(file_name)
        return self.save_image(image, save_path)


    def check_input_format(self):
        """check if file format is valid"""
        valid_formats = ['webp', 'jpg', 'png', 'jpeg']
        if self.convert_format in valid_formats:
            return self.convert_image()

        message = {}
        message["success"] = True
        message["message"] = "Please input a valid format to convert; webp, jpg, jpeg, png."
        return json.dumps(message)


def main():
    """
    image_path = image file location
    image_format = desired file format ('webp', 'jpg', 'png', 'jpeg')
    convert_size = list of desired resize image, default size is orginal image size
    file_dest = save converted image file destination
    """

    image_path = '/path/to/image/image.jpg'
    image_format = 'jpeg'
    convert_sizes = [200, 400]
    save_path = '/save/path/'
    convert = ConvertImage(image_path, image_format, convert_sizes, save_path)
    convert.check_input_format()


if __name__ == "__main__":
    main()
