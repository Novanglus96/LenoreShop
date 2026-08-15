# [1.9.0-alpha.3](https://github.com/Novanglus96/LenoreShop/compare/v1.9.0-alpha.2...v1.9.0-alpha.3) (2026-08-15)


### Bug Fixes

* add Pillow to the CI test requirements ([98dddf6](https://github.com/Novanglus96/LenoreShop/commit/98dddf6eb957246f4c5c65bec134d324e5200023))
* offer the camera as its own control when adding a photo ([65c72ec](https://github.com/Novanglus96/LenoreShop/commit/65c72ecc0d267782449e539b3123a5b67db7b7b4))


### Features

* add a photo to an item from a shopping list row ([2d2dcd9](https://github.com/Novanglus96/LenoreShop/commit/2d2dcd97b09a4d1eabcc0e517f7683123a492946))
* add photos to items and freezer foods ([40cdc81](https://github.com/Novanglus96/LenoreShop/commit/40cdc8172c4d27fa4b0a9952eda77c80d9bd04a7))

# [1.9.0-alpha.2](https://github.com/Novanglus96/LenoreShop/compare/v1.9.0-alpha.1...v1.9.0-alpha.2) (2026-08-15)


### Bug Fixes

* adding a purchased item again no longer un-buys it ([05be699](https://github.com/Novanglus96/LenoreShop/commit/05be699493f31012e6975dc0b9dcace4028e6706))
* fold a list item back together once both rows are in the same state ([48ab9dc](https://github.com/Novanglus96/LenoreShop/commit/48ab9dc4464e5505322cc20326df968a0d0d9488))
* keep form defaults after cancelling a dialog ([3e827d1](https://github.com/Novanglus96/LenoreShop/commit/3e827d1571cfa10c5701b0217839217ca3f96ae5))
* make the torn and iced card edges actually visible ([4d7503f](https://github.com/Novanglus96/LenoreShop/commit/4d7503f16b887053d996a607b36f50118a2646c1))
* rebuild the broken /alllists route as a list index ([aa77125](https://github.com/Novanglus96/LenoreShop/commit/aa77125161e80482bdd499ef70e3b4f7dbd3d633))
* tear the bottom off the sheet instead of notching above it ([ba8be11](https://github.com/Novanglus96/LenoreShop/commit/ba8be115e260595c394a2b900cb89868fcb3139b))


### Features

* add a freezer section to the dashboard ([f5a7d26](https://github.com/Novanglus96/LenoreShop/commit/f5a7d2669869c51483e5112eed3ea94d1509dd8a))
* bring the dialogs and the nav menu into the new design ([3d5a7cb](https://github.com/Novanglus96/LenoreShop/commit/3d5a7cb5ab91c5e4b6696e48106f0238a5109382))
* cap the dashboard and hoist the freezer warning above the lists ([25993fd](https://github.com/Novanglus96/LenoreShop/commit/25993fdff28f1238bb1333b7a95237819b1d8790))
* expose list progress and preview items on shopping list responses ([304423c](https://github.com/Novanglus96/LenoreShop/commit/304423c474e90634fc253b1d84a5a4498ecf525a))
* merge the two shopping list pages into one ([2e53a3f](https://github.com/Novanglus96/LenoreShop/commit/2e53a3f6207c0891823465d059d799bfefbb4a0c))
* rebuild the active shopping list as a paper sheet ([699b6ec](https://github.com/Novanglus96/LenoreShop/commit/699b6ec8e3b95879055feea75221f6cc6e8295f3))
* rebuild the dashboard as paper notepad cards ([627ad5a](https://github.com/Novanglus96/LenoreShop/commit/627ad5ac1d090ef136568950a590d9989a5733d1))
* rebuild the items and aisles pages as paper sheets ([46286c2](https://github.com/Novanglus96/LenoreShop/commit/46286c2fdf2f130a8133116f92712d6e2811fa8e))
* rebuild the stores and freezer pages ([73bdaca](https://github.com/Novanglus96/LenoreShop/commit/73bdacadde158e6cf27d3b3f04c570ce8f7ea5d6))

# [1.9.0-alpha.1](https://github.com/Novanglus96/LenoreShop/compare/v1.8.1...v1.9.0-alpha.1) (2026-08-12)


### Features

* allow the freezer date added to be unknown ([345d686](https://github.com/Novanglus96/LenoreShop/commit/345d68653d52a51204587bd67935f7124975513f))
* track frozen foods by freezer with throw out dates ([8ed31cb](https://github.com/Novanglus96/LenoreShop/commit/8ed31cb33d785ddd67a2ca3f3a6b4ebf021a7934))

## [1.8.1](https://github.com/Novanglus96/LenoreShop/compare/v1.8.0...v1.8.1) (2026-08-08)


### Bug Fixes

* allow release docs deploy to be re-run manually ([fb59e73](https://github.com/Novanglus96/LenoreShop/commit/fb59e7370b21fd3464b07a9c235f5645b5a85bda))

## [1.8.1](https://github.com/Novanglus96/LenoreShop/compare/v1.8.0...v1.8.1) (2026-08-08)


### Bug Fixes

* allow release docs deploy to be re-run manually ([fb59e73](https://github.com/Novanglus96/LenoreShop/commit/fb59e7370b21fd3464b07a9c235f5645b5a85bda))

# [1.8.0](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0...v1.8.0) (2026-05-28)


### Bug Fixes

* disable devtools plugins in production builds ([#55](https://github.com/Novanglus96/LenoreShop/issues/55)) ([bf2f0aa](https://github.com/Novanglus96/LenoreShop/commit/bf2f0aa003a59abfedea5ec3a6a44467c8cc87f7))
* guard fullshoppinglist bindings against undefined during WebSocket refetch ([#54](https://github.com/Novanglus96/LenoreShop/issues/54)) ([e4842c8](https://github.com/Novanglus96/LenoreShop/commit/e4842c830f4e35fc50ad9a846a8ad40aa27b0d2d))
* render single edit and delete dialog outside v-for in ShoppingList ([#56](https://github.com/Novanglus96/LenoreShop/issues/56)) ([39ce08d](https://github.com/Novanglus96/LenoreShop/commit/39ce08d0e9ce61eebdd4c6b35d2063cba434543c))


### Features

* add WebSocket real-time sync for multi-user list editing ([#53](https://github.com/Novanglus96/LenoreShop/issues/53)) ([53a4230](https://github.com/Novanglus96/LenoreShop/commit/53a423039bf74743321776a5e85695aa39373247))

# [1.8.0-alpha.4](https://github.com/Novanglus96/LenoreShop/compare/v1.8.0-alpha.3...v1.8.0-alpha.4) (2026-05-28)


### Bug Fixes

* render single edit and delete dialog outside v-for in ShoppingList ([#56](https://github.com/Novanglus96/LenoreShop/issues/56)) ([39ce08d](https://github.com/Novanglus96/LenoreShop/commit/39ce08d0e9ce61eebdd4c6b35d2063cba434543c))

# [1.8.0-alpha.3](https://github.com/Novanglus96/LenoreShop/compare/v1.8.0-alpha.2...v1.8.0-alpha.3) (2026-05-28)


### Bug Fixes

* disable devtools plugins in production builds ([#55](https://github.com/Novanglus96/LenoreShop/issues/55)) ([bf2f0aa](https://github.com/Novanglus96/LenoreShop/commit/bf2f0aa003a59abfedea5ec3a6a44467c8cc87f7))

# [1.8.0-alpha.2](https://github.com/Novanglus96/LenoreShop/compare/v1.8.0-alpha.1...v1.8.0-alpha.2) (2026-05-28)


### Bug Fixes

* guard fullshoppinglist bindings against undefined during WebSocket refetch ([#54](https://github.com/Novanglus96/LenoreShop/issues/54)) ([e4842c8](https://github.com/Novanglus96/LenoreShop/commit/e4842c830f4e35fc50ad9a846a8ad40aa27b0d2d))

# [1.8.0-alpha.1](https://github.com/Novanglus96/LenoreShop/compare/v1.7.0...v1.8.0-alpha.1) (2026-05-28)


### Features

* add WebSocket real-time sync for multi-user list editing ([#53](https://github.com/Novanglus96/LenoreShop/issues/53)) ([53a4230](https://github.com/Novanglus96/LenoreShop/commit/53a423039bf74743321776a5e85695aa39373247))

# [1.7.0](https://github.com/Novanglus96/LenoreShop/compare/v1.6.25...v1.7.0) (2026-05-03)


### Bug Fixes

* change aisle reorder endpoint from PUT to POST ([#36](https://github.com/Novanglus96/LenoreShop/issues/36)) ([4aae7cb](https://github.com/Novanglus96/LenoreShop/commit/4aae7cbdfe2af74a1303f1b4dbb628fb0c85bbbf))
* compare API version against package.json instead of hardcoded string ([#29](https://github.com/Novanglus96/LenoreShop/issues/29)) ([a572e3b](https://github.com/Novanglus96/LenoreShop/commit/a572e3b920f2a4d7866371a95e51aaffdc39336c))
* exclude /admin from service worker navigateFallback ([#44](https://github.com/Novanglus96/LenoreShop/issues/44)) ([e0dd0ea](https://github.com/Novanglus96/LenoreShop/commit/e0dd0ea965612185847bde657acab1492e1a1b16))
* improve spacing — top gap on mobile, more margin on desktop ([#41](https://github.com/Novanglus96/LenoreShop/issues/41)) ([c9f93c2](https://github.com/Novanglus96/LenoreShop/commit/c9f93c271d5834a6a887d7f5bcb815cf532fb793))
* move reorder endpoint before parameterized aisle route ([#35](https://github.com/Novanglus96/LenoreShop/issues/35)) ([e25d837](https://github.com/Novanglus96/LenoreShop/commit/e25d837f93fb969d4e787bb9fdf0521bf0df1144))
* remove deprecated show_defaults option from mkdocs config ([#27](https://github.com/Novanglus96/LenoreShop/issues/27)) ([77a6f4a](https://github.com/Novanglus96/LenoreShop/commit/77a6f4aa64c878e5156d72c81b8e7638ffb1eafa))
* remove redundant logo from HomeView ([#46](https://github.com/Novanglus96/LenoreShop/issues/46)) ([2f9e458](https://github.com/Novanglus96/LenoreShop/commit/2f9e45830a197707c4d941d752cd9c0cf9a81cab))
* reorder aisles using individual PUT calls instead of bulk endpoint ([#37](https://github.com/Novanglus96/LenoreShop/issues/37)) ([abd093f](https://github.com/Novanglus96/LenoreShop/commit/abd093f876a56185e6ea5902c969cd0c1025d4c8))
* revert admin link to plain anchor now that SW denylist is in place ([#45](https://github.com/Novanglus96/LenoreShop/issues/45)) ([c63d271](https://github.com/Novanglus96/LenoreShop/commit/c63d271600dde2a9ddb9a4f48b8a961308a80d1a))
* ui spacing, admin link, and version endpoint ([#42](https://github.com/Novanglus96/LenoreShop/issues/42)) ([dbbaaf9](https://github.com/Novanglus96/LenoreShop/commit/dbbaaf9fb685a219f5ba0d4bcdf275fa0cc77f70))
* update jsconfig.json for Vite/Vue 3 and fix unused variable lint error ([12ed1e9](https://github.com/Novanglus96/LenoreShop/commit/12ed1e9efcd747d688a902542ab566ccda63b6fa))
* use window.location.assign for admin link to bypass Vue Router interception ([#43](https://github.com/Novanglus96/LenoreShop/issues/43)) ([a3249cd](https://github.com/Novanglus96/LenoreShop/commit/a3249cd8dac32281531b9fe625c4ecb8e09f464b))


### Features

* add demo data for initial setup ([#23](https://github.com/Novanglus96/LenoreShop/issues/23)) ([#33](https://github.com/Novanglus96/LenoreShop/issues/33)) ([fc7f431](https://github.com/Novanglus96/LenoreShop/commit/fc7f431dc16a331f8baf054ac77085f42e5f1c42))
* add MySQL/MariaDB support ([#19](https://github.com/Novanglus96/LenoreShop/issues/19)) ([#32](https://github.com/Novanglus96/LenoreShop/issues/32)) ([db6ddd9](https://github.com/Novanglus96/LenoreShop/commit/db6ddd92b2b2bcc4b9e205783cae04ec3898f9c1))
* add offline mode with optimistic updates and pending sync queue ([#38](https://github.com/Novanglus96/LenoreShop/issues/38)) ([9defcc0](https://github.com/Novanglus96/LenoreShop/commit/9defcc068f0fdc646ea08d63706c3e30b533ce5b)), closes [#25](https://github.com/Novanglus96/LenoreShop/issues/25)
* add offline mode with optimistic updates and pending sync queue ([#39](https://github.com/Novanglus96/LenoreShop/issues/39)) ([1bc1722](https://github.com/Novanglus96/LenoreShop/commit/1bc17223ef5336a9053bb01a1c791094dbe2c888))
* add PWA support with manifest and service worker ([#31](https://github.com/Novanglus96/LenoreShop/issues/31)) ([a17bcf3](https://github.com/Novanglus96/LenoreShop/commit/a17bcf39519da30bc7dec2b0b3c0d0c8ee5c47ad))
* consolidate nav menu, move version to footer, edge-to-edge mobile layout ([#40](https://github.com/Novanglus96/LenoreShop/issues/40)) ([b53bb5b](https://github.com/Novanglus96/LenoreShop/commit/b53bb5b99e33739993618e7916e22198aea861db))
* consolidate to single app container with optional DB and Redis ([#26](https://github.com/Novanglus96/LenoreShop/issues/26)) ([72ee9bd](https://github.com/Novanglus96/LenoreShop/commit/72ee9bd91ca29d68666e24ede58e76f67d0b04ed))
* drag and drop aisle reordering ([#24](https://github.com/Novanglus96/LenoreShop/issues/24)) ([#34](https://github.com/Novanglus96/LenoreShop/issues/34)) ([751bb88](https://github.com/Novanglus96/LenoreShop/commit/751bb8897c1b6becab840ce7a4d7a8c68fdb1701))

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
