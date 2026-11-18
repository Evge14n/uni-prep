# Урок 17. Драйвери, прошивки, Secure Boot

[← Усі уроки](#/u/mint/uroky)

**Навіщо:** на більшості ноутбуків з Intel і AMD Mint працює одразу, нічого ставити не треба. Драйвер ставлять
переважно для відеокарти NVIDIA і деяких Wi-Fi (Broadcom). Тут - як дізнатись, що за залізо, як поставити драйвер
правильно, що таке Secure Boot і MOK, і що робити, якщо після драйвера чорний екран.

## Коротко

**Драйвер** - програма, яка вчить ядро Linux працювати з пристроєм. У Linux майже всі драйвери вже лежать у ядрі
у вигляді **модулів** (шматків ядра, що підвантажуються, коли треба). **Прошивка** (firmware) - маленька програма,
яку ядро завантажує всередину пристрою (Wi-Fi, відеокарта, Bluetooth). Прошивки лежать у пакеті `linux-firmware`
і оновлюються разом із системою. Прошивку самого ноутбука (BIOS/UEFI, тачпад, SSD) оновлює `fwupdmgr` (урок 02).

```text
Intel / AMD (відео, Wi-Fi)  → драйвер уже в ядрі, прошивка в linux-firmware → нічого не роби
NVIDIA                      → «Керування драйверами» → рекомендований драйвер → перезавантаження
Broadcom Wi-Fi              → «Керування драйверами» (може попросити інтернет або live USB)
```

| Команда | Що показує |
|---|---|
| `inxi -G` | відеокарта(и) і який драйвер працює |
| `inxi -Fxz` | вся система коротко; `z` ховає MAC-адреси і серійні номери - для форуму |
| `lspci -k` | пристрої на шині PCI і рядок `Kernel driver in use` - драйвер, що працює зараз |
| `lsusb` | USB-пристрої (вебкамера, USB Wi-Fi, Bluetooth часто тут) |
| `rfkill list` | чи не вимкнено Wi-Fi/Bluetooth програмно (Soft) або кнопкою (Hard) |
| `nvidia-smi` | чи працює драйвер NVIDIA (лише після його встановлення) |
| `dkms status` | які модулі DKMS зібрані і під які ядра |
| `mokutil --sb-state` | чи увімкнено Secure Boot |
| `driver-manager` | програма «Керування драйверами» (те саме, що з меню) |

**«Керування драйверами»** (англійською Driver Manager, у старих статтях «Менеджер драйверів»): Меню → Адміністрування →
Керування драйверами. Пароль програма спитає, коли застосовуватимеш зміни (ставить пакети через PackageKit, з коду
mintdrivers 1.8.8). Назви в програмі (з українського перекладу mintdrivers 1.8.8):

```text
Пристрій
 ( ) nvidia-driver-580-open (рекомендовані)      ← позначка зеленим
 ( ) nvidia-driver-570 ...
 ( ) Не використовувати пристрій                 ← вільний драйвер nouveau, що вже в ядрі
                                  [По_вернути]  [Застосувати зміни]
Після встановлення: «Потрібно перезавантажити комп'ютер...»  [Перезавантажити...]
```

(Номери версій тут - приклад, у тебе буде список під твою карту.)

- **NVIDIA і `-open`.** У коді Driver Manager (1.8.8) правило таке: для драйверів від версії **560** перевага
  відкритому модулю ядра (`-open`), закритий тоді не показується; до 560 - навпаки, показується закритий. Серверні
  драйвери (`-server`) не показуються зовсім. Тобто бери той, що з позначкою «рекомендовані».
- **Старі карти.** Для GTX 10xx (Pascal) остання гілка - 580 (r/linuxmint, 26.10.2026; офіційно не перевірено).
  Відкритий модуль NVIDIA працює лише з картами Turing (GTX 16xx / RTX 20xx) і новішими (README NVIDIA
  open-gpu-kernel-modules), тому для старіших карт бери закритий драйвер, який покаже Driver Manager.
- **Без інтернету.** Програма напише «Схоже, що ви не в мережі» і «Підключіться до інтернету чи вставте інсталяційний
  диск Linux Mint (або USB-накопичувач)». Встав live USB, з якого ставив Mint, натисни «Змонтувати інсталяційний
  носій» - флешка стане тимчасовим джерелом пакетів (скрипт `mintdrivers-add-live-media` додає її в apt).

**Secure Boot** - функція UEFI (сучасного BIOS): комп'ютер запускає лише підписані програми. Ядро Mint
(Ubuntu 6.14 з ISO 22.3) зібране з `CONFIG_LOCK_DOWN_IN_SECURE_BOOT=y`: коли Secure Boot увімкнено, ядро вантажить
лише **підписані** модулі. Модуль, який **DKMS** (Dynamic Kernel Module Support - система, що збирає модуль драйвера
на твоєму комп'ютері під кожне нове ядро) зібрав у тебе, ніхто не підписав. Тому:

```text
DKMS збирає модуль → підписує твоїм ключем MOK (Machine Owner Key, «ключ власника»)
                  → ключ треба один раз занести в UEFI:
   1. при встановленні драйвера тебе просять придумати пароль (8-16 символів)
   2. перезавантаження → синій екран MOK Manager → «Enroll MOK» → підтвердити → ввести той самий пароль
   3. далі Mint вантажить драйвер і з Secure Boot
Пропустив синій екран (не встиг) → система стартує, але без драйвера (часто чорний екран на NVIDIA)
```

Вручну запросити занесення ключа ще раз: `sudo update-secureboot-policy --enroll-key` і перезавантажитись.
Пароль 8-16 символів і назви «Enroll MOK», «Change Secure Boot state» - з пакета `shim-signed` (Ubuntu 24.04).
Чи сам Driver Manager показує це вікно - не перевірено (у коді Driver Manager 1.8.8 нема нічого про Secure Boot;
питання ставить пакет драйвера). Ubuntu має й готові підписані модулі NVIDIA (`linux-modules-nvidia-580-generic`) -
з ними MOK не потрібен. Який варіант поставить Driver Manager - не перевірено на залізі; дізнаєшся командою
`dkms status` (якщо там є `nvidia` - це DKMS).

## Передбач, потім запусти

1. На ноутбуці з двома відеокартами (Intel + NVIDIA) або у віртуальній машині ти шукаєш відеокарту так:

```bash
lspci -k | grep -A3 -i vga
```

Що буде, якщо карта записана як «3D controller»?

<details markdown="1"><summary>Відповідь</summary>

Нічого не надрукує (код виходу 1), бо `grep -i vga` шукає слово «VGA», а його в рядку нема. У тестовій системі
курсу саме так: там лише `3D controller`. Шукай обидва слова (`-E` - кілька варіантів через `|`, `-A3` - ще 3 рядки
після збігу):

```bash
lspci -k | grep -A3 -iE "vga|3d"
```

Приклад для ноутбука з Intel і NVIDIA (**у тебе буде інше**: адреси, моделі, драйвери):

```text
00:02.0 VGA compatible controller: Intel Corporation ...
	Subsystem: ...
	Kernel driver in use: i915
	Kernel modules: i915
--
01:00.0 3D controller: NVIDIA Corporation ...
	Subsystem: ...
	Kernel driver in use: nouveau
	Kernel modules: nouveau
```

Intel - `VGA compatible controller` з `i915`, NVIDIA на ноутбуках з двома картами - `3D controller` з `nouveau`
(вільний драйвер) або `nvidia` (після встановлення). AMD - `amdgpu`. Рядок `--` grep ставить між шматками виводу.

</details>

2. Ти хочеш викласти опис системи на форум і боїшся показати MAC-адресу. Що `inxi` надрукує замість неї з ключем `z`?

```bash
inxi -c0 -Fxz
```

<details markdown="1"><summary>Відповідь</summary>

Слово `<filter>`. Справжній рядок з розділу Network (`-c0` - без кольорів):

```text
  IF-ID-1: eth0 state: up speed: 10000 Mbps duplex: full mac: <filter>
```

`z` фільтрує MAC-адреси, серійні номери, IP. Тому на форумах просять саме `inxi -Fxz` (або ще докладніше
`inxi -Fxxxz`, урок 26).

</details>

3. Що відповість `mokutil --sb-state` на комп'ютері, який завантажився у старому режимі BIOS (без UEFI)?

<details markdown="1"><summary>Відповідь</summary>

```text
EFI variables are not supported on this system
```

Код виходу 1 (справжній вивід mokutil 0.6.0 з тестової системи, де UEFI нема). На сучасному ноутбуці з UEFI буде
одне з двох: `SecureBoot enabled` або `SecureBoot disabled` (рядки з самої програми mokutil). Якщо «not supported» на
ноутбуці, що продавався з Windows 11, - Mint стоїть у режимі BIOS (Legacy/CSM), і Secure Boot там просто нема.

</details>

## Руками

**Крок 1. Подивись, що за залізо і які драйвери працюють.**

```bash
inxi -G
lspci -k | grep -A3 -iE "vga|3d"
inxi -Fxz
```

У тестовій системі курсу справжньої відеокарти нема, тому тут - **приклад для ноутбука** (у тебе будуть свої
моделі, версії й числа):

```text
Graphics:
  Device-1: Intel ... driver: i915 v: kernel
  Device-2: NVIDIA ... driver: nouveau v: kernel
  Display: x11 server: X.Org v: ... driver: X: loaded: modesetting ...
    resolution: 1920x1080~60Hz
  API: OpenGL v: 4.6 vendor: intel mesa v: ... renderer: Mesa Intel(R) ...
```

Дивись на `driver:` біля кожного `Device`:

```text
  Device-2: NVIDIA ... driver: nouveau      ← працює вільний драйвер, NVIDIA-драйвер ще не стоїть
  Device-2: NVIDIA ... driver: nvidia v: 580.xx   ← так після встановлення
```

`Display: x11` - сеанс X11, як і має бути в Mint 22.x (урок 13). Якщо в рядку OpenGL `renderer: llvmpipe` - 3D
малює процесор, а не відеокарта: драйвер не підхопився. На ноутбуці там має бути назва твоєї карти. `inxi` стоїть на
Mint одразу (є на ISO).

**Крок 2. Знімок, потім драйвер.** Перед драйвером - знімок (урок 01):

```bash
sudo timeshift --create --comments "перед драйвером"
driver-manager
```

Далі мишкою: вибери драйвер з позначкою «рекомендовані» → «Застосувати зміни» → дочекайся кінця →
«Перезавантажити...». Якщо Secure Boot увімкнено і з'явилось питання про пароль MOK - придумай пароль (8-16 символів,
латиницею) і **запиши на папірці**: через хвилину його треба ввести на синьому екрані.

**Крок 3. Після перезавантаження перевір.**

```bash
nvidia-smi
inxi -G
dkms status
mokutil --sb-state
```

- `nvidia-smi` малює табличку. Дивись верхній рядок `Driver Version: 580...` і назву карти в середині. Таблиця
  є - драйвер працює.
- `inxi -G` біля NVIDIA тепер має `driver: nvidia`.
- `dkms status` - рядок на кожне ядро, приклад (версії будуть інші):

```text
nvidia/580.xx.xx, 6.14.0-37-generic, x86_64: installed
```

  Порожньо - значить драйвер прийшов готовим підписаним модулем, а не через DKMS. Це теж нормально.

**Крок 4. Wi-Fi і Bluetooth.** Якщо Wi-Fi нема в аплеті мережі:

```bash
rfkill list
lspci -k | grep -A3 -i net
lsusb
```

`rfkill list` пише по блоку на кожен радіопристрій з рядками `Soft blocked` і `Hard blocked`:
- `Soft blocked: yes` - вимкнено програмно (режим «у літаку» або аплет). Увімкнути: `rfkill unblock wifi`
  (або `rfkill unblock bluetooth`).
- `Hard blocked: yes` - вимкнено кнопкою або Fn-клавішею на ноутбуці, або в BIOS. Команда не допоможе.

`lspci -k` для Wi-Fi показує `Network controller` і рядок `Kernel driver in use`. Нема цього рядка - драйвер не
підхопився, відкрий «Керування драйверами». Вбудований Bluetooth і USB Wi-Fi шукай у `lsusb`.
(У тестовій системі нема ні Wi-Fi, ні USB: там `rfkill` пише `cannot open /dev/rfkill: No such file or directory`.
На ноутбуці так не буде.)

**Крок 5. Прошивки.** Пакет `linux-firmware` оновлюється Диспетчером оновлень разом із системою. Прошивки BIOS,
тачпада, SSD - `fwupdmgr get-updates` і `fwupdmgr update` (урок 02, крок 4). Якщо ти вручну перевстановив пакет
прошивки або драйвера (так лагодили AMD RX 9060/9070 у листопаді 2026, урок 02), онови **initramfs** - маленький
стартовий образ, з якого ядро бере драйвери і прошивки ще до того, як змонтує диск:

```bash
sudo update-initramfs -u -k all
```

`-u` - оновити наявний образ, `-k all` - для всіх встановлених ядер (з довідки `update-initramfs`). Потім
`sudo reboot`.

**Крок 6. Чорний екран після драйвера** - не панікуй, система ціла:
1. Ctrl+Alt+F2 - текстовий вхід (TTY), логін і пароль як звичайно.
2. Відкотися знімком: `sudo timeshift --restore` (урок 01), або прибери драйвер за назвою пакета з `dkms status`
   чи `apt list --installed | grep nvidia-driver`.
3. Якщо навіть TTY не видно - у GRUB параметр `nomodeset`, старе ядро, live USB: урок 26.

## Типові помилки

- **`grep -i vga` нічого не знайшов** - карта записана як `3D controller`. Шукай `grep -A3 -iE "vga|3d"`.
- **`nvidia-smi: command not found`** (українською `nvidia-smi: команду не знайдено`; bash каже, що такої команди
  нема, на ноутбуці може ще підказати пакет; англійський текст для пошуку - `LC_ALL=C nvidia-smi`) -
  драйвер NVIDIA ще не встановлено, команда приходить разом з ним. Відкрий «Керування драйверами», а не став пакет з
  підказки навмання.
- **`Failed to initialize NVML: Driver/library version mismatch`** - драйвер оновився, а в пам'яті ще старий модуль.
  Рішення - перезавантаження (документація Ubuntu про NVIDIA).
- **`No devices were found`** у `nvidia-smi` - часто завантажено вільний `nouveau`, який конфліктує з драйвером
  NVIDIA. Перевір `lsmod | grep nouveau` (документація Ubuntu; на залізі не перевірено).
- **Після драйвера чорний екран, а Secure Boot увімкнено** - ти не підтвердив ключ на синьому екрані MOK. Зайди в
  TTY (Ctrl+Alt+F2), `sudo update-secureboot-policy --enroll-key`, `sudo reboot`, і цього разу на синьому екрані
  вибери «Enroll MOK» і введи пароль (r/linuxmint, 04.02.2026 і 04.12.2025).
- **Драйвер з сайту nvidia.com (файл `.run`)**. Ставить модуль повз apt: його ламає кожне оновлення ядра, і він
  «може зламати secure boot» (документація Ubuntu). Бери драйвер з «Керування драйверами».
- **Вимкнути Secure Boot «щоб не морочитись»** при подвійному завантаженні з Windows з BitLocker - Windows може
  попросити ключ відновлення BitLocker (48 цифр). Зміни завантаження і вимірювань TPM - у списку причин у статті
  Microsoft «BitLocker recovery overview»; на ноутбуці не перевірено. Перед будь-якими змінами в BIOS запиши ключ
  (урок 26).

## Як роблять профі

- **Знімок → драйвер з «Керування драйверами» → перезавантаження → `nvidia-smi`.** Гілку драйвера беруть під
  покоління карти: для GTX 10xx - 580 (r/linuxmint, 26.10.2026, 44 бали).
- **Secure Boot не вимикають, а заносять MOK** - так радять на r/linuxmint при чорному екрані після NVIDIA
  (04.02.2026, 04.12.2025).
- **Перед питанням на форумі** - вивід `inxi -Fxz` (Mint його має з коробки) і точний текст помилки. Без цього
  відповідь буде «а яка в тебе карта?».
- **Свіжий приклад, навіщо знімок і TTY:** 05.11.2026 пакет `linux-firmware-amd-graphics` зламав екран входу на
  AMD RX 9060/9070 (255 балів, 355 коментарів). Лагодили з TTY: `sudo apt update`,
  `sudo apt install linux-firmware-amd-graphics`, `sudo update-initramfs -u -k all`, `sudo reboot`.

## Самоперевірка

1. Що треба зробити з драйверами на ноутбуці з відео Intel і Wi-Fi Intel після встановлення Mint?
2. Чим драйвер відрізняється від прошивки?
3. Ти поставив драйвер NVIDIA, перезавантажився, і бачиш синій екран з англійським меню. Що робити?
4. Як перевірити, що драйвер NVIDIA справді працює?
5. Wi-Fi не видно. `rfkill list` пише `Soft blocked: yes`. Що це і як виправити?

<details markdown="1"><summary>Відповіді</summary>

1. Нічого. Драйвери Intel (і AMD) уже в ядрі, прошивки в `linux-firmware`. Можна відкрити «Керування драйверами» -
   там буде хіба мікрокод процесора.
2. Драйвер - частина ядра Linux, вона працює на процесорі ноутбука. Прошивка - програма, яку ядро завантажує
   всередину самого пристрою (Wi-Fi, відеокарти).
3. Це MOK Manager. Вибери «Enroll MOK», підтверди і введи пароль, який придумав при встановленні драйвера. Інакше
   при Secure Boot ядро не завантажить непідписаний модуль.
4. `nvidia-smi` показує таблицю з `Driver Version`, а `inxi -G` біля карти пише `driver: nvidia`.
5. Wi-Fi вимкнено програмно (режим «у літаку»). `rfkill unblock wifi` або вимкнути режим «у літаку» в аплеті.
   Якщо `Hard blocked: yes` - шукай кнопку чи Fn-клавішу з антеною.

</details>

## Джерела

- Посібник установки Mint, «Hardware drivers» - https://linuxmint-installation-guide.readthedocs.io/en/latest/drivers.html -
  відкрито 18.11.2026
- Код Driver Manager (mintdrivers 1.8.8, правило 560/-open, live USB) - https://github.com/linuxmint/mintdrivers -
  відкрито 18.11.2026 (файли пакета з репозиторію Mint прочитано в тестовій Mint 22.3)
- Документація Ubuntu, встановлення драйверів NVIDIA (Secure Boot, підписані модулі, помилки nvidia-smi) -
  https://ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/ - відкрито 18.11.2026
- Пакет `shim-signed` 1.58 (Ubuntu 24.04): скрипт `update-secureboot-policy` і тексти MOK - прочитано з пакета
  в тестовій Mint 22.3, 18.11.2026
- Конфіг ядра `linux-modules-6.14.0-37-generic` (ядро ISO 22.3, `CONFIG_LOCK_DOWN_IN_SECURE_BOOT=y`) - прочитано
  з пакета, 18.11.2026
- inxi - https://smxi.org/docs/inxi.htm - відкрито 18.11.2026
- NVIDIA open-gpu-kernel-modules, README (Turing і новіші) - https://github.com/NVIDIA/open-gpu-kernel-modules -
  відкрито 18.11.2026
- r/linuxmint: гілка NVIDIA під карту https://www.reddit.com/r/linuxmint/comments/1xfqxjj/ ; чорний екран і MOK
  https://www.reddit.com/r/linuxmint/comments/1qvd91v/ , https://www.reddit.com/r/linuxmint/comments/1pdtvew/ ;
  прошивка AMD і TTY https://www.reddit.com/r/linuxmint/comments/1xo6jg2/ - відкрито 18.11.2026
- `inxi`, `lspci`, `mokutil --sb-state`, `rfkill`, `update-initramfs` - перевірено запуском у тестовій Mint 22.3,
  18.11.2026 (вивід для ноутбука з Intel і NVIDIA - приклад, не запуск)
- BitLocker recovery overview (причини запиту ключа) -
  https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview -
  відкрито 18.11.2026
