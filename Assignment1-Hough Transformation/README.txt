Bilgisayarım kod çalıştırmak için çok uygun değil. Ödevin tamamını Colab üzerinden yaptım. 

Bu yüzden cv.imshow gibi fonksyionlarda kütüphanesi olur mu olmaz mı bilemedim. Sonuç ürettiğim görselleri
kodun çalıştığı dizine folder içinde çıkartıyorum

Kodu terminalden argüman vererek çalıştırabilirsiniz.
İki seçenek mevcut, ilki spesifik bir resim için çıktı almak.
İkincisi tüm veri seti için sırayla çıktı almak.

Argümanlar : image path,image annotation path, threshold, 0 ya 1 ([1]), imgelerin bulunduğu klasör pathi, annotations folder

[1] 0 ya da 1 olmasının sebebi şu 0 tek görsel için sonuç üretiyor. 1 tüm veri seti için sonuç üretiyor.

Algoritmam maalesef yavaş çalışıyor,post processing'i iyi hale getiremedim zamanım yetmedi. Ortalama bir imge için 40 sn civarı. Tabii threshold azaltılırsa süre çok çok artıyor.

Terminal Çalıştırma Kodu
!python main.py 'images/Cars0.png' 'annotations/Cars0.xml' 120 1 'images' 'annotations'

Not: Tek resim çalıştırmada tespit edemediğinde plaka bulunamadı diyor. Eğer plaka bulunursa kodun çalıştırıldığı dizine result çıkartması gerekiyor.

Plaka bulduğu örnek Cars0,Bulamadığı Cars2
