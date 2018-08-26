# imgprocessing 2.0
Pada versi sebelumnya, imgprocessing ditulis menggunakan **nodejs**, namun karena ada 
perubahan pada API twitter, jadi harus saya tulis ulang, tapi
kali ini menggunakan **Python** karena sekarang saya sekarang
bekerja full menggunakan python, sekalian untuk eksplor
python juga hehe. Ada juga beberapa fitur tambahan pada versi ini, seperti:
- Tweet interval tiap 1 menit.
- Notifikasi kepada *sender* saat tweetnya sudah terkirim.
- Tipografi dan estetika baru pada gambar.

# Getting the code
Source code imgprocessing 2.0 ada di 
[sini](https://github.com/pythonfarhan/imgprocessing2.0).

Cek development terakhir secara anonimus dengan:

```
$ git clone https://github.com/pythonfarhan/imgprocessing2.0.git
$ cd improcessing2.0
```

Kemudian, install *dependencies* dengan:
```
$ pip install -r requirements.txt
```

saya sarankan untuk install *dependencies* di virtual environment.

# Running test
Masukan **token key** dan **consumer key** twitter pada file 
**_constant.py**. Apabila anda belum memiliki token dan consumer
key twitter, silahkan daftar terlebih dahulu di [apps.twitter.com](apps.twitter.com).

Jalankan aplikasi dengan:
```
$ python app.py
```