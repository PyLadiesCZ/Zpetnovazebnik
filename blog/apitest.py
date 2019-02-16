import json
import requests


def get_course_data(course_api_url):
    course_page = requests.get(course_api_url)
    course_page.raise_for_status()
    course_data = course_page.json()
    for session in course_data["course"]["sessions"]:
        if "time" in session:
            title = session["title"]
            published_date = session["time"]["start"]
            print(title, published_date)
    return title, published_date


ostrava = 'https://naucse.python.cz/v0/2019/pyladies-ostrava-jaro.json'
get_course_data(ostrava)
