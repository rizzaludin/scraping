import requests
import json
import csv
import time

# Ganti post_id sesuai video target
post_id = '7169910833240100123'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': '*/*',
    'Referer': f'https://www.tiktok.com/video/{post_id}'
}

comments = []
cursor = 0
max_comments = 1000

while len(comments) < max_comments:
    url = f'https://www.tiktok.com/api/comment/list/?aid=1988&count=50&cursor={cursor}&aweme_id={post_id}'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Gagal mengambil data. Status: {response.status_code}")
        break
    
    data = response.json()
    comment_data = data.get('comments', [])

    for comment in comment_data:
        comments.append({
            'comment_id': comment.get('cid'),
            'username': comment.get('user', {}).get('unique_id'),
            'text': comment.get('text'),
            'likes': comment.get('digg_count'),
            'timestamp': comment.get('create_time')
        })
    
    print(f"✅ Komentar dikumpulkan: {len(comments)}")
    
    if not data.get('has_more'):
        break

    cursor = data.get('cursor', 0)
    time.sleep(1)

# Simpan ke CSV
with open(f'tiktok_comments_{post_id}.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=comments[0].keys())
    writer.writeheader()
    writer.writerows(comments)

print("✅ Data komentar berhasil disimpan.")
