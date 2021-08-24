import requests
from facebook_scraper import get_posts
import os

files = os.listdir(os.getcwd())

for item in files:
    if not any([item.endswith(".py"), item.endswith(".txt")]):
        os.remove(os.path.join(os.getcwd(), item))
with open('downloaded.txt') as f:
    downloded = f.readlines()
    downloded = [d.strip() for d in downloded]
posts = get_posts('682047416009944')
for post in posts:
    url_link = post.get('video', None)
    post_id = post.get('post_id')
    if post_id in downloded:
        print(f'{post_id} Already used')
        continue
    video_name = post.get('text', None) if post.get('text', None) else post_id
    print(f'{video_name} Downloading....')
    if url_link and isinstance(url_link, str):
        r = requests.get(url_link)
        with open(video_name, 'wb') as f:
            f.write(r.content)
        with open('downloaded.txt', "a") as f:
            f.write(post_id)
            f.write('\n')

