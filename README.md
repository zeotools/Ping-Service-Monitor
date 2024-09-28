# Ping Service Monitor

Ping Service Monitor, belirli RSS beslemelerindeki en son konuları izleyip, belirli ping servislerine bildirim gönderen bir Python uygulamasıdır. Bu proje, web sitelerinin güncellemelerini takip etmek ve otomatik olarak ping servislerine bildirim göndermek isteyen geliştiriciler için kullanışlıdır. xenforo siteleri için uygundur örneğin: https://enuygunfirmalar.com/sitemap-2.xml

## Özellikler

- Belirtilen RSS beslemesinden en son konuları bulma
- Ping servislerine otomatik bildirim gönderme
- Hatalı ping servislerini otomatik olarak dosyadan silme
- Ping sonuçlarını CSV dosyasına kaydetme

## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki Python kütüphanelerinin yüklü olması gerekmektedir:

- `feedparser`
- `requests`
- `csv`

Bu kütüphaneleri yüklemek için aşağıdaki komutu kullanabilirsiniz:

```bash
pip install feedparser requests



Linkler.txt içeriğindeki linkler bu yapıda olmalıdır. https://enuygunfirmalar.com/forums/-/index.rss
