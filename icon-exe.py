import subprocess
from PIL import Image, ImageChops
import random
import os
import argparse
import string

def add_alpha_channel(image, color=(255, 255, 255)):
    if image.mode == "RGB":
        # 创建一个具有透明通道的新图像
        alpha_img = Image.new("L", image.size, 255)
        image = Image.merge("RGBA", (image, alpha_img))

        # 将背景色变为透明
        bg = Image.new("RGBA", image.size, color + (255,))
        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return image.crop(bbox)
    return image

def modify_icon_color(input_file, output_file, max_color_change):
    # 读取.ico文件
    img = Image.open(input_file)

    # 获取图像的RGB数据，并添加透明通道
    pixels = img.convert("RGBA")
    pixels = add_alpha_channel(pixels)

    # 保存原始图标尺寸信息
    original_sizes = img.info.get("sizes")

    # 遍历每个像素点
    for y in range(pixels.height):
        for x in range(pixels.width):
            r, g, b, a = pixels.getpixel((x, y))

            # 随机修改RGB颜色
            r_change = random.randint(-max_color_change, max_color_change)
            g_change = random.randint(-max_color_change, max_color_change)
            b_change = random.randint(-max_color_change, max_color_change)

            r = max(0, min(255, r + r_change))
            g = max(0, min(255, g + g_change))
            b = max(0, min(255, b + b_change))

            # 更新像素值
            pixels.putpixel((x, y), (r, g, b, a))
            


    # 保存修改后的图像为.ico文件，并保留原始图标尺寸信息
    pixels.save(output_file, format="ICO", sizes=original_sizes, append_images=[Image.new("RGBA", (1, 1), (0, 0, 0, 0))])
    # 添加随机字节以生成不同的哈希值
    with open(output_file, "ab") as f:
        f.write(os.urandom(random.randint(500, 1024)))


def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + ".ico"

def add_icon_to_exe(icon_file, exe_file, output_file):
    command = f'ResourceHacker -open "{exe_file}" -save "{output_file}" -action addskip -res "{icon_file}" -mask ICONGROUP,MAINICON,'
    subprocess.run(command, shell=True)
'''
def generate_random_version():
    # 生成随机版本号，格式为 X.Y.Z.W
    return f"{random.randint(2, 9)}.{random.randint(2, 9)}.{random.randint(2, 9)}.{random.randint(2, 9)}"

def add_version_info(exe_file):
    # 使用rcedit工具为exe文件添加版本信息
    file_version = generate_random_version()
    product_version = generate_random_version()

    command = f'rcedit "{exe_file}" --set-file-version "{file_version}" --set-product-version "{product_version}"'
    subprocess.run(command, shell=True)
'''
def generate_icons(input_icon_file, num_icons, max_color_change,inputfile):
    exe_file = inputfile
    generated_icon_files = []

    # 创建output文件夹
    if not os.path.exists("output"):
        os.makedirs("output")

    for i in range(num_icons):
        output_icon_file = generate_random_filename()
        modify_icon_color(input_icon_file, output_icon_file, max_color_change)
        output_exe_file = f"output/out_{i+1}.exe"  # 将生成的exe文件放入output文件夹
        add_icon_to_exe(output_icon_file, exe_file, output_exe_file)
        #add_version_info(output_exe_file)  # 为每个生成的exe文件添加版本信息

        # 将生成的图标文件名添加到列表中
        generated_icon_files.append(output_icon_file)
        print(f"生成第 {i+1} 个图标并添加到 {output_exe_file}")

    # 删除生成的.ico文件
    for icon_file in generated_icon_files:
        os.remove(icon_file)

def logo():
    logo='''
Author:pant0m & Hyyrent v 1.3
    '''
    return logo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="修改ICO文件的颜色。")
    parser.add_argument("-f", "--file", dest="input_icon_file", required=True, help="输入ICO文件。")
    parser.add_argument("-n", "--number", dest="num_icons", type=int, default=5, help="要生成的图标数量。")
    parser.add_argument("-maxc", "--maxcolorchange", dest="max_color_change", type=int, default=8, help="最大颜色变化范围。")
    parser.add_argument("-i", "--inputfile", dest="inputfile", required=True, help="输入目标PE文件。")
    args = parser.parse_args()
    print(logo())

    # 使用我们定义的函数生成图标并添加到test.exe中
    generate_icons(args.input_icon_file, args.num_icons, args.max_color_change, args.inputfile)
