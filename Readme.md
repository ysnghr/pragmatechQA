
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://pragmatech.az/">
    <img src="https://pragmatech.az/static/assets/images/logo/logo.png" alt="Logo" width= "50%">
  </a>

  <h3 align="center">Pragmatech Q&A Project</h3>

</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Mündəricat</summary>
  <ol>
    <li>
      <a href="#proyekt-haqqında-məlumat">Proyekt haqqında məlumat</a>
      <ul>
        <li><a href="#asılılıqlar">Asılılıqlar</a></li>
      </ul>
    </li>
    <li><a href="#kontribution">Kontribution</a></li>
  </ol>
</details>



## Proyekt haqqında məlumat

Pragmatech Education Center daxilindəki tələbələrin dərslə bağlı suallarını verə biləcəyi eyni zamanda başqa tələbələrin cavablarını cavablaya biləcəyi bir proyekdir.

### Asılılıqlar

Proyekti çalışdırmaq üçün ilk olaraq mysql-də schema yaratmaq lazımdır.

```CREATE SCHEMA `pragmatechqa` DEFAULT CHARACTER SET utf8 ;```

Bundan sonra isə database.cnf faylında database-in məlumatları yazılmalıdır.

```
[client]
database = pragmatechqa
host = localhost
user = DB-USER
password = DB-PASSWORD
default-character-set = utf8
```

Sonra is' django migration kommandları çalışdırılmalıdır.
```
python manage.py makemigrations
```
```
python manage.py migrate
```

Proyektin asılı olduğu plugin və frameworkləri requirements.txt faylında daha ətraflı görə bilərsiz.
* asgiref==3.3.1
* certifi==2020.12.5
* chardet==3.0.4
* Django==3.1.3
* django-ckeditor==6.0.0
* django-cleanup==5.1.0
* django-crispy-forms==1.10.0
* django-el-pagination==3.3.0
* django-js-asset==1.2.2
* django-remember-me==0.1.1
* django-taggit==1.3.0
* idna==2.10
* Pillow==8.0.1
* pytz==2020.4
* requests==2.25.0
* sqlparse==0.4.1
* urllib3==1.26.2



<!-- CONTRIBUTING -->
## Kontribution

Hər bir kontributor üçün bir branch yaradılıb. Sizə issue olaraq assign olunan taskları bitirdikdən sonra öz branchınıza update verib pull request atmağınız lazımdır. Eyni zamanda əgər taskı etməyə başlasanız o zaman projectBoardda həmin taskı In progress hissəsinə əlavə etməyi unutmayın.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[website-url]: https://pragmatech.az/
