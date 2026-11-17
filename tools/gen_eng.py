"""Генератор розділу «eng» (англійська, залік): пише content/eng/quiz.json і content/eng/slovnyk.md.

Запуск:
    python -P -E tools/gen_eng.py                 - записати quiz.json і slovnyk.md
    python -P -E tools/gen_eng.py --check [файл]  - звірити quiz.json (або копію) з даними тут

Джерела слів:
    U1   - фото «Word list Unit 1» 16.10 (1016_13.jpg)
    U2   - файл слів Unit 2 16.10 (1016_u2.docx)
    U3   - фото списку слів з поміткою «U3» 23.10 (1023_40.jpg).
           На фото лише слова, без значень - переклад узято найуживаніший, звір з текстом юніту.
    UNI  - текст презентації про TUM і LMU (тема «університет за кордоном», пара 25.09)
    PHYS - слова фізики і навчання для усних тем і анотації (не з підручника)
Неправильні дієслова: списку викладачки (57 дієслів) у файлах немає - тут стандартний список найуживаніших.
Граматика: Present Simple / Continuous (пара 25.09), verbs + to / -ing (роздатка 06.11),
V2 / V3 неправильних дієслів (ДЗ 16.10).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "eng"

SRC = {
    "U1": "Word list Unit 1 (16.10)",
    "U2": "Unit 2 (16.10)",
    "U3": "Unit 3 (23.10)",
    "UNI": "Презентація про університети TUM і LMU",
    "PHYS": "Слова фізики і навчання (для усних тем і анотації)",
}

# тег | слово | переклад (як показувати) | прийнятні переклади через ; | приклад EN | переклад прикладу
VOCAB_RAW = """
U1|armchair|крісло|крісло|I like reading in the armchair by the window.|Я люблю читати в кріслі біля вікна.
U1|balcony|балкон|балкон|Our flat has a small balcony.|У нашій квартирі є маленький балкон.
U1|bell|дзвоник, дзвін|дзвоник;дзвін;дзвінок|Press the bell, and somebody will open the door.|Натисни на дзвоник, і хтось відчинить двері.
U1|belong|почуватися своїм (belong to - належати)|належати;бути своїм;почуватися своїм|After a month at the faculty I feel that I belong here.|Через місяць на факультеті я відчуваю, що я тут свій.
U1|blanket|ковдра|ковдра;плед|It is cold, so I need a warm blanket.|Холодно, тому мені потрібна тепла ковдра.
U1|bulb|лампочка|лампочка;лампа|The bulb in the corridor doesn't work.|Лампочка в коридорі не працює.
U1|cave|печера|печера|People lived in caves thousands of years ago.|Тисячі років тому люди жили в печерах.
U1|chest of drawers|комод|комод|I keep my clothes in a chest of drawers.|Я тримаю одяг у комоді.
U1|consist (of)|складатися (з)|складатися;складатися з|Water consists of hydrogen and oxygen.|Вода складається з водню і кисню.
U1|contain|містити|містити;вміщати|This box contains old lab equipment.|У цій коробці старе лабораторне обладнання.
U1|cooker|кухонна плита|плита;кухонна плита|We have a gas cooker in the kitchen.|У нас на кухні газова плита.
U1|corridor|коридор|коридор|The physics labs are at the end of the corridor.|Фізичні лабораторії в кінці коридору.
U1|cosy|затишний|затишний|My room is small but cosy.|Моя кімната маленька, але затишна.
U1|cottage|будиночок за містом, котедж|котедж;будиночок;дача|My grandparents live in a cottage in the countryside.|Мої бабуся й дідусь живуть у будиночку в селі.
U1|cushion|диванна подушка|диванна подушка;подушка|There are two cushions on the sofa.|На дивані дві подушки.
U1|design|дизайн, задум, конструкція|дизайн;задум;конструкція;проєкт|I like the design of this building.|Мені подобається дизайн цієї будівлі.
U1|exist|існувати|існувати|Do you think life exists on other planets?|Як ти думаєш, чи існує життя на інших планетах?
U1|fridge|холодильник|холодильник|Put the milk in the fridge.|Постав молоко в холодильник.
U1|guess|вгадувати, припускати|вгадувати;вгадати;припускати|Can you guess my age?|Можеш вгадати мій вік?
U1|improve|покращувати, покращуватися|покращувати;покращуватися;покращити;поліпшувати;вдосконалювати|I want to improve my English.|Я хочу покращити свою англійську.
U1|include|включати|включати;містити|The price includes breakfast.|Ціна включає сніданок.
U1|matter|мати значення|мати значення;важити|It doesn't matter if you are late, just come.|Не має значення, що ти запізнишся, просто приходь.
U1|microwave|мікрохвильовка|мікрохвильовка;мікрохвильова піч;мікрохвильовка піч|I heat my lunch in the microwave.|Я грію обід у мікрохвильовці.
U1|mirror|дзеркало|дзеркало|Practise your speech in front of a mirror.|Тренуй виступ перед дзеркалом.
U1|own|володіти, мати (своє)|володіти;мати|My uncle owns a small shop.|Мій дядько має невеликий магазин.
U1|pillow|подушка (для сну)|подушка|I can't sleep without my pillow.|Я не можу спати без своєї подушки.
U1|relax|відпочивати, розслаблятися|відпочивати;розслаблятися;відпочити|After the exam I want to relax.|Після іспиту я хочу відпочити.
U1|remain|залишатися|залишатися;лишатися|Please remain in your seats.|Будь ласка, залишайтеся на своїх місцях.
U1|right (adv)|саме, якраз, прямо|саме;якраз;прямо|The bus stop is right in front of the faculty.|Зупинка якраз навпроти факультету.
U1|sink|мийка, раковина (на кухні)|мийка;раковина|Put the dirty plates in the sink.|Постав брудні тарілки в мийку.
U1|suppose|припускати, гадати|припускати;гадати;вважати|I suppose the test will be difficult.|Гадаю, тест буде важкий.
U1|tap|кран|кран|Turn off the tap, please.|Закрий кран, будь ласка.
U1|tidy|прибирати, наводити лад|прибирати;прибрати;наводити лад|I tidy my room every Saturday.|Я прибираю свою кімнату щосуботи.
U1|upstairs|нагорі, нагору|нагорі;нагору;на верхньому поверсі|The library is upstairs, on the third floor.|Бібліотека нагорі, на третьому поверсі.
U1|washbasin|умивальник|умивальник;раковина|There is a washbasin in every room.|У кожній кімнаті є умивальник.
U1|windmill|вітряк, вітряний млин|вітряк;вітряний млин;млин|Old windmills were used for crushing grain.|Старі вітряки використовували, щоб молоти зерно.
U2|apologise|вибачатися|вибачатися;перепрошувати;вибачитися|I apologised to the teacher for being late.|Я вибачився перед викладачкою за запізнення.
U2|canteen|їдальня|їдальня|We have lunch in the university canteen.|Ми обідаємо в університетській їдальні.
U2|earn a wage|заробляти (гроші, зарплату)|заробляти;заробляти гроші;заробляти зарплату;отримувати зарплату|Many students work in the evening to earn a wage.|Багато студентів працюють увечері, щоб заробляти гроші.
U2|explain|пояснювати|пояснювати;пояснити|Can you explain this rule again?|Можете пояснити це правило ще раз?
U2|fail an exam|не скласти іспит, провалити іспит|провалити іспит;не скласти іспит;завалити іспит|He failed the exam because he didn't study.|Він не склав іспит, бо не вчився.
U2|have fun|добре проводити час, розважатися|розважатися;добре проводити час;веселитися|We had fun at the student party.|Ми добре провели час на студентській вечірці.
U2|invite|запрошувати|запрошувати;запросити|I want to invite my friends to my birthday party.|Я хочу запросити друзів на день народження.
U2|learn|вчити, вивчати, дізнаватися|вчити;вивчати;дізнаватися;навчитися|I learn ten new words every day.|Я вчу десять нових слів щодня.
U2|lose|губити, загубити|губити;загубити;втратити;програвати|Don't lose your student card!|Не загуби студентський квиток!
U2|make friends|заводити друзів, подружитися|заводити друзів;подружитися;знайомитися|It is easy to make friends at university.|В університеті легко знайти друзів.
U2|miss the bus|запізнитися на автобус|запізнитися на автобус;не встигнути на автобус;пропустити автобус|I missed the bus and came late.|Я запізнився на автобус і прийшов пізно.
U2|pass an exam|скласти іспит (успішно)|скласти іспит;здати іспит|I hope to pass all my exams in January.|Сподіваюся скласти всі іспити в січні.
U2|ring|дзвонити, дзвеніти|дзвонити;дзвеніти|The bell rings at the end of the class.|Дзвоник дзвенить у кінці пари.
U2|set off|вирушати (в дорогу)|вирушати;вирушити;вирушати в дорогу|We set off for the Carpathians early in the morning.|Ми вирушили в Карпати рано-вранці.
U2|spend time doing something|проводити час, роблячи щось|проводити час;витрачати час|I spend a lot of time doing my homework.|Я проводжу багато часу за домашнім завданням.
U2|study|вчитися, вивчати|вчитися;вивчати;навчатися|I study physics at Lviv University.|Я вивчаю фізику у Львівському університеті.
U2|suggest|пропонувати|пропонувати;запропонувати;радити|I suggest going to the library after classes.|Пропоную піти в бібліотеку після пар.
U2|take an exam|складати іспит (йти на іспит)|складати іспит;писати іспит;здавати іспит|We take our first exams in January.|Перші іспити ми складаємо в січні.
U2|take time to do something|робити щось не поспішаючи|не поспішати;робити не поспішаючи;приділити час|Take time to read the question carefully.|Не поспішай, уважно прочитай питання.
U3|admission fee|плата за вхід|плата за вхід;вхідна плата;вартість входу|The admission fee for students is 50 hryvnias.|Плата за вхід для студентів - 50 гривень.
U3|(can) afford|(могти) дозволити собі|дозволити собі;могти дозволити собі|I can't afford a new laptop this year.|Я не можу дозволити собі новий ноутбук цього року.
U3|art gallery|картинна галерея|картинна галерея;галерея;художня галерея|There is a famous art gallery in the centre of Lviv.|У центрі Львова є відома картинна галерея.
U3|backpack|рюкзак|рюкзак|I carry my laptop in a backpack.|Я ношу ноутбук у рюкзаку.
U3|book ahead|бронювати заздалегідь|бронювати заздалегідь;забронювати заздалегідь;бронювати наперед|You should book ahead, the hostel is very popular.|Краще забронювати заздалегідь, хостел дуже популярний.
U3|catch up with|наздогнати|наздогнати;наздоганяти|Go ahead, I'll catch up with you later.|Іди, я тебе потім наздожену.
U3|chess|шахи|шахи|My brother plays chess very well.|Мій брат дуже добре грає в шахи.
U3|cyclist|велосипедист|велосипедист|Cyclists must wear helmets.|Велосипедисти мусять носити шоломи.
U3|deal with|мати справу з, впоратися з|мати справу з;впоратися з;розбиратися з;займатися|I don't know how to deal with this problem.|Я не знаю, як впоратися з цією проблемою.
U3|diving|дайвінг, пірнання|дайвінг;пірнання;підводне плавання|Diving in the Red Sea is very popular.|Дайвінг у Червоному морі дуже популярний.
U3|feel like|хотіти, мати настрій (feel like doing)|хотіти;мати бажання;мати настрій|I don't feel like going out tonight.|Мені не хочеться нікуди йти сьогодні ввечері.
U3|formal|офіційний, формальний|офіційний;формальний|You need formal clothes for the interview.|На співбесіду потрібен офіційний одяг.
U3|get on with|ладнати з|ладнати з;ладнати;мати добрі стосунки|I get on well with my groupmates.|Я добре ладнаю з одногрупниками.
U3|give up|кинути (звичку), здатися|кинути;здатися;відмовитися;покинути|My father gave up smoking last year.|Мій тато кинув курити торік.
U3|go off|задзвонити (про будильник), зіпсуватися (про їжу)|задзвонити;спрацювати;зіпсуватися|My alarm clock went off at 6:30.|Мій будильник задзвонив о 6:30.
U3|go on|тривати, продовжуватися|продовжувати;продовжуватися;тривати;відбуватися|The lecture went on for two hours.|Лекція тривала дві години.
U3|healthy|здоровий, корисний для здоров'я|здоровий;корисний|Swimming is a healthy hobby.|Плавання - корисне для здоров'я хобі.
U3|helmet|шолом|шолом|Always wear a helmet when you ride a bike.|Завжди вдягай шолом, коли їдеш на велосипеді.
U3|instrument|(музичний) інструмент, прилад|інструмент;музичний інструмент;прилад|Do you play a musical instrument?|Ти граєш на якомусь музичному інструменті?
U3|join in|долучатися, брати участь|долучатися;приєднуватися;брати участь|Everyone joined in the game.|Усі долучилися до гри.
U3|look forward to|з нетерпінням чекати|з нетерпінням чекати;чекати з нетерпінням|I'm looking forward to the winter holidays.|Я з нетерпінням чекаю зимових канікул.
U3|make up for|надолужити, компенсувати|надолужити;компенсувати;відшкодувати|I missed a class, so I must make up for it.|Я пропустив пару, тож мушу це надолужити.
U3|mountain-biking|катання на гірському велосипеді|катання на гірському велосипеді;маунтенбайк;гірський велосипед|Mountain-biking in the Carpathians is great fun.|Кататися на гірському велосипеді в Карпатах дуже весело.
U3|opening hours|години роботи|години роботи;графік роботи;розклад роботи|What are the library's opening hours?|Які години роботи бібліотеки?
U3|oven|духовка|духовка;піч|Bake the cake in the oven for 40 minutes.|Печи торт у духовці 40 хвилин.
U3|patient|терплячий; пацієнт|терплячий;пацієнт|Our teacher is very patient with us.|Наша викладачка дуже терпляча з нами.
U3|put someone's name down|записати когось (у список)|записати;записати когось;записатися|I put my name down for the physics olympiad.|Я записався на олімпіаду з фізики.
U3|set out|вирушати (в дорогу)|вирушати;вирушити|They set out on their journey at dawn.|Вони вирушили в дорогу на світанку.
U3|sightseeing|огляд визначних місць|огляд визначних місць;екскурсія;огляд пам'яток|We went sightseeing in Munich.|Ми оглядали визначні місця Мюнхена.
U3|surfing|серфінг|серфінг|Surfing is popular in Australia.|Серфінг популярний в Австралії.
U3|take up|почати займатися (хобі, спортом)|почати займатися;взятися за;зайнятися|I want to take up chess.|Я хочу почати грати в шахи.
U3|tent|намет|намет|We slept in a tent in the mountains.|Ми спали в наметі в горах.
U3|turn into|перетворюватися на|перетворюватися на;перетворитися на;перетворювати на|Water turns into ice at 0 °C.|Вода перетворюється на лід при 0 °C.
U3|value|цінність, вартість; цінувати|цінність;вартість;цінувати|I value my free time.|Я ціную свій вільний час.
U3|water-skiing|катання на водних лижах|водні лижі;катання на водних лижах|Water-skiing is an expensive hobby.|Водні лижі - дороге хобі.
U3|work out|тренуватися; розібратися, розв'язати|тренуватися;розібратися;розв'язати;з'ясувати|I work out in the gym twice a week.|Я тренуюся в залі двічі на тиждень.
UNI|university|університет|університет|I study at Ivan Franko National University of Lviv.|Я навчаюся у Львівському національному університеті імені Івана Франка.
UNI|faculty|факультет|факультет|The Faculty of Physics was founded in 1953.|Фізичний факультет заснували в 1953 році.
UNI|campus|кампус, студмістечко|кампус;студмістечко;студентське містечко|Physics students study on the Garching campus.|Фізики навчаються в кампусі Гархінг.
UNI|main building|головний корпус|головний корпус;головна будівля|This is the main building of the university.|Це головний корпус університету.
UNI|tuition fee|плата за навчання|плата за навчання;оплата навчання|There are no tuition fees at LMU.|В LMU немає плати за навчання.
UNI|scholarship|стипендія|стипендія;грант|TUM has scholarships for international students.|У TUM є стипендії для іноземних студентів.
UNI|waiver|звільнення (від плати)|звільнення від плати;звільнення;пільга|There is a fee waiver for Ukrainian refugees.|Для українських біженців є звільнення від плати.
UNI|refugee|біженець|біженець;біженка|Many Ukrainian refugees study in Germany.|Багато українських біженців навчаються в Німеччині.
UNI|dormitory|гуртожиток|гуртожиток|A room in the dormitory costs about 400 euros per month.|Кімната в гуртожитку коштує близько 400 євро на місяць.
UNI|student union|студентська спілка|студентська спілка;студентська організація|The dormitories belong to the student union.|Гуртожитки належать студентській спілці.
UNI|separately|окремо|окремо|You pay for the dormitory separately.|За гуртожиток платиш окремо.
UNI|library|бібліотека|бібліотека|The library is free for all students.|Бібліотека безкоштовна для всіх студентів.
UNI|student card|студентський квиток|студентський квиток;студентський;студентська картка|The student card is also the library card.|Студентський квиток - це і читацький квиток.
UNI|semester|семестр|семестр|Students pay a semester fee of 97 euros.|Студенти платять семестровий внесок 97 євро.
UNI|bachelor's degree|ступінь бакалавра|ступінь бакалавра;бакалаврат;бакалавр|After four years I will get a bachelor's degree.|Через чотири роки я отримаю ступінь бакалавра.
UNI|master's program|магістерська програма|магістерська програма;магістратура|The master's program is in English.|Магістерська програма англійською.
UNI|graduate|випускник; закінчити (університет)|випускник;закінчити;закінчувати|Rudolf Diesel is a famous graduate of TUM.|Рудольф Дізель - відомий випускник TUM.
UNI|Nobel Prize winner|нобелівський лауреат|нобелівський лауреат;лауреат нобелівської премії|LMU has 51 Nobel Prize winners.|У LMU 51 нобелівський лауреат.
UNI|found (founded)|засновувати (заснований)|засновувати;заснувати;заснований|LMU was founded in 1472.|LMU заснували в 1472 році.
UNI|invent|винаходити|винаходити;винайти|Rudolf Diesel invented the diesel engine.|Рудольф Дізель винайшов дизельний двигун.
UNI|receive|отримувати|отримувати;отримати|Heisenberg received the Nobel Prize in 1932.|Гейзенберг отримав Нобелівську премію в 1932 році.
UNI|to sum up|отже, підсумовуючи|підсумовуючи;отже;коротко кажучи|To sum up, both universities are very good.|Отже, обидва університети дуже добрі.
UNI|international student|іноземний студент|іноземний студент;міжнародний студент|There are many international students at TUM.|У TUM багато іноземних студентів.
PHYS|quantum computer|квантовий комп'ютер|квантовий комп'ютер|A quantum computer uses qubits instead of bits.|Квантовий комп'ютер використовує кубіти замість бітів.
PHYS|qubit|кубіт|кубіт|A qubit can be 0 and 1 at the same time.|Кубіт може бути 0 і 1 одночасно.
PHYS|superposition|суперпозиція|суперпозиція|A qubit in superposition is both 0 and 1 until we measure it.|Кубіт у суперпозиції - це і 0, і 1, доки ми його не виміряємо.
PHYS|entanglement|заплутаність (квантова)|заплутаність;сплутаність;квантова заплутаність|Entanglement connects two qubits even when they are far apart.|Заплутаність пов'язує два кубіти, навіть коли вони далеко один від одного.
PHYS|measurement|вимірювання|вимірювання;вимір|Every measurement has an error.|Кожне вимірювання має похибку.
PHYS|error|похибка, помилка|похибка;помилка|We calculated the error of the measurement.|Ми обчислили похибку вимірювання.
PHYS|experiment|експеримент, дослід|експеримент;дослід|We did an experiment with a pendulum.|Ми провели дослід з маятником.
PHYS|laboratory (lab)|лабораторія|лабораторія|First-year students work in the lab every week.|Першокурсники працюють у лабораторії щотижня.
PHYS|lab report|звіт з лабораторної|звіт з лабораторної;звіт;лабораторний звіт|I have to write a lab report by Monday.|Мені треба написати звіт з лабораторної до понеділка.
PHYS|lecture|лекція|лекція|The lecture on mechanics starts at 8:30.|Лекція з механіки починається о 8:30.
PHYS|practical class|практичне заняття|практичне заняття;практична;практика|At the practical class we solve problems.|На практичному занятті ми розв'язуємо задачі.
PHYS|timetable|розклад|розклад|Our timetable is different on odd and even weeks.|Наш розклад різний на чисельник і знаменник.
PHYS|credit test|залік|залік|In the first semester we have a credit test in English, not an exam.|У першому семестрі з англійської в нас залік, а не іспит.
PHYS|homework|домашнє завдання|домашнє завдання;домашка;дз|Our homework is to learn the words of Unit 3.|Наше домашнє завдання - вивчити слова юніту 3.
PHYS|group leader|староста|староста|The group leader collects our homework.|Староста збирає наші домашні завдання.
PHYS|annotation|анотація|анотація|I have to write an annotation to an article.|Мені треба написати анотацію до статті.
PHYS|research|дослідження; досліджувати|дослідження;досліджувати|Research in quantum physics is very expensive.|Дослідження в квантовій фізиці дуже дорогі.
PHYS|physicist|фізик|фізик|Max Planck was a German physicist.|Макс Планк був німецьким фізиком.
PHYS|quantum mechanics|квантова механіка|квантова механіка|Heisenberg is one of the fathers of quantum mechanics.|Гейзенберг - один із батьків квантової механіки.
PHYS|particle|частинка|частинка;частка|An electron is a very small particle.|Електрон - дуже маленька частинка.
PHYS|wavelength|довжина хвилі|довжина хвилі|Blue light has a shorter wavelength than red light.|Синє світло має меншу довжину хвилі, ніж червоне.
PHYS|scatter|розсіювати|розсіювати;розсіюватися|Air molecules scatter blue light more than red light.|Молекули повітря розсіюють синє світло сильніше, ніж червоне.
PHYS|algorithm|алгоритм|алгоритм|A quantum algorithm can solve some problems much faster.|Квантовий алгоритм може розв'язати деякі задачі набагато швидше.
PHYS|programming|програмування|програмування|This semester we are studying programming.|Цього семестру ми вивчаємо програмування.
PHYS|equation|рівняння|рівняння|Write down the equation of motion.|Запишіть рівняння руху.
PHYS|solve a problem|розв'язати задачу|розв'язати задачу;розв'язувати задачу|It took me an hour to solve this problem.|Мені знадобилася година, щоб розв'язати цю задачу.
"""

# V1 | V2 | V3 | переклад  (стандартний список найуживаніших; НЕ список викладачки)
VERBS_RAW = """
be|was / were|been|бути
become|became|become|ставати
begin|began|begun|починати
break|broke|broken|ламати
bring|brought|brought|приносити
build|built|built|будувати
buy|bought|bought|купувати
catch|caught|caught|ловити, встигнути (на транспорт)
choose|chose|chosen|обирати
come|came|come|приходити
cost|cost|cost|коштувати
cut|cut|cut|різати
deal|dealt|dealt|мати справу (deal with)
do|did|done|робити
draw|drew|drawn|малювати
drink|drank|drunk|пити
drive|drove|driven|керувати (авто), їхати
eat|ate|eaten|їсти
fall|fell|fallen|падати
feel|felt|felt|відчувати
find|found|found|знаходити
fly|flew|flown|літати
forget|forgot|forgotten|забувати
get|got|got|отримувати, діставатися
give|gave|given|давати
go|went|gone|йти, їхати
grow|grew|grown|рости, вирощувати
have|had|had|мати
hear|heard|heard|чути
keep|kept|kept|тримати, зберігати
know|knew|known|знати
learn|learnt / learned|learnt / learned|вчити, дізнаватися
leave|left|left|залишати, їхати звідкись
lend|lent|lent|позичати (комусь)
let|let|let|дозволяти
lose|lost|lost|губити, програвати
make|made|made|робити, виготовляти
mean|meant|meant|означати
meet|met|met|зустрічати
pay|paid|paid|платити
put|put|put|класти
read|read|read|читати
ring|rang|rung|дзвонити, дзвеніти
run|ran|run|бігти
say|said|said|сказати
see|saw|seen|бачити
sell|sold|sold|продавати
send|sent|sent|надсилати
set|set|set|ставити, встановлювати (set off, set out)
show|showed|shown|показувати
sing|sang|sung|співати
sit|sat|sat|сидіти
sleep|slept|slept|спати
speak|spoke|spoken|розмовляти
spend|spent|spent|витрачати, проводити (час)
stand|stood|stood|стояти
swim|swam|swum|плавати
take|took|taken|брати
teach|taught|taught|навчати
tell|told|told|розповідати
think|thought|thought|думати
understand|understood|understood|розуміти
wear|wore|worn|носити (одяг)
win|won|won|перемагати
write|wrote|written|писати
"""


def parse_vocab():
    out = []
    for line in VOCAB_RAW.strip().splitlines():
        p = [x.strip() for x in line.split("|")]
        assert len(p) == 6, line
        tag, en, ua, acc, ex, exua = p
        out.append({"tag": tag, "en": en, "ua": ua, "acc": [a.strip() for a in acc.split(";") if a.strip()],
                    "ex": ex, "exua": exua})
    return out


def parse_verbs():
    out = []
    for line in VERBS_RAW.strip().splitlines():
        p = [x.strip() for x in line.split("|")]
        assert len(p) == 4, line
        out.append({"v1": p[0], "v2": p[1], "v3": p[2], "ua": p[3]})
    return out


VOCAB = parse_vocab()
VERBS = parse_verbs()
VD = {w["en"]: w for w in VOCAB}
VBD = {v["v1"]: v for v in VERBS}

# Роздатка 06.11 «Verbs followed by to or -ing» - списки дослівно
ING_VERBS = ["admit", "avoid", "dislike", "enjoy", "fancy", "feel like", "finish", "forget", "hate", "imagine",
             "look forward to", "mention", "mind", "miss", "practise", "put off", "suggest"]
TO_VERBS = ["afford", "agree", "appear", "attempt", "begin", "decide", "demand", "expect", "fail", "hope", "intend",
            "learn", "manage", "offer", "plan", "pretend", "promise", "refuse", "seem", "want", "would like"]
BOTH_VERBS = ["begin", "continue", "forget", "hate", "like", "love", "prefer", "remember", "start"]

# ---------- питання ----------
EN_UA = ["armchair", "blanket", "chest of drawers", "cosy", "fridge", "improve", "mirror", "pillow", "tap",
         "upstairs", "apologise", "canteen", "earn a wage", "fail an exam", "make friends", "miss the bus",
         "set off", "suggest", "admission fee", "book ahead", "deal with", "get on with", "give up",
         "look forward to", "opening hours", "dormitory", "tuition fee"]

# (UA підказка, слово з VOCAB, прийнятні англійські варіанти)
UA_EN = [
    ("дзеркало", "mirror", ["mirror", "a mirror"]),
    ("холодильник", "fridge", ["fridge", "refrigerator", "a fridge"]),
    ("кран (з водою)", "tap", ["tap", "a tap", "faucet"]),
    ("вибачатися", "apologise", ["apologise", "apologize", "to apologise", "to apologize"]),
    ("їдальня (в університеті, на заводі)", "canteen", ["canteen", "a canteen", "the canteen"]),
    ("скласти іспит (успішно)", "pass an exam", ["pass an exam", "pass the exam", "pass exam", "to pass an exam"]),
    ("провалити іспит", "fail an exam", ["fail an exam", "fail the exam", "fail exam", "to fail an exam"]),
    ("вирушати в дорогу (2 слова, U2)", "set off", ["set off", "to set off"]),
    ("запрошувати", "invite", ["invite", "to invite"]),
    ("шолом", "helmet", ["helmet", "a helmet"]),
    ("намет", "tent", ["tent", "a tent"]),
    ("рюкзак", "backpack", ["backpack", "a backpack", "rucksack"]),
    ("гуртожиток", "dormitory", ["dormitory", "dorm", "a dormitory", "the dormitory"]),
    ("стипендія (грант на навчання)", "scholarship", ["scholarship", "a scholarship"]),
    ("плата за навчання", "tuition fee", ["tuition fee", "tuition fees", "tuition"]),
    ("з нетерпінням чекати (чогось)", "look forward to", ["look forward to", "to look forward to", "look forward"]),
    ("ладнати з (кимось)", "get on with", ["get on with", "get along with", "get on"]),
    ("кинути (звичку), здатися", "give up", ["give up", "to give up"]),
]

# (дієслово, яка форма: 2 або 3)
VERB_Q = [("go", 2), ("take", 3), ("write", 2), ("write", 3), ("begin", 3), ("bring", 2), ("buy", 3),
          ("teach", 2), ("think", 2), ("speak", 3), ("choose", 2), ("lose", 2), ("spend", 3), ("ring", 3),
          ("know", 3), ("leave", 2), ("forget", 3)]

# граматика: (тема, питання, правильний, [неправильні], пояснення, джерело)
T_PS = "Present Simple чи Continuous"
T_TO = "Verbs + to чи -ing"
T_PAST = "V2 і V3 неправильних дієслів"
T_VOC = "Слова юнітів у реченні"
SRC_PS = "пара 25.09, Present Simple і Continuous"
SRC_TO = "роздатка 06.11 Verbs followed by to or -ing"
SRC_PAST = "ДЗ 16.10: неправильні дієслова"

GRAMMAR = [
    (T_PS, "Water ___ at 100 °C.", "boils", ["is boiling", "boil", "boiling"],
     "Закон природи, істина - Present Simple. water = it, тому -s: boils.", SRC_PS),
    (T_PS, "Listen! Somebody ___ in the corridor.", "is singing", ["sings", "sing", "singed"],
     "Listen! = просто зараз - Present Continuous: is + singing.", SRC_PS),
    (T_PS, "I ___ the answer to this question.", "know", ["am knowing", "knows", "is knowing"],
     "know - дієслово стану, у Continuous не буває. I + know без -s.", SRC_PS),
    (T_PS, "This semester we ___ mechanics and molecular physics.", "are studying", ["study", "is studying", "studies"],
     "This semester = тимчасово, на цей період - Present Continuous. we → are.", SRC_PS),
    (T_PS, "Our English class ___ at 13:30 on Wednesdays.", "starts", ["is starting", "start", "starting"],
     "Розклад - Present Simple (на парі 25.09: timetables and schedules - Present Simple). class = it → starts.", SRC_PS),
    (T_PS, "___ she usually ___ to the university by tram?", "Does ... go", ["Is ... going", "Do ... go", "Does ... goes"],
     "usually = звичка - Present Simple. she → does, а після does дієслово без -s: go.", SRC_PS),
    (T_PS, "I ___ my group leader tomorrow at 5 pm, we have already agreed.", "am meeting", ["meet", "meets", "will meeting"],
     "Домовлена зустріч у майбутньому - Present Continuous (так казали на парі 25.09).", SRC_PS),
    (T_PS, "He ___ coffee. He prefers tea.", "doesn't like", ["isn't liking", "don't like", "not likes"],
     "like - дієслово стану, Continuous не буває. he → doesn't + like (без -s).", SRC_PS),
    (T_PS, "Why ___ you ___ the milk? Is it bad?", "are ... smelling", ["do ... smell", "does ... smell", "is ... smelling"],
     "smell тут = нюхати, це дія просто зараз - Continuous. you → are. Приклад з пари 25.09.", SRC_PS),
    (T_TO, "I enjoy ___ physics problems.", "solving", ["to solve", "solve"],
     "enjoy - зі списку 1 роздатки (+ -ing): enjoy solving.", SRC_TO, "enjoy"),
    (T_TO, "We decided ___ a taxi.", "to take", ["taking", "take"],
     "decide - зі списку 2 (+ to infinitive): decided to take.", SRC_TO, "decide"),
    (T_TO, "I'm looking forward to ___ you.", "seeing", ["see", "to see"],
     "look forward to - зі списку 1. Тут to - прийменник, після нього -ing: to seeing.", SRC_TO, "look forward to"),
    (T_TO, "He suggested ___ to the library.", "going", ["to go", "go"],
     "suggest - зі списку 1 (+ -ing): suggested going. Помилка українців - suggested to go.", SRC_TO, "suggest"),
    (T_TO, "I can't afford ___ a new phone.", "to buy", ["buying", "buy"],
     "afford - зі списку 2. Приклад з роздатки: I can't afford to buy a bike.", SRC_TO, "afford"),
    (T_TO, "She refused ___ the question.", "to answer", ["answering", "answer"],
     "refuse - зі списку 2 (+ to): refused to answer.", SRC_TO, "refuse"),
    (T_TO, "Do you mind ___ the window?", "opening", ["to open", "open"],
     "mind - зі списку 1 (+ -ing): mind opening.", SRC_TO, "mind"),
    (T_TO, "I would like ___ in Germany.", "to study", ["studying", "study"],
     "would like - зі списку 2 (+ to): would like to study. Не плутай з like, де можна обидва.", SRC_TO, "would like"),
    (T_TO, "They managed ___ the experiment on time.", "to finish", ["finishing", "finish"],
     "manage - зі списку 2 (+ to): managed to finish.", SRC_TO, "manage"),
    (T_TO, "Do you fancy ___ to the cinema tonight?", "going", ["to go", "go"],
     "fancy - зі списку 1 (+ -ing): fancy going.", SRC_TO, "fancy"),
    (T_TO, "We expect ___ the lab work by Friday.", "to finish", ["finishing", "finish"],
     "expect - зі списку 2. Приклад з роздатки: We expected to win the game.", SRC_TO, "expect"),
    (T_TO, "Which sentence is WRONG?", "I want going home.", ["It started raining.", "It started to rain.", "I love playing tennis."],
     "want - лише + to: I want to go home. start і love - зі списку 3, з ними можна і to, і -ing.", SRC_TO),
    (T_PAST, "Did you ___ to the lab yesterday?", "go", ["went", "gone", "goes"],
     "Після did - перша форма (V1). Минуле вже показує did, тому не went.", SRC_PAST),
    (T_PAST, "I have already ___ my lab report.", "written", ["wrote", "write", "writed"],
     "have + третя форма (V3): write - wrote - written.", SRC_PAST),
    (T_PAST, "They ___ the exam last week.", "took", ["taken", "take", "taked"],
     "last week - Past Simple, друга форма (V2): take - took - taken.", SRC_PAST),
    (T_PAST, "I ___ my student card yesterday and still can't find it.", "lost", ["losed", "lose", "have lost"],
     "yesterday - Past Simple, V2: lose - lost - lost. Present Perfect з yesterday не вживають.", SRC_PAST),
    (T_PAST, "LMU ___ in 1472.", "was founded", ["founded", "was found", "is founded"],
     "Пасив у минулому: was + V3. found (засновувати) - founded - founded; found без -ed - це минуле від find (знаходити).",
     "текст презентації TUM і LMU"),
    (T_VOC, "Я склав іспит (успішно) = I ___ the exam.", "passed", ["took", "failed", "gave"],
     "pass an exam - скласти успішно. take an exam - лише складати (йти на іспит), fail - провалити. Слова U2.", "U2"),
    (T_VOC, "My alarm clock ___ at 6:30, but I didn't get up.", "went off", ["went on", "set off", "gave up"],
     "go off - задзвонити (про будильник). went on - тривав, set off - вирушив, gave up - кинув. Слова U3.", "U3"),
    (T_VOC, "I missed two classes, so now I have to ___ them.", "make up for", ["take up", "turn into", "join in"],
     "make up for - надолужити, компенсувати. take up - почати займатися хобі. Слова U3.", "U3"),
    (T_VOC, "Water ___ of hydrogen and oxygen.", "consists", ["contains", "includes", "belongs"],
     "consist of - складатися з. contains of так не кажуть. Слова U1.", "U1"),
]

NORM = re.compile(r"[^\w' ]+", re.U)


def norm(s):
    s = s.lower().replace("’", "'").replace("ʼ", "'")
    s = NORM.sub(" ", s)
    return " ".join(s.split())


def build_questions():
    qs = []
    n = 0

    def add(q):
        nonlocal n
        n += 1
        q = {"id": f"eng-{n:03d}", **q}
        qs.append(q)

    for en in EN_UA:
        w = VD[en]
        add({"topic": f"Слова {w['tag']}" if w["tag"].startswith("U") else "Слова: університет",
             "type": "short", "q": f"Переклади українською: «{en}»",
             "answer": w["acc"][0], "accept": w["acc"],
             "explain": f"{en} - {w['ua']}. Приклад: {w['ex']} - {w['exua']}",
             "src": SRC[w["tag"]]})
    for ua, en, acc in UA_EN:
        w = VD[en]
        add({"topic": f"Слова {w['tag']}" if w["tag"].startswith("U") else "Слова: університет",
             "type": "short", "q": f"Як англійською: «{ua}»?",
             "answer": acc[0], "accept": acc,
             "explain": f"{en} - {w['ua']}. Приклад: {w['ex']} - {w['exua']}",
             "src": SRC[w["tag"]]})
    for v1, form in VERB_Q:
        v = VBD[v1]
        ans = v["v2"] if form == 2 else v["v3"]
        acc = [a.strip() for a in ans.split("/")]
        name = "друга форма (V2, Past Simple)" if form == 2 else "третя форма (V3, Past Participle)"
        add({"topic": "Неправильні дієслова", "type": "short",
             "q": f"{v1} ({v['ua']}): {name}?",
             "answer": acc[0], "accept": acc,
             "explain": f"{v1} - {v['v2']} - {v['v3']} ({v['ua']}).",
             "src": "ДЗ 16.10: неправильні дієслова (стандартний список)"})
    for i, g in enumerate(GRAMMAR):
        topic, q, right, wrong, expl, src = g[:6]
        opts = [right] + list(wrong)
        k = i % len(opts)  # правильний варіант не завжди перший
        opts = opts[k:] + opts[:k]
        add({"topic": topic, "type": "single", "q": q, "options": opts,
             "answer": opts.index(right), "explain": expl, "src": src})
    return qs


def self_check(qs):
    """Перевірки, незалежні від того, як питання записано у файл."""
    errs = []
    ids = [q["id"] for q in qs]
    if len(ids) != len(set(ids)):
        errs.append("дублікати id")
    for q in qs:
        if q["type"] == "short":
            if norm(q["answer"]) not in {norm(a) for a in q["accept"]}:
                errs.append(f"{q['id']}: answer «{q['answer']}» нема в accept")
        if q["type"] == "single":
            if not (0 <= q["answer"] < len(q["options"])):
                errs.append(f"{q['id']}: індекс поза варіантами")
    # verb + to / -ing: правильний варіант мусить відповідати списку роздатки
    for g in GRAMMAR:
        if len(g) < 7:
            continue
        verb, right = g[6], g[2]
        if verb in ING_VERBS and not right.endswith("ing"):
            errs.append(f"«{g[1]}»: {verb} зі списку -ing, а відповідь {right}")
        if verb in TO_VERBS and not right.startswith("to "):
            errs.append(f"«{g[1]}»: {verb} зі списку to, а відповідь {right}")
        if verb not in ING_VERBS and verb not in TO_VERBS:
            errs.append(f"«{g[1]}»: {verb} нема в списках 1-2 роздатки")
    # неправильні дієслова: V2/V3 не закінчуються на -ed, крім learned і showed (show - showed - shown)
    for v in VERBS:
        for f in (v["v2"], v["v3"]):
            for x in f.split("/"):
                x = x.strip()
                if x.endswith("ed") and x not in ("learned", "showed"):
                    errs.append(f"{v['v1']}: підозріла форма {x}")
    for b in ("\u2014", "\u2013", "$" + "$", "\\" + "frac", "begin" + "{"):
        if b in VOCAB_RAW or b in VERBS_RAW or any(b in json.dumps(q, ensure_ascii=False) for q in qs):
            errs.append(f"заборонене «{b}»")
    return errs


def check_file(path):
    """Звіряє quiz.json (або його копію) з даними генератора: id, тип, відповідь, accept, варіанти."""
    want = {q["id"]: q for q in build_questions()}
    have = json.loads(Path(path).read_text(encoding="utf-8"))["questions"]
    errs = self_check(have)
    if len(have) < 60:
        errs.append(f"мало питань: {len(have)}")
    for q in have:
        w = want.get(q["id"])
        if w is None:
            errs.append(f"{q['id']}: нема в даних генератора")
            continue
        if q["type"] != w["type"]:
            errs.append(f"{q['id']}: тип {q['type']} ≠ {w['type']}")
        if q["type"] == "short":
            if norm(q["answer"]) != norm(w["answer"]) or sorted(map(norm, q["accept"])) != sorted(map(norm, w["accept"])):
                errs.append(f"{q['id']}: відповідь «{q['answer']}» ≠ еталон «{w['answer']}»")
        else:
            if q.get("options") != w.get("options") or q["answer"] != w["answer"]:
                errs.append(f"{q['id']}: правильний варіант {q['answer']} ≠ еталон {w['answer']}")
    missing = set(want) - {q["id"] for q in have}
    if missing:
        errs.append(f"бракує питань: {sorted(missing)}")
    return errs


def slovnyk_md():
    L = ["# Словник тем заліку з англійської", "",
         "Слова U1-U3 - зі списків, які давала викладачка. Переклади і приклади -",
         "мої, бо в списках англійські пояснення, а в U3 лише самі слова. Значення U3 звір з текстом юніту (с. 18-19).",
         "", "> Слова «Університет» і «Фізика і навчання» не з підручника: вони для усної теми, презентації й анотації.",
         ""]
    titles = {"U1": "Unit 1", "U2": "Unit 2", "U3": "Unit 3", "UNI": "Університет (з презентації)",
              "PHYS": "Фізика і навчання"}
    for tag in ["U1", "U2", "U3", "UNI", "PHYS"]:
        ws = [w for w in VOCAB if w["tag"] == tag]
        L += [f"## {titles[tag]} ({len(ws)} слів)", "", "| EN | UA | Приклад | Переклад |", "|---|---|---|---|"]
        for w in ws:
            L.append(f"| **{w['en']}** | {w['ua']} | {w['ex']} | {w['exua']} |")
        L.append("")
    L += ["## Неправильні дієслова", "",
          "> Викладачка задала «всі неправильні дієслова» (57 слів, знати переклад), але самого її списку",
          "> у файлах немає. Нижче стандартний список найуживаніших - звір зі своїм.", "",
          "| V1 | V2 | V3 | Переклад |", "|---|---|---|---|"]
    for v in VERBS:
        L.append(f"| {v['v1']} | {v['v2']} | {v['v3']} | {v['ua']} |")
    L.append("")
    return "\n".join(L)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--check" in sys.argv:
        i = sys.argv.index("--check")
        path = sys.argv[i + 1] if len(sys.argv) > i + 1 else str(OUT / "quiz.json")
        errs = check_file(path)
        if errs:
            print(f"ПОМИЛОК {len(errs)}:")
            for e in errs:
                print("  ", e)
            return 1
        print(f"OK: {path} збігається з даними генератора")
        return 0
    qs = build_questions()
    errs = self_check(qs)
    if errs:
        for e in errs:
            print("  ", e)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "quiz.json").write_text(json.dumps({"questions": qs}, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "slovnyk.md").write_text(slovnyk_md(), encoding="utf-8")
    by = {}
    for q in qs:
        by[q["type"]] = by.get(q["type"], 0) + 1
    print(f"eng: питань {len(qs)} {by}; слів {len(VOCAB)}; дієслів {len(VERBS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
