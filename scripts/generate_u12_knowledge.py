#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Unit 1-2 knowledge lectures (bodyHtml) in Unit 3 Part B style."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from textbook_catalog import UNITS  # noqa: E402
from appendix_parser import (  # noqa: E402
    expressions_for_part,
    find_example_for_word,
    parse_catalog,
    reading_sentence_pairs,
    words_for_part,
)

ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_BANK = ROOT / "data" / "study-hub" / "knowledge-bank.json"
KNOWLEDGE_DIR = ROOT / "data" / "study-hub" / "library" / "knowledge"

PART_LABELS = {
    "part-a": "Part A",
    "part-b": "Part B",
    "part-c": "Part C",
    "reading": "Reading 阅读",
}

PART_FOCUS = {
    "part-a": "听说入门：认读核心词汇，模仿对话，能问答交流",
    "part-b": "读写拓展：读懂语篇，能复述并写简单句",
    "part-c": "语法发现：归纳规则，举一反三完成练习",
}

PAGE_IDS = [
    "u1-k-part-a", "u1-k-part-b", "u1-k-part-c", "u1-k-reading",
    "u2-k-part-a", "u2-k-part-b", "u2-k-part-c", "u2-k-reading",
    "u3-k-part-a", "u3-k-part-c", "u3-k-reading",
    "u4-k-part-a", "u4-k-part-b", "u4-k-part-c", "u4-k-reading",
    "u5-k-part-a", "u5-k-part-b", "u5-k-part-c", "u5-k-reading",
    "u6-k-part-a", "u6-k-part-b", "u6-k-part-c", "u6-k-reading",
    "appendix-k-revision",
]

# 保留用户满意的精讲正文，仅追加标准填空/写作区块
PATCH_APPEND_PAGE_IDS = {"u3-k-part-b"}

SENTENCE_KEY = {
    "part-a": "part_a_sentences",
    "part-b": "part_b_sentences",
    "part-c": "part_a_sentences",
    "reading": "part_b_sentences",
}

EXCERPT_RE = re.compile(
    r'<section\s+class="reading-excerpt">[\s\S]*?</section>',
    re.IGNORECASE,
)


def vocab_key(part_key: str) -> str:
    if part_key in ("part-a", "part-c", "reading"):
        return "part_a_vocab"
    return "part_b_vocab"


def phrase_key(part_key: str) -> str:
    if part_key in ("part-a", "part-c"):
        return "part_a_phrases"
    return "part_b_phrases"


def infer_pos(gloss: str) -> str:
    if "过去式" in gloss or "动词" in gloss:
        return "v."
    if gloss.endswith("的") or "形容词" in gloss:
        return "adj."
    if "千米" in gloss or "公里" in gloss:
        return "n."
    return "n./v."


APPENDIX_DISPLAY_FIX = {
    "hong kong": ("Hong Kong-Zhuhai-Macao Bridge", "/brɪdʒ/", "n.", "港珠澳大桥"),
    "eiffel": ("Eiffel Tower", "/ˈaɪfl ˈtaʊə(r)/", "n.", "埃菲尔铁塔"),
    "terracotta": ("Terracotta Warriors", "/ˌterəˈkɒtə ˈwɒriəz/", "n.", "兵马俑"),
    "jinggangshan": ("Jinggangshan Revolution Museum", "/dʒɪŋˈɡæŋʃæn/", "n.", "井冈山革命博物馆"),
}


def appendix_vocab_table(unit_num: int, part_key: str) -> str:
    """第三步：附录2词汇，★二级词，词性栏备注页码，课文例句（≤20词，无中文）。"""
    pairs = reading_sentence_pairs(unit_num, part_key)
    unit = next(u for u in UNITS if u["num"] == unit_num)
    catalog_vocab = {str(w[0]).lower(): w for w in unit.get(vocab_key(part_key), [])}
    rows = []
    for w in words_for_part(unit_num, part_key):
        wl = w.word.lower()
        cat = None
        best_len = 0
        for key, row in catalog_vocab.items():
            if key in wl or wl in key:
                if len(key) > best_len:
                    cat = row
                    best_len = len(key)
        display = w.display_word
        gloss = w.gloss
        ipa = f"/{w.ipa}/"
        pos = infer_pos(w.gloss)
        for fix_key, fix_row in APPENDIX_DISPLAY_FIX.items():
            if fix_key in wl:
                display, ipa, pos, gloss = fix_row[0], fix_row[1], fix_row[2], fix_row[3]
                break
        if cat:
            display = f"★{cat[0]}" if w.level2 else cat[0]
            gloss, ipa, pos = cat[3], cat[1], cat[2]
        elif w.level2 and not any(fix_key in wl for fix_key in APPENDIX_DISPLAY_FIX):
            display = w.display_word
        ex_en = find_example_for_word(display.lstrip("★"), pairs)
        star_note = "（二级词汇★）" if w.level2 else ""
        rows.append(
            f'<tr><td class="en"><strong>{display}</strong></td>'
            f'<td class="en">{ipa}</td>'
            f'<td class="en">{pos} {w.pos_page}{star_note}</td>'
            f'<td class="zh">{gloss}</td>'
            f'<td class="en">{ex_en}</td></tr>'
        )
    body = "\n".join(rows) or '<tr><td class="zh" colspan="5">见附录2词汇表</td></tr>'
    return (
        '<p class="zh tip-box">词汇来源：<strong>附录2 单元词汇表</strong>；加★为课标二级词。</p>'
        '<table class="rich-table"><thead><tr>'
        '<th class="zh">单词</th><th class="en">音标</th>'
        '<th class="en">词性·课本页</th><th class="zh">释义</th>'
        '<th class="en">课文例句</th>'
        f"</tr></thead><tbody>\n{body}\n</tbody></table>"
    )


def appendix_phrase_table(unit_num: int, part_key: str) -> str:
    """第四步：glossary/目录短语块 + 附录四常用表达。"""
    pages = words_for_part(unit_num, part_key)
    default_page = pages[0].pos_page if pages else "P.—"
    unit = next(u for u in UNITS if u["num"] == unit_num)
    seen: set[str] = set()
    rows: list[str] = []

    def add_row(en: str, zh: str, page: str) -> None:
        key = en.strip().lower()
        if not key or key in seen:
            return
        seen.add(key)
        rows.append(
            f'<tr><td class="en">{en}</td><td class="zh">{zh}</td>'
            f'<td class="en">{page}</td></tr>'
        )

    for en, zh in unit.get(phrase_key(part_key), []):
        add_row(en, zh, default_page)

    for expr in expressions_for_part(unit_num, part_key):
        add_row(expr.en, expr.zh, expr.page or default_page)

    body = "\n".join(rows) or '<tr><td class="zh" colspan="3">见附录四常用表达</td></tr>'
    return (
        '<p class="zh tip-box">短语来源：<strong>glossary 必背短语</strong> + <strong>附录四 常用表达</strong>。</p>'
        '<table class="rich-table"><thead><tr>'
        '<th class="en">英文</th><th class="zh">中文</th><th class="en">课本页</th>'
        f"</tr></thead><tbody>\n{body}\n</tbody></table>"
    )


def catalog_focus_html(unit_num: int, part_key: str) -> str:
    cat = parse_catalog().get((unit_num, part_key))
    if not cat:
        return ""
    return f"""<p class="teaching-focus zh"><strong>目录重点（{PART_LABELS.get(part_key, part_key)}）：</strong>{cat.focus_zh}</p>
<p class="teaching-focus zh"><strong>读写/语法要点：</strong>{cat.grammar_zh or "见本讲知识点精讲"}</p>"""


CULTURE = {
    (1, "part-a"): "长城始建于春秋战国，总长约两万一千公里，是世界文化遗产。新西兰「姜饼屋」实为奥马鲁火车站，因童话造型闻名，体现旅行中的文化发现。",
    (1, "part-b"): "秦始皇兵马俑被誉为「世界第八大奇迹」，展现秦代军事与陶塑艺术。井冈山革命博物馆记录中国革命历史，红色故事激励后人。",
    (1, "part-c"): "假期剪贴簿（scrapbook）是英美学生记录旅行的传统方式，图文结合保存回忆。",
    (1, "reading"): "西安古称长安，是十三朝古都；兵马俑、古城墙与面食文化使其成为中华文明重要窗口。",
    (2, "part-a"): "春节贴「福」字倒贴寓意「福到」；穿红衣象征吉祥；除夕倒计时源于辞旧迎新的民俗。",
    (2, "part-b"): "龙舟赛纪念爱国诗人屈原；马拉松源于古希腊马拉松战役传说；社区志愿活动体现现代节日新形式。",
    (2, "part-c"): "校园活动快照（snapshots）记录集体生活，是西方学校常用的展示方式。",
    (2, "reading"): "春节是中国最重要的传统节日，团圆饭、贴福字、赏月吃月饼等习俗承载家庭与文化的纽带。",
    (3, "part-a"): "感冒、发烧等症状的英文表达体现关爱文化；及时就医是负责任的健康态度。",
    (3, "part-b"): "身心健康密不可分：合理饮食、规律锻炼与积极社交都有助于保持健康。",
    (3, "part-c"): "健康生活方式宣传册是向公众传递科学健康理念的有效方式。",
    (3, "reading"): "搬家与友谊主题提醒我们：关心朋友心理健康与身体健康同样重要。",
    (4, "part-a"): "货币作为交换媒介简化交易；区分 need 与 want 是理财启蒙的第一步。",
    (4, "part-b"): "量入为出、储蓄与理性消费是中华传统美德「勤俭」的现代体现。",
    (4, "part-c"): "制定消费计划培养计划意识，是终身受益的生活技能。",
    (4, "reading"): "金钱管理帮助我们建立正确的财富观与价值观。",
    (5, "part-a"): "太阳系行星与人类对宇宙的探索，体现好奇心与科学精神。",
    (5, "part-b"): "中国航天成就（火星探测器等）激发民族自豪感。",
    (5, "part-c"): "分享天体知识项目促进合作学习与科学传播。",
    (5, "reading"): "宇航员日常生活让我们了解太空工作的真实面貌。",
    (6, "part-a"): "风能、太阳能、水能等绿色能源是可持续发展的重要方向。",
    (6, "part-b"): "3R（减少、重复使用、回收）是全球环境保护共识。",
    (6, "part-c"): "绿色能源演讲培养环保行动力与公众表达能力。",
    (6, "reading"): "节约能源、保护地球是每个人应尽的责任。",
}


from knowledge_u12_sections import FILLBLANK_QA_U12, WRITING_MODELS_U12  # noqa: E402
from knowledge_u36_sections import FILLBLANK_QA_U36, WRITING_MODELS_U36  # noqa: E402

FILLBLANK_QA: dict = {}
FILLBLANK_QA.update(FILLBLANK_QA_U12)
FILLBLANK_QA.update(FILLBLANK_QA_U36)


def fillblank_qa_section(unit_num: int, part_key: str) -> str:
    items = FILLBLANK_QA.get((unit_num, part_key), [])
    if not items:
        return ""
    lis = "".join(
        f"<li><strong class=\"zh\">{q}</strong><br><span class=\"en\">{a}</span></li>"
        for q, a in items
    )
    return f"""<h4 class="zh">课文填空与问答精讲</h4>
<ol class="zh">{lis}</ol>"""


WRITING_MODELS: dict = {}
WRITING_MODELS.update(WRITING_MODELS_U12)
WRITING_MODELS.update(WRITING_MODELS_U36)


def writing_section(unit_num: int, part_key: str) -> str:
    return WRITING_MODELS.get((unit_num, part_key), "")


def example_table(headers: list[tuple[str, str]], rows: list[list[str]]) -> str:
    """headers: [(text, class), ...]; rows: [[cell, class], ...] per row as plain strings with class."""
    th = "".join(f'<th class="{cls}">{text}</th>' for text, cls in headers)
    trs = []
    for row in rows:
        tds = "".join(f'<td class="{cls}">{cell}</td>' for cell, cls in row)
        trs.append(f"<tr>{tds}</tr>")
    return (
        f'<table class="rich-table"><thead><tr>{th}</tr></thead>'
        f"<tbody>{''.join(trs)}</tbody></table>"
    )


def knowledge_point(
    num: int,
    title: str,
    subtitle: str,
    explain_zh: str,
    table_html: str,
    memory_zh: str,
    memory_type: str,
    practice_en: str,
) -> str:
    mem_label = "🎵 【歌曲记忆法】" if memory_type == "song" else "🏰 【记忆宫殿法】"
    return f"""
<h2 class="zh">🔑 知识点{num}：{title}</h2>
<h3 class="en">{subtitle}</h3>
<h3 class="zh">📖 【新知识讲解】</h3>
<p class="zh">{explain_zh}</p>
{table_html}
<p class="zh">{mem_label}</p>
<p class="zh">{memory_zh}</p>
<h3 class="zh">✍️ 【举一反三练习】</h3>
<pre class="en"><code class="en">{practice_en}</code></pre>
"""


def strip_excerpt(html: str) -> str:
    return EXCERPT_RE.sub("", html).strip()


# ---------------------------------------------------------------------------
# Per-page content (knowledge tree, points, review, summary, quotes, homework)
# ---------------------------------------------------------------------------

def u1_content(part_key: str) -> dict:
    specs = {
        "part-a": {
            "summary": "本课围绕「奇妙之地」旅行主题，掌握一般过去时入门、How was...? 感受询问、What did you do? 活动问答，以及中外地标词汇。",
            "tree": """【知识点大树🌳】
How was your trip?
│
├─ 🌿 1. 一般过去时：went / climbed / visited
├─ 🌿 2. 感受询问：How was your weekend / holiday?
├─ 🌿 3. 活动问答：What did you do last Saturday?
├─ 🌿 4. 世界地标：Great Wall / Eiffel Tower / Gingerbread House
└─ 🌿 5. 拍照与分享：take photos / send pictures""",
            "goals": [
                "听懂并说出旅行相关核心词汇与短语",
                "用 How was...? 询问并回答旅行感受",
                "用 What did you do? 问答过去活动",
                "认读中外著名地标英文名称",
            ],
            "points": [
                knowledge_point(
                    1,
                    "一般过去时入门",
                    "went / climbed / visited — Past Simple for travel",
                    "六年级全新语法重点：<strong>一般过去时</strong>表示<strong>已经发生过</strong>的事情。"
                    "规则动词加 <code class=\"en\">-ed</code>：climb→climbed, visit→visited；"
                    "不规则动词要单独记：go→went。",
                    example_table(
                        [("动词原形", "en"), ("过去式", "en"), ("例句", "en"), ("中文", "zh")],
                        [
                            [("go", "en"), ("went", "en"), ("I went to Beijing.", "en"), ("我去了北京。", "zh")],
                            [("climb", "en"), ("climbed", "en"), ("I climbed the Great Wall.", "en"), ("我爬了长城。", "zh")],
                            [("visit", "en"), ("visited", "en"), ("I visited the museum.", "en"), ("我参观了博物馆。", "zh")],
                        ],
                    ),
                    "（曲调：《两只老虎》）Went went went，过去已发生；Climbed climbed climbed，爬山真开心；"
                    "Visited visited visited，参观记心间；过去式，要记牢！",
                    "song",
                    """句型变换：
原句：I go to the park.（现在）
过去：I went to the park last Sunday.（上周日）

填空：
1. I ___ (climb) the Great Wall last weekend.
2. She ___ (visit) the Gingerbread House yesterday.
3. We ___ (go) to Paris by plane.

答案：1.climbed  2.visited  3.went""",
                ),
                knowledge_point(
                    2,
                    "How was...? 感受询问",
                    "How was your weekend / holiday?",
                    "旅行回来，朋友最关心你过得怎么样。全新句型 <strong>How was + 名词?</strong> "
                    "用 was（is/am 的过去式）询问<strong>过去的感受</strong>。",
                    example_table(
                        [("问句", "en"), ("答句", "en"), ("中文", "zh")],
                        [
                            [("How was your weekend?", "en"), ("It was great!", "en"), ("你周末过得怎么样？— 非常棒！", "zh")],
                            [("How was your holiday?", "en"), ("It was amazing!", "en"), ("你假期过得怎么样？— 太棒了！", "zh")],
                            [("How was the trip?", "en"), ("It was fun!", "en"), ("旅行怎么样？— 很有趣！", "zh")],
                        ],
                    ),
                    "想象你家<strong>客厅沙发</strong>是「旅行回忆角」：墙上贴着 How was your trip? 的便签；"
                    "沙发上放着 It was amazing! 的抱枕；茶几上摆着旅行照片——三步走完，感受问答全记住！",
                    "palace",
                    """配对练习：
A: How was your summer holiday?
B: It was ___! (great / fun / amazing)

情景造句：
1. 问同学上周末：How was your ___?
2. 回答：It was ___!
3. 再追问：What did you do?""",
                ),
                knowledge_point(
                    3,
                    "What did you do? 活动问答",
                    "What did you do last Saturday?",
                    "想知道对方<strong>具体做了什么</strong>，用全新疑问句："
                    "<strong>What did + 主语 + 动词原形?</strong> "
                    "注意：did 出现后，动词必须用<strong>原形</strong>！",
                    example_table(
                        [("问句", "en"), ("答句", "en"), ("中文", "zh")],
                        [
                            [("What did you do last Saturday?", "en"), ("I visited the museum.", "en"), ("你上周六做了什么？— 我参观了博物馆。", "zh")],
                            [("What did you do there?", "en"), ("I took many photos.", "en"), ("你在那儿做了什么？— 我拍了很多照片。", "zh")],
                            [("What did she do?", "en"), ("She climbed the Great Wall.", "en"), ("她做了什么？— 她爬了长城。", "zh")],
                        ],
                    ),
                    "（曲调：《小星星》）What did you do, what did you do? "
                    "Last Saturday, I visited you. Climbed the wall, took photos too, "
                    "Past tense, we can do!",
                    "song",
                    """问答接龙：
A: What did you do last weekend?
B: I visited the Great Wall.
A: How was it?
B: It was amazing!

改错：
❌ What did you climbed?  → ✅ What did you climb?
❌ I did went there.       → ✅ I went there.""",
                ),
                knowledge_point(
                    4,
                    "世界地标词汇",
                    "Great Wall / Eiffel Tower / Terracotta Warriors",
                    "本单元引入多个<strong>中外名胜</strong>，介绍景点时专有名词首字母大写，"
                    "前面通常加 the：the Great Wall, the Eiffel Tower。",
                    example_table(
                        [("地标", "en"), ("地点", "en"), ("必背短语", "en"), ("中文", "zh")],
                        [
                            [("Great Wall", "en"), ("China", "en"), ("climb the Great Wall", "en"), ("长城；爬长城", "zh")],
                            [("Eiffel Tower", "en"), ("France", "en"), ("visit the Eiffel Tower", "en"), ("埃菲尔铁塔", "zh")],
                            [("Gingerbread House", "en"), ("story place", "en"), ("a must-see attraction", "en"), ("姜饼屋；必游景点", "zh")],
                        ],
                    ),
                    "走进<strong>地球仪宫殿</strong>：中国区旋转出长城（climb）；欧洲区弹出埃菲尔铁塔（visit）；"
                    "童话区飘来姜饼屋（amazing view）——转一圈，地标全进脑！",
                    "palace",
                    """看图说话：
1. I climbed the ___ last year. (Great Wall)
2. We visited the ___ in France. (Eiffel Tower)
3. That is a must-see ___!

写作：用 2 个地标写 3 句旅行介绍。""",
                ),
            ],
            "review": """<ol class="zh">
<li><strong>游戏「旅行小记者」：</strong>两人一组，用 How was...? 和 What did you do? 采访对方的「虚拟旅行」。</li>
<li><strong>游戏「地标快问快答」：</strong>老师说中文，学生抢答英文地标名。</li>
<li><strong>听音排序：</strong>将 went / climbed / visited 与图片配对。</li>
</ol>""",
            "summary_rows": [
                ["一般过去时", "动词过去式", "went/climbed/visited", "I went to Beijing.", "en"],
                ["感受询问", "How was + 名词?", "沙发回忆角", "How was your holiday?", "en"],
                ["活动问答", "What did + 主语 + 原形?", "did 后原形", "What did you do?", "en"],
                ["地标词汇", "the + 专有名词", "地球仪宫殿", "climb the Great Wall", "en"],
            ],
            "quotes": """1. "How was your weekend?" — "It was great!"
2. "What did you do last Saturday?" — "I visited the Gingerbread House."
3. "I climbed the Great Wall last weekend."
4. "Please send me some pictures."
5. "That sounds interesting!"
""",
            "homework": [
                "用 went / climbed / visited 各造 2 个句子",
                "完成 How was...? 与 What did you do? 问答各 3 组",
                "画一张「地标思维导图」并标注英文",
                "（挑战）写 5 句「我的上周末」小日记",
            ],
            "teacher": "旅行是最好的课堂！一般过去时就像相册，把美好经历一页页翻出来。"
            "多开口说 How was your trip，英语就会越来越自然。",
        },
        "part-b": {
            "summary": "本课深入西安旅行话题，掌握 Where did you go? 地点问答、by+交通工具表达，以及兵马俑等文化地标描述。",
            "tree": """【知识点大树🌳】
Where did you go?
│
├─ 🌿 1. 地点问答：Where did you go over the holidays?
├─ 🌿 2. 交通方式：by train / by plane / by cable car
├─ 🌿 3. 文化地标：Terracotta Warriors / Jinggangshan Museum
├─ 🌿 4. 数量表达：21,000 kilometres / over seven thousand
└─ 🌿 5. 感受评价：inspiring / amazing stories""",
            "goals": [
                "用 Where did you go? 询问并回答旅行目的地",
                "运用 by + 交通工具描述出行方式",
                "读懂并介绍兵马俑等文化景点",
                "用一般过去时复述旅行经历",
            ],
            "points": [
                knowledge_point(
                    1,
                    "Where did you go? 地点问答",
                    "Where did you go over the summer holidays?",
                    "询问<strong>过去去了哪里</strong>，用 <strong>Where did + 主语 + go?</strong> "
                    "回答用过去式：I went to Xi'an with my family.",
                    example_table(
                        [("问句", "en"), ("答句", "en"), ("中文", "zh")],
                        [
                            [("Where did you go?", "en"), ("I went to Xi'an.", "en"), ("你去哪儿了？— 我去了西安。", "zh")],
                            [("Where did they go?", "en"), ("They went to Beijing.", "en"), ("他们去哪儿了？— 他们去了北京。", "zh")],
                            [("Where did she go?", "en"), ("She went to France.", "en"), ("她去哪儿了？— 她去了法国。", "zh")],
                        ],
                    ),
                    "西安<strong>古城门楼</strong>上挂着 Where 的旗帜；城楼下石碑刻着 did you go；"
                    "城门洞里传出 I went to Xi'an——三座门，地点问答记牢！",
                    "palace",
                    """填空：
1. Where ___ you ___ (go) last summer?
2. I ___ (go) to Xi'an with my family.
3. ___ did they go? — They went to Shanghai.

翻译：你暑假去哪儿了？— 我和家人去了西安。""",
                ),
                knowledge_point(
                    2,
                    "by + 交通工具",
                    "by train / by plane / by high-speed train / by cable car",
                    "表示<strong>乘坐某种交通工具</strong>，介词 by 后面直接加交通工具名词，<strong>不加 the</strong>。"
                    "by bus, by plane, by high-speed train 都是固定搭配。",
                    example_table(
                        [("交通方式", "en"), ("完整句子", "en"), ("中文", "zh")],
                        [
                            [("by train", "en"), ("We went to Xi'an by train.", "en"), ("我们乘火车去西安。", "zh")],
                            [("by plane", "en"), ("They flew to Paris by plane.", "en"), ("他们乘飞机去巴黎。", "zh")],
                            [("by cable car", "en"), ("We went up the mountain by cable car.", "en"), ("我们乘缆车上山。", "zh")],
                        ],
                    ),
                    "（曲调：《粉刷匠》）By train by train，火车嘟嘟；By plane by plane，飞机呼呼；"
                    "By bus by bus，公交稳稳；By cable car，缆车悠悠！",
                    "song",
                    """选词填空：by train / by plane / by bus / by cable car
1. I went to Beijing ___.
2. We went to the island ___.
3. They went to school ___.

造句：写 3 句，说说你和家人怎么去旅行。""",
                ),
                knowledge_point(
                    3,
                    "文化地标与描述",
                    "Terracotta Warriors / inspiring stories",
                    "介绍景点时，除了名称，还要会用<strong>数量词</strong>和<strong>形容词</strong>描述："
                    "over seven thousand clay warriors；The stories were really inspiring.",
                    example_table(
                        [("表达", "en"), ("例句", "en"), ("中文", "zh")],
                        [
                            [("数量", "en"), ("There are over seven thousand clay warriors.", "en"), ("有七千多个陶俑。", "zh")],
                            [("长度", "en"), ("The Great Wall is 21,000 kilometres in all.", "en"), ("长城全长21000公里。", "zh")],
                            [("评价", "en"), ("The stories were really inspiring.", "en"), ("那些故事非常鼓舞人心。", "zh")],
                        ],
                    ),
                    "兵马俑博物馆大厅：左边陈列 seven thousand warriors；"
                    "右边屏幕播放 inspiring stories；中间大桥模型写着 Hong Kong-Zhuhai-Macao Bridge。",
                    "palace",
                    """连词成句：
1. really / were / inspiring / The / stories / .
2. thousand / over / seven / There / warriors / are / clay / .
3. noodles / ate / We / Xi'an / .

仿写：介绍一个你去过（或想去的）景点，至少 3 句。""",
                ),
            ],
            "review": """<ol class="zh">
<li><strong>「交通大转盘」：</strong>转动转盘说出 by + 交通工具，并造完整句。</li>
<li><strong>「西安导游」角色扮演：</strong>一人当导游介绍兵马俑，听众用 Where/What 提问。</li>
<li><strong>数字听写：</strong>听 21,000 / seven thousand 快速写下英文。</li>
</ol>""",
            "summary_rows": [
                ["地点问答", "Where did + 主语 + go?", "古城门楼", "Where did you go?", "en"],
                ["交通方式", "by + 交通工具", "交通歌", "by high-speed train", "en"],
                ["景点描述", "数量 + 名词", "博物馆大厅", "over seven thousand warriors", "en"],
                ["评价形容词", "was/were + adj.", "inspiring", "The stories were inspiring.", "en"],
            ],
            "quotes": """1. "Where did you go over the summer holidays?"
2. "I went to Xi'an with my family."
3. "We went to see the Terracotta Warriors."
4. "The Great Wall is 21,000 kilometres in all."
5. "The stories were really inspiring."
""",
            "homework": [
                "用 Where did you go? 写一段问答（至少 4 句）",
                "用 by + 交通工具造 5 个句子",
                "介绍兵马俑或长城（英文 5 句，含数量词）",
                "（挑战）画旅行路线图并英文标注交通方式",
            ],
            "teacher": "西安是历史文化宝库，英语是打开世界的钥匙。"
            "把景点名称和过去时句型结合起来，你就能像小导游一样流利介绍中国！",
        },
        "part-c": {
            "summary": "本课系统归纳一般过去时规则：肯定句、否定句 didn't、疑问句 Did...?，以及常见不规则动词变化。",
            "tree": """【知识点大树🌳】
Past Simple Rules
│
├─ 🌿 1. 肯定句：主语 + 动词过去式
├─ 🌿 2. 否定句：didn't + 动词原形
├─ 🌿 3. 疑问句：Did + 主语 + 动词原形?
├─ 🌿 4. 规则变化：-ed（climbed, visited）
└─ 🌿 5. 不规则动词：go→went, see→saw, eat→ate, take→took""",
            "goals": [
                "归纳一般过去时肯定、否定、疑问句结构",
                "区分规则动词 -ed 与不规则动词变化",
                "正确使用 didn't 和 Did 疑问句",
                "完成语法填空与句型转换练习",
            ],
            "points": [
                knowledge_point(
                    1,
                    "肯定句结构",
                    "Subject + Verb (past form)",
                    "一般过去时<strong>肯定句</strong>：主语 + 动词过去式 + 其他。"
                    "时间标志词：last weekend, yesterday, over the summer holidays。",
                    example_table(
                        [("结构", "en"), ("例句", "en"), ("中文", "zh")],
                        [
                            [("规则 -ed", "en"), ("I visited the museum.", "en"), ("我参观了博物馆。", "zh")],
                            [("不规则", "en"), ("She went to Xi'an.", "en"), ("她去了西安。", "zh")],
                            [("be 动词", "en"), ("It was amazing!", "en"), ("太棒了！", "zh")],
                        ],
                    ),
                    "时间轴宫殿：入口牌 last weekend → 走廊 climbed/visited → "
                    "终点柜 went/saw/ate。沿时间轴走一遍，肯定句全会！",
                    "palace",
                    """写出过去式：
go→___  see→___  eat→___  climb→___  visit→___

造肯定句（各 1 句）：
1. last Sunday + go
2. yesterday + visit
3. last year + climb""",
                ),
                knowledge_point(
                    2,
                    "否定句 didn't",
                    "I didn't go to Beijing.",
                    "否定句用 <strong>didn't（did not）+ 动词原形</strong>，"
                    "过去式变化全部「还原」成原形！",
                    example_table(
                        [("肯定", "en"), ("否定", "en"), ("中文", "zh")],
                        [
                            [("I went to Beijing.", "en"), ("I didn't go to Beijing.", "en"), ("我没去北京。", "zh")],
                            [("She climbed the wall.", "en"), ("She didn't climb the wall.", "en"), ("她没爬长城。", "zh")],
                            [("They visited Paris.", "en"), ("They didn't visit Paris.", "en"), ("他们没参观巴黎。", "zh")],
                        ],
                    ),
                    "（曲调：《上学歌》）Didn't didn't，否定来；动词原形放后面；"
                    "Went climbed visited，全部变回原形！",
                    "song",
                    """否定句转换：
1. I went to Shanghai. → I ___ go to Shanghai.
2. She visited the museum. → She ___ visit the museum.
3. They climbed the hill. → They ___ climb the hill.

答案：1.didn't  2.didn't  3.didn't""",
                ),
                knowledge_point(
                    3,
                    "疑问句 Did...?",
                    "Did you climb the Great Wall? — Yes, I did. / No, I didn't.",
                    "一般疑问句：<strong>Did + 主语 + 动词原形?</strong> "
                    "肯定答 Yes, 主语 + did. 否定答 No, 主语 + didn't.",
                    example_table(
                        [("问句", "en"), ("肯定答", "en"), ("否定答", "en")],
                        [
                            [("Did you climb the Great Wall?", "en"), ("Yes, I did.", "en"), ("No, I didn't.", "en")],
                            [("Did she go to Xi'an?", "en"), ("Yes, she did.", "en"), ("No, she didn't.", "en")],
                            [("Did they take photos?", "en"), ("Yes, they did.", "en"), ("No, they didn't.", "en")],
                        ],
                    ),
                    "电话亭宫殿：拿起听筒问 Did you...?；按绿色键答 Yes, I did；"
                    "按红色键答 No, I didn't。三色按钮，疑问应答分清！",
                    "palace",
                    """句型转换：
1. You visited the museum. → ___ you ___ the museum?
2. She went to Paris. → ___ she ___ to Paris?
3. They climbed the hill. → ___ they ___ the hill?

问答配对：自编 3 组 Did 问句与答句。""",
                ),
                knowledge_point(
                    4,
                    "不规则动词速记",
                    "go→went  see→saw  eat→ate  take→took",
                    "不规则动词没有 -ed 规律，需要<strong>整词记忆</strong>。"
                    "本单元高频：go→went, see→saw, eat→ate, take→took, send→sent。",
                    example_table(
                        [("原形", "en"), ("过去式", "en"), ("例句", "en")],
                        [
                            [("go", "en"), ("went", "en"), ("I went to Xi'an.", "en")],
                            [("see", "en"), ("saw", "en"), ("We saw the warriors.", "en")],
                            [("eat", "en"), ("ate", "en"), ("They ate noodles.", "en")],
                            [("take", "en"), ("took", "en"), ("I took many photos.", "en")],
                        ],
                    ),
                    "（口诀歌）Go went走，See saw看，Eat ate吃，Take took拍；"
                    "Send sent发，五个兄弟记心间！",
                    "song",
                    """不规则动词填空：
1. I ___ (go) to Beijing last year.
2. We ___ (see) the Terracotta Warriors.
3. She ___ (eat) Xi'an noodles.
4. They ___ (take) many photos.

答案：1.went  2.saw  3.ate  4.took""",
                ),
            ],
            "review": """<ol class="zh">
<li><strong>「句型三轮变」：</strong>同一句话轮流变肯定、否定、疑问。</li>
<li><strong>「不规则动词接龙」：</strong>说原形，下一位说过去式。</li>
<li><strong>语法闯关：</strong>10 道填空，正确率 80% 过关。</li>
</ol>""",
            "summary_rows": [
                ["肯定句", "主语 + 过去式", "时间轴宫殿", "I visited the museum.", "en"],
                ["否定句", "didn't + 原形", "否定歌", "I didn't go to Beijing.", "en"],
                ["疑问句", "Did + 主语 + 原形?", "电话亭", "Did you climb the wall?", "en"],
                ["不规则动词", "整词记忆", "五兄弟歌", "go→went, see→saw", "en"],
            ],
            "quotes": """1. "I climbed the Great Wall last weekend."
2. "I didn't go to Beijing."
3. "Did you climb the Great Wall? — Yes, I did."
4. "What did you do? — I went to Xi'an."
5. "They ate Xi'an noodles and visited the warriors."
""",
            "homework": [
                "整理本单元不规则动词表（至少 8 个）",
                "各写 2 句肯定、否定、疑问句",
                "完成 Part C 语法练习并订正",
                "（挑战）用 8 个过去式动词写「旅行故事」",
            ],
            "teacher": "语法是骨架，词汇是血肉。把过去时三种句型练熟，"
            "你的英语表达就有了坚实的支撑！",
        },
        "reading": {
            "summary": "阅读精讲《My Trip to Xi'an》，掌握旅行记叙文阅读策略、人物与事件梳理，以及仿写旅行日记。",
            "tree": """【知识点大树🌳】
My Trip to Xi'an
│
├─ 🌿 1. 阅读策略：抓人物、时间、地点、事件
├─ 🌿 2. 记叙顺序：First → Then → Finally
├─ 🌿 3. 文化理解：兵马俑 / 井冈山革命博物馆
├─ 🌿 4. 词汇复现：went / visited / ate / inspiring
└─ 🌿 5. 写作输出：仿写 My Trip to... 短文""",
            "goals": [
                "读懂 My Trip to Xi'an 全文大意与细节",
                "梳理陈洁与 Sarah 的不同旅行经历",
                "积累旅行记叙文常用连接词",
                "仿写 5-8 句旅行日记",
            ],
            "points": [
                knowledge_point(
                    1,
                    "阅读抓主干",
                    "Who? When? Where? What?",
                    "阅读记叙文先找<strong>四个 W</strong>：Who（谁）、When（何时）、"
                    "Where（何地）、What（做了什么）。",
                    example_table(
                        [("要素", "en"), ("陈洁 Chen Jie", "en"), ("Sarah", "en")],
                        [
                            [("When", "en"), ("Last summer", "en"), ("(课文同期)", "en")],
                            [("Where", "en"), ("Xi'an", "en"), ("Jinggangshan Museum", "en")],
                            [("What", "en"), ("ate noodles, visited warriors", "en"), ("heard inspiring stories", "en")],
                        ],
                    ),
                    "阅读宫殿四个房间：Who 挂照片、When 摆日历、Where 放地图、What 贴活动卡片。"
                    "进房间取信息，阅读理解不迷路！",
                    "palace",
                    """阅读填空（不看课文，根据精讲回忆）：
1. Chen Jie went to ___ last summer.
2. They ate famous ___ noodles.
3. There were over seven thousand ___ warriors.
4. Sarah went to the Jinggangshan Revolution ___.
5. The stories were really ___.""",
                ),
                knowledge_point(
                    2,
                    "记叙顺序词",
                    "First / Then / Next / Finally",
                    "写旅行故事要有<strong>时间顺序</strong>，常用连接词让文章更流畅："
                    "First... Then... Finally...",
                    example_table(
                        [("连接词", "en"), ("例句", "en"), ("中文", "zh")],
                        [
                            [("First", "en"), ("First, we went to Xi'an by train.", "en"), ("首先，我们乘火车去西安。", "zh")],
                            [("Then", "en"), ("Then, we ate famous noodles.", "en"), ("然后，我们吃了名小吃。", "zh")],
                            [("Finally", "en"), ("Finally, we visited the warriors.", "en"), ("最后，我们参观了兵马俑。", "zh")],
                        ],
                    ),
                    "（曲调：《排排队》）First first 第一先，Then then 接着干，"
                    "Next next 再一步，Finally 圆满完！",
                    "song",
                    """排序写作：
用 First / Then / Finally 描述「我的一次旅行」：
First, I ______________________.
Then, I ______________________.
Finally, I ______________________.""",
                ),
                knowledge_point(
                    3,
                    "红色文化表达",
                    "Jinggangshan / inspiring stories",
                    "课文介绍<strong>井冈山革命博物馆</strong>，用 inspiring 形容鼓舞人心的故事，"
                    "体现英语学习中<strong>中国文化传播</strong>。",
                    example_table(
                        [("表达", "en"), ("用法", "zh"), ("例句", "en")],
                        [
                            [("inspiring", "en"), ("鼓舞人心的", "zh"), ("The stories were really inspiring.", "en")],
                            [("red culture", "en"), ("红色文化", "zh"), ("We learned about red culture.", "en")],
                            [("museum", "en"), ("博物馆", "zh"), ("Sarah visited the museum.", "en")],
                        ],
                    ),
                    "博物馆长廊：左边兵马俑 clay warriors；右边井冈山 revolution stories；"
                    "尽头大屏幕写 inspiring——一条长廊，文化双记！",
                    "palace",
                    """翻译：
1. 那些故事非常鼓舞人心。
2. Sarah 参观了井冈山革命博物馆。
3. 有七千多个陶俑。

讨论：Why are these places important?（用英语说 1-2 句）""",
                ),
                knowledge_point(
                    4,
                    "仿写旅行日记",
                    "My Trip to... writing frame",
                    "仿照课文结构写<strong>5-8 句</strong>旅行日记："
                    "时间 + 地点 + 交通 + 活动 + 感受。",
                    example_table(
                        [("写作步骤", "zh"), ("句型支架", "en")],
                        [
                            [("开头", "zh"), ("Last summer, I went to ... with ...", "en")],
                            [("交通", "zh"), ("We went there by ...", "en")],
                            [("活动", "zh"), ("We ate ... and visited ...", "en")],
                            [("结尾", "zh"), ("It was amazing / inspiring!", "en")],
                        ],
                    ),
                    "作文宫殿：门口写 Last summer；客厅摆 by train；"
                    "厨房放 ate noodles；卧室挂 It was amazing！",
                    "palace",
                    """仿写任务：
My Trip to _______
Last ____, I went to ______ with ______.
We went there by ______.
We ______ and ______.
It was ______!

（至少 5 句，用上 3 个过去式动词）""",
                ),
            ],
            "review": """<ol class="zh">
<li><strong>「细节寻宝」：</strong>教师提问细节（数字、地名、动词），学生抢答。</li>
<li><strong>「双故事对比」：</strong>比较 Chen Jie 与 Sarah 旅行的异同。</li>
<li><strong>「口头复述」：</strong>用 First/Then/Finally 复述课文。</li>
</ol>""",
            "summary_rows": [
                ["阅读策略", "4W 抓主干", "阅读四房间", "Who/When/Where/What", "en"],
                ["顺序词", "First/Then/Finally", "排排队歌", "First, we went...", "en"],
                ["文化词汇", "inspiring / museum", "博物馆长廊", "inspiring stories", "en"],
                ["写作框架", "时间+地点+活动+感受", "作文宫殿", "My Trip to...", "en"],
            ],
            "quotes": """1. "Last summer, Chen Jie went to Xi'an with her family."
2. "They ate famous Xi'an noodles."
3. "There were over seven thousand clay warriors."
4. "The stories were really inspiring."
5. "Sarah went to the Jinggangshan Revolution Museum."
""",
            "homework": [
                "默写课文关键句 5 句",
                "完成阅读理解题（人物、地点、事件）",
                "仿写 My Trip to...（8 句以上）",
                "（挑战）制作「西安旅行」英文手抄报",
            ],
            "teacher": "阅读是输入，写作是输出。读懂陈洁的西安之旅，"
            "你也一定能用英语讲述自己的精彩经历！",
        },
    }
    return specs[part_key]


def u2_content(part_key: str) -> dict:
    specs = {
        "part-a": {
            "summary": "本课围绕中外节日欢聚主题，掌握 Did you...? 一般疑问句、节日核心词汇，以及春节传统习俗表达。",
            "tree": """【知识点大树🌳】
Did you enjoy the festival?
│
├─ 🌿 1. 一般疑问句：Did you eat mooncakes?
├─ 🌿 2. 节日词汇：Spring Festival / Mid-Autumn Festival
├─ 🌿 3. 春节习俗：paste fu / dress in red / count down
├─ 🌿 4. 感受询问：How was your holiday?
└─ 🌿 5. 规则过去式：cleaned / pasted / dressed""",
            "goals": [
                "用 Did you...? 询问节日活动",
                "说出春节、中秋等节日核心词汇",
                "描述贴福字、穿红衣、倒计时等习俗",
                "正确回答 Yes, we did. / No, we didn't.",
            ],
            "points": [
                knowledge_point(
                    1,
                    "Did you...? 一般疑问句",
                    "Did you eat mooncakes? — Yes, we did. / No, we didn't.",
                    "询问<strong>过去是否做了某事</strong>，用 <strong>Did + 主语 + 动词原形?</strong> "
                    "这是 Unit 2 最核心的全新语法！",
                    example_table(
                        [("问句", "en"), ("肯定答", "en"), ("否定答", "en")],
                        [
                            [("Did you eat mooncakes?", "en"), ("Yes, we did.", "en"), ("No, we didn't.", "en")],
                            [("Did you clean the house?", "en"), ("Yes, I did.", "en"), ("No, I didn't.", "en")],
                            [("Did you watch the gala?", "en"), ("Yes, we did.", "en"), ("No, we didn't.", "en")],
                        ],
                    ),
                    "春节红包宫殿：红包正面写 Did you...?；打开见 Yes, I did；"
                    "空红包写 No, I didn't。一问一答，红包里藏语法！",
                    "palace",
                    """问答练习：
1. Did you ___ (eat) mooncakes? — Yes, we ___.
2. Did she ___ (clean) the house? — No, she ___.
3. ___ you dress in red? — Yes, I ___.

注意：Did 后面用原形 eat，不是 ate！""",
                ),
                knowledge_point(
                    2,
                    "节日词汇与文化",
                    "Spring Festival / Mid-Autumn Festival / mooncakes",
                    "中外节日名称首字母大写：the Spring Festival, the Mid-Autumn Festival。"
                    "节日食物是不可数或复数：mooncakes, zongzi, jiaozi。",
                    example_table(
                        [("节日", "en"), ("活动", "en"), ("食物", "en"), ("中文", "zh")],
                        [
                            [("Spring Festival", "en"), ("paste fu, count down", "en"), ("jiaozi", "en"), ("春节；贴福字；饺子", "zh")],
                            [("Mid-Autumn Festival", "en"), ("enjoy the moon", "en"), ("mooncakes", "en"), ("中秋节；月饼", "zh")],
                            [("Dragon Boat Festival", "en"), ("dragon boat race", "en"), ("zongzi", "en"), ("端午节；粽子", "zh")],
                        ],
                    ),
                    "（曲调：《新年好》）Spring Festival 春节到，Mid-Autumn 月饼香；"
                    "Dragon Boat 赛龙舟，Festivals 记心上！",
                    "song",
                    """节日配对：
1. mooncakes → ___
2. paste fu → ___
3. dragon boat race → ___

选项：Spring Festival / Mid-Autumn Festival / Dragon Boat Festival""",
                ),
                knowledge_point(
                    3,
                    "春节习俗短语",
                    "paste fu on the door / dress in red / count down to the new year",
                    "春节三大习俗动词都是<strong>规则过去式</strong>：paste→pasted, dress→dressed, count→counted。"
                    "描述习俗用 We pasted fu on the door.",
                    example_table(
                        [("短语", "en"), ("过去式句子", "en"), ("中文", "zh")],
                        [
                            [("paste fu on the door", "en"), ("We pasted fu on the door.", "en"), ("我们在门上贴了福字。", "zh")],
                            [("dress in red", "en"), ("We dressed in red.", "en"), ("我们穿了红色衣服。", "zh")],
                            [("count down to the new year", "en"), ("We counted down to the new year.", "en"), ("我们倒计时迎接新年。", "zh")],
                        ],
                    ),
                    "春节客厅宫殿：大门贴 pasted fu；镜子前 dressed in red；"
                    "电视前 counted down——三个位置，习俗全记住！",
                    "palace",
                    """用过去时描述春节：
1. We ___ (clean) the house.
2. We ___ (paste) fu on the door.
3. We ___ (dress) in red.
4. We ___ (count) down to the new year.

答案：1.cleaned  2.pasted  3.dressed  4.counted""",
                ),
                knowledge_point(
                    4,
                    "How was your holiday?",
                    "How was your Mid-Autumn Festival holiday?",
                    "节日问候延续 Unit 1 的 How was...? 句型，"
                    "询问整个假期感受：How was your Mid-Autumn Festival holiday?",
                    example_table(
                        [("问句", "en"), ("答句", "en"), ("中文", "zh")],
                        [
                            [("How was your holiday?", "en"), ("It was exciting!", "en"), ("你假期过得怎么样？— 很激动！", "zh")],
                            [("What did you do?", "en"), ("We enjoyed mooncakes.", "en"), ("你们做了什么？— 我们吃了月饼。", "zh")],
                            [("Did you eat mooncakes?", "en"), ("Yes, we did.", "en"), ("你们吃月饼了吗？— 是的。", "zh")],
                        ],
                    ),
                    "节日圆桌宫殿：圆桌中央 How was your holiday?；"
                    "每人面前一道菜对应一个节日活动，边吃边练英语！",
                    "palace",
                    """综合对话（4 句以上）：
A: How was your Spring Festival?
B: It was great!
A: What did you do?
B: We cleaned the house and pasted fu.
A: Did you eat jiaozi?
B: Yes, we did!""",
                ),
            ],
            "review": """<ol class="zh">
<li><strong>「节日 Bingo」：</strong>听到节日活动短语就标记，先连成线者胜。</li>
<li><strong>「Did you 快问快答」：</strong>两人轮流问 Did you...? 真实回答。</li>
<li><strong>习俗动作秀：</strong>做 paste fu / dress in red 动作并说英文。</li>
</ol>""",
            "summary_rows": [
                ["Did 疑问句", "Did + 主语 + 原形?", "红包宫殿", "Did you eat mooncakes?", "en"],
                ["节日词汇", "专有名词大写", "节日歌", "Spring Festival", "en"],
                ["春节习俗", "paste/dress/count", "客厅三位置", "pasted fu on the door", "en"],
                ["感受询问", "How was...?", "节日圆桌", "It was exciting!", "en"],
            ],
            "quotes": """1. "How was your Mid-Autumn Festival holiday, Binbin?"
2. "Did you eat mooncakes?" — "Yes, we did."
3. "We pasted fu on the door."
4. "We dressed in red and counted down to the new year."
5. "We enjoyed some mooncakes and fruit."
""",
            "homework": [
                "用 Did you...? 写 5 组问答",
                "描述你家春节习俗（英文 5 句，过去时）",
                "制作节日词汇卡片（中英对照）",
                "（挑战）介绍一个中国节日给外国朋友（8 句）",
            ],
            "teacher": "节日是文化的窗口，英语是分享的桥梁。"
            "用 Did you eat mooncakes? 开启跨文化交流吧！",
        },
        "part-b": {
            "summary": "本课拓展节日活动语篇，重点掌握不规则动词 ate/ran/made，以及马拉松、龙舟赛等欢聚活动表达。",
            "tree": """【知识点大树🌳】
What did you do for the festival?
│
├─ 🌿 1. 不规则动词：ate / ran / made / won
├─ 🌿 2. 活动短语：go to a marathon / cheer for runners
├─ 🌿 3. 龙舟文化：dragon boat race / make zongzi
├─ 🌿 4. 分享表达：share ideas / work as a volunteer
└─ 🌿 5. 最高级评价：the best festival ever""",
            "goals": [
                "掌握 ate / ran / made / won 等不规则过去式",
                "描述马拉松、书市、龙舟赛等活动",
                "用一般过去时讲述节日经历",
                "理解中外欢聚活动的文化差异",
            ],
            "points": [
                knowledge_point(
                    1,
                    "不规则动词 ate / ran / made",
                    "eat→ate  run→ran  make→made",
                    "节日活动中常出现<strong>不规则动词</strong>，必须整词记忆："
                    "eat→ate, run→ran, make→made, win→won, wake→woke。",
                    example_table(
                        [("原形", "en"), ("过去式", "en"), ("例句", "en"), ("中文", "zh")],
                        [
                            [("eat", "en"), ("ate", "en"), ("We ate jiaozi.", "en"), ("我们吃了饺子。", "zh")],
                            [("run", "en"), ("ran", "en"), ("He ran in the marathon.", "en"), ("他参加了马拉松。", "zh")],
                            [("make", "en"), ("made", "en"), ("We made zongzi.", "en"), ("我们包了粽子。", "zh")],
                            [("win", "en"), ("won", "en"), ("His team won the race.", "en"), ("他的队赢了比赛。", "zh")],
                        ],
                    ),
                    "（口诀）Eat ate 吃，Run ran 跑，Make made 做，Win won 赢；"
                    "Wake woke 醒，Begin began 始，不规则要记清！",
                    "song",
                    """填空：
1. We ___ (eat) mooncakes yesterday.
2. She ___ (run) in the marathon.
3. They ___ (make) zongzi together.
4. His team ___ (win) the dragon boat race.

答案：1.ate  2.ran  3.made  4.won""",
                ),
                knowledge_point(
                    2,
                    "马拉松与志愿者",
                    "go to a marathon / work as a volunteer / cheer for the runners",
                    "除了传统节日，课文还介绍<strong>现代欢聚活动</strong>："
                    "马拉松、线上书市，体现多元生活方式。",
                    example_table(
                        [("短语", "en"), ("例句", "en"), ("中文", "zh")],
                        [
                            [("go to a marathon", "en"), ("I went to a marathon yesterday.", "en"), ("我昨天参加了马拉松。", "zh")],
                            [("work as a volunteer", "en"), ("My dad worked as a volunteer.", "en"), ("我爸爸做了志愿者。", "zh")],
                            [("cheer for the runners", "en"), ("We cheered for the runners.", "en"), ("我们为选手加油。", "zh")],
                        ],
                    ),
                    "赛道宫殿：起点 go to a marathon；路旁 work as a volunteer；"
                    "终点线 cheer for the runners——跑完全程，短语全会！",
                    "palace",
                    """造句：
1. Yesterday I ___ (go) to a marathon.
2. We ___ (cheer) for the runners.
3. My mum ___ (work) as a volunteer.

讨论：What did you like about it? — I liked watching the runners.""",
                ),
                knowledge_point(
                    3,
                    "龙舟赛与包粽子",
                    "dragon boat race / make zongzi",
                    "端午节核心活动：<strong>dragon boat race</strong>（龙舟赛）和 <strong>make zongzi</strong>（包粽子），"
                    "描述结果用 won the race。",
                    example_table(
                        [("表达", "en"), ("例句", "en"), ("中文", "zh")],
                        [
                            [("dragon boat race", "en"), ("We watched the dragon boat race.", "en"), ("我们观看了龙舟赛。", "zh")],
                            [("make zongzi", "en"), ("We made zongzi with grandma.", "en"), ("我们和奶奶包粽子。", "zh")],
                            [("the best festival ever", "en"), ("It was the best Dragon Boat Festival ever!", "en"), ("这是最棒的端午节！", "zh")],
                        ],
                    ),
                    "江边宫殿：码头停着 dragon boat；岸边桌上有 zongzi；"
                    "领奖台写着 won the race——江边一日游，端午文化记！",
                    "palace",
                    """阅读问答：
1. What festival is it?
2. What did they make?
3. Who won the race?
4. How do they feel? (the best ... ever)

写作：写 3 句描述你的端午节。""",
                ),
                knowledge_point(
                    4,
                    "分享与书市",
                    "join an online book fair / share ideas",
                    "线上书市 join an online book fair 和 share ideas 体现<strong>现代学习交流</strong>方式。",
                    example_table(
                        [("短语", "en"), ("例句", "en"), ("中文", "zh")],
                        [
                            [("join an online book fair", "en"), ("I joined an online book fair.", "en"), ("我参加了线上书市。", "zh")],
                            [("share ideas", "en"), ("We shared ideas about books.", "en"), ("我们分享了读书想法。", "zh")],
                            [("exciting", "en"), ("It was exciting!", "en"), ("太令人激动了！", "zh")],
                        ],
                    ),
                    "（曲调：《读书郎》）Book fair book fair 线上逛，Share ideas 互启发；"
                    "Exciting exciting 真有趣，读书分享乐哈哈！",
                    "song",
                    """综合写作：
Last week I joined ___. I shared ___ with my friends.
It was ___!

（用上 joined / shared / exciting）""",
                ),
            ],
            "review": """<ol class="zh">
<li><strong>「不规则动词擂台」：</strong>快速说出 eat/run/make/win 的过去式。</li>
<li><strong>「活动猜猜看」：</strong>描述活动，同学猜短语名称。</li>
<li><strong>节日故事接龙：</strong>每人一句过去时，串联成故事。</li>
</ol>""",
            "summary_rows": [
                ["不规则动词", "整词记忆", "口诀歌", "ate / ran / made / won", "en"],
                ["马拉松", "go to a marathon", "赛道宫殿", "cheer for the runners", "en"],
                ["端午文化", "dragon boat / zongzi", "江边宫殿", "won the race", "en"],
                ["现代交流", "online book fair", "读书郎", "share ideas", "en"],
            ],
            "quotes": """1. "Did you take a trip?" — "No, we didn't."
2. "We made zongzi with grandma."
3. "Finally, his team won the race!"
4. "It was the best Dragon Boat Festival ever!"
5. "I joined an online book fair and shared ideas."
""",
            "homework": [
                "背诵不规则动词 ate/ran/made/won/wake/begin",
                "写端午节或马拉松经历（6 句）",
                "用 cheer for / share ideas 各造 2 句",
                "（挑战）比较春节与端午习俗（英文对照表）",
            ],
            "teacher": "不规则动词像节日的烟花，每一个都很特别。"
            "多写多练，ate ran made 就会变成你的老朋友！",
        },
        "part-c": {
            "summary": "本课系统梳理 Did 疑问句规则、规则/不规则过去式对照，以及节日主题句型综合练习。",
            "tree": """【知识点大树🌳】
Past Simple Review (Festivals)
│
├─ 🌿 1. Did 问句：Did + 主语 + 原形?
├─ 🌿 2. 规则 -ed：cleaned / pasted / enjoyed
├─ 🌿 3. 不规则：ate / ran / made / won
├─ 🌿 4. 答句：Yes, ... did. / No, ... didn't.
└─ 🌿 5. 综合：How was...? + What did...? + Did you...?""",
            "goals": [
                "熟练运用 Did you...? 及回答",
                "区分规则与不规则动词过去式",
                "综合使用 Unit 2 三大句型",
                "完成节日主题语法综合练习",
            ],
            "points": [
                knowledge_point(
                    1,
                    "Did 疑问句三大规则",
                    "Did + subject + base verb?",
                    "规则一：Did 提前；规则二：Did 后动词用原形；"
                    "规则三：答句用 did/didn't，不再重复实义动词过去式。",
                    example_table(
                        [("规则", "zh"), ("正确", "en"), ("错误", "en")],
                        [
                            [("Did 后用原形", "zh"), ("Did you eat mooncakes?", "en"), ("Did you ate...? ❌", "en")],
                            [("答句简洁", "zh"), ("Yes, we did.", "en"), ("Yes, we ate. ❌", "en")],
                            [("否定答", "zh"), ("No, we didn't.", "en"), ("No, we don't. ❌", "en")],
                        ],
                    ),
                    "红绿灯宫殿：绿灯 Did + 原形通过；红灯 ate/went 禁止进入 Did 后；"
                    "黄灯答句只亮 did/didn't！",
                    "palace",
                    """改错：
1. Did you ate mooncakes? → ___
2. Yes, I ate. (回答 Did you...) → ___
3. No, I don't. → ___

答案：
1. Did you eat mooncakes?
2. Yes, I did.
3. No, I didn't.""",
                ),
                knowledge_point(
                    2,
                    "规则 vs 不规则对照",
                    "clean→cleaned  vs  eat→ate",
                    "规则动词加 -ed；不规则动词单独背。"
                    "节日主题高频对照表要熟记。",
                    example_table(
                        [("规则动词", "en"), ("过去式", "en"), ("不规则", "en"), ("过去式", "en")],
                        [
                            [("clean", "en"), ("cleaned", "en"), ("eat", "en"), ("ate", "en")],
                            [("paste", "en"), ("pasted", "en"), ("run", "en"), ("ran", "en")],
                            [("enjoy", "en"), ("enjoyed", "en"), ("make", "en"), ("made", "en")],
                            [("dress", "en"), ("dressed", "en"), ("win", "en"), ("won", "en")],
                        ],
                    ),
                    "（分类歌）-ed -ed 规则带，Ate ran made 不规则；"
                    "左边贴 -ed 标签，右边放不规则篮！",
                    "song",
                    """分类练习：将下列动词填入规则/不规则栏
clean, eat, paste, run, enjoy, make, win, dress

规则：__________
不规则：__________""",
                ),
                knowledge_point(
                    3,
                    "三大句型综合",
                    "How was...? + What did...? + Did you...?",
                    "Unit 2 综合运用三种句型，完成节日主题对话："
                    "先问感受，再问活动，最后用 Did 确认细节。",
                    example_table(
                        [("句型", "en"), ("例句", "en"), ("用途", "zh")],
                        [
                            [("How was...?", "en"), ("How was your holiday?", "en"), ("问感受", "zh")],
                            [("What did...?", "en"), ("What did you do?", "en"), ("问活动", "zh")],
                            [("Did you...?", "en"), ("Did you eat mooncakes?", "en"), ("确认细节", "zh")],
                        ],
                    ),
                    "三层蛋糕宫殿：底层 How was（感受奶油）；"
                    "中层 What did（活动夹心）；顶层 Did you（细节樱桃）！",
                    "palace",
                    """完整对话编写（8 句）：
A: How was your ___ Festival?
B: It was ___!
A: What did you do?
B: We ___ and ___.
A: Did you ___?
B: Yes, we did. / No, we didn't.""",
                ),
            ],
            "review": """<ol class="zh">
<li><strong>「语法三轮变」：</strong>肯定句 → Did 问句 → 回答。</li>
<li><strong>「规则不规则分类赛」：</strong>10 个动词快速分类。</li>
<li><strong>单元综合测验：</strong>20 题限时完成。</li>
</ol>""",
            "summary_rows": [
                ["Did 问句", "Did + 主语 + 原形", "红绿灯", "Did you eat...?", "en"],
                ["规则过去式", "-ed", "分类歌", "cleaned / pasted", "en"],
                ["不规则过去式", "整词记忆", "不规则篮", "ate / ran / made", "en"],
                ["句型综合", "How/What/Did", "三层蛋糕", "节日对话", "en"],
            ],
            "quotes": """1. "Did you eat mooncakes?" — "Yes, we did."
2. "What did you do for the Spring Festival?"
3. "We dressed in red and counted down."
4. "His team won the dragon boat race."
5. "It was the best festival ever!"
""",
            "homework": [
                "整理 Unit 2 不规则动词表（10 个）",
                "写出 Did 问句规则三条并举例",
                "完成综合语法练习",
                "（挑战）编写「节日采访」完整对话（10 句）",
            ],
            "teacher": "语法归纳像包粽子，把零散知识点包成整齐的一束。"
            "复习透了，考试就能稳拿分！",
        },
        "reading": {
            "summary": "阅读精讲《The Spring Festival》，掌握节日记叙文阅读、春节文化细节理解，以及仿写节日日记。",
            "tree": """【知识点大树🌳】
The Spring Festival
│
├─ 🌿 1. 文章结构：准备 → 庆祝 → 感受
├─ 🌿 2. 春节序列：clean → paste fu → dress → count down
├─ 🌿 3. 情感表达：great fun / the best festival ever
├─ 🌿 4. 语法复现：过去时动词链
└─ 🌿 5. 写作：My Festival Story""",
            "goals": [
                "读懂 The Spring Festival 全文",
                "按顺序复述春节准备与庆祝活动",
                "理解 the best festival ever 等情感表达",
                "仿写自己的节日故事",
            ],
            "points": [
                knowledge_point(
                    1,
                    "文章结构三分法",
                    "Before → During → Feeling",
                    "节日记叙文常按<strong>准备—庆祝—感受</strong>展开："
                    "先 clean/paste，再 dress/count down，最后评价 great fun。",
                    example_table(
                        [("阶段", "en"), ("活动", "en"), ("动词", "en")],
                        [
                            [("准备 Before", "en"), ("clean the house, paste fu", "en"), ("cleaned, pasted", "en")],
                            [("庆祝 During", "en"), ("dress in red, count down, enjoy food", "en"), ("dressed, counted, enjoyed", "en")],
                            [("感受 Feeling", "en"), ("great fun / the best festival ever", "en"), ("was", "en")],
                        ],
                    ),
                    "时间轴宫殿：左栏 Before 打扫贴福；中栏 During 穿衣倒计时；"
                    "右栏 Feeling 写 great fun！",
                    "palace",
                    """段落匹配：
将活动填入正确阶段：
a. counted down to the new year
b. cleaned the house
c. It was the best festival ever
d. pasted fu on the door""",
                ),
                knowledge_point(
                    2,
                    "春节活动动词链",
                    "cleaned → pasted → dressed → counted → enjoyed",
                    "课文用一连串<strong>过去式动词</strong>按时间推进叙事，"
                    "读时要注意动词先后顺序。",
                    example_table(
                        [("顺序", "en"), ("句子", "en"), ("中文", "zh")],
                        [
                            [("1", "en"), ("My family cleaned the house.", "en"), ("我家打扫了房子。", "zh")],
                            [("2", "en"), ("We pasted fu on the door.", "en"), ("我们贴了福字。", "zh")],
                            [("3", "en"), ("We dressed in red.", "en"), ("我们穿了红衣。", "zh")],
                            [("4", "en"), ("We counted down to the new year.", "en"), ("我们倒计时迎新年。", "zh")],
                            [("5", "en"), ("We enjoyed mooncakes and fruit.", "en"), ("我们享用了月饼和水果。", "zh")],
                        ],
                    ),
                    "（曲调：《春节序曲》片段）Cleaned cleaned 扫房子，Pasted pasted 贴福字；"
                    "Dressed dressed 穿红衣，Counted counted 迎新年！",
                    "song",
                    """动词排序：
enjoyed / cleaned / counted / pasted / dressed
正确顺序：___ → ___ → ___ → ___ → ___

口头复述：按顺序说出 5 个活动。""",
                ),
                knowledge_point(
                    3,
                    "情感评价表达",
                    "great fun / the best festival ever",
                    "结尾常用<strong>高度评价</strong>总结感受："
                    "The Spring Festival was great fun! "
                    "It was the best festival ever!",
                    example_table(
                        [("表达", "en"), ("含义", "zh"), ("例句", "en")],
                        [
                            [("great fun", "en"), ("非常有趣", "zh"), ("The festival was great fun!", "en")],
                            [("the best ... ever", "en"), ("有史以来最棒的", "zh"), ("It was the best festival ever!", "en")],
                            [("exciting", "en"), ("令人激动的", "zh"), ("It was exciting!", "en")],
                        ],
                    ),
                    "烟花夜空宫殿：每放一朵烟花说一句评价句；"
                    "最大烟花绽放时喊 the best festival ever！",
                    "palace",
                    """仿写结尾：
1. The Mid-Autumn Festival was ___!
2. It was the best ___ ever!
3. The dragon boat race was ___!

用 great fun / exciting / amazing 填空。""",
                ),
                knowledge_point(
                    4,
                    "仿写 My Festival Story",
                    "Writing frame for festival narrative",
                    "仿写框架：开头评价 + 准备活动 + 庆祝活动 + 结尾感叹。",
                    example_table(
                        [("部分", "zh"), ("句型支架", "en")],
                        [
                            [("开头", "zh"), ("The ___ Festival was great fun!", "en")],
                            [("准备", "zh"), ("My family cleaned ... and pasted ...", "en")],
                            [("庆祝", "zh"), ("We dressed ... and counted ...", "en")],
                            [("结尾", "zh"), ("It was the best festival ever!", "en")],
                        ],
                    ),
                    "作文纸宫殿：四格漫画对应四段写作，"
                    "每格一个句型支架，填词即成文！",
                    "palace",
                    """仿写任务：
The _______ Festival
The _______ Festival was great fun!
My family _______ and _______.
We _______ and _______.
We enjoyed _______.
It was the best festival ever!

（至少 6 句，8 个以上过去式动词）""",
                ),
            ],
            "review": """<ol class="zh">
<li><strong>「动词链复述」：</strong>不看课文，按顺序说出 5 个春节活动。</li>
<li><strong>「情感口号」：</strong>齐喊 the best festival ever!</li>
<li><strong>「仿写朗读」：</strong>朗读自己的 My Festival Story。</li>
</ol>""",
            "summary_rows": [
                ["文章结构", "准备-庆祝-感受", "时间轴", "Before/During/Feeling", "en"],
                ["动词链", "过去式顺序", "春节序曲", "cleaned→pasted→...", "en"],
                ["情感表达", "great fun / best ever", "烟花夜空", "the best festival ever", "en"],
                ["仿写框架", "四段式", "四格漫画", "My Festival Story", "en"],
            ],
            "quotes": """1. "The Spring Festival was great fun!"
2. "We pasted fu on the door."
3. "We dressed in red and counted down to the new year."
4. "We enjoyed mooncakes and fruit."
5. "It was the best festival ever!"
""",
            "homework": [
                "按顺序默写课文动词链 5 句",
                "仿写 My Festival Story（8 句）",
                "用 the best ... ever 写 3 个不同节日结尾",
                "（挑战）制作春节英文绘本（6 页）",
            ],
            "teacher": "春节的故事用英语讲给世界听，是最美的文化分享。"
            "你的 My Festival Story 就是最好的练习！",
        },
    }
    return specs[part_key]


def summary_table(rows: list[list[str]]) -> str:
    trs = []
    for row in rows:
        kp, formula, memory, example, ex_cls = row
        trs.append(
            f'<tr><td class="zh">{kp}</td><td class="en">{formula}</td>'
            f'<td class="zh">{memory}</td><td class="{ex_cls}">{example}</td></tr>'
        )
    return (
        '<table class="rich-table"><thead><tr>'
        '<th class="zh">知识点</th><th class="en">核心公式</th>'
        '<th class="zh">记忆方法</th><th class="en">重点例句</th>'
        f"</tr></thead><tbody>{''.join(trs)}</tbody></table>"
    )


def build_body(unit: dict | None, part_key: str, page_id: str = "") -> str:
    if page_id == "appendix-k-revision":
        u = 0
        spec = revision_content()
        part_label = "Revision 复习"
        focus = "全册语法词汇综合复习"
        theme = "复习"
        title = "Revision"
        title_cn = "复习"
    else:
        u = unit["num"]
        if u in (1, 2):
            content_fn = u1_content if u == 1 else u2_content
            spec = content_fn(part_key)
        else:
            spec = generic_content(unit, part_key)
        part_label = PART_LABELS[part_key]
        if part_key == "reading":
            focus = f"阅读精讲：{unit.get('reading_title', 'Reading')} 全文理解与写作"
        else:
            focus = PART_FOCUS[part_key]
        theme = unit["theme"]
        title = unit["title"]
        title_cn = unit["title_cn"]

    goals_li = "".join(f"<li>{g}</li>" for g in spec["goals"])
    points_html = "\n".join(spec["points"])
    homework_li = "".join(f"<li>{h}</li>" for h in spec["homework"])

    catalog_html = catalog_focus_html(u, part_key) if u else ""
    culture_html = culture_section(u, part_key)
    fill_qa_html = fillblank_qa_section(u, part_key) if u else ""
    writing_html = writing_section(u, part_key) if u else ""
    vocab_html = appendix_vocab_table(u, part_key) if u else "<p class=\"zh\">见各单元附录2词汇表。</p>"
    phrase_html = appendix_phrase_table(u, part_key) if u else "<p class=\"zh\">见附录四常用表达。</p>"

    unit_heading = f"Unit {u} {title}（{title_cn}）" if u else "Revision 复习单元"
    return f"""<h3>{unit_heading} — {part_label}</h3>
<p class="teaching-focus zh"><strong>单元主题：</strong>{theme}</p>
<p class="teaching-focus zh"><strong>本讲目标：</strong>{focus}</p>
{catalog_html}
<h4 class="zh">第一步：课文知识点总览地图</h4>
<blockquote class="zh"><p><strong>一句话概括：</strong>{spec['summary']}</p></blockquote>
<pre class="en"><code class="en">{spec['tree']}</code></pre>
<h4 class="zh">第二步：学习目标</h4>
<ul class="zh">{goals_li}</ul>
<h4 class="zh">第三步：核心词汇（附录2 · {part_label}）</h4>
{vocab_html}
<h4 class="zh">第四步：常用短语（附录四 · {part_label}）</h4>
{phrase_html}
{culture_html}
<h4 class="zh">第六步：全新知识点逐一精讲</h4>
{points_html}
{fill_qa_html}
{writing_html}
<h4 class="zh">第七步：综合复习</h4>
{spec['review']}
<h4 class="zh">第八步：知识点总结表格</h4>
{summary_table(spec['summary_rows'])}
<h4 class="zh">第九步：课堂金句——孩子们要会说！</h4>
<p class="en"><pre class="en"><code class="en">{spec['quotes']}</code></pre></p>
<h4 class="zh">第十步：课后作业清单</h4>
<ul class="zh">{homework_li}</ul>
<p class="tip-box zh">🎓 <strong>老师寄语：</strong>{spec['teacher']}</p>"""


def generic_content(unit: dict, part_key: str) -> dict:
    u = unit["num"]
    gd = unit.get("grammar_discover", {})
    grammar_title = gd.get("title", "本单元语法重点")
    lmap = unit.get("learning_map", {})
    tree_lines = [f"Unit {u} {unit.get('title_cn', '')}"]
    for k, vals in list(lmap.items())[:5]:
        tree_lines.append(f"├─ {k}: {', '.join(vals[:3])}")
    sk = SENTENCE_KEY.get(part_key, "part_a_sentences")
    sents = unit.get(sk, []) or unit.get("part_a_sentences", [])
    goals = list(unit.get("goals", []))[:4]
    if part_key == "part-c":
        goals.append("归纳语法规则，完成课本练习")
    elif part_key == "reading":
        goals = [
            f"读懂 {unit.get('reading_title', 'Reading')} 全文",
            "提取关键词复述大意",
            "运用本单元语法写简短段落",
        ]
    ex_en = [s[0] for s in sents[:4] if s]
    quotes = "\n".join(f'{i + 1}. "{s}"' for i, s in enumerate(ex_en[:5]))
    hints = gd.get("hints", [])
    obs_rows = []
    for en, zh in gd.get("observe", [])[:5]:
        obs_rows.append([[en, "en"], [zh, "zh"]])
    observe_html = (
        example_table([("英文例句", "en"), ("中文", "zh")], obs_rows)
        if obs_rows
        else "<p class=\"zh\">见本单元语法重点。</p>"
    )
    sent_rows = [[[en, "en"], [zh, "zh"]] for en, zh in sents[:5]]
    vocab_rows = [[[k, "zh"], [", ".join(v[:4]), "en"]] for k, v in list(lmap.items())[:4]]
    points = [
        knowledge_point(
            1, grammar_title, grammar_title,
            f"本课核心语法：<strong>{grammar_title}</strong>。请对照课文例句理解用法。",
            observe_html, "；".join(hints[:2]) if hints else "多读例句，模仿造句。", "song",
            "\n".join(unit.get("mini_challenge", [])[:5]),
        ),
        knowledge_point(
            2, "核心词汇运用", f"Unit {u} Vocabulary",
            "将附录2词汇放入句子中记忆，比孤立背单词更有效。",
            example_table([("词汇主题", "zh"), ("代表词", "en")], vocab_rows),
            "按主题分块记忆。", "palace", "用本 Part 5 个新词各造 1 句。",
        ),
        knowledge_point(
            3, "交际句型实战", "Key sentences",
            "以下句型来自课文与附录四，请朗读并替换练习。",
            example_table([("英文", "en"), ("中文", "zh")], sent_rows),
            "师生问答：一人问一人答。", "song", "仿照课文编一段 4 句对话。",
        ),
    ]
    if part_key in ("part-b", "reading"):
        points.append(knowledge_point(
            4, "读写任务精讲", "Reading & writing",
            "先列提纲，再写完整句：开头—活动—感受。",
            example_table(
                [("步骤", "zh"), ("要求", "zh")],
                [[["开头", "zh"], ["交代时间/主题", "zh"]], [["中间", "zh"], ["2–3 个活动", "zh"]], [["结尾", "zh"], ["感受或建议", "zh"]]],
            ),
            "写作像搭积木。", "palace",
            f"仿写一段关于 {unit.get('title_cn', '')} 的短文（6–8 句）。",
        ))
    challenges = unit.get("mini_challenge", [])
    return {
        "summary": f"本课围绕「{unit.get('title_cn', '')}」主题，掌握{grammar_title}、核心词汇与交际句型。",
        "tree": "【知识点大树🌳】\n" + "\n".join(tree_lines),
        "goals": goals,
        "points": points,
        "review": "<ol class=\"zh\">" + "".join(f"<li>{c}</li>" for c in challenges[:4]) + "</ol>",
        "summary_rows": [
            [grammar_title, hints[0] if hints else "见语法表", "口诀", ex_en[0] if ex_en else "—", "en"],
            ["词汇", "附录2", "主题块", ", ".join(list(lmap.values())[0][:3]) if lmap else "—", "en"],
            ["句型", "附录四", "对话", ex_en[1] if len(ex_en) > 1 else "—", "en"],
        ],
        "quotes": quotes or "1. Review key sentences.",
        "homework": challenges[:4] or ["背诵核心词汇", "朗读课文 3 遍", "完成课本练习"],
        "teacher": unit.get("learning_tip", "多听多说，把语法用在真实对话里。"),
    }


def revision_content() -> dict:
    blocks = [
        ("Unit 1–2", "一般过去时", "How was...? / Did you...?"),
        ("Unit 3", "should / be going to", "How do you feel? / You should..."),
        ("Unit 4", "be going to", "I am going to buy... / I need to save."),
        ("Unit 5", "can / There be", "We can use telescopes."),
        ("Unit 6", "一般现在时 + should", "Where does... come from?"),
    ]
    points = [
        knowledge_point(
            i + 1, title, title, f"复习：<strong>{focus}</strong>",
            example_table([("单元", "zh"), ("要点", "en")], [[[title, "zh"], [focus, "en"]]]),
            "整理语法表格。", "palace", f"写出 {title} 的两个例句。",
        )
        for i, (title, _g, focus) in enumerate(blocks[:4])
    ]
    return {
        "summary": "全册六大单元语法、词汇与句型综合复习，查漏补缺。",
        "tree": "【复习地图🌳】\nU1–2 过去时 → U3 健康 → U4 理财 → U5 太空 → U6 能源",
        "goals": ["回顾各单元核心语法", "巩固附录2词汇与附录四表达", "复习不规则动词", "完成综合自测"],
        "points": points,
        "review": "<ol class=\"zh\"><li>按单元默写 5 个核心词</li><li>各语法写 1 个例句</li><li>错题本专项复习</li></ol>",
        "summary_rows": [[b[0], b[1], "复习", b[2], "en"] for b in blocks],
        "quotes": '1. "How was your weekend?"\n2. "You should see a doctor."\n3. "I am going to save up."\n4. "We should save energy."',
        "homework": ["整理全册语法思维导图", "附录2听写 20 词", "错题本重做一遍"],
        "teacher": "复习让知识更牢固、运用更自如。",
    }


def culture_section(unit_num: int, part_key: str) -> str:
    if unit_num == 0:
        text = "本课为全册复习，串联各单元文化主题：旅行地标、节日团聚、健康生活、理财、太空探索与绿色能源。"
    else:
        text = CULTURE.get((unit_num, part_key), "本课人文与历史背景见课文与图片。")
    return f"""<h4 class="zh">第五步：文化知识拓展</h4>
<p class="zh">{text}</p>"""


APPEND_BLOCK_RE = re.compile(
    r'<h4 class="zh">(?:课文填空与问答精讲|课文填空与问答 ·|重要写作练习讲解)[\s\S]*?(?=<h[1-4]|<blockquote|</div>\s*$|$)',
    re.IGNORECASE,
)


def strip_standard_append_blocks(html: str) -> str:
    """Remove previously appended fill/writing blocks (safe re-run)."""
    prev = None
    out = html
    while prev != out:
        prev = out
        out = APPEND_BLOCK_RE.sub("", out)
    return out.rstrip()


def patch_append_sections(page_id: str) -> str:
    """Append fill Q&A + writing to preserved pages (e.g. u3-k-part-b)."""
    path = KNOWLEDGE_DIR / f"{page_id}.html"
    if not path.is_file():
        raise FileNotFoundError(f"Missing preserved lecture: {path}")
    unit_num, part_key = page_id_to_keys(page_id)
    if unit_num is None:
        raise ValueError(f"Cannot patch revision page: {page_id}")
    base = strip_standard_append_blocks(path.read_text(encoding="utf-8"))
    fill_qa = fillblank_qa_section(unit_num, part_key)
    writing = writing_section(unit_num, part_key)
    parts = [p for p in (fill_qa, writing) if p]
    if not parts:
        return base
    return base + "\n\n" + "\n".join(parts)


def page_id_to_keys(page_id: str) -> tuple[int | None, str]:
    if page_id == "appendix-k-revision":
        return None, "revision"
    m = re.match(r"u(\d+)-k-(part-[abc]|reading)", page_id)
    if not m:
        raise ValueError(f"Unknown page id: {page_id}")
    return int(m.group(1)), m.group(2)


def main() -> None:
    units_by_num = {u["num"]: u for u in UNITS}
    generated: dict[str, str] = {}

    for page_id in PAGE_IDS:
        unit_num, part_key = page_id_to_keys(page_id)
        if page_id == "appendix-k-revision":
            html = strip_excerpt(build_body(None, "revision", page_id))
        else:
            unit = units_by_num[unit_num]
            html = strip_excerpt(build_body(unit, part_key, page_id))
        generated[page_id] = html

    for page_id in PATCH_APPEND_PAGE_IDS:
        generated[page_id] = patch_append_sections(page_id)
        print(f"  patched (append only): {page_id}")

    bank = json.loads(KNOWLEDGE_BANK.read_text(encoding="utf-8"))
    updated = 0
    for unit_block in bank.get("units", []):
        for page in unit_block.get("pages", []):
            pid = page.get("id", "")
            if pid in generated:
                page["bodyHtml"] = generated[pid]
                updated += 1
    # appendix / revision block
    for page in bank.get("appendix", {}).get("pages", []):
        pid = page.get("id", "")
        if pid in generated:
            page["bodyHtml"] = generated[pid]
            updated += 1

    KNOWLEDGE_BANK.write_text(
        json.dumps(bank, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    for page_id, html in generated.items():
        out = KNOWLEDGE_DIR / f"{page_id}.html"
        out.write_text(html, encoding="utf-8")

    print("=" * 60)
    print("Knowledge Lecture Generator (U1–U6 + Revision)")
    print("=" * 60)
    print(f"Updated knowledge-bank.json: {updated} pages")
    print(f"Wrote HTML files to: {KNOWLEDGE_DIR}")
    print()
    all_ids = list(PAGE_IDS) + list(PATCH_APPEND_PAGE_IDS)
    for page_id in all_ids:
        html = generated[page_id]
        lines = html.count("\n") + 1
        chars = len(html)
        print(f"  {page_id}: {lines} lines, {chars:,} chars")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
