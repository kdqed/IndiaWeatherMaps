from PIL import Image
import requests
from io import BytesIO
from datetime import datetime
import os
import telegram

import config

os.makedirs("outputs", exist_ok=True)
outfile_name = "outputs/" + datetime.now().isoformat() + ".png"

r = requests.get("https://mausam.imd.gov.in/Satellite/3Dasiasec_ir1.jpg")
infrared = Image.open(BytesIO(r.content))

r = requests.get("https://mausam.imd.gov.in/Satellite/3Dasiasec_wv.jpg")
water_vapor = Image.open(BytesIO(r.content))

r = requests.get("https://mausam.imd.gov.in/Satellite/3Dasiasec_vis.jpg")
visible = Image.open(BytesIO(r.content))

width, height = infrared.size
image = Image.new("RGB", (width,height))
img_handle = image.load()
for x in range(width):
  for y in range(height):
    r = int(sum(infrared.getpixel((x,y)))/3)
    g = int(sum(visible.getpixel((x,y)))/3)
    b = int(sum(water_vapor.getpixel((x,y)))/3)
    img_handle[x,y] = (r,g,b)

image.save(outfile_name)

bot = telegram.Bot(token=config.BOT_TOKEN)
with open(outfile_name,"rb") as f:
  bot.send_photo(chat_id="@IndiaWeatherMaps", photo=f, timeout=200)
  f.close()
  
    
