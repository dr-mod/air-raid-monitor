import os
import xml.etree.ElementTree as ET
import io
from collections import Counter

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image, ImageDraw, ImageFont
from observer import Observer

try:
    from waveshare_epd import epd2in13_V2
except ImportError:
    pass

SCREEN_HEIGHT = 122
SCREEN_WIDTH = 250

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), 'Monaco.ttf'), 11)


class Eink(Observer):

    def __init__(self, observable):
        super().__init__(observable=observable)
        self.epd = self._init_display()
        self.screen_image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.screen_draw = ImageDraw.Draw(self.screen_image)

    @staticmethod
    def _init_display():
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        return epd

    def update(self, data):
        self.form_image(data, self.screen_draw, self.screen_image)
        screen_image_rotated = self.screen_image.rotate(180)
        self.epd.display(self.epd.getbuffer(screen_image_rotated))

    def close(self):
        epd2in13_V2.epdconfig.module_exit()

    def form_image(self, regions, screen_draw, image):
        def pos(x, y):
            side = 14
            return [(x, y), (x + side, y + side)]

        screen_draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="#ffffff")

        if not regions:
            self.connection_lost_text(screen_draw)
            return

        map = self.generate_map(regions)
        image.paste(map, (SCREEN_WIDTH - 182, 0))
        self.text(screen_draw)
        self.legend(image, pos, regions, screen_draw)

    def legend(self, image, pos, regions, screen_draw):
        tmp = Image.new('RGB', (15, 15), "#FFFFFF")
        ImageDraw.Draw(tmp).rounded_rectangle(pos(0, 0), 3, fill="#FF0000", outline="#000000")
        tmp = tmp.convert('1', dither=True)
        counter = Counter(regions.values())
        screen_draw.rounded_rectangle(pos(1, 106), 3, fill="#FFFFFF", outline="#000000")
        screen_draw.text((20, 108), "nothing - %d" % counter[None], font=FONT_SMALL)
        image.paste(tmp, (1, 90))
        screen_draw.text((20, 92), "partial - %d" % counter['partial'], font=FONT_SMALL)
        screen_draw.rounded_rectangle(pos(1, 74), 3, fill="#000000")
        screen_draw.text((20, 76), "full - %d" % counter['full'], font=FONT_SMALL)

    def text(self, screen_draw):
        screen_draw.text((6, 4), "Air raid", font=FONT_SMALL)
        screen_draw.text((2, 16), "sirens in", font=FONT_SMALL)
        screen_draw.text((2, 28), " Ukraine", font=FONT_SMALL)

    def connection_lost_text(self, screen_draw):
        screen_draw.text((79, 56), 'NO CONNECTION', font=FONT_SMALL)

    @staticmethod
    def render_svg(_svg, _scale):
        drawing = svg2rlg(io.BytesIO(bytes(_svg, 'utf-8')))
        return renderPM.drawToPIL(drawing)

    def generate_map(self, regions):
        tree = ET.parse(os.path.join(os.path.dirname(__file__), 'ua.svg'))
        for region in regions:
            elements = tree.findall(f'.//*[@name="{region}"]')
            for element in elements:
                if regions[region] == "full":
                    element.set("fill", "#000000")
                elif regions[region] == "partial":
                    element.set("fill", "#FF0000")
                elif regions[region] == "no_data":
                    element.set("fill", "#AA0000")
        xmlstr = ET.tostring(tree.getroot(), encoding='utf8', method='xml').decode("utf-8")
        img = Eink.render_svg(xmlstr, 1)
        img = img.convert('1', dither=True)
        img = img.resize((182, 122))
        return img

    def show_all(self):
        elements = self.tree.findall(".//*[@name]")
        for element in elements:
            print(element.get("name"))
