<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Novanglus96/LenoreShop">
    <img src="https://novanglus96.github.io/LenoreShop/images/logov2.png" alt="Logo" height="40">
  </a>

  <p align="center">
    A simple shopping app.
    <br />
    <a href="https://github.com/Novanglus96/LenoreShop/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Novanglus96/LenoreShop/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

![LenoreShop Screen Shot][product-screenshot]

Introducing LenoreShop, the ultimate shopping list app designed to streamline your grocery shopping experience. Whether you're managing a single shopping trip or juggling multiple stores, LenoreShop has you covered with its intuitive features and user-friendly interface.

<b>Key Features:</b>
<ul>
<li><b>Multiple Stores:</b> Easily add as many stores as you frequent, ensuring all your favorite shopping destinations are covered.</li>
<li><b>Unlimited Shopping Lists:</b> Create and manage multiple shopping lists for each store, helping you stay organized and efficient.</li>
<li><b>Customizable Aisles:</b> Add aisles specific to each store and arrange them in the order you typically shop, making your trips faster and more convenient.</li>
<li><b>Item Organization:</b> Add items to your lists by aisle, so you never miss a thing and can quickly find what you need.</li>
</ul>

<b>Why Choose LenoreShop?</b>
LenoreShop is perfect for anyone who needs to shop, offering a tailored shopping experience that adapts to your personal preferences. With its seamless integration of Django for a robust backend and Vue for a sleek, responsive frontend, LenoreShop ensures a smooth and reliable user experience.

Simplify your shopping routine with LenoreShop and enjoy the convenience of a perfectly organized shopping trip every time.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


 
### Built With

* [![Django][Django]][Django-url]
* [![Vue][Vue.js]][Vue-url]
* [![Docker][Docker]][Docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Welcome to LenoreShop! This guide will help you set up and run the application using Docker.

### Prerequisites

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

> **Upgrading from a pre-1.7.0 multi-container install?** See the [Migration Guide](migration-v1-to-v2.md).

<!-- INSTALLATION -->
### Step 1: Create a `.env` File

Create a `.env` file in your deployment directory. The minimum required configuration:

```env
DEBUG=0
SECRET_KEY=your-long-random-secret-key
DJANGO_ALLOWED_HOSTS=your-host-or-ip
CSRF_TRUSTED_ORIGINS=https://your-domain

# Optional: superuser created on first run
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=changeme
```

See `example.env` in the repository for the full list of options including PostgreSQL, MySQL, and Redis.

### Step 2: Create a `docker-compose.yml` File

**Minimal setup (SQLite — no external database required):**

```yaml
services:
  app:
    image: novanglus96/lenoreshop:latest
    volumes:
      - lenoreshop_data:/home/app/web/data
      - lenoreshop_static:/home/app/web/staticfiles
      - lenoreshop_media:/home/app/web/mediafiles
    env_file:
      - ./.env
    ports:
      - "${APP_PORT:-7000}:80"
    restart: unless-stopped

volumes:
  lenoreshop_data:
  lenoreshop_static:
  lenoreshop_media:
```

**Full setup (PostgreSQL + Redis):**

```yaml
services:
  app:
    image: novanglus96/lenoreshop:latest
    volumes:
      - lenoreshop_static:/home/app/web/staticfiles
      - lenoreshop_media:/home/app/web/mediafiles
    env_file:
      - ./.env
    ports:
      - "${APP_PORT:-7000}:80"
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env
    environment:
      - POSTGRES_USER=${SQL_USER}
      - POSTGRES_PASSWORD=${SQL_PASSWORD}
      - POSTGRES_DB=${SQL_DATABASE}
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
  lenoreshop_static:
  lenoreshop_media:
```

For PostgreSQL, add these to your `.env`:

```env
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=lenoreshop
SQL_USER=lenoreshopuser
SQL_PASSWORD=somepassword
SQL_HOST=db
SQL_PORT=5432
REDIS_URL=redis://redis:6379/0
```

**Full setup (MySQL/MariaDB + Redis):**

```yaml
services:
  app:
    image: novanglus96/lenoreshop:latest
    volumes:
      - lenoreshop_static:/home/app/web/staticfiles
      - lenoreshop_media:/home/app/web/mediafiles
    env_file:
      - ./.env
    ports:
      - "${APP_PORT:-7000}:80"
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: mysql:8
    volumes:
      - mysql_data:/var/lib/mysql
    env_file:
      - ./.env
    environment:
      - MYSQL_DATABASE=${SQL_DATABASE}
      - MYSQL_USER=${SQL_USER}
      - MYSQL_PASSWORD=${SQL_PASSWORD}
      - MYSQL_ROOT_PASSWORD=${SQL_PASSWORD}
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  mysql_data:
  lenoreshop_static:
  lenoreshop_media:
```

For MySQL, add these to your `.env`:

```env
SQL_ENGINE=django.db.backends.mysql
SQL_DATABASE=lenoreshop
SQL_USER=lenoreshopuser
SQL_PASSWORD=somepassword
SQL_HOST=db
SQL_PORT=3306
REDIS_URL=redis://redis:6379/0
```

### Step 3: Run the Application

```bash
docker compose up -d
```

Access the application at `http://your-host:7000` (or your configured `APP_PORT`).

### Notes

* Static files and database migrations are applied automatically on startup.
* The superuser is created automatically on first run if `DJANGO_SUPERUSER_*` vars are set.
* If you encounter any issues, ensure your `.env` file has the correct values.

Enjoy using LenoreShop!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

**v1.7.0** ✅ Released
- Single-container deployment
- MySQL/MariaDB support
- Demo data loader
- Drag-and-drop aisle reordering
- Offline mode (PWA)
- UI refresh

**v2.0.0** — Planned
- [ ] Wishlists
- [ ] Packing lists

See the [open issues](https://github.com/Novanglus96/LenoreShop/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Support

<a href="https://www.buymeacoffee.com/novanglus" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<p>Or</p> 

<a href="https://www.patreon.com/novanglus">
    <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

<!-- CONTACT -->
## Contact

John Adams - Lenore.Apps@gmail.com

Project Link: [https://github.com/Novanglus96/LenoreShop](https://github.com/Novanglus96/LenoreShop)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgements

A heartfelt thanks to our Patrons for their generous support! Your contributions help us maintain and improve this project.

### ⭐ Thank You to Our Supporters:

![Red Supporter Badge](https://img.shields.io/badge/Eleanor-E41B17?style=for-the-badge&logo=patreon&logoColor=gray)
![Red Supporter Badge](https://img.shields.io/badge/Danielle-E41B17?style=for-the-badge&logo=patreon&logoColor=gray)
![BuyMeACoffee Supporter Badge](https://img.shields.io/badge/SuperDev-white?style=for-the-badge&logo=buymeacoffee&logoColor=black)
<!--![Gold Supporter Badge](https://img.shields.io/badge/Eleanor-gold?style=for-the-badge&logo=patreon&logoColor=gray)-->
<!--![Silver Supporter Badge](https://img.shields.io/badge/Jane_Smith-silver?style=for-the-badge&logo=patreon&logoColor=gray)-->
<!--![BuyMeACoffee Supporter Badge](https://img.shields.io/badge/Jane_Smith-white?style=for-the-badge&logo=buymeacoffee&logoColor=black)-->

Want to see your name here? Support us on [Patreon](https://www.patreon.com/novanglus) to join our amazing community and shape the future of LenoreShop!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Novanglus96/LenoreShop?style=for-the-badge
[contributors-url]: https://github.com/Novanglus96/LenoreShop/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Novanglus96/LenoreShop?style=for-the-badge
[forks-url]: https://github.com/Novanglus96/LenoreShop/forks
[stars-shield]: https://img.shields.io/github/stars/Novanglus96/LenoreShop?style=for-the-badge
[stars-url]: https://github.com/Novanglus96/LenoreShop/stargazers
[issues-shield]: https://img.shields.io/github/issues/Novanglus96/LenoreShop?style=for-the-badge
[issues-url]: https://github.com/Novanglus96/LenoreShop/issues
[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge
[license-url]: https://github.com/Novanglus96/LenoreShop/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/johnmadamsjr
[product-screenshot]: images/LenoreShop_Screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Django]: https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Documentaion-url]: https://novanglus96.github.io/LenoreShop/
