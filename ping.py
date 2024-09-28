import feedparser 
import requests
import csv
import time

def read_ping_services(file_path):
    ping_services = []
    with open(file_path, 'r') as file:
        for line in file:
            ping_service = line.strip()
            ping_services.append(ping_service)
    return ping_services

def remove_ping_service(file_path, service):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() != service:
                file.write(line)

def find_latest_topic_links(url, count):
    feed = feedparser.parse(url)
    links = []
    for i in range(count):
        if 'entries' in feed and i < len(feed.entries):
            latest_topic = feed.entries[i]
            link = latest_topic.link
            links.append(link)
    return links

def send_pings(links, ping_services_file):
    results = []
    for link in links:
        result = {'Link': link, 'Ping Details': []}
        for service in ping_services_file.copy():  # Servisleri kopyala, böylece hatalıları hemen silebilirsiniz
            try:
                response = requests.post(service, data={'url': link})
                if response.status_code == 200:
                    result['Ping Details'].append({'Service': service, 'Status': 'Success'})
                    print(f"Ping Başarılı: Service - {service}, Link - {link}")
                else:
                    result['Ping Details'].append({'Service': service, 'Status': 'Failed'})
                    print(f"Ping Başarısız: Service - {service}, Link - {link}")
                    remove_ping_service('ping.txt', service)  # Hatalı servisi hemen sil
            except requests.exceptions.RequestException:
                result['Ping Details'].append({'Service': service, 'Status': 'Failed'})
                print(f"Ping Hatası: Service - {service}, Link - {link}")
            time.sleep(1)  # 1 saniye bekle
        time.sleep(100)  # Her link sonrası 100 saniye bekle
        results.append(result)

    return results

def main():
    links = [
        "https://enuygunfirmalar.com/forums/-/index.rss"  # Eklendi
    ]
    
    with open('linkler.txt', 'r') as file:
        for line in file:
            link = line.strip()
            links.append(link)

    ping_services_file = read_ping_services('ping.txt')

    results = []
    for link in links:
        rss_url = link
        latest_topic_links = find_latest_topic_links(rss_url, 9)

        if latest_topic_links:
            print(f"Link: {link}")
            print("Son Konu Linkleri:")
            for topic_link in latest_topic_links:
                print(topic_link)

            print("Ping Detayları:")
            ping_results = send_pings(latest_topic_links, ping_services_file)
            for result in ping_results:
                print(f"- Link: {result['Link']}")
                for ping_detail in result['Ping Details']:
                    print(f"  Service: {ping_detail['Service']}")
                    print(f"  Status: {ping_detail['Status']}")

            print("------------------------")
            results.append({
                'Link': link,
                'Latest Topic Links': latest_topic_links,
                'Ping Details': ping_results
            })
        else:
            print(f"Link: {link}")
            print("Konular bulunamadı.")
            print("------------------------")
            results.append({
                'Link': link,
                'Latest Topic Links': [],
                'Ping Details': []
            })

    # Raporu CSV dosyasına kaydet
    with open('rapor.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Link', 'Latest Topic Links', 'Ping Details']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()
