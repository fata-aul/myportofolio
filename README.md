Nama : Fata Akhmad Aulia
NPM : 2506540853
kelas : PBP G

Jadi step by step saya mengerjakan ini, pada awalnya saya ingin memutuskan dulu mau nambahin section apa.
Pada awalnya saya hanya ingin menambahkan experience tapi karna merasa kurang saya tambahkan section riwayat akademik

Setelah menemukan ide awal, saya membuka kode saya bekas tutorial 1, disitu saya coba untuk memahami lebih lanjut apa kode saya itu sebelum saya memulai menambahkan.
setelah mempelajarinya saya mencoba dulu secara sendiri dengan refrensi kode yang sudah ada, namun stelah saya mencobanya malah jadi seperti ini kalo di minimize![alt text](image.png)

jadinya gambarkan sketsanya di kertas agar jelas  dan saya memutuskan untuk minta bantuan AI untuk tolong saya gimana si cara rapiin agar jadi rapih ketika di minimize. ![alt text](image-2.png)

setelah membuat yang section experience, saya coba membuat bagian yang my academic records, pada awalnya saya cukup copy paste bagian yang my experience dan diganti aja title nya jadi seperti ini ![alt text](image-3.png), namun setelah itu saya sadar bahwa agak boring aja kalo sama jadi aku coba ngesketsa ulang jadi seperti ini ![alt text](image-1.png), untuk smp, sma dan kuliah aku bikin cards masing masing dan anak panah buat ngehubunginnya.

Karna pada awal aku bingung gimana cara biar ada anak panah yang bisa ngelengkung gitu, aku akhirnya coba nanya AI lagi tentang gimana si cara gambar anak panahnya dengan ngasih sketsa bikinan di awal ![alt text](image-4.png)

setelah itu saya coba mengupdatenya sendiri dengan bantuan ai yang tadi sudah dikasih, pada awalnya garis yang menghubungkan cards malah ga kesambung dengan cardsnya, setelah beberapa adjustment akhirnya jadi.
Namun saat saya lagi testing dan ubah ke minimize ada masalah baru, ![alt text](image-5.png) jadi berantakan banget kalo di minimize. Aku coba otak atik sendiri dengan mengubah size cards nya, menurunkan tinggi cards nya, namun masih berantakan.

Setelah memikirkannya sampe keesokan hari akhirnya saya punya ide, jadi di mode tab normal akan terliha cards dengan panah yang menghubunginya seperti biasa dan ketika di minimize tampilannya akan berubah mengikuti yang experience, agar ga bingung nantinya saya memutuskan buat gambarin dulu sketsanya ![alt text](image-6.png) Setelah itu dengan bantuan AI buat tau gimana caranya ngerubah tampilnnya ketika di minimize, Dan portofolio nya pun selesai

### Tugas 1

1. Ya, jadi saya pakai beberapa elemen semantik <header> untuk bagian nav/brand di atas, <main> untuk membungkus konten utama, <section> untuk tiap blok konten (hero/profile dan journey/experience-education), serta <footer> untuk bagian bawah.

buat manfaatnya si elemen semantik ini bikin struktur halaman lebih jelas maknanya (bukan cuma <div> semua)  dan memudahkan saya sendiri saat membaca/mengedit kode karena tiap bagian punya batas yang jelas misalnya waktu nambah section "Journey" kemarin saya  tinggal taruh <section> baru di dalam <main> tanpa bingung struktur sebelumnya.

2. Tantangan yang saya rasakan adalah waktu ukuran layar di minimize jadi sekecil HP tapi juga gak selebar laptop, tampilannya jadi berantakan apa lagi yang bagian academic records. 

Cara saya menentukan mana yang perlu diubah: saya lihat bagian mana yang ukurannya udah gede dari sananya, kayak foto profil dan judul nama, itu yang paling gampang kelihatan aneh kalau ruangnya dipersempit, jadi itu yang saya atur duluan supaya ikut mengecil menyesuaikan layar. Tantangan paling besarnya di academic records jadi agar bisa terlihat rapi walau di minimize saya ngide kalo di minimize tampilannya jadi kayak yang experience


3. Karena websitenya masih static (isinya ditulis langsung di file HTML), kalau saya mau update sesuatu  misalnya nambah pengalaman baru atau ganti riwayat sekolah saya harus buka lagi file HTML-nya terus edit manual satu-satu. Ini kurang praktis kalau kontennya sering berubah, dan lumayan ribet karena formatnya berulang-ulang jadi gampang salah ketik atau lupa update salah satu bagian.

Untuk pengembangan selanjutnya, saya pengen nambahin sesuatu yang lebih dinamis, misalnya bikin data pengalaman dan riwayat pendidikan itu tersimpan terpisah (bukan ditulis langsung di HTML), jadi kalau mau update tinggal ganti datanya aja tanpa perlu edit ulang tampilan HTML dan cssnya.






### Tugas 2

Lanjut dari rencana pengembangan yang saya tulis di poin 3 Tugas 1, kali ini saya coba beneran mindahin section Experience dan Academic Records yang sebelumnya masih hardcode di index.html supaya datanya bisa disimpan di database dan gak perlu ditulis manual lagi di HTML.

Awalnya saya masih bingung modelnya mau ditaruh dimana, akhirnya saya putuskan untuk taruh di app main yang sudah ada aja supaya gak perlu bikin app baru dulu. Setelah itu saya coba ngerjainnya step-by-step, mulai dari bikin model di models.py, lalu menjalankan makemigrations dan migrate. Setelah itu saya bikin view yang tugasnya mengambil data dari database dan mengirimkannya ke template, lalu saya daftarkan urlnya dan menambahkan link-nya ke navbar. Sempat ada masalah karena saya lupa menjalankan migrate, jadi waktu dibuka muncul error no such table. Ternyata migration filenya sudah ada, tapi tabelnya belum dibuat di database karena migratenya belum dijalankan.

Setelah section Experience-nya berhasil dibuat, saya merasa tampilannya bakal lebih rapi kalau pengalaman saya dikelompokkan berdasarkan kategorinya, misalnya Internship, Volunteer, dan lain-lain seperti desain awal yang saya buat. Jadi saya menambahkan field organization di model supaya nama perusahaan atau organisasinya bisa dipisahkan dari judul perannya. Setelah itu saya ubah bagian view supaya datanya bisa dikelompokkan otomatis berdasarkan kategori sebelum dikirim ke template.



1. Alur yang terjadi ketika halaman portofolio baru, misalnya Academic Records, dibuka kira-kira seperti ini:

* Pertama browser mengirim request ke server, misalnya GET /academic/.
* Request tersebut pertama masuk ke urls.py yang ada di project (portofolio/urls.py). Di sini Django akan mengecek path yang diminta cocok dengan pola URL yang mana. Karena academic/ diarahkan ke app main, request tersebut diteruskan ke urls.py yang ada di app main.
* Setelah masuk ke main/urls.py, Django mencari lagi URL yang sesuai. Karena menemukan path("academic/", show_academic, name="show_academic"), akhirnya function show_academic yang ada di views.py` dipanggil.
* Di dalam view show_academic, Django mengambil data dari model AcademicRecord menggunakan AcademicRecord.objects.all(). Data yang diambil ini masih berupa objek Python atau QuerySet dari database.
* Setelah itu data tersebut dimasukkan ke dalam ontext, lalu view menggunakan render()untuk menentukan template yang akan digunakan, yaitu academic.html, sekaligus mengirimkan context tadi.
* Setelah template diproses oleh Django, setiap data di dalam context akan di-loop menggunakan {% for %} dan dimasukkan ke bagian HTML yang sesuai.
* Setelah semuanya selesai, hasil HTML tersebut dikirim kembali ke browser dan akhirnya halaman Academic Records bisa ditampilkan ke user.

Jadi kalau disimpulkan, alurnya dimulai dari urls.py project yang menentukan app mana yang menangani request, lalu urls.py di app menentukan view mana yang dipanggil. Setelah itu view mengambil data dari model dan menentukan template yang digunakan. Terakhir, template menampilkan data tersebut menjadi HTML yang dikirim kembali ke browser.

2. Data untuk bagian portofolio baru menurut saya lebih baik disimpan di model daripada ditulis langsung di template karena sebelumnya saya sendiri sudah merasakan ribetnya ketika masih menggunakan hardcode di index.html.

Kalau datanya masih ditulis langsung di template, setiap kali saya ingin menambah, mengubah, atau menghapus data, misalnya menambahkan pengalaman kerja baru, saya harus membuka file HTML dan mengeditnya secara manual. Karena formatnya juga berulang-ulang, jadi lebih gampang salah ketik atau lupa mengubah salah satu bagian.

Sedangkan kalau datanya disimpan di model, data dan tampilan bisa dipisahkan. Jadi kalau saya ingin menambahkan data baru, saya cukup menggunakan Model.objects.create(...) lewat shell atau admin tanpa perlu mengubah template atau CSS-nya. Menurut saya ini juga bikin kode jadi lebih rapi karena bagian data dan bagian tampilannya gak tercampur.

Selain itu, karena datanya sudah ada di database, data tersebut juga bisa digunakan lagi di bagian lain. Misalnya saya ingin menampilkan ringkasan pengalaman di halaman utama, saya gak perlu menulis data yang sama dari awal.
Menurut saya cara ini juga lebih mudah untuk di-test karena saya bisa membuat data dummy menggunakan Model.objects.create() di unit test lalu mengecek apakah data tersebut berhasil muncul di response. Kalau datanya masih hardcode di HTML, menurut saya bakal lebih susah untuk melakukan testing seperti itu.

Kalau nanti datanya semakin banyak dan saya ingin mengurutkan atau memfilter data, misalnya berdasarkan tanggal terbaru, saya juga tinggal menggunakan query dari model seperti .order_by() atau .filter()``````````` daripada harus mengaturnya satu-satu di HTML.

Jadi menurut saya, menggunakan model membuat website lebih gampang dipelihara karena kalau mau update isi portofolio saya gak harus mengubah kode tampilan lagi. Selain itu, ke depannya juga lebih fleksibel karena data dan tampilannya sudah dipisahkan.

3. Perbedaan makemigrations dan migrate yang saya pahami adalah:

* makemigrations digunakan untuk membuat semacam blueprint atau instruksi perubahan berdasarkan perubahan yang saya buat di models.py. Jadi Django akan melihat perubahan pada model saya lalu membuat file migration baru. Pada tahap ini database belum benar-benar berubah.
* Sedangkan migrate digunakan untuk menjalankan file migration tersebut ke database. Jadi perubahan seperti membuat tabel baru atau menambahkan kolom baru baru benar-benar diterapkan ke database setelah saya menjalankan migrate`.

Jadi urutannya adalah makemigrations dulu baru migrate Saya harus membuat file migration-nya terlebih dahulu sebelum menjalankan perubahan tersebut ke database.

Contoh perubahan model yang saya lakukan adalah ketika saya menambahkan field logo di model AcademicRecord dan field organization di model Experience.