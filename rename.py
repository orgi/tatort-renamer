from bs4 import BeautifulSoup
import os
import re
import difflib

url = '/home/mac/documents/Tatort - Aired Order - All Seasons - TheTVDB.com.htm'
episodes_data = []
episode_names = []

with open(url) as html:
    soup = BeautifulSoup(html, 'html.parser')

for episode_data in soup.find_all('h4', class_='list-group-item-heading'):
    # print(episode_data)
    episode_number = ''
    if episode_data.span is not None:
        episode_number = episode_data.span.text.strip()
    if episode_data.small is not None:
        episode_number = episode_data.small.text.strip()
    episode_file_name = episode_data.a.text.strip()
    episode_name = re.sub(r"[^ ]* - \d\d - (.*)", r"\1", episode_file_name)
    print(f"{episode_number}: {episode_file_name}")
    
    episode_names.append(episode_name)
    episodes_data.append((episode_number, episode_file_name,))


tatort_folder = '/mnt/TV Shows/Tatort'

def similarity(word, pattern):
    return difflib.SequenceMatcher(a=word.lower(), b=pattern.lower()).ratio()

def find_episode_data(episode_name):
    ratio = 0.0
    index = None
    for i in range(0, len(episode_names)):
        current_ratio = similarity(episode_names[i], episode_name)
        if (current_ratio > ratio):
            ratio = current_ratio
            index = i

    if index is not None:
        return episodes_data[index]
    else:
        return None

for episode_old_name in os.listdir(tatort_folder):
    filename = os.fsdecode(episode_old_name)
    if (filename.endswith('.mkv')):
        # print(f"found: {filename}")
        episode_name = re.sub(r"Tatort[_ ]*(.*)\.mkv", r"\1", filename)

        episode_data = find_episode_data(episode_name)
        if episode_data is not None:
            # print(f"{episode_name}: {episode_data}")
            new_file_name = f"Tatort - {episode_data[0]} - {episode_data[1]}.mkv"
            print(f"rename: {filename} -> {new_file_name}")
        else:
            print(f"Error: Episode data not found for {episode_name}")

# print(soup.prettify)