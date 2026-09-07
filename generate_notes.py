# -*- coding: utf-8 -*-
"""Generate 六年级上册英语学霸笔记 Word document using stdlib only."""
import zipfile
import os
from xml.sax.saxutils import escape

OUTPUT = r"C:\Users\guoqren\.cursor\englishi learn\六年级上册英语学霸笔记.docx"

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="微软雅黑" w:hAnsi="微软雅黑" w:eastAsia="微软雅黑"/><w:sz w:val="22"/></w:rPr></w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:pPr><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="44"/><w:color w:val="1F4E79"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:color w:val="2E75B6"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="240" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:color w:val="C00000"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="160" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="548235"/></w:rPr>
  </w:style>
</w:styles>"""


def p(text, style=None, bold=False, color=None, indent=False):
    text = escape(text)
    ppr = ""
    if style:
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/>'
        if indent:
            ppr += '<w:ind w:left="360"/>'
        ppr += '</w:pPr>'
    elif indent:
        ppr = '<w:pPr><w:ind w:left="360"/></w:pPr>'
    rpr = ""
    if bold or color:
        rpr = "<w:rPr>"
        if bold:
            rpr += "<w:b/>"
        if color:
            rpr += f'<w:color w:val="{color}"/>'
        rpr += "</w:rPr>"
    return f"<w:p>{ppr}<w:r>{rpr}<w:t xml:space=\"preserve\">{text}</w:t></w:r></w:p>"


def empty():
    return "<w:p/>"


def build_document():
    parts = []

    parts.append(p("人教版 PEP（2024）", style="Title"))
    parts.append(p("六年级上册 · 英语学霸笔记", style="Title"))
    parts.append(empty())
    parts.append(p("适用教材：人教版 PEP 小学英语六年级上册（2024 新教材）", bold=True))
    parts.append(p("内容涵盖：各单元重点词汇 · 核心语法 · 常用句型 · 优秀作文范例"))
    parts.append(p("用途：课堂复习 · 考前冲刺 · 知识点巩固加强"))
    parts.append(empty())

    # ========== UNIT 1 ==========
    parts.append(p("Unit 1  Amazing places（奇妙之地）", style="Heading1"))
    parts.append(p("一、单元主题与学习目标", style="Heading2"))
    parts.append(p("主题：旅行与著名地标（中外名胜、红色文化景点）", indent=True))
    parts.append(p("目标：用一般过去时描述过去的旅行经历，介绍中外著名地标", indent=True))
    parts.append(empty())

    parts.append(p("二、重点词汇", style="Heading2"))
    vocab1 = [
        "climb 攀登；爬（过去式 climbed）    go 去（过去式 went）    see 看见（过去式 saw）",
        "eat 吃（过去式 ate）    take 拍摄；进行（过去式 took）    send 邮寄；发送",
        "kilometre 千米    thousand 一千    village 村庄    view 景色；风景",
        "bamboo 竹子    pumpkin 南瓜    restaurant 餐馆    airport 机场    dry 干的    inspiring 鼓舞人心的",
        "Great Wall 长城    Eiffel Tower 埃菲尔铁塔    Terracotta Warriors 兵马俑",
        "Hong Kong-Zhuhai-Macao Bridge 港珠澳大桥    Gingerbread House 姜饼屋",
    ]
    for v in vocab1:
        parts.append(p(v, indent=True))
    parts.append(empty())

    parts.append(p("三、常考短语", style="Heading2"))
    phrases1 = [
        "climb the Great Wall 爬长城    last weekend 上周末    over the summer holidays 暑假期间",
        "visit famous landmarks 参观著名地标    take many photos 拍很多照片",
        "delicious food 美味的食物    a must-see attraction 必游景点",
        "ride bikes on the old city wall 在古城墙上骑自行车    walk around the old city 逛古城",
    ]
    for ph in phrases1:
        parts.append(p(ph, indent=True))
    parts.append(empty())

    parts.append(p("四、核心语法：一般过去时", style="Heading2"))
    grammar1 = [
        "【用法】表示过去某个时间发生的动作或存在的状态（常与 last weekend / yesterday / over the summer holidays 连用）",
        "【肯定句】主语 + 动词过去式 + 其他.   例：I visited the Great Wall last Saturday.",
        "【否定句】主语 + didn't + 动词原形 + 其他.   例：I didn't go to Beijing.",
        "【一般疑问句】Did + 主语 + 动词原形 + 其他?   答：Yes, I did. / No, I didn't.",
        "【特殊疑问句】特殊疑问词 + did + 主语 + 动词原形?   例：What did you do?",
        "【be动词过去式】am/is → was    are → were    例：It was great!",
        "【不规则动词】go→went  see→saw  eat→ate  take→took  have→had  do→did",
        "【规则动词】+ed：climb→climbed  visit→visited  walk→walked",
    ]
    for g in grammar1:
        parts.append(p(g, indent=True))
    parts.append(empty())

    parts.append(p("五、重点句型", style="Heading2"))
    sent1 = [
        "— How was your weekend / holiday?  你周末/假期过得怎么样？",
        "— It was great / fun / amazing!  非常棒/很有趣/太棒了！",
        "— What did you do (last Saturday)?  你（上周六）做什么了？",
        "— I / We + 动词过去式 + 其他.  例：I visited the Gingerbread House.",
        "— Where did you go (over the summer holidays)?  你暑假去哪儿了？",
        "— I / We went to + 地点 (+ with sb.).  例：I went to Xi'an with my family.",
        "— Did you + 动词原形...?  — Yes, I / we did. / No, I / we didn't.",
    ]
    for s in sent1:
        parts.append(p(s, indent=True))
    parts.append(empty())

    parts.append(p("六、补充语法：by + 交通工具", style="Heading2"))
    by_transport = [
        "by + 交通工具（名词原形，不加 a/an/the）",
        "✅ by cable car / by train / by plane / by bus    ❌ by a train / by the bus",
        "例：I went to the top by cable car.  We travelled to Xi'an by high-speed train.",
    ]
    for b in by_transport:
        parts.append(p(b, indent=True))
    parts.append(empty())

    parts.append(p("七、优秀作文范例", style="Heading2"))
    parts.append(p("【范文一】旅行游记（满分模板）", style="Heading3"))
    essay1a = """My trip to Zhangjiajie was wonderful! I walked along the glass bridge and saw amazing mountain views. The mountains looked like they were floating in the clouds. I tried delicious local fish and rice. Zhangjiajie is about 4 hours from Changsha by bus. You should visit there in autumn — it is really beautiful! I learnt a lot about nature and I want to go there again!"""
    for line in essay1a.split("\n"):
        parts.append(p(line, indent=True))
    parts.append(empty())
    parts.append(p("【范文二】红色文化之旅", style="Heading3"))
    essay1b = """My trip to the Jinggang Mountains was amazing! I visited the Jinggangshan Revolution Museum with my class. I learnt a lot about Chinese history. The views from the mountains were inspiring. It was a must-see attraction. I want to go there again someday!"""
    for line in essay1b.split("\n"):
        parts.append(p(line, indent=True))
    parts.append(empty())
    parts.append(p("【范文三】西安之旅（仿课文）", style="Heading3"))
    essay1c = """Last summer, I went to Xi'an with my family. We ate famous Xi'an noodles and visited the Terracotta Warriors. There were over seven thousand clay warriors. We also walked around the old city. It was amazing! I think the trip was special because of the Terracotta Warriors."""
    for line in essay1c.split("\n"):
        parts.append(p(line, indent=True))
    parts.append(empty())

    # ========== UNIT 2 ==========
    parts.append(p("Unit 2  Getting together（相聚在一起）", style="Heading1"))
    parts.append(p("一、单元主题与学习目标", style="Heading2"))
    parts.append(p("主题：中外传统节日与家庭聚会（春节、中秋节等）", indent=True))
    parts.append(p("目标：用一般过去时描述节日活动，了解中外节日文化", indent=True))
    parts.append(empty())

    parts.append(p("二、重点词汇", style="Heading2"))
    vocab2 = [
        "celebrate 庆祝（过去式 celebrated）    gather 聚集（gathered）    share 分享（shared）",
        "festival 节日    relative 亲戚    fireworks 烟花    mooncake 月饼    zongzi 粽子",
        "dumpling 饺子    delicious 美味的    wonderful 精彩的    together 一起",
        "Spring Festival 春节    Mid-Autumn Festival 中秋节    Dragon Boat Festival 端午节",
    ]
    for v in vocab2:
        parts.append(p(v, indent=True))
    parts.append(empty())

    parts.append(p("三、核心语法：一般过去时（疑问与否定）", style="Heading2"))
    grammar2 = [
        "【一般疑问句】Did + 主语 + 动词原形?  答：Yes, 主语 + did. / No, 主语 + didn't.",
        "【否定句】主语 + didn't + 动词原形.  例：I didn't set off fireworks.",
        "【特殊疑问句】What did you do / eat?  答：I + 动词过去式 + 其他.",
        "【规则动词过去式】+ed：watch→watched  dance→danced  share→shared",
        "  以 e 结尾 +d：celebrate→celebrated",
        "  辅音+y 变 i+ed：study→studied",
        "  重读闭音节双写+ed：stop→stopped",
        "【不规则动词】run→ran  read→read(/red/)  eat→ate  go→went  have→had",
        "【顺序词】First... Then... Next... Finally... 用于叙述活动顺序",
        "⚠ 易错点：出现 did / didn't 时，后面动词必须用原形！",
    ]
    for g in grammar2:
        parts.append(p(g, indent=True))
    parts.append(empty())

    parts.append(p("四、重点句型", style="Heading2"))
    sent2 = [
        "— Did you celebrate the Spring Festival last year?  你去年庆祝春节了吗？",
        "— Yes, I did. / No, I didn't.",
        "— What did you do last Spring Festival?  你去年春节做了什么？",
        "— I gathered with my relatives and shared mooncakes.",
        "— How was your festival holiday?  — It was wonderful!",
        "叙述句：First, we had a big dinner. Then, we watched fireworks. Finally, we shared gifts.",
    ]
    for s in sent2:
        parts.append(p(s, indent=True))
    parts.append(empty())

    parts.append(p("五、写作技巧：叙事文「三段式」", style="Heading2"))
    writing2 = [
        "第一段（开头）：点明节日 + 总体感受  The Spring Festival was great fun!",
        "第二段（主体）：First... Then... Later... Finally... 按顺序写活动",
        "第三段（结尾）：表达感受 + 展望未来  It was the best day ever!",
        "加分技巧：加入感官描写（saw/heard/smelled/tasted/felt）让文章有画面感",
    ]
    for w in writing2:
        parts.append(p(w, indent=True))
    parts.append(empty())

    parts.append(p("六、优秀作文范例", style="Heading2"))
    parts.append(p("【范文一】春节", style="Heading3"))
    essay2a = """The Spring Festival was great fun!
First, our family cleaned the house and put up red decorations. Everything looked bright and beautiful.
Then, we cooked a big New Year's dinner together. The food smelled amazing and tasted delicious!
Later, we watched the fireworks outside. The sky was full of colours — red, gold, and green.
Finally, grandma gave me a red envelope with lucky money inside. I felt so happy and loved!
It was the best Spring Festival ever! I hope every year can be this wonderful."""
    for line in essay2a.split("\n"):
        parts.append(p(line, indent=True))
    parts.append(empty())
    parts.append(p("【范文二】运动会", style="Heading3"))
    essay2b = """The sports meet was great fun!
First, all the students stood in lines and walked into the stadium. We wore our sports uniforms and felt very proud.
Then, the race began. I ran as fast as I could. Later, my classmates cheered for me loudly. I could hear my heart beating fast!
Finally, I won second place and got a medal. It was the most exciting day of my life!
I will work harder and try to win first place next time!"""
    for line in essay2b.split("\n"):
        parts.append(p(line, indent=True))
    parts.append(empty())

    # ========== UNIT 3 ==========
    parts.append(p("Unit 3  Healthy life（健康生活）", style="Heading1"))
    parts.append(p("一、单元主题与学习目标", style="Heading2"))
    parts.append(p("主题：身体健康、疾病表达与健康生活习惯", indent=True))
    parts.append(p("目标：描述身体状况，给出健康建议，制定健康计划", indent=True))
    parts.append(empty())

    parts.append(p("二、重点词汇", style="Heading2"))
    vocab3 = [
        "ill 生病的    headache 头痛    fever 发烧    cough 咳嗽    medicine 药",
        "healthy 健康的    exercise 锻炼    rest 休息    vegetable 蔬菜    early 早地",
        "feel 感觉    hurt 疼痛    hospital 医院    well 健康的；好地",
        "should 应该    shouldn't = should not 不应该",
    ]
    for v in vocab3:
        parts.append(p(v, indent=True))
    parts.append(empty())

    parts.append(p("三、核心语法", style="Heading2"))
    grammar3 = [
        "【一般现在时·描述身体状况】I feel ill. / My head hurts. / I have a fever.",
        "【should / shouldn't 提建议】should + 动词原形（应该做某事）",
        "  肯定：You should exercise. / You should have a rest. / You should go to bed early.",
        "  否定：You shouldn't eat too much junk food.",
        "【be going to 表打算】主语 + am/is/are + going to + 动词原形",
        "  例：I am going to see a doctor. / We are going to play sports.",
        "【询问身体状况】What's wrong? / How do you feel? / Do you feel ill?",
        "⚠ 易错点：should 和 be going to 后面都接动词原形！",
    ]
    for g in grammar3:
        parts.append(p(g, indent=True))
    parts.append(empty())

    parts.append(p("四、重点句型", style="Heading2"))
    sent3 = [
        "— What's wrong? / What's the matter?  怎么了？",
        "— I feel ill. / My head hurts. / I have a cough.",
        "— You should drink more water and have a rest.  你应该多喝水并休息。",
        "— You shouldn't watch TV for too long.  你不应该看太久电视。",
        "— What are you going to do?  — I'm going to see a doctor.",
        "— Do you feel ill?  — Yes, I do. / No, I don't.",
    ]
    for s in sent3:
        parts.append(p(s, indent=True))
    parts.append(empty())

    parts.append(p("五、优秀作文范例", style="Heading2"))
    essay3 = """How to Keep Healthy

Health is very important. Here are some tips for a healthy life.

First, you should exercise every day. Running and swimming are good for you. Second, you should eat more vegetables and fruit. You shouldn't eat too much junk food. Third, you should go to bed early and get enough rest.

If you feel ill, you should see a doctor. Don't wait too long! I'm going to play sports and eat healthy food every day. Let's keep healthy together!"""
    for line in essay3.split("\n"):
        parts.append(p(line, indent=True))
    parts.append(empty())

    # ========== UNIT 4 ==========
    parts.append(p("Unit 4  Managing money well（合理管理金钱）", style="Heading1"))
    parts.append(p("一、单元主题与学习目标", style="Heading2"))
    parts.append(p("主题：零花钱管理、理性消费与储蓄", indent=True))
    parts.append(p("目标：谈论用钱计划，学会量入为出、合理储蓄", indent=True))
    parts.append(empty())

    parts.append(p("二、重点词汇", style="Heading2"))
    vocab4 = [
        "money 钱    pocket money 零花钱    piggy bank 存钱罐    save 储蓄    spend 花费",
        "buy 买    need 需要    want 想要    plan 计划    pay 支付    price 价格",
        "goods 商品    services 服务    cash 现金    dictionary 字典    on sale 打折",
        "save up 攒钱    lucky money 压岁钱",
    ]
    for v in vocab4:
        parts.append(p(v, indent=True))
    parts.append(empty())

    parts.append(p("三、核心语法", style="Heading2"))
    grammar4 = [
        "【be going to 表将来计划】主语 + am/is/are + going to + 动词原形",
        "  疑问：How are you going to spend / save it?  你打算怎么花/存？",
        "  答：I am going to buy a schoolbag. / I am going to save it in my piggy bank.",
        "【want / need + to do】I want to buy some books. / I need to save more.",
        "【use...to... 表用途】We use money to buy goods. / We use money to pay for services.",
        "【should 提建议】Should I buy a new dictionary? / What should I do?",
        "【How much 询问金额】How much is it? / How much money do you have?",
        "【顺序词叙述计划】First... Then... Finally...",
    ]
    for g in grammar4:
        parts.append(p(g, indent=True))
    parts.append(empty())

    parts.append(p("四、重点句型", style="Heading2"))
    sent4 = [
        "— How are you going to spend your pocket money / lucky money?",
        "— I am going to save up for a new bike.",
        "— I am going to buy some books first. They're on sale.",
        "— I also want to buy a dictionary. / I need to save more.",
        "— Should I buy some ice cream?  — Sure, but don't eat too much.",
        "— What should I do with 50 yuan?  — You should save half and spend half wisely.",
    ]
    for s in sent4:
        parts.append(p(s, indent=True))
    parts.append(empty())

    parts.append(p("五、优秀作文范例", style="Heading2"))
    essay4 = """How I Manage My Pocket Money

I get some pocket money every month. I learn to manage it well.

First, I am going to save half of it in my piggy bank. I want to save up for a new basketball. Then, I am going to buy some books. They are on sale, so I can save money. I also need to buy a dictionary for school.

I use money to buy goods and pay for services. I shouldn't waste money on things I don't need. Managing money well is an important life skill!"""
    for line in essay4.split("\n"):
        parts.append(p(line, indent=True))
    parts.append(empty())

    # ========== UNIT 5 ==========
    parts.append(p("Unit 5  Exploring space（探索太空）", style="Heading1"))
    parts.append(p("一、单元主题与学习目标", style="Heading2"))
    parts.append(p("主题：太空探索、宇宙天体与中国航天成就", indent=True))
    parts.append(p("目标：描述太空景象，谈论太空探索的能力与可能性", indent=True))
    parts.append(empty())

    parts.append(p("二、重点词汇", style="Heading2"))
    vocab5 = [
        "space 太空    planet 行星    star 星星    moon 月亮    Mars 火星    Earth 地球",
        "rocket 火箭    spaceship 宇宙飞船    astronaut 宇航员    telescope 望远镜",
        "solar system 太阳系    look into 观察    live 居住",
    ]
    for v in vocab5:
        parts.append(p(v, indent=True))
    parts.append(empty())

    parts.append(p("三、核心语法", style="Heading2"))
    grammar5 = [
        "【There be 句型·描述存在】",
        "  肯定：There is a big rocket. / There are many stars.",
        "  否定：There isn't a planet. / There aren't any spaceships.",
        "  一般疑问：Is there a museum? / Are there any planets?  答：Yes, there is/are. / No, there isn't/aren't.",
        "  ⚠ 就近原则：There is a star and two planets. / There are two planets and a star.",
        "【can / can't 表能力或可能性】",
        "  肯定：We can see the moon at night. / Astronauts can live in the spaceship.",
        "  否定：We can't live on Mars now.  ⚠ can 后接动词原形",
        "【What can we see...?】询问能看到什么",
        "【Can we...?】询问是否可能  答：Yes, we can. / No, we can't.",
    ]
    for g in grammar5:
        parts.append(p(g, indent=True))
    parts.append(empty())

    parts.append(p("四、重点句型", style="Heading2"))
    sent5 = [
        "— What can we see in space?  — We can see stars, planets and the moon.",
        "— Can we live on Mars?  — No, we can't. / Not yet.",
        "— Are there any spaceships in the museum?  — Yes, there are.",
        "— There is a big rocket in the science museum.",
        "— Astronauts use telescopes to look into space.",
    ]
    for s in sent5:
        parts.append(p(s, indent=True))
    parts.append(empty())

    parts.append(p("五、优秀作文范例", style="Heading2"))
    essay5 = """Exploring Space

Space is amazing! There are many stars and planets in the solar system.

We can see the moon at night. Astronauts can travel to space in rockets and spaceships. They use telescopes to look into space. There is one beautiful Earth, and there are seven other planets.

China has great achievements in space. Shenzhou and Tiangong make us proud! I want to be an astronaut someday. Space exploration never stops!"""
    for line in essay5.split("\n"):
        parts.append(p(line, indent=True))
    parts.append(empty())

    # ========== UNIT 6 ==========
    parts.append(p("Unit 6  Energy, nature and us（能源、自然与我们）", style="Heading1"))
    parts.append(p("一、单元主题与学习目标", style="Heading2"))
    parts.append(p("主题：能源来源、环保与 3R 原则（Reduce, Reuse, Recycle）", indent=True))
    parts.append(p("目标：了解能源知识，用 should 提出环保建议", indent=True))
    parts.append(empty())

    parts.append(p("二、重点词汇", style="Heading2"))
    vocab6 = [
        "energy 能源    electricity 电    solar power 太阳能    wind power 风能    water power 水能",
        "green energy 绿色能源    resource 资源    save energy 节约能源",
        "reduce 减少    reuse 重复使用    recycle 回收利用    unplug 拔掉插头",
        "air conditioner 空调    shower 淋浴    LED lighting LED 照明",
    ]
    for v in vocab6:
        parts.append(p(v, indent=True))
    parts.append(empty())

    parts.append(p("三、核心语法", style="Heading2"))
    grammar6 = [
        "【询问来源】Where does + 主语 + come from?  答：It comes from...",
        "  例：Where does water come from? — It comes from rivers and lakes.",
        "  例：Where does electricity come from? — It comes from power stations.",
        "  ⚠ 第三人称单数：Where does water come from? (does + 原形 come)",
        "【询问方式】How do we make power from water?  答：Water turns the wheel.",
        "【should 提建议】We should save energy. / We should unplug our computers.",
        "【can 表可以】We can take quick showers. / We can use LED lighting.",
        "【不定式表目的】To follow the 3R rules, we should reduce, reuse and recycle.",
        "【一般现在时·第三人称单数】Water turns the wheel. / The sun gives us light and heat.",
    ]
    for g in grammar6:
        parts.append(p(g, indent=True))
    parts.append(empty())

    parts.append(p("四、重点句型", style="Heading2"))
    sent6 = [
        "— Where does water / electricity come from?",
        "— It comes from rivers, lakes and rain. / It comes from power stations.",
        "— How do we make power from water / wind / the sun?",
        "— Water turns the wheel. / Wind turns the blades. / Solar panels collect sunlight.",
        "— We should save energy and use green energy.",
        "— We should always unplug our computers and TVs when we don't use them.",
        "— To protect the Earth, we should reduce, reuse and recycle.",
    ]
    for s in sent6:
        parts.append(p(s, indent=True))
    parts.append(empty())

    parts.append(p("五、优秀作文范例", style="Heading2"))
    essay6 = """Save Energy, Save the Earth

Energy is important for our life. We should use it wisely.

Water, wind and the sun can make electricity. They are green energy. We should save energy every day. We can take quick showers and turn off lights when we leave. We should always unplug our computers and TVs.

To follow the 3R rules, we should reduce, reuse and recycle. Let's protect nature and make our Earth more beautiful!"""
    for line in essay6.split("\n"):
        parts.append(p(line, indent=True))
    parts.append(empty())

    # ========== 总复习 ==========
    parts.append(p("附：全册语法总览 & 复习锦囊", style="Heading1"))
    parts.append(p("一、全册核心语法一览", style="Heading2"))
    review = [
        "Unit 1  一般过去时（肯定/否定/疑问）— 描述旅行经历",
        "Unit 2  一般过去时（规则/不规则动词）— 描述节日活动",
        "Unit 3  should/shouldn't + 动词原形；be going to — 健康建议与计划",
        "Unit 4  be going to；want/need to do — 用钱计划",
        "Unit 5  There be 句型；can/can't — 太空描述与能力",
        "Unit 6  Where does...come from?；should — 能源与环保",
    ]
    for r in review:
        parts.append(p(r, indent=True))
    parts.append(empty())

    parts.append(p("二、高频易错点提醒", style="Heading2"))
    tips = [
        "1. 一般过去时：出现 did/didn't，后面动词用原形！",
        "2. be going to / should / can 后面都接动词原形！",
        "3. There be 遵循就近原则：There is a book and two pens.",
        "4. 第三人称单数：Where does water come from? (不是 Where does water comes)",
        "5. read 的过去式拼写不变，读音变为 /red/。",
        "6. How was...? 用 was/were 回答，不是 is/am/are。",
    ]
    for t in tips:
        parts.append(p(t, indent=True))
    parts.append(empty())

    parts.append(p("三、写作万能连接词", style="Heading2"))
    connectors = [
        "开头：Hello! / Last weekend, ... / I want to talk about...",
        "顺序：First, ... Then, ... Next, ... After that, ... Finally, ...",
        "补充：Also, ... / Besides, ... / What's more, ...",
        "结尾：I had a wonderful time. / Let's ... together! / I hope ...",
    ]
    for c in connectors:
        parts.append(p(c, indent=True))
    parts.append(empty())
    parts.append(p("—— 祝学习进步，英语越来越棒！——", style="Title"))

    body = "\n".join(parts)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>"""


def main():
    doc_xml = build_document()
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", RELS)
        zf.writestr("word/_rels/document.xml.rels", DOC_RELS)
        zf.writestr("word/styles.xml", STYLES)
        zf.writestr("word/document.xml", doc_xml.encode("utf-8"))
    print(f"Generated: {OUTPUT}")
    print(f"Size: {os.path.getsize(OUTPUT)} bytes")


if __name__ == "__main__":
    main()
