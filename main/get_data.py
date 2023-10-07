
import requests
from bs4 import BeautifulSoup
import json
import wikipedia
import re


def get_info(keyword="", type="", url="", contenturl="", img_url=""):

    SOLAR_SYSTEM_PLANETS = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    is_solar_sys_planet = keyword.capitalize() in SOLAR_SYSTEM_PLANETS

    if url == "":
        # new_keyword = keyword.title() + "_(" + str(type.title()) + ")"
        # URL = "https://en.wikipedia.org/wiki/" + new_keyword
        # CONTENT_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&exlimit=1&explaintext=1&formatversion=2&format=json&titles="
        # content_url = CONTENT_URL + new_keyword
        # response = requests.get(URL)
        # print(URL)
        # if response.status_code != 200:
        #     new_keyword = keyword.title().replace(" ", "_")
        #     URL = "https://en.wikipedia.org/wiki/" + new_keyword
        #     CONTENT_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&exlimit=1&explaintext=1&formatversion=2&format=json&titles="
        #     content_url = CONTENT_URL + new_keyword.title()
        #     response = requests.get(URL)
        #     print(URL)
        #     if response.status_code != 200:
        #         URL = "https://en.wikipedia.org/wiki/" + keyword.title()
        #     print(URL)
        try:
            new_keyword = str(keyword).title() + "(" + str(type) + ")"
            temp_url = wikipedia.page(new_keyword).url
            res = requests.get(temp_url)
            if res.status_code != 200:
                temp_url = wikipedia.page(keyword.title()).url
                res = requests.get(temp_url)
                if res.status_code == 200:
                    URL = temp_url
                    content_url = keyword.title()
            else:
                URL = temp_url
                content_url = temp_url.split("/")[-1]
        except:
            pass
    else:
        URL = url
        if contenturl:
            content_url = contenturl
        else:
            content_url =  keyword.title()
            try:
                x = wikipedia.page(content_url).url
            except:
                content_url = str(keyword).title() + "(" + str(type) + ")"
                pass

    TABLE_CLASS = "infobox"
    cleaned_data = {}

    if URL:
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                cleaned_data["page_url"] = URL

                soup = BeautifulSoup(response.text, "html.parser")
                table = soup.find('table', {"class" : TABLE_CLASS})

                # Getting image
                if img_url:
                    cleaned_data["img_url"] = img_url
                else:
                    try:
                        image = table.find("td", {"class" : "infobox-image"})
                        t = image.findChildren()
                        img_url = t[1].get("src")
                        cleaned_data["img_url"] = img_url
                    except:
                        try:
                            image = table.find_all("a", {"class" : "image"})
                            t = image[1].findChildren()
                            img_url = t[0].get("src")
                            cleaned_data["img_url"] = img_url
                        except:
                            try:
                                image = table.find_all("a", {"class" : "image"})
                                t = image[0].findChildren()
                                img_url = t[0].get("src")
                                cleaned_data["img_url"] = img_url
                            except:
                                pass

                # Getting Heading
                heading = soup.find("h1", {"class": "firstHeading"})
                heading = heading.text
                cleaned_data["Heading"] = heading

                # Getting Content
                # response = requests.get(content_url)
                # data = response.json()
                # content = data["query"]["pages"][0]["extract"]
                try:
                    content = wikipedia.page(content_url).content.split("==")[0]
                    cleaned_data["content_url"] = content_url
                except:
                    CONTENT_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&exlimit=1&explaintext=1&formatversion=2&format=json&titles="+content_url
                    response = requests.get(CONTENT_URL)
                    data = response.json()
                    content = data["query"]["pages"][0]["extract"]
                if len(content) > 40:
                    content = re.sub(r"== .+ ==", "", content)
                    cleaned_data["content"] = content
                    cleaned_data["content_url"] = content_url

                # Getting table information
                temp = table.findChildren("tbody", recursive=False)
                x = temp[0].findChildren("tr", recursive=False)

                table_data = {}
                for child in x:
                    tem = child.findChildren(recursive=False)
                    if len(tem) == 2:
                        key = re.sub("\[.+\]", "", str(tem[0].text))
                        value = re.sub("\[.+\]", "", str(tem[1].text))
                        if key and value and key != "SIMBAD":
                            table_data[key] = value
                cleaned_data["table_data"] = table_data

                
                # images_url = []
                # try:
                #     # images = soup.find_all("img", {"class": "thumbimage"})
                #     # captopns = soup.find_all("div", {"class": "thumbcaption"})

                #     # for i in range(len(images)):
                #     #     images_url.append({"url":images[i]["src"], "caption": captopns[i].text})
                #     block = soup.find_all("div", {"class": "thumbinner"})
    
                #     for blk in block:
                #         images = blk.find_all("img")
                #         captions = blk.find_all("div", {"class": "thumbcaption"})
                #         images_url.append({"url":images[0]["src"],"caption":captions[0].text})
                # except:
                #     pass
                # cleaned_data["images"] = images_url

                # Getting surface temperature
                if is_solar_sys_planet:
                    url = "https://planets-by-api-ninjas.p.rapidapi.com/v1/planets"
                    querystring = {"name": keyword.capitalize()}
                    headers = {
                        "X-RapidAPI-Host": "planets-by-api-ninjas.p.rapidapi.com",
                        "X-RapidAPI-Key": "dad6ddf7ffmsh093816ecd635b17p161856jsn13a01988ee7a"
                    }
                    response = requests.request("GET", url, headers=headers, params=querystring)
                    data = json.loads(response.text)[0]
                    average_surface_temp = data["temperature"]
                    cleaned_data["table_data"]["Average Temperature"] = str(average_surface_temp) + " Kelvin"
            else:
                print(response.status_code)
                print(URL)
        except Exception as e:
            print(e)
    else:
        pass
    return cleaned_data



# def get_Models():
#     # end=2406
#     i=2340
#     content = []
#     while i < 2345:
#         url = "https://solarsystem.nasa.gov/resources/" + str(i)
#         res = requests.get(url)
#         if res.status_code == 200:
#             soup = BeautifulSoup(res.text, "html.parser")
#             title = soup.find("h1", {"class": "article_title"})
#             caption_container = soup.find("div", {"class": "wysiwyg_content"})
#             caption = caption_container.findChildren("p", recursive=False)
#             caption = caption[0].text
#             # print(title.text)
#             if "3D Model" in title.text:
#                 link = soup.find("pre", {"class":"wrapped embed_code"})
#                 raw_name = title.text.split(" ")[:-2]
#                 name = " ".join(raw_name).removeprefix("\n")
#                 model_url = link.text.removesuffix("\n")
#                 content.append([name, model_url, caption])
#         i += 1
#     return content
