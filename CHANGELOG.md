# [1.7.0-rc.18](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.17...v1.7.0-rc.18) (2026-05-03)


### Bug Fixes

* remove redundant logo from HomeView ([#46](https://github.com/Novanglus96/LenoreShop/issues/46)) ([2f9e458](https://github.com/Novanglus96/LenoreShop/commit/2f9e45830a197707c4d941d752cd9c0cf9a81cab))

# [1.7.0-rc.17](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.16...v1.7.0-rc.17) (2026-05-03)


### Bug Fixes

* revert admin link to plain anchor now that SW denylist is in place ([#45](https://github.com/Novanglus96/LenoreShop/issues/45)) ([c63d271](https://github.com/Novanglus96/LenoreShop/commit/c63d271600dde2a9ddb9a4f48b8a961308a80d1a))

# [1.7.0-rc.16](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.15...v1.7.0-rc.16) (2026-05-03)


### Bug Fixes

* exclude /admin from service worker navigateFallback ([#44](https://github.com/Novanglus96/LenoreShop/issues/44)) ([e0dd0ea](https://github.com/Novanglus96/LenoreShop/commit/e0dd0ea965612185847bde657acab1492e1a1b16))

# [1.7.0-rc.15](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.14...v1.7.0-rc.15) (2026-05-02)


### Bug Fixes

* use window.location.assign for admin link to bypass Vue Router interception ([#43](https://github.com/Novanglus96/LenoreShop/issues/43)) ([a3249cd](https://github.com/Novanglus96/LenoreShop/commit/a3249cd8dac32281531b9fe625c4ecb8e09f464b))

# [1.7.0-rc.14](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.13...v1.7.0-rc.14) (2026-05-02)


### Bug Fixes

* ui spacing, admin link, and version endpoint ([#42](https://github.com/Novanglus96/LenoreShop/issues/42)) ([dbbaaf9](https://github.com/Novanglus96/LenoreShop/commit/dbbaaf9fb685a219f5ba0d4bcdf275fa0cc77f70))

# [1.7.0-rc.13](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.12...v1.7.0-rc.13) (2026-05-02)


### Bug Fixes

* improve spacing — top gap on mobile, more margin on desktop ([#41](https://github.com/Novanglus96/LenoreShop/issues/41)) ([c9f93c2](https://github.com/Novanglus96/LenoreShop/commit/c9f93c271d5834a6a887d7f5bcb815cf532fb793))

# [1.7.0-rc.12](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.11...v1.7.0-rc.12) (2026-05-02)


### Features

* consolidate nav menu, move version to footer, edge-to-edge mobile layout ([#40](https://github.com/Novanglus96/LenoreShop/issues/40)) ([b53bb5b](https://github.com/Novanglus96/LenoreShop/commit/b53bb5b99e33739993618e7916e22198aea861db))

# [1.7.0-rc.11](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.10...v1.7.0-rc.11) (2026-05-02)


### Features

* add offline mode with optimistic updates and pending sync queue ([#39](https://github.com/Novanglus96/LenoreShop/issues/39)) ([1bc1722](https://github.com/Novanglus96/LenoreShop/commit/1bc17223ef5336a9053bb01a1c791094dbe2c888))

# [1.7.0-rc.10](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.9...v1.7.0-rc.10) (2026-05-02)


### Bug Fixes

* reorder aisles using individual PUT calls instead of bulk endpoint ([#37](https://github.com/Novanglus96/LenoreShop/issues/37)) ([abd093f](https://github.com/Novanglus96/LenoreShop/commit/abd093f876a56185e6ea5902c969cd0c1025d4c8))

# [1.7.0-rc.9](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.8...v1.7.0-rc.9) (2026-05-02)


### Bug Fixes

* change aisle reorder endpoint from PUT to POST ([#36](https://github.com/Novanglus96/LenoreShop/issues/36)) ([4aae7cb](https://github.com/Novanglus96/LenoreShop/commit/4aae7cbdfe2af74a1303f1b4dbb628fb0c85bbbf))

# [1.7.0-rc.8](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.7...v1.7.0-rc.8) (2026-05-02)


### Bug Fixes

* move reorder endpoint before parameterized aisle route ([#35](https://github.com/Novanglus96/LenoreShop/issues/35)) ([e25d837](https://github.com/Novanglus96/LenoreShop/commit/e25d837f93fb969d4e787bb9fdf0521bf0df1144))

# [1.7.0-rc.7](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.6...v1.7.0-rc.7) (2026-05-02)


### Features

* drag and drop aisle reordering ([#24](https://github.com/Novanglus96/LenoreShop/issues/24)) ([#34](https://github.com/Novanglus96/LenoreShop/issues/34)) ([751bb88](https://github.com/Novanglus96/LenoreShop/commit/751bb8897c1b6becab840ce7a4d7a8c68fdb1701))

# [1.7.0-rc.6](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.5...v1.7.0-rc.6) (2026-05-02)


### Features

* add demo data for initial setup ([#23](https://github.com/Novanglus96/LenoreShop/issues/23)) ([#33](https://github.com/Novanglus96/LenoreShop/issues/33)) ([fc7f431](https://github.com/Novanglus96/LenoreShop/commit/fc7f431dc16a331f8baf054ac77085f42e5f1c42))

# [1.7.0-rc.5](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.4...v1.7.0-rc.5) (2026-05-02)


### Features

* add MySQL/MariaDB support ([#19](https://github.com/Novanglus96/LenoreShop/issues/19)) ([#32](https://github.com/Novanglus96/LenoreShop/issues/32)) ([db6ddd9](https://github.com/Novanglus96/LenoreShop/commit/db6ddd92b2b2bcc4b9e205783cae04ec3898f9c1))

# [1.7.0-rc.4](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.3...v1.7.0-rc.4) (2026-04-14)


### Features

* add PWA support with manifest and service worker ([#31](https://github.com/Novanglus96/LenoreShop/issues/31)) ([a17bcf3](https://github.com/Novanglus96/LenoreShop/commit/a17bcf39519da30bc7dec2b0b3c0d0c8ee5c47ad))

# [1.7.0-rc.3](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.2...v1.7.0-rc.3) (2026-04-14)


### Bug Fixes

* compare API version against package.json instead of hardcoded string ([#29](https://github.com/Novanglus96/LenoreShop/issues/29)) ([a572e3b](https://github.com/Novanglus96/LenoreShop/commit/a572e3b920f2a4d7866371a95e51aaffdc39336c))

# [1.7.0-rc.2](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0-rc.1...v1.7.0-rc.2) (2026-04-14)


### Bug Fixes

* remove deprecated show_defaults option from mkdocs config ([#27](https://github.com/Novanglus96/LenoreShop/issues/27)) ([77a6f4a](https://github.com/Novanglus96/LenoreShop/commit/77a6f4aa64c878e5156d72c81b8e7638ffb1eafa))

# [1.7.0-rc.1](https://github.com/Novanglus96/LenoreShop/compare/v1.6.26-rc.1...v1.7.0-rc.1) (2026-04-14)


### Features

* consolidate to single app container with optional DB and Redis ([#26](https://github.com/Novanglus96/LenoreShop/issues/26)) ([72ee9bd](https://github.com/Novanglus96/LenoreShop/commit/72ee9bd91ca29d68666e24ede58e76f67d0b04ed))

## [1.6.26-rc.1](https://github.com/Novanglus96/LenoreShop/compare/v1.6.25...v1.6.26-rc.1) (2026-04-14)


### Bug Fixes

* update jsconfig.json for Vite/Vue 3 and fix unused variable lint error ([12ed1e9](https://github.com/Novanglus96/LenoreShop/commit/12ed1e9efcd747d688a902542ab566ccda63b6fa))
