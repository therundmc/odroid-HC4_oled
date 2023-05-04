import os
import psutil
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont, ImageDraw, Image

serial = i2c(port=0, address=0x3C)
device = ssd1306(serial, rotate=2)

def draw_line_graph(values, width, height):
    # Create a new image with a black background
    img = Image.new('1', (width, height), color=0)
    draw = ImageDraw.Draw(img)

    # Determine the x and y scaling factors to fit the values within the image size
    if (len(values) - 1 == 0):
        return
    if (max(values) == 0):
        return
    x_scale = width / (len(values) - 1)
    y_scale = height / max(values)

    # Draw the line graph by connecting the dots
    for i in range(len(values) - 1):
        x1 = i * x_scale
        y1 = height - (values[i] * y_scale)
        x2 = (i + 1) * x_scale
        y2 = height - (values[i + 1] * y_scale)
        draw.line((x1, y1, x2, y2), fill=1)

    return img

def draw_cpu():
    cpu_values = []
    start_time = time.time()
    while time.time() - start_time < 10:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_values.append(cpu_percent)
        with canvas(device) as draw:
            font_percent = ImageFont.truetype('/usr/local/FreePixel.ttf', 40)
            font_label = ImageFont.truetype('/usr/local/FreePixel.ttf', 14)
            label = "CPU"
            label_width, _ = draw.textbbox((0, 0), label, font=font_label)[2:]
            draw.text((0, 50), label, font=font_label, fill=1)
            draw.text((label_width, 10), f"{cpu_percent}%", font=font_percent, fill=1)

            if len(cpu_values) > 1:
                # Draw line graph of CPU values
                graph_width = 95
                graph_height = 10
                graph_img = draw_line_graph(cpu_values, graph_width, graph_height)
                draw.bitmap((33, 54), graph_img, fill=1)     


def draw_ram():
    ram_values = []
    start_time = time.time()    
    while time.time() - start_time < 10:
        svmem = psutil.virtual_memory()
        ram_used = svmem.used/(1024*1024)
        ram_total = svmem.total/(1024*1024)
        ram_percent = svmem.percent
        ram_values.append(ram_percent)
        with canvas(device) as draw:
            font_percent = ImageFont.truetype('/usr/local/FreePixel.ttf', 40)
            font_label = ImageFont.truetype('/usr/local/FreePixel.ttf', 14)
            label = "RAM"
            label_width, _ = draw.textbbox((0, 0), label, font=font_label)[2:]
            draw.text((0, 50), label, font=font_label, fill=1)
            draw.text((label_width + 1, 10), f"{ram_percent}%", font=font_percent, fill=1)

            if len(ram_values) > 1:
                # Draw line graph of CPU values
                graph_width = 100
                graph_height = 10
                graph_img = draw_line_graph(ram_values, graph_width, graph_height)
                draw.bitmap((33, 54), graph_img, fill=1)

def draw_temp():
    temp_values = []
    start_time = time.time()
    while time.time() - start_time < 10:
        temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        temp_values.append(temp)
        with canvas(device) as draw:
            font_percent = ImageFont.truetype('/usr/local/FreePixel.ttf', 40)
            font_label = ImageFont.truetype('/usr/local/FreePixel.ttf', 14)
            label = "TMP"
            label_width, _ = draw.textbbox((0, 0), label, font=font_label)[2:]
            draw.text((0, 50), label, font=font_label, fill=1)
            draw.text((label_width, 10), f"{temp}C", font=font_percent, fill=1)

            if len(temp_values) > 1:
                # Draw line graph of temperature values
                graph_width = 100
                graph_height = 10
                graph_img = draw_line_graph(temp_values, graph_width, graph_height)
                draw.bitmap((33, 54), graph_img, fill=1)


if __name__ == "__main__":
    try:
        while True:
            draw_cpu()
            draw_ram()
            draw_temp()
    except KeyboardInterrupt:
        pass
