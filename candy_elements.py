# candy_elements.py
"""
╔══════════════════════════════════════════════════════════════╗
║ 🍬 Candy Crush Saga - Complete Element Database ║
║ قاعدة بيانات شاملة لجميع عناصر اللعبة ║
║ 50+ عنصر مع أوصاف CLIP لكل واحد ║
╚══════════════════════════════════════════════════════════════╝
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

# ═══════════════════════════════════════════
# تصنيفات العناصر
# ═══════════════════════════════════════════
class ElementCategory(Enum):
    BASIC_CANDY = "basic_candy"      # حلوى أساسية
    SPECIAL_CANDY = "special_candy"  # حلوى خاصة
    BLOCKER = "blocker"              # عائق / حاجز
    COVER = "cover"                  # غطاء / طبقة
    BOARD = "board"                  # عنصر لوحة
    INGREDIENT = "ingredient"        # مكون / مقتنى
    BOOSTER = "booster"              # معزز
    MODIFIER = "modifier"            # معدّل

@dataclass
class GameElement:
    """عنصر واحد من عناصر اللعبة"""
    id: str                                 # معرف فريد
    name_en: str                            # الاسم بالإنجليزية
    name_ar: str                            # الاسم بالعربية
    category: ElementCategory               # الفئة
    emoji: str                              # إيموجي تمثيلي
    color: tuple                            # لون RGB
    clip_descriptions: List[str]            # أوصاف CLIP للتعرف
    layers: int = 1                         # عدد الطبقات
    is_movable: bool = True                 # هل يمكن تحريكه؟
    is_matchable: bool = True               # هل يمكن مطابقته؟
    blocks_gravity: bool = False            # هل يمنع السقوط؟
    spreads: bool = False                   # هل ينتشر؟
    has_timer: bool = False                 # هل له مؤقت؟
    special_behavior: str = ""              # سلوك خاص
    priority_score: int = 0                 # أولوية في التقييم

# ═══════════════════════════════════════════════════════════
# الفئة 1: الحلوى الأساسية (Basic Candies)
# ═══════════════════════════════════════════════════════════
BASIC_CANDIES = {
    'red': GameElement(
        id='red',
        name_en='Red Jelly Bean',
        name_ar='حلوى حمراء',
        category=ElementCategory.BASIC_CANDY,
        emoji='🔴',
        color=(220, 50, 50),
        clip_descriptions=[
            "a red candy piece on game board",
            "red jelly bean candy",
            "bright red oval shaped candy",
            "a shiny red candy drop",
            "red colored game piece candy crush",
        ],
    ),
    'orange': GameElement(
        id='orange',
        name_en='Orange Lozenge',
        name_ar='حلوى برتقالية',
        category=ElementCategory.BASIC_CANDY,
        emoji='🟠',
        color=(240, 160, 40),
        clip_descriptions=[
            "an orange candy piece on game board",
            "orange lozenge diamond shaped candy",
            "bright orange candy piece",
            "an orange colored game piece",
            "orange diamond candy crush",
        ],
    ),
    'yellow': GameElement(
        id='yellow',
        name_en='Yellow Lemon Drop',
        name_ar='حلوى صفراء',
        category=ElementCategory.BASIC_CANDY,
        emoji='🟡',
        color=(240, 220, 40),
        clip_descriptions=[
            "a yellow candy piece on game board",
            "yellow lemon drop candy",
            "bright yellow teardrop candy",
            "a yellow colored game piece",
            "yellow drop shaped candy crush",
        ],
    ),
    'green': GameElement(
        id='green',
        name_en='Green Square Candy',
        name_ar='حلوى خضراء',
        category=ElementCategory.BASIC_CANDY,
        emoji='🟢',
        color=(60, 200, 60),
        clip_descriptions=[
            "a green candy piece on game board",
            "green square shaped candy",
            "bright green candy piece",
            "a green colored game piece",
            "green square candy crush",
        ],
    ),
    'blue': GameElement(
        id='blue',
        name_en='Blue Lollipop Head',
        name_ar='حلوى زرقاء',
        category=ElementCategory.BASIC_CANDY,
        emoji='🔵',
        color=(40, 100, 220),
        clip_descriptions=[
            "a blue candy piece on game board",
            "blue lollipop head candy",
            "bright blue candy piece",
            "a blue colored game piece",
            "blue round candy crush",
        ],
    ),
    'purple': GameElement(
        id='purple',
        name_en='Purple Cluster Candy',
        name_ar='حلوى بنفسجية',
        category=ElementCategory.BASIC_CANDY,
        emoji='🟣',
        color=(160, 50, 180),
        clip_descriptions=[
            "a purple candy piece on game board",
            "purple cluster candy",
            "bright purple candy piece",
            "a purple colored game piece",
            "purple grape candy crush",
        ],
    ),
}

# ═══════════════════════════════════════════════════════════
# الفئة 2: الحلوى الخاصة (Special Candies)
# ═══════════════════════════════════════════════════════════
SPECIAL_CANDIES = {
    'striped_h': GameElement(
        id='striped_h',
        name_en='Horizontal Striped Candy',
        name_ar='حلوى مخططة أفقياً',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='↔️',
        color=(255, 255, 100),
        clip_descriptions=[
            "a candy with horizontal stripes",
            "striped candy with horizontal lines",
            "candy with lines going left to right",
            "horizontally striped game piece",
            "candy with horizontal stripe pattern",
        ],
        special_behavior="يمسح صفاً كاملاً أفقياً",
        priority_score=30,
    ),
    'striped_v': GameElement(
        id='striped_v',
        name_en='Vertical Striped Candy',
        name_ar='حلوى مخططة عمودياً',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='↕️',
        color=(255, 255, 100),
        clip_descriptions=[
            "a candy with vertical stripes",
            "striped candy with vertical lines",
            "candy with lines going up and down",
            "vertically striped game piece",
            "candy with vertical stripe pattern",
        ],
        special_behavior="يمسح عموداً كاملاً",
        priority_score=30,
    ),
    'wrapped': GameElement(
        id='wrapped',
        name_en='Wrapped Candy',
        name_ar='حلوى مغلفة',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='🎁',
        color=(255, 200, 0),
        clip_descriptions=[
            "a wrapped candy with bow",
            "candy wrapped in cellophane",
            "shiny wrapped candy piece",
            "candy with gift wrap pattern",
            "wrapped candy with cross pattern on it",
        ],
        special_behavior="ينفجر مرتين - يمسح 3×3",
        priority_score=50,
    ),
    'color_bomb': GameElement(
        id='color_bomb',
        name_en='Color Bomb',
        name_ar='قنبلة الألوان',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='💣',
        color=(30, 30, 30),
        clip_descriptions=[
            "a dark chocolate color bomb ball",
            "black spherical candy with sparkles",
            "dark round bomb candy with colors",
            "color bomb game piece dark ball",
            "black ball with colorful sprinkles",
            "dark chocolate bomb candy crush",
        ],
        special_behavior="يزيل كل الحلوى من نفس اللون",
        priority_score=100,
    ),
    'candy_fish': GameElement(
        id='candy_fish',
        name_en='Swedish Fish / Candy Fish',
        name_ar='سمكة الحلوى',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='🐟',
        color=(255, 100, 100),
        clip_descriptions=[
            "a fish shaped candy",
            "candy fish game piece",
            "swedish fish candy on board",
            "fish shaped game piece with tail",
            "small fish candy red or blue",
        ],
        special_behavior="يسبح ويزيل حلوى عشوائية أو جيلي",
        priority_score=25,
    ),
    'coloring_candy': GameElement(
        id='coloring_candy',
        name_en='Coloring Candy',
        name_ar='حلوى التلوين',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='🌈',
        color=(255, 100, 255),
        clip_descriptions=[
            "a rainbow colored candy",
            "multicolor candy piece",
            "candy with rainbow swirl pattern",
            "coloring candy with multiple colors",
            "rainbow candy game piece",
        ],
        special_behavior="يحول حلوى عشوائية لنفس اللون",
        priority_score=80,
    ),
    'coconut_wheel': GameElement(
        id='coconut_wheel',
        name_en='Coconut Wheel',
        name_ar='عجلة جوز الهند',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='🥥',
        color=(139, 90, 43),
        clip_descriptions=[
            "a coconut wheel candy",
            "brown coconut shaped candy",
            "round brown coconut game piece",
            "coconut wheel with white and brown",
            "half coconut candy piece",
        ],
        special_behavior="يتدحرج ويحول 3 حلوى لمخططة",
        priority_score=35,
    ),
}

# ═══════════════════════════════════════════════════════════
# الفئة 3: العوائق والحواجز (Blockers)
# ═══════════════════════════════════════════════════════════
BLOCKERS = {
    # ─── الشوكولاتة ───
    'chocolate': GameElement(
        id='chocolate',
        name_en='Chocolate',
        name_ar='شوكولاتة',
        category=ElementCategory.BLOCKER,
        emoji='🍫',
        color=(101, 67, 33),
        clip_descriptions=[
            "a brown chocolate blocker square",
            "dark brown chocolate piece on board",
            "chocolate block game piece",
            "brown chocolate square blocker",
            "dark chocolate game obstacle",
        ],
        is_movable=False,
        is_matchable=False,
        spreads=True,
        special_behavior="ينتشر كل دور إذا لم تطابق بجانبه",
        priority_score=20,
    ),
    'dark_chocolate': GameElement(
        id='dark_chocolate',
        name_en='Dark Chocolate',
        name_ar='شوكولاتة داكنة',
        category=ElementCategory.BLOCKER,
        emoji='🟫',
        color=(60, 30, 10),
        clip_descriptions=[
            "very dark brown chocolate square",
            "dark chocolate with multiple layers",
            "thick dark brown blocker",
            "multilayer dark chocolate piece",
            "extra dark chocolate blocker candy crush",
        ],
        layers=3,
        is_movable=False,
        is_matchable=False,
        spreads=True,
        special_behavior="شوكولاتة بطبقات متعددة - تنتشر",
        priority_score=25,
    ),
    'white_chocolate': GameElement(
        id='white_chocolate',
        name_en='White Chocolate',
        name_ar='شوكولاتة بيضاء',
        category=ElementCategory.BLOCKER,
        emoji='🤍',
        color=(250, 240, 220),
        clip_descriptions=[
            "white chocolate blocker square",
            "cream colored white chocolate piece",
            "light colored chocolate blocker",
            "white chocolate mousse blocker",
            "pale cream chocolate block",
        ],
        layers=3,
        is_movable=False,
        is_matchable=False,
        spreads=True,
        special_behavior="مثل الشوكولاتة لكن بلون أبيض",
        priority_score=25,
    ),
    'chocolate_fountain': GameElement(
        id='chocolate_fountain',
        name_en='Chocolate Fountain / Spawner',
        name_ar='نافورة الشوكولاتة',
        category=ElementCategory.BLOCKER,
        emoji='⛲',
        color=(80, 40, 10),
        clip_descriptions=[
            "chocolate fountain spawner",
            "dark brown fountain piece",
            "chocolate source spawner on board",
            "fountain shaped chocolate dispenser",
            "chocolate spawner game piece",
        ],
        is_movable=False,
        is_matchable=False,
        special_behavior="يُنتج شوكولاتة جديدة كل دور",
        priority_score=30,
    ),
    # ─── القفل / السجن ───
    'licorice_lock': GameElement(
        id='licorice_lock',
        name_en='Licorice Lock / Cage',
        name_ar='قفل العرقسوس / السجن',
        category=ElementCategory.BLOCKER,
        emoji='🔒',
        color=(20, 20, 20),
        clip_descriptions=[
            "a candy locked in a cage",
            "licorice lock cage over candy",
            "black cage bars over a candy piece",
            "locked candy with prison bars",
            "candy behind black metal cage bars",
            "licorice lock grid pattern over candy",
        ],
        is_movable=False,
        is_matchable=True,           # الحلوى تحته قابلة للمطابقة
        special_behavior="يقفل الحلوى - طابق بجانبه لفتحه",
        priority_score=15,
    ),
    'licorice_swirl': GameElement(
        id='licorice_swirl',
        name_en='Licorice Swirl',
        name_ar='لولب العرقسوس',
        category=ElementCategory.BLOCKER,
        emoji='🌀',
        color=(10, 10, 10),
        clip_descriptions=[
            "a black licorice swirl candy",
            "dark twisted licorice piece",
            "black spiral candy blocker",
            "licorice swirl game piece",
            "dark black twisted candy piece",
        ],
        is_movable=True,
        is_matchable=False,
        special_behavior="يتحرك مع الجاذبية لكن لا يُطابق",
        priority_score=10,
    ),
    'licorice_fence': GameElement(
        id='licorice_fence',
        name_en='Licorice Fence / Candy Cane Fence',
        name_ar='سياج العرقسوس',
        category=ElementCategory.BLOCKER,
        emoji='🚧',
        color=(200, 50, 50),
        clip_descriptions=[
            "red and white striped fence between cells",
            "candy cane fence barrier",
            "red white striped barrier line",
            "licorice fence between two candies",
            "candy cane colored fence divider",
        ],
        is_movable=False,
        is_matchable=False,
        blocks_gravity=False,
        special_behavior="يمنع التبديل بين خليتين متجاورتين",
        priority_score=10,
    ),
    # ─── الثلج / التجميد ───
    'ice_1': GameElement(
        id='ice_1',
        name_en='Ice Layer 1 (Thin)',
        name_ar='ثلج (طبقة واحدة)',
        category=ElementCategory.COVER,
        emoji='🧊',
        color=(200, 230, 255),
        clip_descriptions=[
            "candy covered with thin ice layer",
            "frozen candy with ice coating",
            "candy behind thin ice crystal",
            "light blue ice covered candy",
            "slightly frozen candy piece",
            "thin transparent ice over candy",
        ],
        layers=1,
        is_matchable=True,
        special_behavior="طبقة ثلج رقيقة - مطابقة واحدة تكسرها",
        priority_score=5,
    ),
    'ice_2': GameElement(
        id='ice_2',
        name_en='Ice Layer 2 (Thick)',
        name_ar='ثلج (طبقتان)',
        category=ElementCategory.COVER,
        emoji='❄️',
        color=(150, 200, 255),
        clip_descriptions=[
            "candy covered with thick ice",
            "heavily frozen candy piece",
            "candy behind thick ice block",
            "dark blue thick ice covered candy",
            "double layer ice over candy",
            "very frozen icy candy piece",
        ],
        layers=2,
        is_matchable=True,
        special_behavior="ثلج سميك - يحتاج مطابقتين",
        priority_score=10,
    ),
    # ─── الجيلي ───
    'jelly_1': GameElement(
        id='jelly_1',
        name_en='Jelly (Single Layer)',
        name_ar='جيلي (طبقة واحدة)',
        category=ElementCategory.COVER,
        emoji='🟦',
        color=(100, 180, 255),
        clip_descriptions=[
            "candy on light blue jelly background",
            "single layer jelly under candy",
            "light colored jelly square",
            "translucent blue jelly layer",
            "candy on top of light jelly",
        ],
        layers=1,
        is_matchable=True,
        special_behavior="جيلي خفيف - مطابقة واحدة تزيله",
        priority_score=8,
    ),
    'jelly_2': GameElement(
        id='jelly_2',
        name_en='Jelly (Double Layer)',
        name_ar='جيلي (طبقتان)',
        category=ElementCategory.COVER,
        emoji='🟪',
        color=(60, 60, 200),
        clip_descriptions=[
            "candy on dark blue jelly background",
            "double layer thick jelly under candy",
            "dark colored jelly square",
            "deep blue jelly layer",
            "candy on top of dark thick jelly",
        ],
        layers=2,
        is_matchable=True,
        special_behavior="جيلي سميك - يحتاج مطابقتين",
        priority_score=12,
    ),
    # ─── الكريمة / الصقيع ───
    'frosting_1': GameElement(
        id='frosting_1',
        name_en='Frosting / Meringue (1 Layer)',
        name_ar='كريمة / صقيع (طبقة واحدة)',
        category=ElementCategory.BLOCKER,
        emoji='🧁',
        color=(255, 250, 240),
        clip_descriptions=[
            "white frosting meringue block one layer",
            "thin white icing blocker",
            "light cream colored frosting square",
            "single layer meringue blocker",
            "white cream colored game blocker",
        ],
        layers=1,
        is_movable=False,
        is_matchable=False,
        special_behavior="طبقة كريمة - طابق بجانبها لإزالة طبقة",
        priority_score=8,
    ),
    'frosting_2': GameElement(
        id='frosting_2',
        name_en='Frosting / Meringue (2 Layers)',
        name_ar='كريمة (طبقتان)',
        category=ElementCategory.BLOCKER,
        emoji='🍰',
        color=(255, 240, 220),
        clip_descriptions=[
            "thick white frosting meringue block",
            "double layer white icing blocker",
            "thick cream frosting square blocker",
            "multi layer meringue game piece",
            "heavy white frosting block",
        ],
        layers=2,
        is_movable=False,
        is_matchable=False,
        priority_score=12,
    ),
    'frosting_3': GameElement(
        id='frosting_3',
        name_en='Frosting / Meringue (3 Layers)',
        name_ar='كريمة (3 طبقات)',
        category=ElementCategory.BLOCKER,
        emoji='🎂',
        color=(255, 230, 200),
        clip_descriptions=[
            "very thick frosting meringue block",
            "triple layer heavy icing blocker",
            "massive cream frosting square",
            "three layer meringue blocker",
            "extremely thick frosting block",
        ],
        layers=3,
        is_movable=False,
        is_matchable=False,
        priority_score=15,
    ),
    'frosting_5': GameElement(
        id='frosting_5',
        name_en='Frosting / Meringue (5 Layers)',
        name_ar='كريمة (5 طبقات)',
        category=ElementCategory.BLOCKER,
        emoji='🏔️',
        color=(240, 220, 190),
        clip_descriptions=[
            "maximum thickness frosting block",
            "five layer meringue massive blocker",
            "tallest frosting blocker piece",
            "extremely thick multilayer icing",
            "biggest cream frosting block",
        ],
        layers=5,
        is_movable=False,
        is_matchable=False,
        priority_score=20,
    ),
    # ─── المربى ───
    'marmalade': GameElement(
        id='marmalade',
        name_en='Marmalade / Honey',
        name_ar='مربى / عسل',
        category=ElementCategory.COVER,
        emoji='🍯',
        color=(255, 180, 0),
        clip_descriptions=[
            "candy covered in golden honey marmalade",
            "amber colored marmalade over candy",
            "golden sticky honey coating on candy",
            "candy trapped in orange marmalade",
            "honey glazed candy piece",
        ],
        layers=1,
        is_matchable=True,
        special_behavior="يغطي الحلوى - مطابقة تحرر الحلوى",
        priority_score=10,
    ),
    # ─── قنبلة الحلوى (مؤقتة) ───
    'candy_bomb': GameElement(
        id='candy_bomb',
        name_en='Candy Bomb (Timed)',
        name_ar='قنبلة الحلوى (مؤقتة)',
        category=ElementCategory.BLOCKER,
        emoji='💣',
        color=(20, 20, 20),
        clip_descriptions=[
            "dark bomb with number countdown",
            "black candy bomb with timer number",
            "timed bomb game piece with digits",
            "countdown bomb dark colored",
            "numbered dark bomb candy piece",
        ],
        is_movable=True,
        is_matchable=True,
        has_timer=True,
        special_behavior="ينفجر عند الصفر = خسارة! طابقه قبل ذلك",
        priority_score=100,          # أعلى أولوية!
    ),
    # ─── الفشار ───
    'popcorn': GameElement(
        id='popcorn',
        name_en='Popcorn',
        name_ar='فشار',
        category=ElementCategory.BLOCKER,
        emoji='🍿',
        color=(255, 230, 150),
        clip_descriptions=[
            "popcorn kernel game piece",
            "yellow popcorn blocker on board",
            "popcorn shaped blocker piece",
            "light yellow popcorn game element",
            "small popcorn kernel candy crush",
        ],
        layers=3,
        is_movable=False,
        is_matchable=False,
        special_behavior="طابق 3 مرات بجانبه ليفرقع ويعطي معزز",
        priority_score=20,
    ),
    # ─── صندوق السكر ───
    'sugar_chest': GameElement(
        id='sugar_chest',
        name_en='Sugar Chest',
        name_ar='صندوق السكر',
        category=ElementCategory.BLOCKER,
        emoji='📦',
        color=(180, 130, 70),
        clip_descriptions=[
            "brown sugar chest treasure box",
            "locked treasure chest game piece",
            "wooden chest with lock on board",
            "brown locked box candy crush",
            "sugar chest locked game element",
        ],
        is_movable=False,
        is_matchable=False,
        special_behavior="يحتاج مفتاح سكر لفتحه",
        priority_score=15,
    ),
    'sugar_key': GameElement(
        id='sugar_key',
        name_en='Sugar Key',
        name_ar='مفتاح السكر',
        category=ElementCategory.BLOCKER,
        emoji='🔑',
        color=(255, 215, 0),
        clip_descriptions=[
            "golden key candy piece",
            "sugar key golden colored",
            "small golden key on game board",
            "key shaped candy piece",
            "golden sugar key game element",
        ],
        is_movable=True,
        is_matchable=True,
        special_behavior="طابقه ليصل للصندوق ويفتحه",
        priority_score=25,
    ),
    # ─── العلكة ───
    'bubblegum': GameElement(
        id='bubblegum',
        name_en='Bubblegum',
        name_ar='علكة',
        category=ElementCategory.BLOCKER,
        emoji='🫧',
        color=(255, 150, 200),
        clip_descriptions=[
            "pink bubblegum blob on board",
            "sticky pink gum blocker",
            "bubblegum pink mass game piece",
            "pink blob bubblegum candy crush",
            "expanding pink bubblegum blocker",
        ],
        is_movable=False,
        is_matchable=False,
        spreads=True,
        special_behavior="ينتشر ويغطي خلايا جديدة",
        priority_score=20,
    ),
    # ─── الخلاط السحري ───
    'magic_mixer': GameElement(
        id='magic_mixer',
        name_en='Magic Mixer',
        name_ar='الخلاط السحري',
        category=ElementCategory.BLOCKER,
        emoji='🌪️',
        color=(130, 0, 200),
        clip_descriptions=[
            "purple magic mixer machine",
            "blender shaped purple blocker",
            "magic mixer purple game element",
            "spinning purple mixer on board",
            "purple vortex mixer candy crush",
        ],
        is_movable=False,
        is_matchable=False,
        special_behavior="يُنتج عوائق جديدة - دمّره بسرعة!",
        priority_score=35,
    ),
    # ─── كيكة القنبلة ───
    'cake_bomb': GameElement(
        id='cake_bomb',
        name_en='Cake Bomb',
        name_ar='كيكة قنبلة',
        category=ElementCategory.BLOCKER,
        emoji='🎂',
        color=(255, 200, 220),
        clip_descriptions=[
            "pink cake bomb with layers",
            "birthday cake shaped game piece",
            "layered cake bomb candy crush",
            "pink multi layer cake blocker",
            "cake shaped bomb with frosting",
        ],
        layers=4,
        is_movable=False,
        is_matchable=False,
        special_behavior="طابق بجانبه 4 مرات لتفجيره",
        priority_score=18,
    ),
    # ─── الوافل ───
    'waffle': GameElement(
        id='waffle',
        name_en='Waffle',
        name_ar='وافل',
        category=ElementCategory.COVER,
        emoji='🧇',
        color=(200, 170, 100),
        clip_descriptions=[
            "waffle grid pattern under candy",
            "brown waffle textured background",
            "candy on waffle grid surface",
            "waffle pattern game element",
            "brown grid waffle candy crush",
        ],
        layers=2,
        is_matchable=True,
        special_behavior="طابق فوقه لإزالة طبقاته",
        priority_score=8,
    ),
    # ─── لفة قوس قزح ───
    'rainbow_twist': GameElement(
        id='rainbow_twist',
        name_en='Rainbow Twist / Rapids',
        name_ar='لفة قوس قزح',
        category=ElementCategory.BLOCKER,
        emoji='🌈',
        color=(255, 100, 100),
        clip_descriptions=[
            "rainbow colored twist spiral",
            "colorful rainbow twist game piece",
            "rainbow rapids swirl on board",
            "multicolor spiral twist element",
            "rainbow tornado twist candy crush",
        ],
        is_movable=False,
        is_matchable=False,
        special_behavior="يدور ويغير ترتيب الحلوى حوله",
        priority_score=12,
    ),
    # ─── طلاء السكر ───
    'sugar_coat': GameElement(
        id='sugar_coat',
        name_en='Sugar Coat',
        name_ar='طلاء السكر',
        category=ElementCategory.COVER,
        emoji='✨',
        color=(255, 255, 230),
        clip_descriptions=[
            "sparkling sugar coat over candy",
            "shiny crystal sugar coating",
            "candy with glittery sugar coat",
            "sparkly sugar coated candy piece",
            "crystallized sugar over candy",
        ],
        layers=1,
        is_matchable=True,
        special_behavior="طلاء لامع - يُزال بمطابقة واحدة",
        priority_score=5,
    ),
}

# ═══════════════════════════════════════════════════════════
# الفئة 5: عناصر اللوحة (Board Elements)
# ═══════════════════════════════════════════════════════════
BOARD_ELEMENTS = {
    'conveyor_belt': GameElement(
        id='conveyor_belt',
        name_en='Conveyor Belt',
        name_ar='حزام ناقل',
        category=ElementCategory.BOARD,
        emoji='➡️',
        color=(150, 150, 150),
        clip_descriptions=[
            "conveyor belt arrows on board",
            "moving belt with directional arrows",
            "conveyor belt track game element",
            "arrow marked moving belt path",
        ],
        is_movable=False,
        is_matchable=False,
        special_behavior="يحرك الحلوى في اتجاه محدد كل دور",
    ),
    'portal': GameElement(
        id='portal',
        name_en='Portal / Teleporter',
        name_ar='بوابة / ناقل',
        category=ElementCategory.BOARD,
        emoji='🌀',
        color=(0, 200, 255),
        clip_descriptions=[
            "swirling portal teleporter on board",
            "blue green portal entrance",
            "teleporter vortex game element",
            "magical portal doorway candy crush",
        ],
        is_movable=False,
        is_matchable=False,
        special_behavior="ينقل الحلوى من مكان لآخر",
    ),
    'tornado': GameElement(
        id='tornado',
        name_en='Tornado',
        name_ar='إعصار',
        category=ElementCategory.BOARD,
        emoji='🌪️',
        color=(180, 180, 180),
        clip_descriptions=[
            "tornado whirlwind on game board",
            "spinning tornado game element",
            "grey tornado vortex candy crush",
            "whirlwind spinning on board cell",
        ],
        is_movable=False,
        is_matchable=False,
        special_behavior="يتحرك عشوائياً ويدمر ما حوله",
    ),
    'chameleon_candy': GameElement(
        id='chameleon_candy',
        name_en='Chameleon Candy',
        name_ar='حلوى الحرباء',
        category=ElementCategory.BOARD,
        emoji='🦎',
        color=(100, 200, 100),
        clip_descriptions=[
            "chameleon candy changing colors",
            "color changing candy piece",
            "shifting color candy chameleon",
            "candy that changes color each turn",
        ],
        is_movable=True,
        is_matchable=True,
        special_behavior="يغير لونه كل دور",
    ),
    'bobber': GameElement(
        id='bobber',
        name_en='Bobber (Soda Levels)',
        name_ar='عوامة (مراحل الصودا)',
        category=ElementCategory.BOARD,
        emoji='🎈',
        color=(255, 100, 100),
        clip_descriptions=[
            "bobber floating on soda water",
            "red bobber on liquid surface",
            "floating buoy on soda level",
            "bobber game piece in soda",
        ],
        is_movable=False,
        is_matchable=False,
        special_behavior="يطفو على الصودا - أوصله للأعلى",
    ),
    'ufo': GameElement(
        id='ufo',
        name_en='UFO / Spaceship',
        name_ar='صحن طائر',
        category=ElementCategory.BOARD,
        emoji='🛸',
        color=(150, 255, 150),
        clip_descriptions=[
            "small ufo spaceship game piece",
            "flying saucer candy crush element",
            "green ufo game piece on board",
            "spaceship shaped game element",
        ],
        is_movable=False,
        is_matchable=False,
        special_behavior="يطير ويزيل عوائق عشوائية",
    ),
    'empty': GameElement(
        id='empty',
        name_en='Empty Cell',
        name_ar='خلية فارغة',
        category=ElementCategory.BOARD,
        emoji='⬜',
        color=(200, 200, 200),
        clip_descriptions=[
            "empty cell on game board",
            "blank space with no candy",
            "empty game board square",
            "vacant cell background only",
        ],
        is_movable=False,
        is_matchable=False,
    ),
}

# ═══════════════════════════════════════════════════════════
# الفئة 6: المكونات (Ingredients)
# ═══════════════════════════════════════════════════════════
INGREDIENTS = {
    'cherry': GameElement(
        id='cherry',
        name_en='Cherry',
        name_ar='كرز',
        category=ElementCategory.INGREDIENT,
        emoji='🍒',
        color=(200, 0, 0),
        clip_descriptions=[
            "red cherry fruit on game board",
            "cherry ingredient candy crush",
            "small red cherry with stem",
            "cherry fruit game piece to collect",
        ],
        is_movable=True,
        is_matchable=False,
        special_behavior="أوصله للأسفل لجمعه",
    ),
    'hazelnut': GameElement(
        id='hazelnut',
        name_en='Hazelnut / Acorn',
        name_ar='بندق / جوزة',
        category=ElementCategory.INGREDIENT,
        emoji='🌰',
        color=(139, 90, 43),
        clip_descriptions=[
            "brown hazelnut acorn on game board",
            "nut ingredient candy crush",
            "brown acorn shaped game piece",
            "hazelnut collectible on board",
        ],
        is_movable=True,
        is_matchable=False,
        special_behavior="أوصله للأسفل لجمعه",
    ),
}

# ═══════════════════════════════════════════════════════════
# الفئة 7: عناصر إضافية حديثة
# ═══════════════════════════════════════════════════════════
EXTRA_ELEMENTS = {
    'lucky_candy': GameElement(
        id='lucky_candy',
        name_en='Lucky Candy',
        name_ar='حلوى الحظ',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='❓',
        color=(200, 200, 200),
        clip_descriptions=[
            "candy with question mark",
            "lucky candy with unknown symbol",
            "mystery candy question mark piece",
            "unknown lucky candy game element",
        ],
        special_behavior="يتحول لمعزز عشوائي عند المطابقة",
        priority_score=15,
    ),
    'extra_time': GameElement(
        id='extra_time',
        name_en='Extra Time Candy (+5)',
        name_ar='حلوى الوقت الإضافي',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='⏰',
        color=(0, 200, 0),
        clip_descriptions=[
            "candy with plus five number",
            "green time candy with +5",
            "extra time candy piece",
            "clock candy adding five seconds",
        ],
        special_behavior="يضيف 5 ثواني في المراحل المؤقتة",
        priority_score=20,
    ),
    'candy_frog': GameElement(
        id='candy_frog',
        name_en='Candy Frog',
        name_ar='ضفدع الحلوى',
        category=ElementCategory.SPECIAL_CANDY,
        emoji='🐸',
        color=(0, 200, 0),
        clip_descriptions=[
            "green frog candy game piece",
            "frog shaped candy on board",
            "candy frog sitting on board",
            "green frog game element candy crush",
        ],
        special_behavior="يأكل حلوى من نفس اللون ثم ينفجر",
        priority_score=30,
    ),
    'jelly_fish_booster': GameElement(
        id='jelly_fish_booster',
        name_en='Jelly Fish (Booster)',
        name_ar='سمكة الجيلي (معزز)',
        category=ElementCategory.BOOSTER,
        emoji='🐠',
        color=(100, 200, 255),
        clip_descriptions=[
            "blue jelly fish swimming on board",
            "jellyfish shaped candy piece",
            "floating jelly fish game booster",
            "blue fish jelly booster candy crush",
        ],
        special_behavior="3 سمكات تسبح وتزيل جيلي",
        priority_score=20,
    ),
}

# ═══════════════════════════════════════════════════════════
# تجميع كل العناصر
# ═══════════════════════════════════════════════════════════
ALL_ELEMENTS: Dict[str, GameElement] = {}
ALL_ELEMENTS.update(BASIC_CANDIES)
ALL_ELEMENTS.update(SPECIAL_CANDIES)
ALL_ELEMENTS.update(BLOCKERS)
ALL_ELEMENTS.update(BOARD_ELEMENTS)
ALL_ELEMENTS.update(INGREDIENTS)
ALL_ELEMENTS.update(EXTRA_ELEMENTS)

def get_all_clip_descriptions() -> Dict[str, List[str]]:
    """إرجاع كل الأوصاف مجمعة حسب المعرف"""
    return { elem_id: elem.clip_descriptions for elem_id, elem in ALL_ELEMENTS.items() }

def get_flat_descriptions() -> tuple:
    """
    إرجاع قائمة مسطحة من الأوصاف مع ربطها بالمعرفات
    Returns: (descriptions_list, id_for_each_description)
    """
    descriptions = []
    ids = []
    for elem_id, elem in ALL_ELEMENTS.items():
        for desc in elem.clip_descriptions:
            descriptions.append(desc)
            ids.append(elem_id)
    return descriptions, ids

def get_elements_by_category(category: ElementCategory) -> Dict[str, GameElement]:
    """إرجاع عناصر فئة معينة"""
    return { k: v for k, v in ALL_ELEMENTS.items() if v.category == category }

def get_priority_elements() -> List[GameElement]:
    """العناصر مرتبة حسب الأولوية (الأهم أولاً)"""
    return sorted(ALL_ELEMENTS.values(), key=lambda e: e.priority_score, reverse=True)

def print_catalog():
    """طباعة الكتالوج الكامل"""
    categories = {}
    for elem in ALL_ELEMENTS.values():
        cat = elem.category.value
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(elem)

    cat_names = {
        'basic_candy':   '📦 الحلوى الأساسية',
        'special_candy': '⭐ الحلوى الخاصة',
        'blocker':       '🧱 العوائق والحواجز',
        'cover':         '🧊 الأغطية والطبقات',
        'board':         '🎯 عناصر اللوحة',
        'ingredient':    '🍒 المكونات',
        'booster':       '🔧 المعززات',
        'modifier':      '🔄 المعدلات',
    }

    total = 0
    for cat, elements in categories.items():
        name = cat_names.get(cat, cat)
        print(f"\n{'═' * 50}")
        print(f" {name} ({len(elements)} عنصر)")
        print(f"{'═' * 50}")
        for elem in elements:
            flags = []
            if not elem.is_movable:
                flags.append("ثابت")
            if elem.spreads:
                flags.append("ينتشر")
            if elem.has_timer:
                flags.append("مؤقت⚠️")
            if elem.layers > 1:
                flags.append(f"{elem.layers} طبقات")
            flag_str = f" [{', '.join(flags)}]" if flags else ""
            print(
                f" {elem.emoji} {elem.id:20s} "
                f"│ {elem.name_ar:25s} "
                f"│ P:{elem.priority_score:3d}"
                f"{flag_str}"
            )
        total += len(elements)

    print(f"\n{'═' * 50}")
    print(f" 📊 إجمالي العناصر: {total}")
    print(f"{'═' * 50}")

# تشغيل تجريبي
if __name__ == "__main__":
    print_catalog()
