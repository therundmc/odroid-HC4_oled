import os
import psutil
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont, ImageDraw, Image


# Initialize OLED device
serial = i2c(port=0, address=0x3C)
device = ssd1306(serial, rotate=2)


FONT_PATH = "/usr/local/FreePixel.ttf"


def draw_line_graph(values, width, height):
    """Draw a line graph on a PIL image."""
    # Create a new image with a black background
    img = Image.new('1', (width, height), color=0)
    draw = ImageDraw.Draw(img)

    # Determine the x and y scaling factors to fit the values within the image size
    if len(values) < 2 or max(values) == 0:
        return None
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


def draw_stat(stat_func, label):
    """Draw a stat (CPU usage, RAM usage, temperature) on the OLED display."""
    values = []
    start_time = time.time()

    while time.time() - start_time < 10:
        value = stat_func()
        if value is not None:
            values.append(value)

        with canvas(device) as draw:
            font_percent = ImageFont.truetype(FONT_PATH, 40)
            font_label = ImageFont.truetype(FONT_PATH, 14)
            label_width, _ = draw.textbbox((0, 0), label, font=font_label)[2:]
            draw.text((0, 50), label, font=font_label, fill=1)
            draw.text((label_width + 1, 10), f"{value:.1f}%", font=font_percent, fill=1)

            if len(values) > 1:
                # Draw line graph of values
                graph_width = 100
                graph_height = 10
                graph_img = draw_line_graph(values, graph_width, graph_height)
                if graph_img is not None:
                    draw.bitmap((33, 54), graph_img, fill=1)


def get_cpu_percent():
    """Get the CPU usage percentage."""
    return psutil.cpu_percent(interval=1)


def get_ram_percent():
    """Get the RAM usage percentage."""
    svmem = psutil.virtual_memory()
    return svmem.percent


def get_temperature():
    """Get the CPU temperature in degrees Celsius."""
    temps = psutil.sensors_temperatures().get('coretemp', [])
    if temps:
        return temps[0].current


if __name__ == "__main__":
    try:
        while True:
            draw_stat(get_cpu_percent, "CPU")
            draw_stat(get_ram_percent, "RAM")
            draw_stat(get_temperature, "TMP")
    except KeyboardInterrupt:
        pass
