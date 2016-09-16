import urllib.request
import urllib.parse
import http.cookiejar
import re
import ast
import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, PageBreak, PageTemplate, Frame
import reportlab

BID = '12221386'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
base_url = 'http://114.212.7.104:8181'

IS_PIC_NAME_ALPHA_SORTED = True


def request_book(BID):
    prepare = urllib.request.Request(url=base_url, method='GET')
    opener.open(prepare)
    params = {
        'BID': BID,
        'ReadMode': 0,
        'pdfread': 0,
        'displaystyle': 0
    }
    request = urllib.request.Request(
        url=base_url + '/getbookread?' + urllib.parse.urlencode(params), method='GET')
    response = opener.open(request)
    res = urllib.parse.unquote(response.read().decode('utf-8'))
    return base_url + res


def get_book(url):
    requset = urllib.request.Request(url=url)
    response = opener.open(requset)
    html = response.read().decode('utf-8')
    pic_base_url = re.findall(r"var str='(.*?)'", html)[0]
    main_start_page = re.findall(r'spage\s*=\s*(\d+)', html)[0]
    main_end_page = re.findall(r'epage\s*=\s*(\d+)', html)[0]

    pages = re.findall(r'pages\s*:\s*(\[.*\])', html)[0]
    pages = pages.replace('spage', main_start_page)
    pages = pages.replace('epage', main_end_page)
    pages = ast.literal_eval(pages)
    book_info = {
        'pic_base_url': pic_base_url,
        'pages': pages,
        'pages_info': ["cov", "bok", "leg", "fow", "!", "", "att", "cov"]
    }
    return book_info


def download_book(book_info):
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    pic_base_url = book_info['pic_base_url']
    os.mkdir(BID)
    for index, pages_cat in enumerate(book_info['pages']):
        cat = book_info['pages_info'][index]
        cat_alpha = alpha[index]
        for page in range(pages_cat[0], pages_cat[1] + 1):
            pic_name = cat + str(page).zfill(6 - len(cat)) + '.jpg'
            url = pic_base_url + pic_name
            pic_save_name = pic_name
            if IS_PIC_NAME_ALPHA_SORTED:
                pic_save_name = cat_alpha + \
                    str(page).zfill(6 - len(cat_alpha)) + '.jpg'
            urllib.request.urlretrieve(url, BID + '/' + pic_save_name)
            # print(url)


def restore_image_extention(dir):
    entries = os.scandir(dir)
    for entry in entries:
        path = entry.path
        im = Image.open(path)
        real_format = im.format
        im.close()
        os.rename(path, os.path.splitext(path)[0] + '.' + real_format.lower())


def convert_to_pdf(dir):
    width, height = A4
    story = []
    entries = os.scandir(dir)
    for entry in entries:
        path = entry.path
        story.append(reportlab.platypus.Image(path, width, height))
        story.append(PageBreak())
    doc = SimpleDocTemplate("out.pdf", pagesize=A4)
    template = PageTemplate(
        'Later', [Frame(0, 0, width, height, 0, 0, 0, 0, id='F1')])
    doc.addPageTemplates(template)
    doc.build(story)


# book_url = request_book(BID)
# book_info = get_book(book_url)
# download_book(book_info)
# restore_image_extention('12221386')
convert_to_pdf('12221386')
