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
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Gamunda/LenoreShop">
    <img src="frontend/public/logov2.png" alt="Logo" height="40">
  </a>

<h3 align="center">LenoreShop</h3>

  <p align="center">
    A simple shopping app.
    <br />
    <a href="https://github.com/Gamunda/LenoreShop"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Gamunda/LenoreShop/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Gamunda/LenoreShop/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#step-1-create-a-env-file">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![LenoreShop Screen Shot][product-screenshot]]

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

Welcome to LenoreShop! This guide will help you set up and run the application using Docker and Docker Compose.

### Prerequisites

Make sure you have the following installed on your system:

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

<!-- INSTALLATION -->
### Step 1: Create a `.env` File

Create a `.env` file in the root directory of the project. This file will store environment variables required to run the application. Below is an example of the variables you need to define:

```env
DEBUG=0
SECRET_KEY=mysupersecretkey
DJANGO_ALLOWED_HOSTS=localhost
CSRF_TRUSTED_ORIGINS=http://localhost
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=lenoreshop
SQL_USER=lenoreshopuser
SQL_PASSWORD=somepassword
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
DJANGO_SUPERUSER_PASSWORD=suepervisorpassword
DJANGO_SUPERUSER_EMAIL=someone@somewhere.com
DJANGO_SUPERUSER_USERNAME=supervisor
```

Adjust these values according to your environment and application requirements.

### Step 2: Create a `.env.db` File

Create a `.env.db` file in the root directory of the project. This file will store environment variables required to run the application. Below is an example of the variables you need to define:

```env
POSTGRES_USER=lenoreshopuser
POSTGRES_PASSWORD=somepassword
POSTGRES_DB=lenoreshop
```

Make sure these match the settings in .env file!

### Step 3: Create a `docker-compose.yml` File

Create a `docker-compose.yml` file in the root directory of the project. Below is an example configuration:

```yaml
services:
  frontend:
    image: novanglus96/lenoreshop_frontend:latest
    container_name: lenoreshop_frontend
    networks:
      - lenoreshop
    restart: unless-stopped
    expose:
      - 80
    env_file:
      - ./.env
  backend:
    image: novanglus96/lenoreshop_backend:latest
    container_name: lenoreshop_backend
    command: /home/app/web/start.sh
    volumes:
      - lenoreshop_static_volume:/home/app/web/staticfiles
      - lenoreshop_media_volume:/home/app/web/mediafiles
    expose:
      - 8000
    depends_on:
      - db
    networks:
      - lenoreshop
    env_file:
      - ./.env
  db:
    image: postgres:15
    container_name: lenoreshop_db
    volumes:
      - lenoreshop_postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env.db
    networks:
      - lenoreshop
  nginx:
    image: novanglus96/lenoreapps_proxy:latest
    container_name: lenoreshop_nginx
    ports:
      - "8080:80"
    volumes:
      - lenoreshop_static_volume:/home/app/web/staticfiles
      - lenoreshop_media_volume:/home/app/web/mediafiles
    depends_on:
      - backend
      - frontend
    networks:
      - lenoreshop

networks:
  lenoreshop:

volumes:
  lenoreshop_postgres_data:
    external: true
  lenoreshop_static_volume:
    external: true
  lenoreshop_media_volume:
    external: true
```

### Step 4: Run the Application

1. Start the services:

   ```bash
   docker compose up -d
   ```

2. Access the application in your browser at `http://localhost:8080`.

### Notes

* Adjust exposed ports as needed for your environment.
* If you encounter any issues, ensure your `.env` file has the correct values and your Docker and Docker Compose installations are up to date.

Enjoy using LenoreShop!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

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
[product-screenshot]: screenshots/LenoreShop_Screenshot.png
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
