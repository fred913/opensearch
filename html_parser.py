import re


def re_get_url_list(html):
    exp = r"((https?):\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:\/~\+#]*[\w\-\@?^=%&\/~\+#])?)"
    return [i[0] for i in re.findall(exp, html, re.IGNORECASE)]
