const unitMeta = {
  1: "Unit 1 Amazing places",
  2: "Unit 2 Getting together",
  3: "Unit 3 Healthy life",
  4: "Unit 4 Managing money well",
  5: "Unit 5 Exploring space",
  6: "Unit 6 Energy, nature and us",
};

const unitLocalImage = {
  1: "./assets/images/unit1-travel.svg",
  2: "./assets/images/unit2-festival.svg",
  3: "./assets/images/unit3-health.svg",
  4: "./assets/images/unit4-money.svg",
  5: "./assets/images/unit5-space.svg",
  6: "./assets/images/unit6-energy.svg",
};

const POINT_REWARD = 50;
const POINT_PENALTY = 20;

// Data source: appendix catalog in textbook_catalog.py (PEP Grade 6 Book 1, 2024 edition).
const appendixUnits = [
  {
    num: 1,
    partAVocab: [["was", "/wɒz/", "v.", "是（am/is 的过去式）"], ["climb", "/klaɪm/", "v.", "攀登；爬"], ["go", "/ɡəʊ/", "v.", "去"], ["see", "/siː/", "v.", "看见"], ["eat", "/iːt/", "v.", "吃"], ["take", "/teɪk/", "v.", "拍摄；拿"], ["send", "/send/", "v.", "邮寄；发送"], ["kilometre", "/ˈkɪləmiːtə(r)/", "n.", "千米"], ["thousand", "/ˈθaʊznd/", "num.", "一千"], ["view", "/vjuː/", "n.", "景色；风景"], ["amazing", "/əˈmeɪzɪŋ/", "adj.", "极好的；令人惊奇的"], ["Great Wall", "/ɡreɪt wɔːl/", "n.", "长城"], ["Gingerbread House", "/ˈdʒɪndʒəbred haʊs/", "n.", "姜饼屋"], ["Eiffel Tower", "/ˈaɪfl ˈtaʊə(r)/", "n.", "埃菲尔铁塔"]],
    partBVocab: [["village", "/ˈvɪlɪdʒ/", "n.", "村庄"], ["dry", "/draɪ/", "adj.", "干的"], ["clay", "/kleɪ/", "n.", "黏土；陶土"], ["inspiring", "/ɪnˈspaɪərɪŋ/", "adj.", "鼓舞人心的"], ["bamboo", "/ˌbæmˈbuː/", "n.", "竹子"], ["pumpkin", "/ˈpʌmpkɪn/", "n.", "南瓜"], ["restaurant", "/ˈrestrɒnt/", "n.", "餐馆"], ["airport", "/ˈeəpɔːt/", "n.", "机场"], ["Terracotta Warriors", "/ˌterəˈkɒtə ˈwɒriəz/", "n.", "兵马俑"]],
    partAPhrases: [["climb the Great Wall", "爬长城"], ["last weekend", "上周末"], ["over the summer holidays", "暑假期间"], ["take many photos", "拍很多照片"], ["a must-see attraction", "必游景点"], ["visit the Gingerbread House", "参观姜饼屋"], ["send me some pictures", "给我发一些照片"], ["walk around the Palace Museum", "逛故宫博物院"]],
    partBPhrases: [["go to Xi'an", "去西安"], ["eat Xi'an noodles", "吃西安面条"], ["see the Terracotta Warriors", "看兵马俑"], ["ride bikes on the old city wall", "在古城墙上骑自行车"], ["the bamboo forest", "竹林"], ["pumpkin soup", "南瓜汤"], ["red rice", "红米饭"], ["by high-speed train", "乘高铁"], ["by cable car", "乘缆车"]],
    partASentences: [["How was your weekend / holiday?", "你周末/假期过得怎么样？"], ["It was great / fun / amazing!", "非常棒！"], ["What did you do last Saturday?", "你上周六做了什么？"], ["I visited the Gingerbread House.", "我参观了姜饼屋。"], ["Please send me some pictures.", "请发给我一些照片。"]],
    partBSentences: [["Where did you go over the summer holidays?", "你暑假去哪儿了？"], ["I went to Xi'an with my family.", "我和家人去了西安。"], ["What did you do there?", "你们在那儿做了什么？"], ["We went to see the Terracotta Warriors.", "我们去看了兵马俑。"], ["Did you climb the Great Wall?", "你爬长城了吗？"], ["Yes, I did. / No, I didn't.", "是的/不，没有。"]],
  },
  {
    num: 2,
    partAVocab: [["dress", "/dres/", "v.", "穿衣服"], ["paste", "/peɪst/", "v.", "粘贴"], ["gala", "/ˈɡɑːlə/", "n.", "演出；庆典"], ["count down", "/kaʊnt daʊn/", "phr.", "倒计时"], ["marathon", "/ˈmærəθən/", "n.", "马拉松"], ["cheer", "/tʃɪə(r)/", "v.", "欢呼；加油"], ["book fair", "/bʊk feə(r)/", "n.", "书市"], ["yesterday", "/ˈjestədeɪ/", "adv.", "昨天"], ["exciting", "/ɪkˈsaɪtɪŋ/", "adj.", "令人激动的"]],
    partBVocab: [["race", "/reɪs/", "n.", "赛跑"], ["run", "/rʌn/", "v.", "跑"], ["winner", "/ˈwɪnə(r)/", "n.", "获胜者"], ["wake", "/weɪk/", "v.", "醒；醒来"], ["begin", "/bɪˈɡɪn/", "v.", "开始"], ["win", "/wɪn/", "v.", "获胜"], ["share", "/ʃeə(r)/", "v.", "分享"], ["make zongzi", "/meɪk ˈzɒŋzi/", "phr.", "包粽子"]],
    partAPhrases: [["paste fu on the door", "在门上贴福字"], ["dress in red", "穿红色衣服"], ["wait for the Spring Festival Gala", "等待春节联欢晚会"], ["count down to the new year", "倒计时迎接新年"], ["clean the house", "打扫房子"], ["have a big dinner", "吃一顿大餐"]],
    partBPhrases: [["go to a marathon", "参加马拉松"], ["work as a volunteer", "志愿者工作"], ["cheer for the runners", "为跑步者加油"], ["join an online book fair", "参加线上书市"], ["share ideas", "分享想法"], ["the dragon boat race", "龙舟赛"], ["wake up early", "早起"], ["make zongzi", "包粽子"]],
    partASentences: [["Did you eat mooncakes?", "你们吃月饼了吗？"], ["Yes, we did. / No, we didn't.", "是的/不，没有。"], ["What did you do for the Spring Festival?", "你春节做了什么？"]],
    partBSentences: [["Did you take a trip?", "你们去旅行了吗？"], ["What did you like about it?", "你喜欢哪一点？"], ["My dad and I cleaned the house.", "我和爸爸打扫了房子。"], ["Finally, his team won the race!", "最后，他的队伍赢得了比赛！"]],
  },
  {
    num: 3,
    partAVocab: [["cold", "/kəʊld/", "n.", "感冒"], ["ill", "/ɪl/", "adj.", "不舒服"], ["head", "/hed/", "n.", "头"], ["runny nose", "/ˈrʌni nəʊz/", "n.", "流鼻涕"], ["fever", "/ˈfiːvə(r)/", "n.", "发烧"], ["cough", "/kɒf/", "n./v.", "咳嗽"], ["soon", "/suːn/", "adv.", "很快"], ["hospital", "/ˈhɒspɪtl/", "n.", "医院"], ["better", "/ˈbetə(r)/", "adj.", "好转的"]],
    partBVocab: [["diet", "/ˈdaɪət/", "n.", "日常饮食"], ["stay up", "/steɪ ʌp/", "phr.", "熬夜"], ["unhappy", "/ʌnˈhæpi/", "adj.", "不快乐的"], ["video", "/ˈvɪdiəʊ/", "n.", "视频"], ["should", "/ʃʊd/", "modal v.", "应该"], ["exercise", "/ˈeksəsaɪz/", "n./v.", "锻炼"], ["healthy", "/ˈhelθi/", "adj.", "健康的"], ["club", "/klʌb/", "n.", "俱乐部"]],
    partAPhrases: [["have a bad cold", "得了重感冒"], ["have a fever", "发烧"], ["have a cough", "咳嗽"], ["see a doctor", "看医生"], ["go to hospital", "去医院"], ["get well soon", "早日康复"]],
    partBPhrases: [["have a healthy diet", "保持健康饮食"], ["exercise often", "经常锻炼"], ["think about happy things", "想开心的事情"], ["join clubs and teams", "加入俱乐部和团队"], ["make video calls", "打视频电话"], ["cheer you up", "让你振作起来"]],
    partASentences: [["How do you feel?", "你感觉怎么样？"], ["I feel ill. My head hurts and I have a runny nose.", "我感觉不舒服。"], ["Maybe you should see a doctor.", "也许你应该看医生。"], ["You shouldn't stay up late.", "你不应该熬夜。"]],
    partBSentences: [["How can we live a healthy life?", "我们怎样过健康生活？"], ["We should exercise too.", "我们也应该锻炼。"], ["What are you going to do?", "你打算做什么？"], ["I'm going to see a doctor.", "我打算看医生。"]],
  },
  {
    num: 4,
    partAVocab: [["money", "/ˈmʌni/", "n.", "钱"], ["pocket money", "/ˈpɒkɪt ˈmʌni/", "n.", "零花钱"], ["schoolbag", "/ˈskuːlbæɡ/", "n.", "书包"], ["goods", "/ɡʊdz/", "n.", "商品"], ["service", "/ˈsɜːvɪs/", "n.", "服务"], ["drink", "/drɪŋk/", "n.", "饮料"], ["buy", "/baɪ/", "v.", "买"], ["spend", "/spend/", "v.", "花费"]],
    partBVocab: [["save", "/seɪv/", "v.", "储蓄"], ["save up", "/seɪv ʌp/", "phr.", "攒钱"], ["sale", "/seɪl/", "n.", "打折出售"], ["ticket", "/ˈtɪkɪt/", "n.", "票"], ["manage", "/ˈmænɪdʒ/", "v.", "管理"], ["need", "/niːd/", "v.", "需要"], ["want", "/wɒnt/", "v.", "想要"], ["plan", "/plæn/", "n./v.", "计划"], ["half", "/hɑːf/", "n.", "一半"]],
    partAPhrases: [["pocket money", "零花钱"], ["buy goods", "购买商品"], ["pay for services", "支付服务费用"], ["a cold drink", "一杯冷饮"], ["spend pocket money", "花零花钱"]],
    partBPhrases: [["save up for a computer", "攒钱买电脑"], ["write a spending plan", "写花钱计划"], ["wait for a sale", "等打折"], ["be careful with money", "谨慎用钱"], ["buy a nice gift", "买一份礼物"], ["use money wisely", "明智用钱"]],
    partASentences: [["How are you going to spend your pocket money?", "你打算怎么花零花钱？"], ["I am going to buy a schoolbag.", "我打算买书包。"], ["We use money to buy goods.", "我们用钱买商品。"]],
    partBSentences: [["I need to save more.", "我需要多存钱。"], ["Should I also buy some ice cream?", "我也该买冰淇淋吗？"], ["Maybe you can wait for a sale.", "也许你可以等打折。"]],
  },
  {
    num: 5,
    partAVocab: [["space", "/speɪs/", "n.", "太空"], ["planet", "/ˈplænɪt/", "n.", "行星"], ["star", "/stɑː(r)/", "n.", "星星"], ["moon", "/muːn/", "n.", "月亮"], ["Earth", "/ɜːθ/", "n.", "地球"], ["sky", "/skaɪ/", "n.", "天空"], ["telescope", "/ˈtelɪskəʊp/", "n.", "望远镜"], ["spaceship", "/ˈspeɪsʃɪp/", "n.", "宇宙飞船"]],
    partBVocab: [["Mars", "/mɑːz/", "n.", "火星"], ["astronaut", "/ˈæstrənɔːt/", "n.", "宇航员"], ["space station", "/speɪs ˈsteɪʃn/", "n.", "空间站"], ["outer space", "/ˈaʊtə speɪs/", "n.", "外太空"], ["rover", "/ˈrəʊvə(r)/", "n.", "探测器"], ["soil", "/sɔɪl/", "n.", "土壤"], ["solar system", "/ˈsəʊlə ˈsɪstəm/", "n.", "太阳系"], ["rocket", "/ˈrɒkɪt/", "n.", "火箭"]],
    partAPhrases: [["look into space", "观察太空"], ["in the solar system", "在太阳系中"], ["use a telescope", "使用望远镜"], ["travel in outer space", "在外太空旅行"], ["in the science museum", "在科学博物馆"]],
    partBPhrases: [["explore space", "探索太空"], ["live on a space station", "住在空间站"], ["the red planet", "红色星球"], ["send a rover to Mars", "向火星发送探测器"], ["go into space by spaceship", "乘宇宙飞船进入太空"], ["make us proud", "让我们自豪"]],
    partASentences: [["How can we explore space?", "我们怎样探索太空？"], ["We can use telescopes.", "我们可以使用望远镜。"], ["There are eight planets in our solar system.", "太阳系有八颗行星。"]],
    partBSentences: [["Where do astronauts live in space?", "宇航员住在哪？"], ["On a space station.", "在空间站。"], ["China sent a rover to Mars last year.", "中国去年向火星发送了探测器。"]],
  },
  {
    num: 6,
    partAVocab: [["energy", "/ˈenədʒi/", "n.", "能源"], ["electricity", "/ɪˌlekˈtrɪsəti/", "n.", "电"], ["solar power", "/ˈsəʊlə ˈpaʊə(r)/", "n.", "太阳能"], ["wind power", "/wɪnd ˈpaʊə(r)/", "n.", "风能"], ["water power", "/ˈwɔːtə ˈpaʊə(r)/", "n.", "水能"], ["green energy", "/ɡriːn ˈenədʒi/", "n.", "绿色能源"], ["power station", "/ˈpaʊə ˈsteɪʃn/", "n.", "发电站"], ["come from", "/kʌm frɒm/", "phr.", "来自"]],
    partBVocab: [["reduce", "/rɪˈdjuːs/", "v.", "减少"], ["reuse", "/ˌriːˈjuːz/", "v.", "重复使用"], ["recycle", "/ˌriːˈsaɪkl/", "v.", "回收利用"], ["unplug", "/ʌnˈplʌɡ/", "v.", "拔掉插头"], ["air conditioner", "/eə kənˈdɪʃənə(r)/", "n.", "空调"], ["shower", "/ˈʃaʊə(r)/", "n./v.", "淋浴"], ["LED lighting", "/ˌel iː ˈdiː/", "n.", "LED 照明"], ["save energy", "/seɪv ˈenədʒi/", "phr.", "节约能源"]],
    partAPhrases: [["come from rivers and lakes", "来自江河湖泊"], ["make electricity", "发电"], ["green energy", "绿色能源"], ["turn off lights", "关灯"], ["save energy", "节约能源"]],
    partBPhrases: [["take quick showers", "快速淋浴"], ["the 3R rules", "3R 原则"], ["protect the Earth", "保护地球"], ["unplug the computer", "拔掉电脑插头"], ["use LED lighting", "使用 LED 照明"], ["reduce, reuse and recycle", "减少、重复使用、回收"]],
    partASentences: [["Where does water come from?", "水来自哪里？"], ["It comes from rivers and lakes.", "它来自江河湖泊。"], ["Where does electricity come from?", "电来自哪里？"], ["It comes from power stations.", "它来自发电站。"]],
    partBSentences: [["We should save energy and use green energy.", "我们应该节约能源并使用绿色能源。"], ["We should reduce, reuse and recycle.", "我们应该减少、重复使用和回收。"], ["Take quick showers to save water.", "快速淋浴节约用水。"]],
  },
];

function cleanWord(word) {
  return word.toLowerCase().replace(/[^a-z\s-]/g, "").trim();
}

function regularPastVerb(word) {
  if (word.endsWith("e")) return `${word}d`;
  if (word.endsWith("y") && !/[aeiou]y$/.test(word)) return `${word.slice(0, -1)}ied`;
  return `${word}ed`;
}

function getVerbForms(base, irregularMap) {
  const exact = irregularMap[base];
  if (exact) return exact;
  if (!base.includes(" ")) {
    return { past: regularPastVerb(base), participle: regularPastVerb(base) };
  }
  const parts = base.split(" ");
  const first = parts[0];
  const tail = parts.slice(1).join(" ");
  const firstExact = irregularMap[first];
  if (firstExact) {
    return {
      past: `${firstExact.past} ${tail}`.trim(),
      participle: `${firstExact.participle} ${tail}`.trim(),
    };
  }
  const reg = regularPastVerb(first);
  return { past: `${reg} ${tail}`.trim(), participle: `${reg} ${tail}`.trim() };
}

function buildBlankSentenceFromText(sentence, candidates) {
  for (const candidate of candidates) {
    const safe = candidate.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const re = new RegExp(`\\b${safe}\\b`, "i");
    if (re.test(sentence)) {
      return sentence.replace(re, "___");
    }
  }
  return "";
}

function pickKeyFromText(text) {
  const tokens = text.replace(/[^A-Za-z\s-]/g, " ").split(/\s+/).filter(Boolean);
  const preferred = tokens.find((token) => token.length >= 5);
  return preferred || tokens[tokens.length - 1] || text.split(" ")[0];
}

function pickKeyFromText(text) {
  const tokens = text.replace(/[^A-Za-z\s-]/g, " ").split(/\s+/).filter(Boolean);
  const preferred = tokens.find((token) => token.length >= 5);
  return preferred || tokens[tokens.length - 1] || text.split(" ")[0];
}

function findSentenceForWord(unit, part, word) {
  const sentencePool = part === "A" ? unit.partASentences : unit.partBSentences;
  const normalized = cleanWord(word);
  const found = sentencePool.find(([en]) => cleanWord(en).includes(normalized));
  if (found) return found;
  return sentencePool[0] || ["Let's learn this word.", "让我们学习这个单词。"];
}

function buildVocabularyCardsFromAppendix() {
  const cards = [];
  appendixUnits.forEach((unit) => {
    [["A", unit.partAVocab], ["B", unit.partBVocab]].forEach(([part, vocabList]) => {
      vocabList.forEach(([word, ipa, pos, zh]) => {
        const [example, exampleZh] = findSentenceForWord(unit, part, word);
        cards.push({
          unit: unit.num,
          category: `Part ${part} · ${pos}`,
          front: word,
          ipa,
          zh,
          example,
          exampleZh,
          image: unitLocalImage[unit.num],
        });
      });
    });
  });
  return cards;
}

function buildPhraseCardsFromAppendix() {
  const all = [];
  appendixUnits.forEach((unit) => {
    [["A", unit.partAPhrases, unit.partASentences], ["B", unit.partBPhrases, unit.partBSentences]].forEach(([part, phraseList, sentenceList]) => {
      phraseList.forEach(([en, zh]) => {
        all.push({ unit: unit.num, scene: `Unit ${unit.num} Part ${part}`, en, key: pickKeyFromText(en), zh });
      });
      sentenceList.forEach(([en, zh]) => {
        all.push({ unit: unit.num, scene: `Unit ${unit.num} Part ${part}`, en, key: pickKeyFromText(en), zh });
      });
    });
  });
  return all;
}

function buildIrregularVerbsFromAppendix5(verbs) {
  return (verbs || []).map((v) => ({
    id: v.id,
    unit: 0,
    base: v.base,
    past: v.past,
    participle: v.participle,
    usage: `附录5 不规则动词 · ${v.zh || ""}`,
    sentence: `${v.base} — ${v.past} — ${v.participle}`,
    fillPrompt: `写出「${v.base}」的过去式（附录5）`,
    fillAnswer: String(v.past).split("/")[0].trim(),
    fillClue: v.zh ? `释义：${v.zh}` : "Irregular verbs",
  }));
}

async function loadIrregularVerbs() {
  try {
    const res = await fetch("data/practice/irregular-verbs.json", { cache: "no-store" });
    if (!res.ok) throw new Error("irregular-verbs.json missing");
    const data = await res.json();
    const list = Array.isArray(data.verbs) ? data.verbs : [];
    if (list.length !== 47) {
      console.warn(`附录5动词表：期望 47 个，当前 ${list.length} 个`);
    }
    return buildIrregularVerbsFromAppendix5(list);
  } catch (err) {
    console.warn("附录5不规则动词加载失败", err);
    return [];
  }
}

let vocabularyCards = buildVocabularyCardsFromAppendix();

function inferGrammarUnit(title) {
  const m = String(title || "").match(/Unit\s*(\d+)/i);
  return m ? Number(m[1]) : 0;
}

function applyUnitFilter(list, filterValue, unitKey = "unit") {
  if (!filterValue || filterValue === "all") return [...list];
  return list.filter((item) => String(item[unitKey] ?? 0) === String(filterValue));
}

const GRAMMAR_POINTS_BASE = [
  {
    title: "Unit 1 一般过去时",
    rule: "描述过去发生的事用过去式；否定用 didn't + 动词原形；疑问用 Did + 主语 + 动词原形。",
    examples: [
      "I climbed the Great Wall last weekend.",
      "Did you visit Xi'an? Yes, I did.",
      "I didn't take many photos.",
    ],
  },
  {
    title: "Unit 2 Did you...? 询问过去经历",
    rule: "询问过去是否做过某事：Did you + 动词原形 ...? 回答用 Yes, ... did / No, ... didn't。",
    examples: [
      "Did you eat mooncakes? Yes, we did.",
      "Did you take a trip? No, we didn't.",
      "What did you do for the Spring Festival?",
    ],
  },
  {
    title: "Unit 3 should / shouldn't",
    rule: "should 表示建议，后接动词原形；shouldn't 表示不应该。",
    examples: [
      "You should see a doctor.",
      "You should exercise every day.",
      "You shouldn't stay up late.",
    ],
  },
  {
    title: "Unit 4 be going to + 动词原形",
    rule: "表示计划或打算。",
    examples: [
      "I am going to save up for a computer.",
      "She is going to buy a schoolbag.",
      "We are going to write a spending plan.",
    ],
  },
  {
    title: "Unit 5 There is / There are + can",
    rule: "There is + 单数；There are + 复数；can + 动词原形表示能力。",
    examples: [
      "There is a rocket in the museum.",
      "There are eight planets in the solar system.",
      "We can use telescopes to look into space.",
    ],
  },
  {
    title: "Unit 6 Where does...come from? + should",
    rule: "询问来源：Where does + 单数主语 + come from? 提建议用 should。",
    examples: [
      "Where does electricity come from? It comes from power stations.",
      "Where does water come from? It comes from rivers.",
      "We should reduce, reuse and recycle.",
    ],
  },
  {
    title: "补充语法 1：一般现在时（三单）",
    rule: "主语是 he/she/it 或单数名词时，动词通常加 -s/-es。",
    examples: [
      "He likes science very much.",
      "She watches TV after dinner.",
      "The train goes to Beijing every day.",
    ],
  },
  {
    title: "补充语法 2：There be 就近原则",
    rule: "There be 句型中，be 动词与后面最近的名词保持一致。",
    examples: [
      "There is a book and two pens on the desk.",
      "There are two pens and a book on the desk.",
      "There is some water in the bottle.",
    ],
  },
  {
    title: "补充语法 3：特殊疑问词",
    rule: "what/where/when/how/why/how many/how much 根据提问对象选择。",
    examples: [
      "Where did you go yesterday?",
      "How many apples do you want?",
      "Why are you late for school?",
    ],
  },
  {
    title: "补充语法 4：情态动词 can / should",
    rule: "can / should 后都接动词原形，不加 to，不加 -s。",
    examples: [
      "I can swim very well.",
      "You should drink more water.",
      "He can help his classmates.",
    ],
  },
];

let grammarPoints = GRAMMAR_POINTS_BASE.map((point) => ({
  ...point,
  unit: point.unit ?? inferGrammarUnit(point.title),
}));

let commonPhrases = buildPhraseCardsFromAppendix();

let quizzes = [];
let fillBlankBank = [];

let verbTriples = [];

let writingSamples = [];

const STORAGE_KEY = "english_grade6_trainer_stats_v3";
const WRONG_BOOK_KEY = "english_grade6_wrong_quiz_ids_v1";
const PROFILE_KEY = "english_grade6_profile_v1";
const CHALLENGE_LOG_KEY = "english_grade6_challenge_logs_v1";
const REDEEM_LOG_KEY = "english_grade6_redeem_logs_v1";
const JOURNAL_KEY = "english_grade6_journal_v1";
const WRONG_BOOK_ITEMS_KEY = "english_grade6_wrong_items_v1";
const LEADERBOARD_KEY = "english_grade6_leaderboard_v1";
const BEHAVIOR_LOG_KEY = "english_grade6_behavior_logs_v1";
const BADGE_KEY = "english_grade6_badges_v1";
const REWARDED_KEY = "english_grade6_rewarded_v1";
const CUSTOM_BANKS_KEY = "english_grade6_custom_banks_v1";
const LAN_SYNC_KEY = "english_grade6_lan_sync_id_v1";
const DATA_UPDATED_AT_KEY = "english_grade6_data_updated_at_v1";
const SYNC_LOG_KEY = "english_grade6_sync_logs_v1";
const ADMIN_PIN_KEY = "english_grade6_admin_pin_v1";
const DASHBOARD_RESET_AT_KEY = "english_grade6_dashboard_reset_at_v1";
const PARENT_MODE_PASSPHRASE = "旭日长空光照人生";
let suppressDataTouch = false;
let suppressLanSync = false;
let lanSyncTimer = null;
let lanSyncInFlight = false;
let lanSyncPollTimer = null;
const LAN_SYNC_DEBOUNCE_MS = 10000;
const LAN_SYNC_POLL_MS = 10000;

let defaultQuizzes = [];
let defaultFillBlankBank = [];
let defaultWritingSamples = [];

let svoExercises = [
  { unit: 1, sentenceHint: "I visited the museum yesterday.", subject: "I", verb: "visited", object: "the museum yesterday" },
  { unit: 3, sentenceHint: "We should save energy every day.", subject: "We", verb: "should save", object: "energy every day" },
  { unit: 4, sentenceHint: "They are going to buy books.", subject: "They", verb: "are going to buy", object: "books" },
  { unit: 5, sentenceHint: "China sent a rover to Mars.", subject: "China", verb: "sent", object: "a rover to Mars" },
  { unit: 2, sentenceHint: "My mum cleaned the house.", subject: "My mum", verb: "cleaned", object: "the house" },
];

const behaviorActions = [
  { id: "help_others", label: "乐于助人 +200", points: 200, category: "good" },
  { id: "homework_star", label: "作业优星 +300", points: 300, category: "good" },
  { id: "reading_clock", label: "阅读打卡 +150", points: 150, category: "good" },
  { id: "english_speak", label: "主动英语表达 +250", points: 250, category: "good" },
  { id: "tidy_room", label: "整理房间 +100", points: 100, category: "good" },
  { id: "wash_tidy", label: "洗漱整理 +100", points: 100, category: "good" },
  { id: "exercise", label: "运动锻炼 +100", points: 100, category: "good" },
  { id: "family_help", label: "家务帮助 +150", points: 150, category: "good" },
  { id: "class_answer", label: "课堂积极回答 +150", points: 150, category: "good" },
  { id: "dictation_full", label: "听写满分 +200", points: 200, category: "good" },
  { id: "review_notes", label: "自主复习 +100", points: 100, category: "good" },
  { id: "good_sleep", label: "早睡早起 +100", points: 100, category: "good" },
  { id: "kindness", label: "文明礼貌 +100", points: 100, category: "good" },
  { id: "goal_done", label: "完成学习目标 +200", points: 200, category: "good" },
  { id: "focus_30", label: "专注学习30分钟 +200", points: 200, category: "good" },
  { id: "watch_tv", label: "看电视超时 -150", points: -150, category: "bad" },
  { id: "play_game", label: "玩游戏超时 -200", points: -200, category: "bad" },
  { id: "late_sleep", label: "熬夜 -150", points: -150, category: "bad" },
  { id: "homework_delay", label: "作业拖延 -200", points: -200, category: "bad" },
  { id: "argue", label: "顶嘴争吵 -150", points: -150, category: "bad" },
  { id: "messy_room", label: "房间杂乱 -100", points: -100, category: "bad" },
  { id: "snack_too_much", label: "零食过量 -100", points: -100, category: "bad" },
  { id: "late_arrive", label: "迟到 -100", points: -100, category: "bad" },
  { id: "no_review", label: "未复习 -100", points: -100, category: "bad" },
];

let cardIndex = 0;
let cardFlipped = false;
let grammarIndex = 0;
let phraseIndex = 0;
let phraseFlipped = false;
let writingIndex = 0;
let filteredWritingSamples = [];
let currentQuiz = null;
let verbIndex = 0;
let svoIndex = 0;
let svoTokenLayoutKey = "";
let svoTokenLayout = [];
let activeSvoSlot = "subject";
let svoUserAnswer = { subject: "", verb: "", object: "" };
let filteredCards = [...vocabularyCards];
let filteredGrammarPoints = [...grammarPoints];
let filteredPhrases = [...commonPhrases];
let filteredVerbTriples = [...verbTriples];
let filteredSvoExercises = [...svoExercises];
let filteredQuizzes = [];
let wrongBookMode = false;
let stats = loadStats();
let wrongQuizIds = loadWrongQuizIds();
let studentProfile = loadStudentProfile();
let challengeLogs = loadChallengeLogs();
let redeemLogs = loadRedeemLogs();
let journalEntries = loadJournalEntries();
let wrongBookItems = loadWrongBookItems();
let leaderboard = loadLeaderboard();
let behaviorLogs = loadBehaviorLogs();
let badges = loadBadges();
let rewarded = loadRewarded();
let parentUnlocked = false;
let cumulativeTitleClicks = 0;
let cumulativeTitleClickTimer = null;
let currentFillQuestions = [];

const elements = {
  correctCount: document.getElementById("correctCount"),
  wrongCount: document.getElementById("wrongCount"),
  attemptCount: document.getElementById("attemptCount"),
  accuracy: document.getElementById("accuracy"),
  pointCount: document.getElementById("pointCount"),
  cumulativePointCount: document.getElementById("cumulativePointCount"),
  wrongBookCount: document.getElementById("wrongBookCount"),
  nicknameInput: document.getElementById("nicknameInput"),
  saveNickname: document.getElementById("saveNickname"),
  resetAllStats: document.getElementById("resetAllStats"),
  exportReport: document.getElementById("exportReport"),
  exportReportHtml: document.getElementById("exportReportHtml"),
  exportPointsHtml: document.getElementById("exportPointsHtml"),
  markAnswerCorrect: document.getElementById("markAnswerCorrect"),
  markAnswerWrong: document.getElementById("markAnswerWrong"),
  nicknameDisplay: document.getElementById("nicknameDisplay"),
  lastPracticeTime: document.getElementById("lastPracticeTime"),
  redeemName: document.getElementById("redeemName"),
  redeemCost: document.getElementById("redeemCost"),
  redeemPoints: document.getElementById("redeemPoints"),
  leaderboardList: document.getElementById("leaderboardList"),
  leaderboardSort: document.getElementById("leaderboardSort"),
  behaviorActionSelect: document.getElementById("behaviorActionSelect"),
  applyBehaviorAction: document.getElementById("applyBehaviorAction"),
  badgeList: document.getElementById("badgeList"),
  redeemList: document.getElementById("redeemList"),
  wrongItemList: document.getElementById("wrongItemList"),
  exportFeedback: document.getElementById("exportFeedback"),
  challengeList: document.getElementById("challengeList"),
  fxLayer: document.getElementById("fxLayer"),
  tabs: document.querySelectorAll(".tab[data-tab]"),
  panels: document.querySelectorAll(".panel"),
  unitFilter: document.getElementById("unitFilter"),
  grammarUnitFilter: document.getElementById("grammarUnitFilter"),
  phraseUnitFilter: document.getElementById("phraseUnitFilter"),
  verbUnitFilter: document.getElementById("verbUnitFilter"),
  journalUnitFilter: document.getElementById("journalUnitFilter"),
  journalListUnitFilter: document.getElementById("journalListUnitFilter"),
  flashcard: document.getElementById("flashcard"),
  cardCategory: document.getElementById("cardCategory"),
  cardFront: document.getElementById("cardFront"),
  cardBack: document.getElementById("cardBack"),
  cardPhonetic: document.getElementById("cardPhonetic"),
  cardZh: document.getElementById("cardZh"),
  cardExample: document.getElementById("cardExample"),
  cardExampleZh: document.getElementById("cardExampleZh"),
  cardImage: document.getElementById("cardImage"),
  prevCard: document.getElementById("prevCard"),
  nextCard: document.getElementById("nextCard"),
  grammarTitle: document.getElementById("grammarTitle"),
  grammarRule: document.getElementById("grammarRule"),
  grammarExample: document.getElementById("grammarExample"),
  nextGrammar: document.getElementById("nextGrammar"),
  svoSentenceHint: document.getElementById("svoSentenceHint"),
  slotSubject: document.getElementById("slotSubject"),
  slotVerb: document.getElementById("slotVerb"),
  slotObject: document.getElementById("slotObject"),
  svoTokens: document.getElementById("svoTokens"),
  checkSvo: document.getElementById("checkSvo"),
  nextSvo: document.getElementById("nextSvo"),
  svoFeedback: document.getElementById("svoFeedback"),
  phraseScene: document.getElementById("phraseScene"),
  phraseCard: document.getElementById("phraseCard"),
  phraseMasked: document.getElementById("phraseMasked"),
  phraseEn: document.getElementById("phraseEn"),
  phraseZh: document.getElementById("phraseZh"),
  phraseHint: document.getElementById("phraseHint"),
  nextPhrase: document.getElementById("nextPhrase"),
  writingTitle: document.getElementById("writingTitle"),
  writingEn: document.getElementById("writingEn"),
  writingZh: document.getElementById("writingZh"),
  writingUnitFilter: document.getElementById("writingUnitFilter"),
  writingFillPrompt: document.getElementById("writingFillPrompt"),
  writingFillInput: document.getElementById("writingFillInput"),
  checkWritingFill: document.getElementById("checkWritingFill"),
  writingFillFeedback: document.getElementById("writingFillFeedback"),
  writingStudentInput: document.getElementById("writingStudentInput"),
  scoreWriting: document.getElementById("scoreWriting"),
  writingScore: document.getElementById("writingScore"),
  writingAdvice: document.getElementById("writingAdvice"),
  nextWriting: document.getElementById("nextWriting"),
  quizUnitFilter: document.getElementById("quizUnitFilter"),
  quizPartFilter: document.getElementById("quizPartFilter"),
  startWrongBook: document.getElementById("startWrongBook"),
  clearWrongBook: document.getElementById("clearWrongBook"),
  wrongBookStatus: document.getElementById("wrongBookStatus"),
  wrongBookModuleFilter: document.getElementById("wrongBookModuleFilter"),
  wrongBookUnitFilter: document.getElementById("wrongBookUnitFilter"),
  wrongBookPanelList: document.getElementById("wrongBookPanelList"),
  wrongBookPanelSummary: document.getElementById("wrongBookPanelSummary"),
  reviewWrongVocab: document.getElementById("reviewWrongVocab"),
  reviewWrongQuiz: document.getElementById("reviewWrongQuiz"),
  clearWrongBookPanel: document.getElementById("clearWrongBookPanel"),
  parentModeStatus: document.getElementById("parentModeStatus"),
  exitParentMode: document.getElementById("exitParentMode"),
  quizBadge: document.getElementById("quizBadge"),
  quizPrompt: document.getElementById("quizPrompt"),
  quizOptions: document.getElementById("quizOptions"),
  quizFeedback: document.getElementById("quizFeedback"),
  quizAnalysis: document.getElementById("quizAnalysis"),
  nextQuestion: document.getElementById("nextQuestion"),
  fillUnitFilter: document.getElementById("fillUnitFilter"),
  fillQuestions: document.getElementById("fillQuestions"),
  submitFillSet: document.getElementById("submitFillSet"),
  nextFillSet: document.getElementById("nextFillSet"),
  fillSetFeedback: document.getElementById("fillSetFeedback"),
  verbBase: document.getElementById("verbBase"),
  verbInfinitive: document.getElementById("verbInfinitive"),
  verbPast: document.getElementById("verbPast"),
  verbParticiple: document.getElementById("verbParticiple"),
  verbUsage: document.getElementById("verbUsage"),
  verbSentence: document.getElementById("verbSentence"),
  verbFillPrompt: document.getElementById("verbFillPrompt"),
  verbFillInput: document.getElementById("verbFillInput"),
  checkVerb: document.getElementById("checkVerb"),
  nextVerb: document.getElementById("nextVerb"),
  verbFeedback: document.getElementById("verbFeedback"),
  appendixSummary: document.getElementById("appendixSummary"),
  appendixTable: document.getElementById("appendixTable"),
  refreshAppendix: document.getElementById("refreshAppendix"),
  journalToday: document.getElementById("journalToday"),
  journalInput: document.getElementById("journalInput"),
  saveJournal: document.getElementById("saveJournal"),
  journalFeedback: document.getElementById("journalFeedback"),
  journalList: document.getElementById("journalList"),
  pointsBreakdown: document.getElementById("pointsBreakdown"),
  importBankFile: document.getElementById("importBankFile"),
  importBankBtn: document.getElementById("importBankBtn"),
  downloadImportTemplate: document.getElementById("downloadImportTemplate"),
  clearCustomBanks: document.getElementById("clearCustomBanks"),
  importBankFeedback: document.getElementById("importBankFeedback"),
  syncDataBtn: document.getElementById("syncDataBtn"),
  lanSyncFeedback: document.getElementById("lanSyncFeedback"),
  syncLogList: document.getElementById("syncLogList"),
  toggleStudentSidebar: document.getElementById("toggleStudentSidebar"),
  studentSidebar: document.getElementById("studentSidebar"),
  mobileNicknameInput: document.getElementById("mobileNicknameInput"),
  mobileSaveNickname: document.getElementById("mobileSaveNickname"),
  mobileSyncBtn: document.getElementById("mobileSyncBtn"),
  mobileLanSyncFeedback: document.getElementById("mobileLanSyncFeedback"),
  lanAccessBox: document.getElementById("lanAccessBox"),
  lanAccessUrlList: document.getElementById("lanAccessUrlList"),
  lanAccessAlt: document.getElementById("lanAccessAlt"),
  lanAccessCopyFeedback: document.getElementById("lanAccessCopyFeedback"),
  lanAccessBoxMobile: document.getElementById("lanAccessBoxMobile"),
  lanAccessUrlListMobile: document.getElementById("lanAccessUrlListMobile"),
  lanAccessCopyFeedbackMobile: document.getElementById("lanAccessCopyFeedbackMobile"),
  resetParentPin: document.getElementById("resetParentPin"),
  forgotParentPin: document.getElementById("forgotParentPin"),
  parentPinStatus: document.getElementById("parentPinStatus"),
  parentPinRecoverHint: document.getElementById("parentPinRecoverHint"),
  adminPinInput: document.getElementById("adminPinInput"),
  saveAdminPin: document.getElementById("saveAdminPin"),
  requireRemoteApproval: document.getElementById("requireRemoteApproval"),
  pendingEditsList: document.getElementById("pendingEditsList"),
  hostAdminBox: document.getElementById("hostAdminBox"),
  parentPinBox: document.getElementById("parentPinBox"),
};

function loadStats() {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return { correct: 0, wrong: 0, attempts: 0, points: 0, highestPoints: 0, highestAccumulated: 0, accumulatedPoints: 0, behaviorPointsTotal: 0, redeemedTotal: 0, lastPracticeAt: "", lastCompoundDate: "", lastSpendDate: "" };
  }
  try {
    const parsed = JSON.parse(raw);
    return {
      correct: Number(parsed.correct) || 0,
      wrong: Number(parsed.wrong) || 0,
      attempts: Number(parsed.attempts) || 0,
      points: Number(parsed.points) || 0,
      highestPoints: Number(parsed.highestPoints) || 0,
      highestAccumulated: Number(parsed.highestAccumulated) || 0,
      accumulatedPoints: Number(parsed.accumulatedPoints) || 0,
      behaviorPointsTotal: Number(parsed.behaviorPointsTotal) || 0,
      redeemedTotal: Number(parsed.redeemedTotal) || 0,
      lastPracticeAt: parsed.lastPracticeAt || "",
      lastCompoundDate: parsed.lastCompoundDate || "",
      lastSpendDate: parsed.lastSpendDate || "",
    };
  } catch {
    return { correct: 0, wrong: 0, attempts: 0, points: 0, highestPoints: 0, highestAccumulated: 0, accumulatedPoints: 0, behaviorPointsTotal: 0, redeemedTotal: 0, lastPracticeAt: "", lastCompoundDate: "", lastSpendDate: "" };
  }
}

function loadWrongQuizIds() {
  const raw = window.localStorage.getItem(WRONG_BOOK_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function loadStudentProfile() {
  const raw = window.localStorage.getItem(PROFILE_KEY);
  if (!raw) return { nickname: "同学", parentPinHash: "" };
  try {
    const parsed = JSON.parse(raw);
    return { nickname: parsed.nickname || "同学", parentPinHash: parsed.parentPinHash || "" };
  } catch {
    return { nickname: "同学", parentPinHash: "" };
  }
}

function loadChallengeLogs() {
  const raw = window.localStorage.getItem(CHALLENGE_LOG_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function loadRedeemLogs() {
  const raw = window.localStorage.getItem(REDEEM_LOG_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function loadJournalEntries() {
  const raw = window.localStorage.getItem(JOURNAL_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function loadWrongBookItems() {
  const raw = window.localStorage.getItem(WRONG_BOOK_ITEMS_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function loadLeaderboard() {
  const raw = window.localStorage.getItem(LEADERBOARD_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.map((row) => ({
      nickname: row.nickname || "同学",
      bestPoints: Number(row.bestPoints) || 0,
      bestAccuracy: Number(row.bestAccuracy) || 0,
      bestStreakDays: Number(row.bestStreakDays) || 0,
      updatedAt: row.updatedAt || nowText(),
    }));
  } catch {
    return [];
  }
}

function loadBehaviorLogs() {
  const raw = window.localStorage.getItem(BEHAVIOR_LOG_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function loadBadges() {
  const raw = window.localStorage.getItem(BADGE_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function touchDataUpdatedAt() {
  if (suppressDataTouch) return;
  window.localStorage.setItem(DATA_UPDATED_AT_KEY, new Date().toISOString());
  scheduleLanSync();
}

function getDataUpdatedAt() {
  return window.localStorage.getItem(DATA_UPDATED_AT_KEY) || "";
}

function setDataUpdatedAt(iso) {
  if (iso) window.localStorage.setItem(DATA_UPDATED_AT_KEY, iso);
}

function saveStats() {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(stats));
  touchDataUpdatedAt();
}

function saveWrongQuizIds() {
  window.localStorage.setItem(WRONG_BOOK_KEY, JSON.stringify(wrongQuizIds));
  touchDataUpdatedAt();
}

function saveStudentProfile() {
  window.localStorage.setItem(PROFILE_KEY, JSON.stringify(studentProfile));
  touchDataUpdatedAt();
}

function saveChallengeLogs() {
  window.localStorage.setItem(CHALLENGE_LOG_KEY, JSON.stringify(challengeLogs));
  touchDataUpdatedAt();
}

function saveRedeemLogs() {
  window.localStorage.setItem(REDEEM_LOG_KEY, JSON.stringify(redeemLogs));
  touchDataUpdatedAt();
}

function saveJournalEntries() {
  window.localStorage.setItem(JOURNAL_KEY, JSON.stringify(journalEntries));
  touchDataUpdatedAt();
}

function saveWrongBookItems() {
  window.localStorage.setItem(WRONG_BOOK_ITEMS_KEY, JSON.stringify(wrongBookItems));
  touchDataUpdatedAt();
}

function saveLeaderboard() {
  window.localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(leaderboard));
  touchDataUpdatedAt();
}

function saveBehaviorLogs() {
  window.localStorage.setItem(BEHAVIOR_LOG_KEY, JSON.stringify(behaviorLogs));
  touchDataUpdatedAt();
}

function saveBadges() {
  window.localStorage.setItem(BADGE_KEY, JSON.stringify(badges));
  touchDataUpdatedAt();
}

function loadRewarded() {
  const raw = window.localStorage.getItem(REWARDED_KEY);
  if (!raw) return { quiz: [], writing: [], fillblank: [], svo: [], verb: [] };
  try {
    const parsed = JSON.parse(raw);
    return {
      quiz: Array.isArray(parsed.quiz) ? parsed.quiz : [],
      writing: Array.isArray(parsed.writing) ? parsed.writing : [],
      fillblank: Array.isArray(parsed.fillblank) ? parsed.fillblank : [],
      svo: Array.isArray(parsed.svo) ? parsed.svo : [],
      verb: Array.isArray(parsed.verb) ? parsed.verb : [],
    };
  } catch {
    return { quiz: [], writing: [], fillblank: [], svo: [], verb: [] };
  }
}

function saveRewarded() {
  window.localStorage.setItem(REWARDED_KEY, JSON.stringify(rewarded));
  touchDataUpdatedAt();
}

function hasBeenRewarded(category, id) {
  const list = rewarded[category];
  return Array.isArray(list) && list.includes(String(id));
}

function markRewarded(category, id) {
  if (!rewarded[category]) rewarded[category] = [];
  const key = String(id);
  if (!rewarded[category].includes(key)) {
    rewarded[category].push(key);
    saveRewarded();
  }
}

function hashParentPin(pin) {
  let hash = 5381;
  const text = `pep6-parent-${pin}`;
  for (let i = 0; i < text.length; i += 1) {
    hash = ((hash << 5) + hash) ^ text.charCodeAt(i);
  }
  return String(hash >>> 0);
}

function verifyParentPin(pin) {
  if (!studentProfile.parentPinHash) return false;
  return hashParentPin(pin) === studentProfile.parentPinHash;
}

let passwordPromptResolver = null;

function closePasswordPrompt(value) {
  const modal = document.getElementById("passwordPromptModal");
  const input = document.getElementById("passwordPromptInput");
  if (modal) modal.classList.add("hidden");
  if (input) input.value = "";
  const resolve = passwordPromptResolver;
  passwordPromptResolver = null;
  if (resolve) resolve(value);
}

function promptPassword(message, title = "请输入家长密码", options = {}) {
  return new Promise((resolve) => {
    const modal = document.getElementById("passwordPromptModal");
    const input = document.getElementById("passwordPromptInput");
    const titleEl = document.getElementById("passwordPromptTitle");
    const msgEl = document.getElementById("passwordPromptMessage");
    if (!modal || !input) {
      resolve(null);
      return;
    }
    passwordPromptResolver = resolve;
    if (titleEl) titleEl.textContent = title;
    if (msgEl) msgEl.textContent = message || "";
    input.autocomplete = options.newPassword ? "new-password" : "current-password";
    input.value = "";
    modal.classList.remove("hidden");
    window.requestAnimationFrame(() => input.focus());
  });
}

async function promptPasswordTwice(firstMessage, secondMessage, title = "设置家长密码") {
  const pin1 = await promptPassword(firstMessage, title, { newPassword: true });
  if (!pin1) return null;
  const pin2 = await promptPassword(secondMessage, "请再次输入密码确认", { newPassword: true });
  if (!pin2) return null;
  if (pin1 !== pin2) {
    window.alert("两次密码不一致，请重试。");
    return null;
  }
  return pin1;
}

function initPasswordPromptModal() {
  const modal = document.getElementById("passwordPromptModal");
  const input = document.getElementById("passwordPromptInput");
  const okBtn = document.getElementById("passwordPromptOk");
  const cancelBtn = document.getElementById("passwordPromptCancel");
  const backdrop = modal?.querySelector("[data-password-dismiss]");
  if (!modal || !input || !okBtn || !cancelBtn) return;

  const submit = () => closePasswordPrompt(input.value);
  okBtn.addEventListener("click", submit);
  cancelBtn.addEventListener("click", () => closePasswordPrompt(null));
  backdrop?.addEventListener("click", () => closePasswordPrompt(null));
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      submit();
    } else if (event.key === "Escape") {
      event.preventDefault();
      closePasswordPrompt(null);
    }
  });
  modal.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closePasswordPrompt(null);
  });
}

async function requireParentAuth(action) {
  if (!studentProfile.parentPinHash) {
    window.alert("尚未设置家长密码。请先保存学生昵称并按提示设置家长密码。");
    await promptParentPinSetup();
    return;
  }
  if (parentUnlocked) {
    action();
    return;
  }
  const pin = await promptPassword("用于积分兑换、行为记分、手动判题等家长操作。");
  if (!pin) return;
  if (!verifyParentPin(pin)) {
    window.alert("家长密码错误，操作已取消。");
    return;
  }
  parentUnlocked = true;
  updateParentModeUI();
  updateParentPinPanel();
  revealParentSettingsSidebar();
  action();
}

async function requireParentPasswordAlways(action, message) {
  if (!studentProfile.parentPinHash) {
    window.alert("尚未设置家长密码。");
    return;
  }
  const pin = await promptPassword(message || "请输入家长密码以继续。");
  if (!pin) return;
  if (!verifyParentPin(pin)) {
    window.alert("家长密码错误，操作已取消。");
    return;
  }
  action();
}

function exitParentMode() {
  parentUnlocked = false;
  updateParentModeUI();
  window.alert("已退出家长模式。回答正确/错误、积分兑换、行为记分等操作将重新要求输入密码。");
}

function isParentModeActive() {
  return Boolean(parentUnlocked);
}

function guardParentModePanel() {
  if (!parentUnlocked) return false;
  return true;
}

function revealParentSettingsSidebar() {
  if (elements.studentSidebar?.classList.contains("collapsed-on-mobile")) {
    elements.studentSidebar.classList.remove("collapsed-on-mobile");
    if (elements.toggleStudentSidebar) {
      elements.toggleStudentSidebar.setAttribute("aria-expanded", "true");
      elements.toggleStudentSidebar.textContent = "▲ 收起档案与设置";
    }
  }
}

function tryParentModePassphrase(text) {
  if ((text || "").trim() !== PARENT_MODE_PASSPHRASE) return false;
  if (!parentUnlocked) {
    parentUnlocked = true;
    updateParentModeUI();
    updateParentPinPanel();
    revealParentSettingsSidebar();
    window.requestAnimationFrame(() => {
      elements.parentPinBox?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  }
  return true;
}

function updateParentModeUI() {
  if (elements.parentModeStatus) {
    elements.parentModeStatus.textContent = parentUnlocked
      ? "家长模式：已解锁（本会话内免重复输入密码）"
      : "家长模式：未解锁（敏感操作每次需输入密码）";
  }
  if (elements.exitParentMode) {
    elements.exitParentMode.classList.toggle("hidden", !parentUnlocked);
  }
  const showParentPanels = parentUnlocked;
  if (elements.parentPinBox) {
    elements.parentPinBox.classList.toggle("hidden", !showParentPanels);
    elements.parentPinBox.setAttribute("aria-hidden", showParentPanels ? "false" : "true");
  }
  if (elements.hostAdminBox) {
    elements.hostAdminBox.classList.toggle("hidden", !showParentPanels);
    elements.hostAdminBox.setAttribute("aria-hidden", showParentPanels ? "false" : "true");
  }
}

async function promptParentPinSetup() {
  const pin1 = await promptPassword(
    "用于积分兑换、行为记分、手动判题等家长操作。",
    "【家长设置】设置家长密码",
    { newPassword: true },
  );
  if (!pin1) {
    if (window.confirm("未设置家长密码，学生将无法使用手动记分与兑换。是否清零练习统计？")) performResetDashboardStats();
    return;
  }
  const pin2 = await promptPassword("请再次输入相同密码以确认。", "确认家长密码", { newPassword: true });
  if (!pin2) {
    if (window.confirm("未设置家长密码，学生将无法使用手动记分与兑换。是否清零练习统计？")) performResetDashboardStats();
    return;
  }
  if (pin1 !== pin2) {
    window.alert("两次密码不一致，设置失败。");
    if (window.confirm("设定出错，是否清零练习统计？")) performResetDashboardStats();
    return;
  }
  studentProfile.parentPinHash = hashParentPin(pin1);
  saveStudentProfile();
  parentUnlocked = true;
  updateParentModeUI();
  window.alert(parentPinSetupSuccessMessage());
  updateParentPinPanel();
}

function resetParentPin() {
  if (!guardParentModePanel()) return;
  if (!studentProfile.parentPinHash) {
    window.alert("尚未设置家长密码，请先保存昵称并完成首次设置。");
    return;
  }
  requireParentPasswordAlways(async () => {
    const ok = window.confirm("将设置新的家长密码，旧密码立即失效。是否继续？");
    if (!ok) return;
    const pin1 = await promptPasswordTwice(
      "请输入新家长密码。",
      "请再次输入新家长密码确认。",
      "设置新家长密码",
    );
    if (!pin1) return;
    studentProfile.parentPinHash = hashParentPin(pin1);
    saveStudentProfile();
    parentUnlocked = true;
    updateParentModeUI();
    window.alert(parentPinUpdatedMessage());
    updateParentPinPanel();
  }, "请输入当前家长密码以开始重置：");
}

function getAdminPin() {
  return (elements.adminPinInput?.value || window.localStorage.getItem(ADMIN_PIN_KEY) || "").trim();
}

function saveAdminPinLocal(pin) {
  if (pin) window.localStorage.setItem(ADMIN_PIN_KEY, pin);
}

let serverReportsLocalClient = false;

function canRecoverParentPinWithoutOld() {
  return isLocalHostClient() || serverReportsLocalClient;
}

function updateParentPinPanel() {
  const hasPin = Boolean(studentProfile.parentPinHash);
  if (elements.parentPinStatus) {
    elements.parentPinStatus.textContent = hasPin
      ? "当前状态：已设置家长密码（仅存加密摘要，无法显示原密码）"
      : "当前状态：尚未设置家长密码（保存昵称时会提示设置）";
    elements.parentPinStatus.dataset.state = hasPin ? "set" : "unset";
  }
  if (elements.forgotParentPin) {
    elements.forgotParentPin.disabled = !canRecoverParentPinWithoutOld();
  }
  if (elements.parentPinRecoverHint) {
    if (canRecoverParentPinWithoutOld()) {
      elements.parentPinRecoverHint.textContent =
        "本机可直接点「忘记密码 · 本机重设」，无需旧密码；练习与积分数据不会删除。";
    } else {
      elements.parentPinRecoverHint.textContent =
        "手机/其他设备无法免旧密码重设。请在运行 启动.bat 的电脑上打开 http://localhost:8080，在侧栏本区域重设。";
    }
  }
}

function parentPinSetupSuccessMessage() {
  return (
    "家长密码已设置。\n\n" +
    "存放位置：本机浏览器 localStorage\n" +
    `键名：${PROFILE_KEY}\n` +
    "字段：parentPinHash（加密，无法查看明文）\n\n" +
    "请牢记密码，或记下侧栏「家长密码说明」中的存放位置。同步后同昵称设备会使用同一套密码。"
  );
}

function parentPinUpdatedMessage() {
  return `家长密码已更新。新密码仍保存在本机 ${PROFILE_KEY}（parentPinHash），请牢记。`;
}

function isLocalHostClient() {
  const host = window.location.hostname;
  return host === "localhost" || host === "127.0.0.1" || host === "[::1]";
}

async function fetchAdminConfig() {
  try {
    const res = await fetch("/api/study-hub/admin/config", { cache: "no-store" });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

async function saveAdminPinToServer() {
  if (!guardParentModePanel()) return;
  const pin = elements.adminPinInput?.value?.trim() || "";
  if (pin.length < 4) {
    window.alert("管理员密码至少 4 位。");
    return;
  }
  const current = window.localStorage.getItem(ADMIN_PIN_KEY) || "";
  const body = {
    adminPin: pin,
    requireRemoteApproval: Boolean(elements.requireRemoteApproval?.checked),
  };
  if (current) body.currentAdminPin = current;
  const res = await fetch("/api/study-hub/admin/setup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) {
    window.alert(data.error || "保存管理员密码失败");
    return;
  }
  saveAdminPinLocal(pin);
  window.alert("管理员密码已保存。远程设备改写需您批准后才会入库。");
  await refreshPendingEdits();
}

async function refreshPendingEdits() {
  if (!elements.pendingEditsList) return;
  if (!parentUnlocked) {
    elements.pendingEditsList.innerHTML = "";
    return;
  }
  const pin = getAdminPin();
  if (!pin && !isLocalHostClient()) {
    elements.pendingEditsList.innerHTML = "<p class=\"model\">输入管理员密码后可查看待审核项。</p>";
    return;
  }
  try {
    const url = `/api/study-hub/admin/pending?adminPin=${encodeURIComponent(pin)}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) {
      elements.pendingEditsList.innerHTML = "<p class=\"model\">无法加载待审核列表。</p>";
      return;
    }
    const data = await res.json();
    renderPendingEdits(data.items || []);
  } catch {
    elements.pendingEditsList.innerHTML = "";
  }
}

function renderPendingEdits(items) {
  if (!elements.pendingEditsList) return;
  if (!items.length) {
    elements.pendingEditsList.innerHTML = "<p class=\"model\">暂无待审核改写。</p>";
    return;
  }
  elements.pendingEditsList.innerHTML = items
    .map(
      (item) => `
      <div class="pending-edit-item" data-id="${item.id}">
        <div class="pending-meta">${item.createdAt || ""} · ${item.device || "远程设备"} · ${item.summary || item.kind || ""}</div>
        <div>${item.kind === "import-csv" ? "CSV 导入" : item.kind === "knowledge" ? "精讲保存" : "讲读保存"}</div>
        <div class="pending-edit-actions">
          <button type="button" class="primary-btn approve-pending-btn" data-id="${item.id}">批准入库</button>
          <button type="button" class="secondary-btn reject-pending-btn" data-id="${item.id}">拒绝</button>
        </div>
      </div>`,
    )
    .join("");
  elements.pendingEditsList.querySelectorAll(".approve-pending-btn").forEach((btn) => {
    btn.addEventListener("click", () => resolvePendingEdit(btn.dataset.id, true));
  });
  elements.pendingEditsList.querySelectorAll(".reject-pending-btn").forEach((btn) => {
    btn.addEventListener("click", () => resolvePendingEdit(btn.dataset.id, false));
  });
}

async function resolvePendingEdit(id, approve) {
  if (!guardParentModePanel()) return;
  const pin = getAdminPin();
  if (!pin) {
    window.alert("请先输入并保存管理员密码。");
    return;
  }
  const path = approve ? "/api/study-hub/admin/approve" : "/api/study-hub/admin/reject";
  const res = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Admin-Pin": pin },
    body: JSON.stringify({ id, adminPin: pin }),
  });
  const data = await res.json();
  if (!res.ok) {
    window.alert(data.error || "操作失败");
    return;
  }
  await refreshPendingEdits();
  if (window.StudyHub?.applyLanSync) window.StudyHub.applyLanSync();
}

async function initHostAdminPanel() {
  const savedPin = window.localStorage.getItem(ADMIN_PIN_KEY) || "";
  if (elements.adminPinInput && savedPin) elements.adminPinInput.value = savedPin;
  const cfg = await fetchAdminConfig();
  if (cfg && elements.requireRemoteApproval) {
    elements.requireRemoteApproval.checked = Boolean(cfg.requireRemoteApproval);
  }
  if (elements.hostAdminBox && cfg && !cfg.hasAdminPin && isLocalHostClient() && parentUnlocked) {
    elements.hostAdminBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
  await refreshPendingEdits();
  window.setInterval(() => {
    if (document.hidden) return;
    refreshPendingEdits();
  }, 20000);
}

async function promptParentPinChange() {
  const pin1 = await promptPasswordTwice(
    "将覆盖原家长密码。",
    "请再次输入新密码确认。",
    "【家长专用】设置新密码",
  );
  if (!pin1) return;
  studentProfile.parentPinHash = hashParentPin(pin1);
  saveStudentProfile();
  parentUnlocked = true;
  updateParentModeUI();
  window.alert(parentPinUpdatedMessage());
  updateParentPinPanel();
}

function forgotParentPinRecovery() {
  if (!guardParentModePanel()) return;
  if (!canRecoverParentPinWithoutOld()) {
    window.alert(
      "忘记密码恢复需在运行 启动.bat 的电脑上进行。\n请打开 http://localhost:8080，在侧栏「家长密码说明」中点「忘记密码 · 本机重设」。",
    );
    return;
  }
  const ok = window.confirm(
    "将直接设置新的家长密码（无需旧密码）。\n仅建议在忘记密码时使用，练习与积分数据不会删除。\n\n是否继续？",
  );
  if (!ok) return;
  promptParentPinChange();
}

function bindParentPinHiddenPath() {
  const onAltClick = (event) => {
    if (!event.altKey) return;
    cumulativeTitleClicks += 1;
    window.clearTimeout(cumulativeTitleClickTimer);
    cumulativeTitleClickTimer = window.setTimeout(() => {
      cumulativeTitleClicks = 0;
    }, 2000);
    if (cumulativeTitleClicks >= 3) {
      cumulativeTitleClicks = 0;
      promptParentPinChange();
    }
  };
  const titleEl = document.getElementById("cumulativePointTitle");
  const countEl = document.getElementById("cumulativePointCount");
  if (titleEl) titleEl.addEventListener("click", onAltClick);
  if (countEl) countEl.addEventListener("click", onAltClick);
}

function migrateStatsOnLoad() {
  if ((stats.redeemedTotal === undefined || stats.redeemedTotal === null) && redeemLogs.length > 0) {
    stats.redeemedTotal = redeemLogs.reduce((sum, row) => sum + (Number(row.cost) || 0), 0);
  }
  syncAccumulatedPoints();
}

function syncAccumulatedPoints() {
  stats.accumulatedPoints = Math.max(
    0,
    (stats.points || 0) + (stats.behaviorPointsTotal || 0) - (stats.redeemedTotal || 0),
  );
  stats.highestAccumulated = Math.max(stats.highestAccumulated || 0, stats.accumulatedPoints || 0);
  stats.highestPoints = Math.max(stats.highestPoints || 0, stats.points || 0);
}

function adjustPracticePoints(delta) {
  stats.points += delta;
  if (stats.points < 0) stats.points = 0;
  syncAccumulatedPoints();
  checkAndGrantBadges();
}

function adjustBehaviorPoints(delta) {
  stats.behaviorPointsTotal = (stats.behaviorPointsTotal || 0) + delta;
  syncAccumulatedPoints();
  checkAndGrantBadges();
}

function handlePracticePoints(category, id, delta) {
  if (hasBeenRewarded(category, id)) {
    return { awarded: false, delta: 0, alreadyRewarded: true };
  }
  if (delta > 0) markRewarded(category, id);
  adjustPracticePoints(delta);
  return { awarded: true, delta, alreadyRewarded: false };
}

function nowText() {
  return new Date().toLocaleString("zh-CN", { hour12: false });
}

function formatDate(dateObj) {
  return dateObj.toISOString().slice(0, 10);
}

function dateKeyFromText(text) {
  const m = String(text || "").match(/(\d{4})[/-](\d{1,2})[/-](\d{1,2})/);
  if (!m) return "";
  const y = m[1];
  const mm = m[2].padStart(2, "0");
  const dd = m[3].padStart(2, "0");
  return `${y}-${mm}-${dd}`;
}

function buildPracticeDateKeys() {
  const set = new Set();
  if (stats.lastPracticeAt) {
    const key = dateKeyFromText(stats.lastPracticeAt);
    if (key) set.add(key);
  }
  challengeLogs.forEach((log) => {
    const key = dateKeyFromText(log.time);
    if (key) set.add(key);
  });
  return [...set].sort();
}

function calculateCurrentStreakDays() {
  const keys = buildPracticeDateKeys();
  if (keys.length === 0) return 0;
  const keySet = new Set(keys);
  let cursor = new Date();
  let streak = 0;
  while (true) {
    const key = formatDate(cursor);
    if (!keySet.has(key)) {
      if (streak === 0) {
        cursor.setDate(cursor.getDate() - 1);
        const yesterday = formatDate(cursor);
        if (!keySet.has(yesterday)) return 0;
        streak += 1;
      } else break;
    } else {
      streak += 1;
    }
    cursor.setDate(cursor.getDate() - 1);
  }
  return streak;
}

function addWrongBookItem(moduleName, prompt, answer, unit) {
  const resolvedUnit = unit ?? resolveCurrentUnit() ?? 0;
  const existingIndex = wrongBookItems.findIndex((item) => item.module === moduleName && item.prompt === prompt);
  if (existingIndex >= 0) wrongBookItems.splice(existingIndex, 1);
  wrongBookItems.unshift({
    time: nowText(),
    module: moduleName,
    prompt,
    answer,
    unit: resolvedUnit,
  });
  wrongBookItems = wrongBookItems.slice(0, 300);
  saveWrongBookItems();
  if (elements.wrongItemList) renderWrongBookItems();
  renderWrongBookPanel();
  updateWrongBookStatus();
}

function getWrongBookModules() {
  return [...new Set(wrongBookItems.map((item) => item.module))].sort();
}

function getFilteredWrongBookItems() {
  const moduleFilter = elements.wrongBookModuleFilter?.value || "all";
  const unitFilter = elements.wrongBookUnitFilter?.value || "all";
  return wrongBookItems.filter((item) => {
    const okModule = moduleFilter === "all" || item.module === moduleFilter;
    const okUnit = unitFilter === "all" || String(item.unit ?? 0) === unitFilter;
    return okModule && okUnit;
  });
}

function resolveCurrentUnit() {
  const activePanel = document.querySelector(".panel.active");
  if (!activePanel) return 0;
  if (activePanel.id === "flashcards" && filteredCards.length > 0) return filteredCards[cardIndex]?.unit ?? 0;
  if (activePanel.id === "grammar") {
    if (filteredGrammarPoints.length > 0) return filteredGrammarPoints[grammarIndex]?.unit ?? 0;
    if (filteredSvoExercises.length > 0) return filteredSvoExercises[svoIndex]?.unit ?? 0;
  }
  if (activePanel.id === "phrases" && filteredPhrases.length > 0) return filteredPhrases[phraseIndex]?.unit ?? 0;
  if (activePanel.id === "quiz" && currentQuiz) return currentQuiz.unit ?? 0;
  if (activePanel.id === "verbs" && filteredVerbTriples.length > 0) return filteredVerbTriples[verbIndex]?.unit ?? 0;
  if (activePanel.id === "writing" && filteredWritingSamples.length > 0) return filteredWritingSamples[writingIndex]?.unit ?? 0;
  if (activePanel.id === "fillblank" && currentFillQuestions?.length) return currentFillQuestions[0]?.unit ?? 0;
  return Number(elements.journalUnitFilter?.value) || 0;
}

function renderWrongBookItems() {
  const items = getFilteredWrongBookItems().slice(0, 40);
  if (items.length === 0) {
    elements.wrongItemList.textContent = "暂无错题";
    return;
  }
  elements.wrongItemList.innerHTML = items
    .map((item) => `<div>${item.time} | ${item.module} | ${item.prompt} | 正解: ${item.answer}</div>`)
    .join("");
}

function renderWrongBookPanel() {
  if (!elements.wrongBookPanelList) return;
  const items = getFilteredWrongBookItems();
  if (elements.wrongBookPanelSummary) {
    elements.wrongBookPanelSummary.textContent = `共 ${wrongBookItems.length} 条错题${items.length !== wrongBookItems.length ? `（当前筛选 ${items.length} 条）` : ""}`;
  }
  if (items.length === 0) {
    elements.wrongBookPanelList.textContent = "暂无错题，答错后会自动收录到此处。";
    return;
  }
  elements.wrongBookPanelList.innerHTML = items
    .map((item, idx) => `<article class="wrong-book-item"><p><strong>#${idx + 1}</strong> <span class="wrong-module-tag">${item.module}</span> <span class="wrong-module-tag">U${item.unit ?? 0}</span> <span class="wrong-time">${item.time}</span></p><p class="wrong-prompt">${item.prompt}</p><p class="wrong-answer">正解：${item.answer}</p></article>`)
    .join("");
  populateWrongBookModuleFilter();
}

function populateWrongBookModuleFilter() {
  if (!elements.wrongBookModuleFilter) return;
  const current = elements.wrongBookModuleFilter.value || "all";
  const modules = getWrongBookModules();
  const options = ['<option value="all">全部模块</option>']
    .concat(modules.map((m) => `<option value="${m}">${m}</option>`));
  elements.wrongBookModuleFilter.innerHTML = options.join("");
  if (current === "all" || modules.includes(current)) {
    elements.wrongBookModuleFilter.value = current;
  } else {
    elements.wrongBookModuleFilter.value = "all";
  }
}

function getCurrentManualWrongContext() {
  const activePanel = document.querySelector(".panel.active");
  if (!activePanel) return null;
  if (activePanel.id === "flashcards" && filteredCards.length > 0) {
    const card = filteredCards[cardIndex];
    return {
      module: "单词卡片",
      prompt: card.front,
      answer: `${card.zh || ""}${card.example ? ` | 例句: ${card.example}` : ""}`.trim(),
      unit: card.unit,
    };
  }
  if (activePanel.id === "phrases" && filteredPhrases.length > 0) {
    const phrase = filteredPhrases[phraseIndex];
    return { module: "常用语", prompt: phrase.en, answer: phrase.zh, unit: phrase.unit };
  }
  if (activePanel.id === "quiz" && currentQuiz) {
    return { module: "选择题", prompt: currentQuiz.prompt, answer: currentQuiz.answer, unit: currentQuiz.unit };
  }
  if (activePanel.id === "verbs" && filteredVerbTriples.length > 0) {
    const verb = filteredVerbTriples[verbIndex];
    return { module: "动词专项", prompt: verb.fillPrompt, answer: verb.fillAnswer, unit: verb.unit };
  }
  if (activePanel.id === "writing" && filteredWritingSamples.length > 0) {
    const sample = filteredWritingSamples[writingIndex];
    return { module: "作文填空", prompt: sample.fillPrompt, answer: sample.fillAnswer };
  }
  return { module: "手动记录", prompt: "家长标记为答错（未定位到具体题目）", answer: "-" };
}

function startWrongVocabReview() {
  const fronts = new Set(
    wrongBookItems.filter((item) => item.module === "单词卡片").map((item) => item.prompt),
  );
  if (fronts.size === 0) {
    window.alert("错题本中暂无单词卡片错题。");
    return;
  }
  filteredCards = vocabularyCards.filter((card) => fronts.has(card.front));
  cardIndex = 0;
  elements.unitFilter.value = "all";
  setActiveTab("flashcards");
  renderCard();
}

function startWrongQuizReview() {
  if (wrongQuizIds.length === 0 && !wrongBookItems.some((item) => item.module === "选择题")) {
    window.alert("错题本中暂无选择题错题。");
    return;
  }
  wrongBookMode = true;
  setActiveTab("quiz");
  refreshQuizWithFilters();
}

function updateLeaderboard() {
  const accuracy = stats.attempts === 0 ? 0 : Math.round((stats.correct / stats.attempts) * 100);
  const streakDays = calculateCurrentStreakDays();
  const existing = leaderboard.find((row) => row.nickname === studentProfile.nickname);
  const payload = {
    nickname: studentProfile.nickname,
    bestPoints: Math.max(stats.highestAccumulated || 0, stats.accumulatedPoints || 0),
    bestAccuracy: accuracy,
    bestStreakDays: streakDays,
    updatedAt: nowText(),
  };
  if (!existing) leaderboard.push(payload);
  else {
    existing.bestPoints = Math.max(existing.bestPoints, payload.bestPoints);
    existing.bestAccuracy = Math.max(existing.bestAccuracy, payload.bestAccuracy);
    existing.bestStreakDays = Math.max(existing.bestStreakDays || 0, payload.bestStreakDays);
    existing.updatedAt = payload.updatedAt;
  }
  saveLeaderboard();
}

function renderLeaderboard() {
  const mode = elements.leaderboardSort?.value || "points";
  const sorter = {
    points: (a, b) => (b.bestPoints - a.bestPoints) || (b.bestAccuracy - a.bestAccuracy) || ((b.bestStreakDays || 0) - (a.bestStreakDays || 0)),
    accuracy: (a, b) => (b.bestAccuracy - a.bestAccuracy) || (b.bestPoints - a.bestPoints) || ((b.bestStreakDays || 0) - (a.bestStreakDays || 0)),
    streak: (a, b) => ((b.bestStreakDays || 0) - (a.bestStreakDays || 0)) || (b.bestPoints - a.bestPoints) || (b.bestAccuracy - a.bestAccuracy),
  }[mode];
  const top3 = [...leaderboard]
    .sort(sorter)
    .slice(0, 3);
  if (top3.length === 0) {
    elements.leaderboardList.textContent = "暂无排行数据";
    return;
  }
  elements.leaderboardList.innerHTML = top3
    .map((row, idx) => `<div>#${idx + 1} ${row.nickname} | 最佳积分 ${row.bestPoints} | 最佳正确率 ${row.bestAccuracy}% | 连续打卡 ${row.bestStreakDays || 0} 天 | ${row.updatedAt}</div>`)
    .join("");
}

function populateBehaviorActions() {
  elements.behaviorActionSelect.innerHTML = behaviorActions
    .map((item) => `<option value="${item.id}">${item.label}</option>`)
    .join("");
}

function applyBehaviorAction() {
  requireParentAuth(() => {
    const selectedId = elements.behaviorActionSelect.value;
    const action = behaviorActions.find((item) => item.id === selectedId);
    if (!action) return;
    adjustBehaviorPoints(action.points);
    markPractice();
    behaviorLogs.unshift({ time: nowText(), ...action });
    behaviorLogs = behaviorLogs.slice(0, 500);
    saveBehaviorLogs();
    addChallengeLog("行为积分", action.label, action.points);
    if (action.points > 0) showSuccessFx();
    else showFailFx();
    saveStats();
    updateDashboard();
    renderChallengeLogs();
    renderBadgeList();
    renderCharts();
  });
}

function applyCompoundInterestIfNeeded() {
  const today = formatDate(new Date());
  const lastDate = stats.lastCompoundDate || today;
  if (!stats.lastCompoundDate) {
    stats.lastCompoundDate = today;
    saveStats();
    return;
  }
  if (today <= lastDate) return;
  const last = new Date(`${lastDate}T00:00:00`);
  const now = new Date(`${today}T00:00:00`);
  const days = Math.max(0, Math.floor((now - last) / 86400000));
  if (days === 0 || stats.points <= 0) {
    stats.lastCompoundDate = today;
    saveStats();
    return;
  }
  if (stats.lastSpendDate && stats.lastSpendDate >= lastDate) {
    stats.lastCompoundDate = today;
    saveStats();
    return;
  }
  const bonus = Math.floor(stats.points * (Math.pow(1.001, days) - 1));
  if (bonus > 0) {
    adjustPracticePoints(bonus);
    addChallengeLog("复利奖励", `每日千分之一 × ${days}天`, bonus);
  }
  stats.lastCompoundDate = today;
  saveStats();
}

function checkAndGrantBadges() {
  const addBadge = (id, name) => {
    if (badges.some((b) => b.id === id)) return;
    badges.push({ id, name, earnedAt: nowText() });
  };
  if (stats.accumulatedPoints >= 300) addBadge("start_star", "🚀起步之星");
  if (stats.accumulatedPoints >= 800) addBadge("growth_master", "🏆成长达人");
  if (stats.accumulatedPoints >= 1500) addBadge("wealth_guard", "💎理财小能手");

  const washLogs = behaviorLogs.filter((l) => l.id === "wash_tidy").slice(0, 7);
  const daySet = new Set(washLogs.map((l) => l.time.slice(0, 10)));
  if (daySet.size >= 3) addBadge("tooth_guard", "🪥洁牙卫士");
  if (daySet.size >= 5) addBadge("habit_king", "🌟习惯王者");
  saveBadges();
}

function renderBadgeList() {
  if (badges.length === 0) {
    elements.badgeList.textContent = "暂无勋章";
    return;
  }
  elements.badgeList.innerHTML = badges
    .map((b) => `<span class="badge-chip">${b.name} (${b.earnedAt.slice(0, 10)})</span>`)
    .join(" ");
}

function renderCharts() {
  // 用户要求最终版移除积分趋势图和消费饼图。
}

function downloadTextFile(filename, content, mimeType = "text/plain") {
  const blob = new Blob([content], { type: `${mimeType};charset=utf-8` });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function exportLearningReport() {
  const accuracy = stats.attempts === 0 ? 0 : Math.round((stats.correct / stats.attempts) * 100);
  const lines = [
    `学生昵称: ${studentProfile.nickname}`,
    `导出时间: ${nowText()}`,
    `答对: ${stats.correct}`,
    `答错: ${stats.wrong}`,
    `总答题: ${stats.attempts}`,
    `正确率: ${accuracy}%`,
    `做题积分: ${stats.points}`,
    `行为积分: ${stats.behaviorPointsTotal || 0}`,
    `已兑换: ${stats.redeemedTotal || 0}`,
    `累积积分: ${stats.accumulatedPoints || 0}`,
    `错题本数量: ${wrongBookItems.length}`,
    "",
    "=== 最近挑战记录 ===",
    ...challengeLogs.slice(0, 50).map((i) => `${i.time} | ${i.item} | ${i.result} | ${i.pointDelta}`),
    "",
    "=== 兑换记录 ===",
    ...redeemLogs.slice(0, 50).map((i) => `${i.time} | ${i.name} | ${i.cost}`),
    "",
    "=== 错题本 ===",
    ...wrongBookItems.slice(0, 80).map((i) => `${i.time} | ${i.module} | ${i.prompt} | ${i.answer}`),
    "",
    "=== 学习日志 ===",
    ...journalEntries.map((i) => `${i.date} | ${i.text}`),
  ];
  downloadTextFile(`学习报告_${studentProfile.nickname}_${todayKey()}.txt`, lines.join("\n"));
  elements.exportFeedback.textContent = "学习报告已导出（TXT）。";
}

function exportPrintableHtmlReport() {
  const accuracy = stats.attempts === 0 ? 0 : Math.round((stats.correct / stats.attempts) * 100);
  const topRows = [...leaderboard]
    .sort((a, b) => (b.bestPoints - a.bestPoints) || (b.bestAccuracy - a.bestAccuracy) || ((b.bestStreakDays || 0) - (a.bestStreakDays || 0)))
    .slice(0, 3)
    .map((r, idx) => `<tr><td>${idx + 1}</td><td>${r.nickname}</td><td>${r.bestPoints}</td><td>${r.bestAccuracy}%</td><td>${r.bestStreakDays || 0}</td></tr>`)
    .join("");

  const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>学习总报告 - ${studentProfile.nickname}</title>
  <style>
    body { font-family: "Microsoft YaHei", Arial, sans-serif; color: #1f2b56; margin: 24px; }
    h1, h2 { margin: 0 0 10px; }
    .muted { color: #5d6f9a; margin-bottom: 16px; }
    .card { border: 1px solid #d6dff9; border-radius: 12px; padding: 14px; margin-bottom: 14px; }
    .grid { display: grid; grid-template-columns: repeat(4, minmax(120px, 1fr)); gap: 10px; }
    .kpi { background: #f6f8ff; border-radius: 10px; padding: 10px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #dbe3fb; padding: 8px; text-align: left; font-size: 14px; }
    th { background: #edf2ff; }
    .chart { width: 100%; border: 1px solid #dbe3fb; border-radius: 12px; margin-top: 8px; }
    .small { font-size: 13px; color: #5d6f9a; }
    @media print { body { margin: 8mm; } .card { break-inside: avoid; } }
  </style>
</head>
<body>
  <h1>新人教PEP六年上英语学习训练营 - 学习总报告</h1>
  <p class="muted">学生：${studentProfile.nickname} | 导出时间：${nowText()}</p>

  <section class="card">
    <h2>学习概览</h2>
    <div class="grid">
      <div class="kpi">答对：${stats.correct}</div>
      <div class="kpi">答错：${stats.wrong}</div>
      <div class="kpi">总答题：${stats.attempts}</div>
      <div class="kpi">正确率：${accuracy}%</div>
      <div class="kpi">做题积分：${stats.points}</div>
      <div class="kpi">行为积分：${stats.behaviorPointsTotal || 0}</div>
      <div class="kpi">已兑换：${stats.redeemedTotal || 0}</div>
      <div class="kpi highlight">累积积分：${stats.accumulatedPoints || 0}</div>
      <div class="kpi">连续打卡：${calculateCurrentStreakDays()} 天</div>
      <div class="kpi">错题本：${wrongBookItems.length} 条</div>
    </div>
  </section>

  <section class="card">
    <h2>排行榜 Top 3</h2>
    <table>
      <thead><tr><th>名次</th><th>昵称</th><th>最高积分</th><th>最高正确率</th><th>连续打卡天数</th></tr></thead>
      <tbody>${topRows || `<tr><td colspan="5">暂无排行数据</td></tr>`}</tbody>
    </table>
  </section>

  <section class="card">
    <h2>最近挑战记录（前20条）</h2>
    <table>
      <thead><tr><th>时间</th><th>项目</th><th>结果</th><th>积分变化</th></tr></thead>
      <tbody>
        ${(challengeLogs.slice(0, 20).map((i) => `<tr><td>${i.time}</td><td>${i.item}</td><td>${i.result}</td><td>${i.pointDelta}</td></tr>`).join("")) || `<tr><td colspan="4">暂无记录</td></tr>`}
      </tbody>
    </table>
  </section>
</body>
</html>`;

  downloadTextFile(`学习总报告_${studentProfile.nickname}_${todayKey()}.html`, html, "text/html");
  elements.exportFeedback.textContent = "学习总报告已导出（HTML，可直接打印）。";
}

function buildPointLedgerEntries() {
  const entries = [];
  challengeLogs.forEach((log) => {
    if (!log.pointDelta) return;
    entries.push({
      time: log.time,
      flow: log.pointDelta > 0 ? "earn" : "spend",
      category: "练习挑战",
      name: log.item,
      detail: log.result,
      points: log.pointDelta,
    });
  });
  behaviorLogs.forEach((log) => {
    entries.push({
      time: log.time,
      flow: log.points > 0 ? "earn" : "spend",
      category: "行为积分",
      name: log.label,
      detail: log.category === "good" ? "良好行为" : "待改进行为",
      points: log.points,
    });
  });
  redeemLogs.forEach((log) => {
    entries.push({
      time: log.time,
      flow: "spend",
      category: "积分兑换",
      name: log.name,
      detail: "兑换消费",
      points: -Math.abs(log.cost),
    });
  });
  return entries.sort((a, b) => String(b.time).localeCompare(String(a.time)));
}

function exportPointsLedgerHtml() {
  const entries = buildPointLedgerEntries();
  const totalEarned = entries.filter((e) => e.points > 0).reduce((s, e) => s + e.points, 0);
  const totalSpent = entries.filter((e) => e.points < 0).reduce((s, e) => s + Math.abs(e.points), 0);
  const earnRows = entries
    .filter((e) => e.points > 0)
    .map((e) => `<tr><td>${e.time}</td><td>${e.category}</td><td>${e.name}</td><td>${e.detail}</td><td class="earn">+${e.points}</td></tr>`)
    .join("");
  const spendRows = entries
    .filter((e) => e.points < 0)
    .map((e) => `<tr><td>${e.time}</td><td>${e.category}</td><td>${e.name}</td><td>${e.detail}</td><td class="spend">${e.points}</td></tr>`)
    .join("");

  const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>积分台账 - ${studentProfile.nickname}</title>
  <style>
    body { font-family: "Microsoft YaHei", Arial, sans-serif; color: #1f2b56; margin: 24px; }
    h1, h2 { margin: 0 0 10px; }
    .muted { color: #5d6f9a; margin-bottom: 16px; }
    .card { border: 1px solid #d6dff9; border-radius: 12px; padding: 14px; margin-bottom: 14px; }
    .grid { display: grid; grid-template-columns: repeat(4, minmax(120px, 1fr)); gap: 10px; }
    .kpi { background: #f6f8ff; border-radius: 10px; padding: 10px; font-weight: 700; }
    .kpi.highlight { background: linear-gradient(180deg, #f8f0ff 0%, #efe2ff 100%); border: 1px solid #b896ff; }
    table { width: 100%; border-collapse: collapse; margin-top: 8px; }
    th, td { border: 1px solid #dbe3fb; padding: 8px; text-align: left; font-size: 14px; }
    th { background: #edf2ff; }
    .earn { color: #16a34a; font-weight: 800; }
    .spend { color: #dc2626; font-weight: 800; }
    @media print { body { margin: 8mm; } .card { break-inside: avoid; } }
  </style>
</head>
<body>
  <h1>积分获取与消费总报告</h1>
  <p class="muted">学生：${studentProfile.nickname} | 导出时间：${nowText()} | 旭日长空光照人生出品</p>

  <section class="card">
    <h2>积分概览</h2>
    <div class="grid">
      <div class="kpi">做题积分：${stats.points}</div>
      <div class="kpi">行为积分：${stats.behaviorPointsTotal || 0}</div>
      <div class="kpi">已兑换：${stats.redeemedTotal || 0}</div>
      <div class="kpi highlight">累积积分：${stats.accumulatedPoints || 0}</div>
      <div class="kpi earn">流水获得合计：+${totalEarned}</div>
      <div class="kpi spend">流水消费合计：-${totalSpent}</div>
    </div>
    <p class="muted">说明：累积积分 = 做题积分 + 行为积分 - 已兑换；兑换仅扣减累积积分。</p>
  </section>

  <section class="card">
    <h2>积分获取明细</h2>
    <table>
      <thead><tr><th>时间</th><th>类型</th><th>项目</th><th>说明</th><th>积分</th></tr></thead>
      <tbody>${earnRows || `<tr><td colspan="5">暂无获取记录</td></tr>`}</tbody>
    </table>
  </section>

  <section class="card">
    <h2>积分消费明细</h2>
    <table>
      <thead><tr><th>时间</th><th>类型</th><th>项目</th><th>说明</th><th>积分</th></tr></thead>
      <tbody>${spendRows || `<tr><td colspan="5">暂无消费记录</td></tr>`}</tbody>
    </table>
  </section>
</body>
</html>`;

  downloadTextFile(`积分台账_${studentProfile.nickname}_${todayKey()}.html`, html, "text/html");
  elements.exportFeedback.textContent = "积分台账已导出（HTML，含获取与消费明细）。";
}

function updateDashboard() {
  elements.correctCount.textContent = String(stats.correct);
  elements.wrongCount.textContent = String(stats.wrong);
  elements.attemptCount.textContent = String(stats.attempts);
  const accuracy = stats.attempts === 0 ? 0 : Math.round((stats.correct / stats.attempts) * 100);
  elements.accuracy.textContent = `${accuracy}%`;
  elements.pointCount.textContent = String(stats.points);
  elements.cumulativePointCount.textContent = String(stats.accumulatedPoints || 0);
  if (elements.pointsBreakdown) {
    elements.pointsBreakdown.textContent = `累积 = 做题 ${stats.points} + 行为 ${stats.behaviorPointsTotal || 0} - 兑换 ${stats.redeemedTotal || 0}`;
  }
  elements.wrongBookCount.textContent = String(wrongBookItems.length);
  elements.nicknameDisplay.textContent = `学生昵称：${studentProfile.nickname}`;
  elements.lastPracticeTime.textContent = `最近练习时间：${stats.lastPracticeAt || "暂无"}`;
  syncNicknameInputs();
  updateLeaderboard();
  renderLeaderboard();
  renderCharts();
}

function setActiveTab(tabName) {
  elements.tabs.forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.tab === tabName);
  });
  elements.panels.forEach((panel) => {
    panel.classList.toggle("active", panel.id === tabName);
  });
  if (tabName === "wrongbook") renderWrongBookPanel();
  if (tabName === "gratitude" && window.GratitudeHub) window.GratitudeHub.onTabActivate();
}

function renderCard() {
  if (filteredCards.length === 0) {
    elements.cardCategory.textContent = "暂无数据";
    elements.cardFront.textContent = "请切换单元";
    elements.cardPhonetic.textContent = "";
    elements.cardZh.textContent = "当前筛选没有单词。";
    elements.cardExample.textContent = "";
    elements.cardExampleZh.textContent = "";
    elements.cardImage.classList.add("hidden");
    return;
  }
  const card = filteredCards[cardIndex];
  elements.cardCategory.textContent = `${unitMeta[card.unit]} · ${card.category}`;
  elements.cardFront.textContent = card.front;
  elements.cardPhonetic.textContent = card.ipa || "";
  elements.cardZh.textContent = card.zh || "";
  elements.cardExample.textContent = card.example ? `例句: ${card.example}` : "";
  elements.cardExampleZh.textContent = card.exampleZh ? `翻译: ${card.exampleZh}` : "";
  const imageSrc = card.image || unitLocalImage[card.unit];
  if (imageSrc) {
    const preview = new Image();
    preview.onload = () => {
      elements.cardImage.src = imageSrc;
      elements.cardImage.classList.remove("hidden");
    };
    preview.onerror = () => {
      elements.cardImage.classList.add("hidden");
      elements.cardImage.removeAttribute("src");
    };
    preview.src = imageSrc;
  } else {
    elements.cardImage.classList.add("hidden");
    elements.cardImage.removeAttribute("src");
  }
  cardFlipped = false;
  elements.cardBack.classList.add("hidden");
}

function markPractice() {
  stats.lastPracticeAt = nowText();
}

function addChallengeLog(item, result, pointDelta) {
  challengeLogs.unshift({
    time: nowText(),
    item,
    result,
    pointDelta,
  });
  challengeLogs = challengeLogs.slice(0, 200);
  saveChallengeLogs();
}

function renderChallengeLogs() {
  if (challengeLogs.length === 0) {
    elements.challengeList.textContent = "暂无挑战记录";
    return;
  }
  elements.challengeList.innerHTML = challengeLogs
    .slice(0, 4)
    .map((log) => `<div>${log.time} | ${log.item} | ${log.result} | 积分变化 ${log.pointDelta > 0 ? "+" : ""}${log.pointDelta}</div>`)
    .join("");
}

function renderRedeemLogs() {
  if (redeemLogs.length === 0) {
    elements.redeemList.textContent = "暂无兑换记录";
    return;
  }
  elements.redeemList.innerHTML = redeemLogs
    .slice(0, 40)
    .map((log) => `<div>${log.time} | 兑换：${log.name} | 消耗 ${log.cost} 积分</div>`)
    .join("");
}

function redeemPointsRecord() {
  const name = elements.redeemName.value.trim();
  const cost = Number(elements.redeemCost.value || 0);
  if (!name || cost <= 0) {
    addChallengeLog("积分兑换", "失败（信息不完整）", 0);
    renderChallengeLogs();
    return;
  }
  if ((stats.accumulatedPoints || 0) <= 0) {
    window.alert("累积积分为 0，无法兑换。");
    addChallengeLog("积分兑换", "失败（累积积分为0）", 0);
    renderChallengeLogs();
    return;
  }
  if ((stats.accumulatedPoints || 0) < cost) {
    window.alert("累积积分不足，无法兑换。");
    addChallengeLog("积分兑换", "失败（累积积分不足）", 0);
    renderChallengeLogs();
    return;
  }
  stats.redeemedTotal = (stats.redeemedTotal || 0) + cost;
  stats.lastSpendDate = todayKey();
  syncAccumulatedPoints();
  markPractice();
  redeemLogs.unshift({ time: nowText(), name, cost });
  redeemLogs = redeemLogs.slice(0, 200);
  saveRedeemLogs();
  saveStats();
  addChallengeLog("积分兑换", "成功", -cost);
  elements.redeemName.value = "";
  elements.redeemCost.value = "";
  updateDashboard();
  renderRedeemLogs();
  renderChallengeLogs();
  renderCharts();
}

function isMobileDevice() {
  return window.matchMedia("(max-width: 760px)").matches || /Mobile|Android|iPhone|iPad|iPod/i.test(navigator.userAgent || "");
}

function syncNicknameInputs() {
  const nick = studentProfile.nickname && studentProfile.nickname !== "同学" ? studentProfile.nickname : "";
  if (elements.nicknameInput) elements.nicknameInput.value = nick;
  if (elements.mobileNicknameInput) elements.mobileNicknameInput.value = nick;
}

function saveNicknameFromInput(rawNickname) {
  const nickname = String(rawNickname || "").trim();
  if (!nickname) return false;
  if (elements.nicknameInput) elements.nicknameInput.value = nickname;
  if (elements.mobileNicknameInput) elements.mobileNicknameInput.value = nickname;
  studentProfile.nickname = nickname;
  saveStudentProfile();
  window.localStorage.setItem(LAN_SYNC_KEY, nickname);
  updateDashboard();
  scheduleLanSync(true);
  if (!studentProfile.parentPinHash) {
    window.setTimeout(() => promptParentPinSetup(), 200);
  }
  return true;
}

function saveNickname() {
  const nickname = elements.nicknameInput?.value?.trim() || elements.mobileNicknameInput?.value?.trim() || "";
  saveNicknameFromInput(nickname);
}

function getDashboardResetAt() {
  return window.localStorage.getItem(DASHBOARD_RESET_AT_KEY) || "";
}

function setDashboardResetAt(iso) {
  if (iso) window.localStorage.setItem(DASHBOARD_RESET_AT_KEY, iso);
  else window.localStorage.removeItem(DASHBOARD_RESET_AT_KEY);
}

function performResetDashboardStats() {
  const resetAt = new Date().toISOString();
  stats = {
    correct: 0,
    wrong: 0,
    attempts: 0,
    points: 0,
    highestPoints: 0,
    highestAccumulated: 0,
    accumulatedPoints: 0,
    behaviorPointsTotal: 0,
    redeemedTotal: 0,
    lastPracticeAt: "",
    lastCompoundDate: "",
    lastSpendDate: "",
  };
  wrongQuizIds = [];
  wrongBookItems = [];
  wrongBookMode = false;
  rewarded = { quiz: [], writing: [], fillblank: [], svo: [], verb: [] };
  challengeLogs = [];
  behaviorLogs = [];
  redeemLogs = [];
  badges = [];
  const nick = studentProfile.nickname;
  leaderboard = leaderboard.map((row) => {
    if (row.nickname !== nick) return row;
    return {
      ...row,
      bestPoints: 0,
      bestAccuracy: 0,
      bestStreakDays: 0,
      updatedAt: nowText(),
    };
  });
  setDashboardResetAt(resetAt);
  syncAccumulatedPoints();
  saveStats();
  saveWrongQuizIds();
  saveWrongBookItems();
  saveRewarded();
  saveChallengeLogs();
  saveBehaviorLogs();
  saveRedeemLogs();
  saveBadges();
  saveLeaderboard();
  touchDataUpdatedAt();
  refreshQuizWithFilters();
  updateDashboard();
  renderWrongBookItems();
  renderWrongBookPanel();
  updateWrongBookStatus();
  renderChallengeLogs();
  renderRedeemLogs();
  renderBadgeList();
  renderCharts();
  if (typeof scheduleLanSync === "function") scheduleLanSync(true);
}

/** @deprecated use performResetDashboardStats */
function performResetAllData() {
  performResetDashboardStats();
}

function resetAllData() {
  if (!studentProfile.parentPinHash) {
    window.alert("尚未设置家长密码，无法执行一键重置。");
    return;
  }
  requireParentPasswordAlways(() => {
    const ok = window.confirm(
      "此操作将清零首页全部练习统计（答对/答错/总作答/正确率/做题积分/累积积分/错题本及相关积分流水），不会删除课文讲读、知识点精讲及题库内容。是否继续？",
    );
    if (!ok) return;
    requireParentPasswordAlways(() => {
      performResetDashboardStats();
    }, "请再次输入家长密码以确认一键重置：");
  }, "请输入家长密码以开始一键重置：");
}

function markManualAnswerCorrect() {
  requireParentAuth(() => {
    stats.attempts += 1;
    stats.correct += 1;
    adjustPracticePoints(POINT_REWARD);
    markPractice();
    addChallengeLog("手动记录", "回答正确", POINT_REWARD);
    saveStats();
    updateDashboard();
    renderChallengeLogs();
    showSuccessFx();
  });
}

function markManualAnswerWrong() {
  requireParentAuth(() => {
    const ctx = getCurrentManualWrongContext();
    if (ctx) addWrongBookItem(ctx.module, ctx.prompt, ctx.answer, ctx.unit);
    if (ctx?.module === "选择题" && currentQuiz && !wrongQuizIds.includes(currentQuiz.id)) {
      wrongQuizIds.push(currentQuiz.id);
      saveWrongQuizIds();
      updateWrongBookStatus();
    }
    stats.attempts += 1;
    stats.wrong += 1;
    markPractice();
    addChallengeLog("手动记录", ctx ? `${ctx.module}答错` : "回答错误", 0);
    saveStats();
    updateDashboard();
    renderChallengeLogs();
    showFailFx();
  });
}

function clearFxLayerLater() {
  window.setTimeout(() => {
    elements.fxLayer.innerHTML = "";
  }, 1400);
}

function showSuccessFx() {
  const colors = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff", "#ff8fab", "#72ddf7"];
  for (let i = 0; i < 120; i += 1) {
    const piece = document.createElement("span");
    piece.className = "fx-confetti";
    piece.style.left = `${Math.random() * 100}%`;
    piece.style.background = colors[Math.floor(Math.random() * colors.length)];
    piece.style.animationDelay = `${Math.random() * 220}ms`;
    elements.fxLayer.appendChild(piece);
  }
  clearFxLayerLater();
}

function showFailFx() {
  const emojis = ["😞", "😢", "😭", "🙁", "😔"];
  for (let i = 0; i < 28; i += 1) {
    const item = document.createElement("span");
    item.className = "fx-sad";
    item.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    item.style.left = `${Math.random() * 95}%`;
    item.style.animationDelay = `${Math.random() * 160}ms`;
    elements.fxLayer.appendChild(item);
  }
  clearFxLayerLater();
}

function toggleCardFlip() {
  cardFlipped = !cardFlipped;
  elements.cardBack.classList.toggle("hidden", !cardFlipped);
}

function nextCard(step) {
  const total = filteredCards.length;
  if (total === 0) return;
  cardIndex = (cardIndex + step + total) % total;
  renderCard();
}

function clampIndex(index, length) {
  if (length <= 0) return 0;
  return Math.min(Math.max(0, index), length - 1);
}

function updateUnitFilter(resetIndex = true) {
  const unitValue = elements.unitFilter.value;
  filteredCards = unitValue === "all" ? [...vocabularyCards] : vocabularyCards.filter((item) => String(item.unit) === unitValue);
  if (resetIndex) cardIndex = 0;
  else cardIndex = clampIndex(cardIndex, filteredCards.length);
  renderCard();
}

function updateWrongBookStatus() {
  const totalWrong = wrongBookItems.length;
  const modeText = wrongBookMode ? "当前模式：错题本复习" : "当前模式：普通刷题";
  elements.wrongBookStatus.textContent = `${modeText} | 错题数量：${totalWrong}`;
  elements.startWrongBook.textContent = wrongBookMode ? "退出错题本" : "错题本复习";
  elements.wrongBookCount.textContent = String(totalWrong);
  updateTabCounts();
}

function getAppendixItemCount() {
  let total = 0;
  appendixUnits.forEach((unit) => {
    total += unit.partAVocab.length + unit.partBVocab.length;
    total += unit.partAPhrases.length + unit.partBPhrases.length;
    total += unit.partASentences.length + unit.partBSentences.length;
  });
  return total;
}

function updateTabCounts() {
  const counts = {
    flashcards: vocabularyCards.length,
    grammar: grammarPoints.length + svoExercises.length,
    phrases: commonPhrases.length,
    quiz: quizzes.length,
    fillblank: fillBlankBank.length,
    verbs: verbTriples.length,
    writing: writingSamples.length,
    appendix: getAppendixItemCount(),
    journal: journalEntries.length,
    gratitude: window.GratitudeHub ? window.GratitudeHub.getEntryCount() : 0,
    wrongbook: wrongBookItems.length,
  };
  elements.tabs.forEach((tab) => {
    const key = tab.dataset.tab;
    const countEl = tab.querySelector(".tab-count");
    if (!countEl || counts[key] === undefined) return;
    countEl.textContent = String(counts[key]);
    if (key === "wrongbook") {
      tab.classList.toggle("tab-wrongbook-has-items", wrongBookItems.length > 0);
      countEl.setAttribute("aria-label", `错题数量 ${counts[key]}`);
    }
  });
}

function randomFrom(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function shuffle(array) {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function displayQuiz(quiz, options = {}) {
  currentQuiz = quiz;
  const modeTag = wrongBookMode ? "错题本" : "闯关";
  elements.quizBadge.textContent = `${modeTag} | ${currentQuiz.badge}`;
  elements.quizPrompt.textContent = currentQuiz.prompt;
  if (!options.keepFeedback) {
    elements.quizFeedback.textContent = "";
    elements.quizAnalysis.textContent = "请选择一个选项，我会给你详细解析。";
    elements.quizAnalysis.style.color = "#55627a";
  }
  elements.quizOptions.innerHTML = "";

  const optionOrder = options.reshuffleOptions === false && quiz._optionOrder
    ? quiz._optionOrder
    : shuffle(currentQuiz.options);
  quiz._optionOrder = optionOrder;

  optionOrder.forEach((option) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "secondary-btn option-btn";
    button.textContent = option;
    button.addEventListener("click", () => handleQuizAnswer(option));
    elements.quizOptions.appendChild(button);
  });
}

function renderQuiz(options = {}) {
  const forceNew = options.forceNew === true;
  if (filteredQuizzes.length === 0) {
    currentQuiz = null;
    elements.quizBadge.textContent = wrongBookMode ? "错题本暂无可练习题目" : "当前筛选暂无题目";
    elements.quizPrompt.textContent = "请调整 Unit / Part 筛选，或先做一些题生成错题本。";
    elements.quizFeedback.textContent = "";
    elements.quizAnalysis.textContent = "";
    elements.quizOptions.innerHTML = "";
    return;
  }

  if (!forceNew && currentQuiz && filteredQuizzes.some((item) => item.id === currentQuiz.id)) {
    displayQuiz(currentQuiz, { reshuffleOptions: false, keepFeedback: true });
    return;
  }

  displayQuiz(randomFrom(filteredQuizzes), { reshuffleOptions: true });
}

function handleQuizAnswer(option) {
  if (!currentQuiz) return;
  stats.attempts += 1;
  const quizId = currentQuiz.id;
  if (option === currentQuiz.answer) {
    stats.correct += 1;
    const pointResult = handlePracticePoints("quiz", quizId, POINT_REWARD);
    markPractice();
    addChallengeLog("选择题", "正确", pointResult.delta);
    const bonusText = pointResult.alreadyRewarded ? "（此前已答对，本次不计分）" : `+${POINT_REWARD} 做题积分`;
    elements.quizFeedback.textContent = `✅ 回答正确，闯关成功！${bonusText}`;
    elements.quizFeedback.style.color = "#0f9d58";
    elements.quizAnalysis.textContent = `解析：${currentQuiz.explainCorrect}`;
    elements.quizAnalysis.style.color = "#0f9d58";
    if (pointResult.awarded) showSuccessFx();
  } else {
    stats.wrong += 1;
    let penaltyDelta = 0;
    if (!hasBeenRewarded("quiz", quizId)) {
      adjustPracticePoints(-POINT_PENALTY);
      penaltyDelta = -POINT_PENALTY;
    }
    markPractice();
    addChallengeLog("选择题", "错误", penaltyDelta);
    const penaltyText = penaltyDelta ? `，${penaltyDelta} 做题积分` : "（已答对过本题，本次错题不扣分）";
    elements.quizFeedback.textContent = `❌ 回答错误，正确答案是：${currentQuiz.answer}${penaltyText}`;
    elements.quizFeedback.style.color = "#b00020";
    const reason = currentQuiz.optionReasons[option] || "这个选项不符合本题语法规则。";
    elements.quizAnalysis.textContent = `错因分析：${reason}；正确思路：${currentQuiz.explainCorrect}`;
    elements.quizAnalysis.style.color = "#b00020";

    if (!wrongQuizIds.includes(currentQuiz.id)) {
      wrongQuizIds.push(currentQuiz.id);
      saveWrongQuizIds();
    }
    addWrongBookItem("选择题", currentQuiz.prompt, currentQuiz.answer, currentQuiz.unit);
    showFailFx();
  }
  saveStats();
  updateDashboard();
  updateWrongBookStatus();
  renderChallengeLogs();
}

function updateGrammarUnitFilter(resetIndices = true) {
  const unitValue = elements.grammarUnitFilter?.value || "all";
  filteredGrammarPoints = applyUnitFilter(grammarPoints, unitValue);
  filteredSvoExercises = applyUnitFilter(svoExercises, unitValue);
  if (resetIndices) {
    grammarIndex = 0;
    svoIndex = 0;
    renderGrammar();
    renderSvoExercise();
    return;
  }
  grammarIndex = clampIndex(grammarIndex, filteredGrammarPoints.length);
  svoIndex = clampIndex(svoIndex, filteredSvoExercises.length);
  renderGrammar();
  renderSvoExercise({ preserve: true });
}

function updatePhraseUnitFilter(resetIndex = true) {
  const unitValue = elements.phraseUnitFilter?.value || "all";
  filteredPhrases = applyUnitFilter(commonPhrases, unitValue);
  if (resetIndex) phraseIndex = 0;
  else phraseIndex = clampIndex(phraseIndex, filteredPhrases.length);
  renderPhrase();
}

function updateVerbUnitFilter(resetIndex = true) {
  filteredVerbTriples = [...verbTriples];
  if (resetIndex) verbIndex = 0;
  else verbIndex = clampIndex(verbIndex, filteredVerbTriples.length);
  renderVerb();
}

function renderGrammar() {
  if (filteredGrammarPoints.length === 0) {
    elements.grammarTitle.textContent = "当前单元暂无语法点";
    elements.grammarRule.textContent = "";
    elements.grammarExample.innerHTML = "";
    return;
  }
  const point = filteredGrammarPoints[grammarIndex];
  elements.grammarTitle.textContent = point.title;
  elements.grammarRule.textContent = point.rule;
  const rows = point.examples.map((example) => `<p>✅ ${example}</p>`).join("");
  elements.grammarExample.innerHTML = rows;
}

function nextGrammarPoint() {
  if (filteredGrammarPoints.length === 0) return;
  grammarIndex = (grammarIndex + 1) % filteredGrammarPoints.length;
  renderGrammar();
}

function renderPhrase() {
  if (filteredPhrases.length === 0) {
    elements.phraseScene.textContent = "当前单元暂无常用语";
    elements.phraseMasked.textContent = "";
    elements.phraseZh.textContent = "";
    return;
  }
  const phrase = filteredPhrases[phraseIndex];
  elements.phraseScene.textContent = `场景: ${phrase.scene}`;
  elements.phraseMasked.textContent = phrase.en.replace(phrase.key, "______");
  elements.phraseEn.textContent = phrase.en;
  elements.phraseEn.classList.add("hidden");
  elements.phraseMasked.classList.remove("hidden");
  phraseFlipped = false;
  elements.phraseHint.textContent = "点击闪卡显示答案";
  elements.phraseZh.textContent = `中文: ${phrase.zh}`;
}

function nextPhraseItem() {
  if (filteredPhrases.length === 0) return;
  phraseIndex = (phraseIndex + 1) % filteredPhrases.length;
  renderPhrase();
}

function togglePhraseCard() {
  phraseFlipped = !phraseFlipped;
  elements.phraseMasked.classList.toggle("hidden", phraseFlipped);
  elements.phraseEn.classList.toggle("hidden", !phraseFlipped);
  elements.phraseHint.textContent = phraseFlipped ? "再次点击可隐藏关键词" : "点击闪卡显示答案";
}

function updateWritingFilter() {
  const selectedUnit = Number(elements.writingUnitFilter.value);
  filteredWritingSamples = writingSamples.filter((item) => item.unit === selectedUnit);
  writingIndex = 0;
  renderWritingSample();
}

function renderWritingSample() {
  if (filteredWritingSamples.length === 0) {
    elements.writingTitle.textContent = writingSamples.length === 0 ? "作文题库未加载，请通过「启动.bat」访问" : "当前单元暂无范文";
    elements.writingEn.textContent = "";
    elements.writingZh.textContent = "";
    elements.writingFillPrompt.textContent = "";
    elements.writingFillFeedback.textContent = "";
    return;
  }
  const sample = filteredWritingSamples[writingIndex];
  elements.writingTitle.textContent = sample.title;
  elements.writingEn.textContent = sample.en;
  elements.writingZh.textContent = `参考译文: ${sample.zh}`;
  elements.writingFillPrompt.textContent = sample.fillPrompt;
  elements.writingFillInput.value = "";
  elements.writingFillFeedback.textContent = "";
}

function nextWritingSample() {
  if (filteredWritingSamples.length === 0) return;
  writingIndex = (writingIndex + 1) % filteredWritingSamples.length;
  renderWritingSample();
}

function checkWritingFillAnswer() {
  const sample = filteredWritingSamples[writingIndex];
  if (!sample) return;
  const answer = elements.writingFillInput.value.trim().toLowerCase();
  if (!answer) {
    elements.writingFillFeedback.textContent = "请先填写答案。";
    elements.writingFillFeedback.style.color = "#b00020";
    return;
  }
  if (answer === sample.fillAnswer.toLowerCase()) {
    stats.attempts += 1;
    stats.correct += 1;
    const writingId = sample.id || `writing-${writingIndex}`;
    const pointResult = handlePracticePoints("writing", writingId, POINT_REWARD);
    markPractice();
    addChallengeLog("作文填空", "正确", pointResult.delta);
    const bonusText = pointResult.alreadyRewarded ? "（此前已答对，本次不计分）" : `+${POINT_REWARD} 做题积分`;
    elements.writingFillFeedback.textContent = `填空正确！${bonusText}`;
    elements.writingFillFeedback.style.color = "#0f9d58";
    if (pointResult.awarded) showSuccessFx();
  } else {
    stats.attempts += 1;
    stats.wrong += 1;
    const writingId = sample.id || `writing-${writingIndex}`;
    let penaltyDelta = 0;
    if (!hasBeenRewarded("writing", writingId)) {
      adjustPracticePoints(-POINT_PENALTY);
      penaltyDelta = -POINT_PENALTY;
    }
    markPractice();
    addChallengeLog("作文填空", "错误", penaltyDelta);
    addWrongBookItem("作文填空", sample.fillPrompt, sample.fillAnswer, sample.unit);
    const penaltyText = penaltyDelta ? `，${penaltyDelta} 做题积分` : "";
    elements.writingFillFeedback.textContent = `答案不对，正确答案：${sample.fillAnswer}${penaltyText}`;
    elements.writingFillFeedback.style.color = "#b00020";
    showFailFx();
  }
  saveStats();
  updateDashboard();
  renderChallengeLogs();
}

function renderSvoExercise(options = {}) {
  const preserve = options.preserve === true;
  if (filteredSvoExercises.length === 0) {
    elements.svoSentenceHint.textContent = "当前单元暂无语法连连看题目";
    elements.svoTokens.innerHTML = "";
    svoTokenLayoutKey = "";
    svoTokenLayout = [];
    return;
  }
  const item = filteredSvoExercises[svoIndex];
  const layoutKey = item.id || `svo-${svoIndex}-${item.sentenceHint}`;
  elements.svoSentenceHint.textContent = `句子：${item.sentenceHint}`;

  if (!preserve || layoutKey !== svoTokenLayoutKey) {
    svoUserAnswer = { subject: "", verb: "", object: "" };
    activeSvoSlot = "subject";
    elements.slotSubject.textContent = "主语 (S)";
    elements.slotVerb.textContent = "谓语 (V)";
    elements.slotObject.textContent = "宾语/补语 (O)";
    elements.svoFeedback.textContent = "";
    svoTokenLayoutKey = layoutKey;
    svoTokenLayout = shuffle([item.subject, item.verb, item.object]);
  }

  elements.svoTokens.innerHTML = "";
  svoTokenLayout.forEach((token) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "svo-token";
    btn.textContent = token;
    btn.addEventListener("click", () => assignSvoToken(token));
    elements.svoTokens.appendChild(btn);
  });
  highlightActiveSlot();
}

function highlightActiveSlot() {
  const mapping = {
    subject: elements.slotSubject,
    verb: elements.slotVerb,
    object: elements.slotObject,
  };
  Object.entries(mapping).forEach(([key, el]) => {
    el.classList.toggle("active-slot", key === activeSvoSlot);
  });
}

function setActiveSvoSlot(slot) {
  activeSvoSlot = slot;
  highlightActiveSlot();
}

function assignSvoToken(token) {
  svoUserAnswer[activeSvoSlot] = token;
  if (activeSvoSlot === "subject") elements.slotSubject.textContent = `主语 (S): ${token}`;
  if (activeSvoSlot === "verb") elements.slotVerb.textContent = `谓语 (V): ${token}`;
  if (activeSvoSlot === "object") elements.slotObject.textContent = `宾语/补语 (O): ${token}`;
}

function checkSvoExercise() {
  const item = filteredSvoExercises[svoIndex];
  if (!item) return;
  const done = svoUserAnswer.subject && svoUserAnswer.verb && svoUserAnswer.object;
  if (!done) {
    elements.svoFeedback.textContent = "请先把主语、谓语、宾语都填上。";
    elements.svoFeedback.style.color = "#b00020";
    return;
  }
  stats.attempts += 1;
  const ok = svoUserAnswer.subject === item.subject && svoUserAnswer.verb === item.verb && svoUserAnswer.object === item.object;
  const svoId = `svo-${svoIndex}`;
  if (ok) {
    stats.correct += 1;
    const pointResult = handlePracticePoints("svo", svoId, POINT_REWARD);
    markPractice();
    addChallengeLog("语法连连看", "正确", pointResult.delta);
    const bonusText = pointResult.alreadyRewarded ? "（此前已答对，本次不计分）" : `+${POINT_REWARD} 做题积分`;
    elements.svoFeedback.textContent = `主谓宾匹配正确！${bonusText}`;
    elements.svoFeedback.style.color = "#0f9d58";
    if (pointResult.awarded) showSuccessFx();
  } else {
    stats.wrong += 1;
    let penaltyDelta = 0;
    if (!hasBeenRewarded("svo", svoId)) {
      adjustPracticePoints(-POINT_PENALTY);
      penaltyDelta = -POINT_PENALTY;
    }
    markPractice();
    addChallengeLog("语法连连看", "错误", penaltyDelta);
    addWrongBookItem("语法连连看", item.sentenceHint, `S=${item.subject}, V=${item.verb}, O=${item.object}`, item.unit);
    const penaltyText = penaltyDelta ? `，${penaltyDelta} 做题积分` : "";
    elements.svoFeedback.textContent = `匹配有误，标准答案：S=${item.subject}，V=${item.verb}，O=${item.object}${penaltyText}`;
    elements.svoFeedback.style.color = "#b00020";
    showFailFx();
  }
  saveStats();
  updateDashboard();
  renderChallengeLogs();
}

function nextSvoExercise() {
  if (filteredSvoExercises.length === 0) return;
  svoIndex = (svoIndex + 1) % filteredSvoExercises.length;
  renderSvoExercise();
}

function renderAppendixPanel() {
  const lines = [];
  let totalVocab = 0;
  let totalPhrase = 0;
  let totalSentence = 0;
  appendixUnits.forEach((unit) => {
    const vocabA = unit.partAVocab.length;
    const vocabB = unit.partBVocab.length;
    const phraseA = unit.partAPhrases.length;
    const phraseB = unit.partBPhrases.length;
    const sentA = unit.partASentences.length;
    const sentB = unit.partBSentences.length;
    totalVocab += vocabA + vocabB;
    totalPhrase += phraseA + phraseB;
    totalSentence += sentA + sentB;
    const status = vocabA > 0 && vocabB > 0 && phraseA > 0 && phraseB > 0 && sentA > 0 && sentB > 0 ? "完整" : "缺失";
    lines.push(
      `<div class="appendix-row ${status === "完整" ? "ok-row" : "warn-row"}">` +
      `<span>Unit ${unit.num}</span><span>词汇 ${vocabA + vocabB}</span><span>短语 ${phraseA + phraseB}</span><span>句型 ${sentA + sentB}</span><span>${status}</span></div>`,
    );
  });
  elements.appendixSummary.textContent = `全量覆盖统计：词汇 ${totalVocab} 条，短语 ${totalPhrase} 条，句型 ${totalSentence} 条，附录5不规则动词 ${verbTriples.length}/47 组。`;
  elements.appendixTable.innerHTML = `<div class="appendix-head"><span>单元</span><span>词汇</span><span>短语</span><span>句型</span><span>状态</span></div>${lines.join("")}`;
}

function applyQuizFilters() {
  const selectedUnit = elements.quizUnitFilter.value;
  const selectedPart = elements.quizPartFilter.value;

  const unitFiltered = selectedUnit === "all" ? quizzes : quizzes.filter((item) => String(item.unit) === selectedUnit);
  const partFiltered = selectedPart === "all" ? unitFiltered : unitFiltered.filter((item) => item.part === selectedPart);

  if (wrongBookMode) {
    filteredQuizzes = partFiltered.filter((item) => wrongQuizIds.includes(item.id));
  } else {
    filteredQuizzes = partFiltered;
  }
}

function refreshQuizWithFilters(resetQuiz = true) {
  applyQuizFilters();
  updateWrongBookStatus();
  renderQuiz(resetQuiz ? { forceNew: true } : { preserve: true });
}

function toggleWrongBookMode() {
  wrongBookMode = !wrongBookMode;
  refreshQuizWithFilters();
}

function clearWrongBook() {
  requireParentAuth(() => {
    wrongQuizIds = [];
    wrongBookItems = [];
    saveWrongQuizIds();
    saveWrongBookItems();
    if (wrongBookMode) wrongBookMode = false;
    refreshQuizWithFilters();
    updateDashboard();
    renderWrongBookItems();
    renderWrongBookPanel();
  });
}

function renderVerb() {
  if (filteredVerbTriples.length === 0) {
    elements.verbBase.textContent = "当前单元暂无动词专项";
    elements.verbInfinitive.textContent = "";
    elements.verbPast.textContent = "";
    elements.verbParticiple.textContent = "";
    elements.verbUsage.textContent = "";
    elements.verbSentence.textContent = "";
    elements.verbFillPrompt.textContent = "";
    return;
  }
  const verb = filteredVerbTriples[verbIndex];
  elements.verbBase.textContent = `附录5 不规则动词: ${verb.base}`;
  elements.verbInfinitive.textContent = verb.base;
  elements.verbPast.textContent = verb.past;
  elements.verbParticiple.textContent = verb.participle;
  elements.verbUsage.textContent = `用法: ${verb.usage}`;
  elements.verbSentence.textContent = `例句: ${verb.sentence}`;
  elements.verbFillPrompt.textContent = verb.fillPrompt;
  elements.verbFillInput.value = "";
  elements.verbFeedback.textContent = "";
}

function nextVerbItem() {
  if (filteredVerbTriples.length === 0) return;
  verbIndex = (verbIndex + 1) % filteredVerbTriples.length;
  renderVerb();
}

function checkVerbAnswer() {
  const input = elements.verbFillInput.value.trim().toLowerCase();
  if (!input) {
    elements.verbFeedback.textContent = "请先填写答案。";
    elements.verbFeedback.style.color = "#b00020";
    return;
  }

  const current = filteredVerbTriples[verbIndex];
  if (!current) return;
  const acceptedAnswers = current.fillAnswer
    .toLowerCase()
    .split("/")
    .map((item) => item.trim())
    .filter(Boolean);
  stats.attempts += 1;
  const verbId = `verb-${verbIndex}`;
  if (acceptedAnswers.includes(input)) {
    stats.correct += 1;
    const pointResult = handlePracticePoints("verb", verbId, POINT_REWARD);
    markPractice();
    addChallengeLog("动词专项", "正确", pointResult.delta);
    const bonusText = pointResult.alreadyRewarded ? "（此前已答对，本次不计分）" : `+${POINT_REWARD} 做题积分`;
    elements.verbFeedback.textContent = `回答正确！${bonusText}`;
    elements.verbFeedback.style.color = "#0f9d58";
    if (pointResult.awarded) showSuccessFx();
  } else {
    stats.wrong += 1;
    let penaltyDelta = 0;
    if (!hasBeenRewarded("verb", verbId)) {
      adjustPracticePoints(-POINT_PENALTY);
      penaltyDelta = -POINT_PENALTY;
    }
    markPractice();
    addChallengeLog("动词专项", "错误", penaltyDelta);
    addWrongBookItem("动词专项", current.fillPrompt, current.fillAnswer, current.unit);
    const penaltyText = penaltyDelta ? `，${penaltyDelta} 做题积分` : "";
    elements.verbFeedback.textContent = `答案不对，正确答案是: ${current.fillAnswer}${penaltyText}`;
    elements.verbFeedback.style.color = "#b00020";
    showFailFx();
  }
  saveStats();
  updateDashboard();
  renderChallengeLogs();
}

function extractKeywords(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z\s]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length >= 5)
    .slice(0, 8);
}

function scoreWritingDraft() {
  const sample = filteredWritingSamples[writingIndex];
  const draft = elements.writingStudentInput.value.trim();
  if (!draft) {
    elements.writingScore.textContent = "请先写作文再评分。";
    elements.writingAdvice.textContent = "";
    return;
  }
  const words = draft.split(/\s+/).filter(Boolean);
  const sentenceCount = draft.split(/[.!?]+/).map((s) => s.trim()).filter(Boolean).length;
  const completeness = Math.min(40, sentenceCount >= 3 ? 40 : sentenceCount * 12);

  const targetKeywords = extractKeywords(sample.en);
  const lower = draft.toLowerCase();
  const hitCount = targetKeywords.filter((k) => lower.includes(k)).length;
  const keywordScore = targetKeywords.length === 0 ? 0 : Math.round((hitCount / targetKeywords.length) * 35);

  const tenseSignals = ["yesterday", "last", "ago", "did", "went", "saw", "ate", "took", "sent", "won", "was", "were"];
  const tenseHits = tenseSignals.filter((s) => lower.includes(s)).length;
  const tenseScore = Math.min(25, tenseHits * 4);

  const total = Math.min(100, completeness + keywordScore + tenseScore);
  const tips = [];
  if (sentenceCount < 3) tips.push("句型完整度不足：建议至少写 3 句，并加句号。");
  if (keywordScore < 20) tips.push("关键词覆盖偏低：多使用本单元核心词汇与短语。");
  if (tenseScore < 12) tips.push("时态表达偏弱：尝试加入过去时或一般现在时的标准句。");
  if (words.length < 40) tips.push("篇幅偏短：建议写到 40~80 词更完整。");
  if (tips.length === 0) tips.push("表达很好！可以尝试使用更复杂的连接词提升层次。");

  markPractice();
  saveStats();
  updateDashboard();
  addChallengeLog("作文评分器", "完成评分", 0);
  renderChallengeLogs();

  elements.writingScore.textContent = `作文评分：${total}/100（句型 ${completeness}/40，关键词 ${keywordScore}/35，时态 ${tenseScore}/25）`;
  elements.writingScore.style.color = total >= 85 ? "#0f9d58" : total >= 60 ? "#b06d00" : "#b00020";
  elements.writingAdvice.textContent = `改进建议：${tips.join("；")}`;
}

function buildFillBlankSet(options = {}) {
  const preserve = options.preserve === true;
  const selectedUnit = elements.fillUnitFilter.value;
  const pool = selectedUnit === "all"
    ? [...fillBlankBank]
    : fillBlankBank.filter((q) => String(q.unit) === selectedUnit);
  if (pool.length === 0) {
    currentFillQuestions = [];
    const loadHint = fillBlankBank.length === 0
      ? "题库未加载，请通过「启动.bat」本地服务访问（file:// 无法加载 JSON 题库）。"
      : "当前单元暂无审核题库，请在 data/question-banks/fillblank-bank.json 中补充。";
    elements.fillQuestions.innerHTML = `<p class="model">${loadHint}</p>`;
    elements.fillSetFeedback.textContent = "";
    return;
  }
  if (preserve && currentFillQuestions.length > 0) {
    const poolIds = new Set(pool.map((q) => q.id));
    if (currentFillQuestions.every((q) => poolIds.has(q.id))) {
      return;
    }
  }
  const count = Math.min(5, pool.length);
  currentFillQuestions = shuffle(pool).slice(0, count);
  renderFillBlankSet();
}

function renderFillBlankSet() {
  elements.fillQuestions.innerHTML = currentFillQuestions
    .map((q, idx) => `<div class="fill-q"><p><strong>${idx + 1}.</strong> ${q.prompt}</p><p class="model">提示：${q.clue}</p><input id="fillInput-${q.id}" type="text" placeholder="请填写英文单词（可用中文提示）" /></div>`)
    .join("");
  elements.fillSetFeedback.textContent = "";
}

function submitFillBlankSet() {
  if (currentFillQuestions.length === 0) return;
  let correct = 0;
  let invalidCount = 0;
  let practiceDelta = 0;
  currentFillQuestions.forEach((q) => {
    const inputEl = document.getElementById(`fillInput-${q.id}`);
    const value = (inputEl?.value || "").trim().toLowerCase();
    const answerHint = q.analysis ? `${q.answer}（${q.analysis}）` : q.answer;
    if (!/^[a-z][a-z\s'-]*$/.test(value)) {
      invalidCount += 1;
      addWrongBookItem("综合填空", q.prompt, answerHint, q.unit);
      return;
    }
    const validAnswers = String(q.answer)
      .split("/")
      .map((i) => i.trim().toLowerCase())
      .filter(Boolean);
    if (validAnswers.includes(value)) {
      correct += 1;
      const pointResult = handlePracticePoints("fillblank", q.id, 20);
      practiceDelta += pointResult.delta;
    } else {
      const pointResult = handlePracticePoints("fillblank", q.id, -5);
      practiceDelta += pointResult.delta;
      addWrongBookItem("综合填空", q.prompt, answerHint, q.unit);
    }
  });
  const wrong = currentFillQuestions.length - correct - invalidCount;
  stats.attempts += currentFillQuestions.length;
  stats.correct += correct;
  stats.wrong += wrong + invalidCount;
  markPractice();
  addChallengeLog("综合填空5题", `正确${correct}题`, practiceDelta);
  saveStats();
  updateDashboard();
  renderChallengeLogs();
  if (correct >= 4) showSuccessFx(); else showFailFx();
  const total = currentFillQuestions.length;
  elements.fillSetFeedback.textContent = `本组结果：答对 ${correct}/${total}，答错 ${wrong + invalidCount}/${total}，做题积分变化 ${practiceDelta >= 0 ? "+" : ""}${practiceDelta}${invalidCount > 0 ? `（其中 ${invalidCount} 题未按英文单词规范填写）` : ""}`;
  elements.fillSetFeedback.style.color = correct >= 4 ? "#0f9d58" : "#b00020";
}

function todayKey() {
  return new Date().toISOString().slice(0, 10);
}

function renderJournal() {
  const key = todayKey();
  elements.journalToday.textContent = `今天日期：${key}`;
  const listFilter = elements.journalListUnitFilter?.value || "all";
  const visible = journalEntries.filter((entry) => listFilter === "all" || String(entry.unit ?? 0) === listFilter);
  if (visible.length === 0) {
    elements.journalList.textContent = "暂无日志";
    return;
  }
  elements.journalList.innerHTML = visible
    .slice()
    .reverse()
    .map((entry) => `<div><strong>${entry.date}</strong> <span class="wrong-module-tag">U${entry.unit ?? 0}</span>：${entry.text}</div>`)
    .join("");
}

function saveJournalToday() {
  const text = elements.journalInput.value.trim();
  const wordCount = text ? text.split(/\s+/).filter(Boolean).length : 0;
  if (!text) {
    elements.journalFeedback.textContent = "请输入日志内容。";
    elements.journalFeedback.style.color = "#b00020";
    return;
  }
  if (wordCount > 100) {
    elements.journalFeedback.textContent = `超过 100 词（当前 ${wordCount} 词），请精简后再保存。`;
    elements.journalFeedback.style.color = "#b00020";
    return;
  }
  const key = todayKey();
  const journalUnit = Number(elements.journalUnitFilter?.value) || 0;
  const existing = journalEntries.find((item) => item.date === key && (item.unit ?? 0) === journalUnit);
  if (existing) {
    existing.text = text;
  } else {
    journalEntries.push({ date: key, text, unit: journalUnit });
  }
  saveJournalEntries();
  elements.journalFeedback.textContent = "今日日志已保存。";
  elements.journalFeedback.style.color = "#0f9d58";
  addChallengeLog("学习日志", "保存成功", 0);
  renderChallengeLogs();
  renderJournal();
  updateTabCounts();
}

function bindEvents() {
  initPasswordPromptModal();
  elements.saveNickname.addEventListener("click", saveNickname);
  elements.resetAllStats.addEventListener("click", resetAllData);
  elements.redeemPoints.addEventListener("click", () => requireParentAuth(redeemPointsRecord));
  elements.exportReport.addEventListener("click", exportLearningReport);
  elements.exportReportHtml.addEventListener("click", exportPrintableHtmlReport);
  elements.exportPointsHtml.addEventListener("click", exportPointsLedgerHtml);
  elements.markAnswerCorrect.addEventListener("click", markManualAnswerCorrect);
  elements.markAnswerWrong.addEventListener("click", markManualAnswerWrong);
  elements.applyBehaviorAction.addEventListener("click", applyBehaviorAction);
  elements.leaderboardSort.addEventListener("change", renderLeaderboard);
  if (elements.exitParentMode) elements.exitParentMode.addEventListener("click", exitParentMode);
  if (elements.wrongBookModuleFilter) {
    elements.wrongBookModuleFilter.addEventListener("change", () => {
      renderWrongBookPanel();
      renderWrongBookItems();
    });
  }
  if (elements.wrongBookUnitFilter) {
    elements.wrongBookUnitFilter.addEventListener("change", () => {
      renderWrongBookPanel();
      renderWrongBookItems();
    });
  }
  if (elements.reviewWrongVocab) elements.reviewWrongVocab.addEventListener("click", startWrongVocabReview);
  if (elements.reviewWrongQuiz) elements.reviewWrongQuiz.addEventListener("click", startWrongQuizReview);
  if (elements.clearWrongBookPanel) elements.clearWrongBookPanel.addEventListener("click", clearWrongBook);

  elements.tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      setActiveTab(tab.dataset.tab);
      if (window.matchMedia("(max-width: 760px)").matches) {
        tab.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      }
    });
  });

  elements.flashcard.addEventListener("click", toggleCardFlip);
  elements.flashcard.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      toggleCardFlip();
    }
  });

  elements.prevCard.addEventListener("click", () => nextCard(-1));
  elements.nextCard.addEventListener("click", () => nextCard(1));
  elements.unitFilter.addEventListener("change", () => updateUnitFilter(true));
  if (elements.grammarUnitFilter) {
    elements.grammarUnitFilter.addEventListener("change", () => updateGrammarUnitFilter(true));
  }
  if (elements.phraseUnitFilter) {
    elements.phraseUnitFilter.addEventListener("change", () => updatePhraseUnitFilter(true));
  }
  if (elements.journalListUnitFilter) elements.journalListUnitFilter.addEventListener("change", renderJournal);
  elements.nextGrammar.addEventListener("click", nextGrammarPoint);
  elements.slotSubject.addEventListener("click", () => setActiveSvoSlot("subject"));
  elements.slotVerb.addEventListener("click", () => setActiveSvoSlot("verb"));
  elements.slotObject.addEventListener("click", () => setActiveSvoSlot("object"));
  elements.checkSvo.addEventListener("click", checkSvoExercise);
  elements.nextSvo.addEventListener("click", nextSvoExercise);
  elements.phraseCard.addEventListener("click", togglePhraseCard);
  elements.phraseCard.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      togglePhraseCard();
    }
  });
  elements.nextPhrase.addEventListener("click", nextPhraseItem);
  elements.writingUnitFilter.addEventListener("change", updateWritingFilter);
  elements.checkWritingFill.addEventListener("click", checkWritingFillAnswer);
  elements.nextWriting.addEventListener("click", nextWritingSample);
  elements.quizUnitFilter.addEventListener("change", refreshQuizWithFilters);
  elements.quizPartFilter.addEventListener("change", refreshQuizWithFilters);
  elements.startWrongBook.addEventListener("click", toggleWrongBookMode);
  elements.clearWrongBook.addEventListener("click", clearWrongBook);
  elements.nextQuestion.addEventListener("click", () => renderQuiz({ forceNew: true }));
  elements.fillUnitFilter.addEventListener("change", () => buildFillBlankSet({ preserve: false }));
  elements.submitFillSet.addEventListener("click", submitFillBlankSet);
  elements.nextFillSet.addEventListener("click", () => buildFillBlankSet({ preserve: false }));
  elements.checkVerb.addEventListener("click", checkVerbAnswer);
  elements.nextVerb.addEventListener("click", nextVerbItem);
  elements.refreshAppendix.addEventListener("click", renderAppendixPanel);
  elements.scoreWriting.addEventListener("click", scoreWritingDraft);
  elements.saveJournal.addEventListener("click", saveJournalToday);
  if (elements.importBankBtn && elements.importBankFile) {
    elements.importBankBtn.addEventListener("click", () => elements.importBankFile.click());
    elements.importBankFile.addEventListener("change", () => {
      const file = elements.importBankFile.files?.[0];
      if (file) handleImportBankFile(file);
      elements.importBankFile.value = "";
    });
  }
  if (elements.downloadImportTemplate) {
    elements.downloadImportTemplate.addEventListener("click", downloadImportTemplateFile);
  }
  if (elements.clearCustomBanks) {
    elements.clearCustomBanks.addEventListener("click", clearCustomImportedBanks);
  }
  if (elements.resetParentPin) elements.resetParentPin.addEventListener("click", resetParentPin);
  if (elements.forgotParentPin) elements.forgotParentPin.addEventListener("click", forgotParentPinRecovery);
  if (elements.saveAdminPin) elements.saveAdminPin.addEventListener("click", () => saveAdminPinToServer());
  if (elements.adminPinInput) {
    elements.adminPinInput.addEventListener("change", () => saveAdminPinLocal(elements.adminPinInput.value.trim()));
  }
  if (elements.syncDataBtn) elements.syncDataBtn.addEventListener("click", () => syncDataNow());
  if (elements.mobileSaveNickname) {
    elements.mobileSaveNickname.addEventListener("click", () => {
      if (!saveNicknameFromInput(elements.mobileNicknameInput?.value)) {
        setLanSyncFeedback("请先输入学生昵称。", "warn");
      }
    });
  }
  if (elements.mobileSyncBtn) {
    elements.mobileSyncBtn.addEventListener("click", () => syncDataNow());
  }
  if (elements.mobileNicknameInput) {
    elements.mobileNicknameInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        if (!saveNicknameFromInput(elements.mobileNicknameInput.value)) {
          setLanSyncFeedback("请先输入学生昵称。", "warn");
        }
      }
    });
  }
  if (elements.toggleStudentSidebar && elements.studentSidebar) {
    elements.toggleStudentSidebar.addEventListener("click", () => {
      const collapsed = elements.studentSidebar.classList.toggle("collapsed-on-mobile");
      elements.toggleStudentSidebar.setAttribute("aria-expanded", collapsed ? "false" : "true");
      elements.toggleStudentSidebar.textContent = collapsed
        ? "▼ 同步 / 记录 / 导入导出"
        : "▲ 收起档案与设置";
    });
  }
}

const QUESTION_BANK_BASE = "data/question-banks";
const IMPORT_TEMPLATE_PATH = `${QUESTION_BANK_BASE}/import-template.csv`;

const IMPORT_CSV_HEADER = [
  "type", "id", "unit", "part", "itemType", "prompt", "answer", "clue",
  "options", "badge", "explain", "title", "en", "zh", "fillPrompt",
];

function loadCustomBanks() {
  const raw = window.localStorage.getItem(CUSTOM_BANKS_KEY);
  if (!raw) return { quiz: [], fillblank: [], writing: [] };
  try {
    const parsed = JSON.parse(raw);
    return {
      quiz: Array.isArray(parsed.quiz) ? parsed.quiz : [],
      fillblank: Array.isArray(parsed.fillblank) ? parsed.fillblank : [],
      writing: Array.isArray(parsed.writing) ? parsed.writing : [],
    };
  } catch {
    return { quiz: [], fillblank: [], writing: [] };
  }
}

function saveCustomBanks(data) {
  window.localStorage.setItem(CUSTOM_BANKS_KEY, JSON.stringify(data));
  touchDataUpdatedAt();
}

function mergeBankById(defaultList, customList) {
  const map = new Map(defaultList.map((item) => [String(item.id), item]));
  customList.forEach((item) => {
    if (item?.id) map.set(String(item.id), item);
  });
  return [...map.values()];
}

function applyMergedQuestionBanks(custom) {
  quizzes = mergeBankById(defaultQuizzes, custom.quiz);
  fillBlankBank = mergeBankById(defaultFillBlankBank, custom.fillblank);
  writingSamples = mergeBankById(defaultWritingSamples, custom.writing);
  filteredQuizzes = [...quizzes];
  updateTabCounts();
}

function setLanSyncFeedback(message, tone = "info") {
  if (elements.lanSyncFeedback) {
    elements.lanSyncFeedback.textContent = message;
    const colors = { ok: "#0f9d58", warn: "#c77700", error: "#b00020", info: "#374f86" };
    elements.lanSyncFeedback.style.color = colors[tone] || colors.info;
  }
  if (elements.mobileLanSyncFeedback) {
    elements.mobileLanSyncFeedback.textContent = message;
    elements.mobileLanSyncFeedback.dataset.tone = tone;
  }
}

function getLanSyncId() {
  const nick = (studentProfile.nickname || "").trim();
  if (nick && nick !== "同学") return nick;
  return (window.localStorage.getItem(LAN_SYNC_KEY) || "").trim();
}

function resolveLanSyncId() {
  let syncId = getLanSyncId();
  if (!syncId) {
    const input =
      elements.nicknameInput?.value?.trim() ||
      elements.mobileNicknameInput?.value?.trim() ||
      "";
    syncId = window.prompt("请先输入学生昵称（PC与手机须相同）", input)?.trim() || "";
    if (syncId) {
      saveNicknameFromInput(syncId);
    }
  }
  return syncId;
}

function getDeviceLabel() {
  const ua = navigator.userAgent || "";
  if (/Mobile|Android|iPhone|iPad|iPod/i.test(ua)) return "手机";
  return "电脑";
}

const SYNC_ACTION_LABELS = {
  initialized: "首次建立同步",
  local_wins: "本机较新 → 已更新班级",
  remote_wins: "班级较新 → 已更新本机",
  merged: "已合并双向数据",
  same: "两端一致",
};

function scheduleLanSync(immediate = false) {
  if (suppressLanSync || suppressDataTouch) return;
  if (!getLanSyncId()) return;
  if (lanSyncTimer) window.clearTimeout(lanSyncTimer);
  if (immediate) {
    syncDataNow({ silent: true, reason: "immediate" });
    return;
  }
  lanSyncTimer = window.setTimeout(() => {
    lanSyncTimer = null;
    syncDataNow({ silent: true, reason: "auto" });
  }, LAN_SYNC_DEBOUNCE_MS);
}

function startLanSyncPolling() {
  if (lanSyncPollTimer) return;
  lanSyncPollTimer = window.setInterval(() => {
    if (document.hidden || !getLanSyncId()) return;
    syncDataNow({ silent: true, reason: "poll" });
  }, LAN_SYNC_POLL_MS);
}

function loadLocalSyncLogs() {
  const raw = window.localStorage.getItem(SYNC_LOG_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveLocalSyncLogs(logs) {
  window.localStorage.setItem(SYNC_LOG_KEY, JSON.stringify(logs.slice(-50)));
}

function appendLocalSyncLog(entry) {
  if (!entry) return;
  const logs = loadLocalSyncLogs();
  logs.push(entry);
  saveLocalSyncLogs(logs);
  renderSyncLogs(logs);
}

function formatSyncLogTime(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

function renderSyncLogs(logs) {
  if (!elements.syncLogList) return;
  const list = Array.isArray(logs) ? logs : [];
  if (list.length === 0) {
    elements.syncLogList.innerHTML = "<p class=\"model sync-log-empty\">暂无同步记录，点上方按钮开始同步。</p>";
    return;
  }
  const rows = [...list].reverse().slice(0, 12).map((item) => {
    const action = SYNC_ACTION_LABELS[item.action] || item.action || "同步";
    const device = item.device || "未知";
    const msg = item.message || action;
    const time = formatSyncLogTime(item.time);
    return `<div class="sync-log-item"><span class="sync-log-time">${time}</span> <span class="sync-log-device">[${device}]</span> ${msg}</div>`;
  });
  elements.syncLogList.innerHTML = rows.join("");
}

function collectSyncPayload() {
  if (!getDataUpdatedAt()) touchDataUpdatedAt();
  let studyHubNotes = {};
  let studyHubState = {};
  let studyHubKnowledgeCustom = null;
  let masteryProgress = {};
  try {
    studyHubNotes = JSON.parse(window.localStorage.getItem("study_hub_notes_v1") || "{}");
    studyHubState = JSON.parse(window.localStorage.getItem("study_hub_state_v1") || "{}");
    studyHubKnowledgeCustom = JSON.parse(window.localStorage.getItem("study_hub_knowledge_custom_v1") || "null");
    masteryProgress = JSON.parse(window.localStorage.getItem("english_grade6_mastery_v1") || "{}");
  } catch { /* ignore */ }
  return {
    version: 1,
    updatedAt: getDataUpdatedAt(),
    dashboardResetAt: getDashboardResetAt(),
    stats,
    studentProfile,
    wrongQuizIds,
    challengeLogs,
    redeemLogs,
    journalEntries,
    wrongBookItems,
    leaderboard,
    behaviorLogs,
    badges,
    rewarded,
    customBanks: loadCustomBanks(),
    studyHubNotes,
    studyHubState,
    studyHubKnowledgeCustom,
    masteryProgress,
    ...(window.GratitudeHub ? window.GratitudeHub.getSyncPayload() : {}),
  };
}

function refreshUiAfterSync(options = {}) {
  const preservePractice = options.preservePractice !== false;
  migrateStatsOnLoad();
  applyCompoundInterestIfNeeded();
  updateDashboard();
  renderLeaderboard();
  renderWrongBookItems();
  renderWrongBookPanel();
  updateParentModeUI();
  renderBadgeList();
  renderCharts();
  renderChallengeLogs();
  renderRedeemLogs();
  if (preservePractice) {
    updateUnitFilter(false);
    updateGrammarUnitFilter(false);
    updatePhraseUnitFilter(false);
    updateVerbUnitFilter(false);
    applyQuizFilters();
    updateWrongBookStatus();
    buildFillBlankSet({ preserve: true });
    renderQuiz({ preserve: true });
    renderGrammar();
    renderSvoExercise({ preserve: true });
    renderPhrase();
    renderVerb();
  } else {
    updateUnitFilter(true);
    updateGrammarUnitFilter(true);
    updatePhraseUnitFilter(true);
    updateVerbUnitFilter(true);
    updateWritingFilter();
    buildFillBlankSet();
    applyQuizFilters();
    updateWrongBookStatus();
    renderGrammar();
    renderSvoExercise();
    renderPhrase();
    renderQuiz({ forceNew: true });
    renderVerb();
  }
  renderAppendixPanel();
  renderJournal();
  updateParentPinPanel();
  if (window.StudyHub && typeof window.StudyHub.applyLanSync === "function") {
    window.StudyHub.applyLanSync();
  }
}

function applySyncPayload(payload) {
  if (!payload || typeof payload !== "object") throw new Error("无效同步数据");
  const keepParentUnlock = parentUnlocked;
  suppressDataTouch = true;
  suppressLanSync = true;
  try {
    stats = payload.stats || loadStats();
    studentProfile = payload.studentProfile || loadStudentProfile();
    wrongQuizIds = Array.isArray(payload.wrongQuizIds) ? payload.wrongQuizIds : [];
    challengeLogs = Array.isArray(payload.challengeLogs) ? payload.challengeLogs : [];
    redeemLogs = Array.isArray(payload.redeemLogs) ? payload.redeemLogs : [];
    journalEntries = Array.isArray(payload.journalEntries) ? payload.journalEntries : [];
    wrongBookItems = Array.isArray(payload.wrongBookItems) ? payload.wrongBookItems : [];
    leaderboard = Array.isArray(payload.leaderboard) ? payload.leaderboard : [];
    behaviorLogs = Array.isArray(payload.behaviorLogs) ? payload.behaviorLogs : [];
    badges = Array.isArray(payload.badges) ? payload.badges : [];
    rewarded = payload.rewarded || loadRewarded();
    parentUnlocked = keepParentUnlock;
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(stats));
    window.localStorage.setItem(WRONG_BOOK_KEY, JSON.stringify(wrongQuizIds));
    window.localStorage.setItem(PROFILE_KEY, JSON.stringify(studentProfile));
    window.localStorage.setItem(CHALLENGE_LOG_KEY, JSON.stringify(challengeLogs));
    window.localStorage.setItem(REDEEM_LOG_KEY, JSON.stringify(redeemLogs));
    window.localStorage.setItem(JOURNAL_KEY, JSON.stringify(journalEntries));
    window.localStorage.setItem(WRONG_BOOK_ITEMS_KEY, JSON.stringify(wrongBookItems));
    window.localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(leaderboard));
    window.localStorage.setItem(BEHAVIOR_LOG_KEY, JSON.stringify(behaviorLogs));
    window.localStorage.setItem(BADGE_KEY, JSON.stringify(badges));
    window.localStorage.setItem(REWARDED_KEY, JSON.stringify(rewarded));
    if (payload.customBanks) window.localStorage.setItem(CUSTOM_BANKS_KEY, JSON.stringify(payload.customBanks));
    if (payload.studyHubNotes !== undefined) {
      window.localStorage.setItem("study_hub_notes_v1", JSON.stringify(payload.studyHubNotes || {}));
    }
    if (payload.studyHubState !== undefined) {
      window.localStorage.setItem("study_hub_state_v1", JSON.stringify(payload.studyHubState || {}));
    }
    if ("studyHubKnowledgeCustom" in payload) {
      const custom = payload.studyHubKnowledgeCustom;
      if (custom) window.localStorage.setItem("study_hub_knowledge_custom_v1", JSON.stringify(custom));
      else window.localStorage.removeItem("study_hub_knowledge_custom_v1");
    }
    if (payload.masteryProgress) {
      window.localStorage.setItem("english_grade6_mastery_v1", JSON.stringify(payload.masteryProgress));
      if (window.MasteryHub && typeof window.MasteryHub.applyMasteryImport === "function") {
        window.MasteryHub.applyMasteryImport({ progress: payload.masteryProgress });
      }
    }
    if (window.GratitudeHub && typeof window.GratitudeHub.applySyncPayload === "function") {
      window.GratitudeHub.applySyncPayload(payload);
    }
    setDataUpdatedAt(payload.updatedAt || getDataUpdatedAt());
    if (elements.nicknameInput) {
      elements.nicknameInput.value = studentProfile.nickname === "同学" ? "" : studentProfile.nickname;
    }
    syncNicknameInputs();
    if (studentProfile.nickname && studentProfile.nickname !== "同学") {
      window.localStorage.setItem(LAN_SYNC_KEY, studentProfile.nickname);
    }
    if (payload.dashboardResetAt !== undefined) {
      const incoming = String(payload.dashboardResetAt || "");
      const local = getDashboardResetAt();
      if (!incoming) setDashboardResetAt("");
      else if (!local || incoming >= local) setDashboardResetAt(incoming);
    }
  } finally {
    suppressDataTouch = false;
    suppressLanSync = false;
  }
  applyMergedQuestionBanks(loadCustomBanks());
  refreshUiAfterSync();
}

async function pingLanServer() {
  const res = await fetch("/api/ping", { cache: "no-store" });
  return res.ok;
}

async function fetchLanPingInfo() {
  try {
    const res = await fetch("/api/ping", { cache: "no-store" });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

function buildLanAccessUrls(ping) {
  if (!ping) return [];
  const port = Number(ping.port) || 8080;
  const ips = Array.isArray(ping.lanIps) ? ping.lanIps.filter(Boolean) : [];
  if (ips.length) {
    return ips.map((ip) => ({ ip, url: `http://${ip}:${port}` }));
  }
  if (ping.mobileUrl) {
    try {
      const u = new URL(ping.mobileUrl);
      return [{ ip: u.hostname, url: ping.mobileUrl }];
    } catch {
      return [{ ip: "", url: ping.mobileUrl }];
    }
  }
  return [];
}

function renderLanAccessUrlList(container, urls, feedbackEl) {
  if (!container) return;
  if (!urls.length) {
    container.innerHTML =
      '<p class="lan-access-empty">未检测到局域网 IP。请用 <strong>启动.bat</strong> 运行，并确保电脑与手机在同一 WiFi。</p>';
    return;
  }
  container.innerHTML = urls
    .map((row, idx) => {
      const safeUrl = String(row.url).replace(/"/g, "&quot;");
      const target = feedbackEl?.id || "";
      return `<div class="lan-access-row">
        <input type="text" class="lan-access-url" readonly value="${safeUrl}" aria-label="局域网地址 ${idx + 1}" />
        <button type="button" class="secondary-btn lan-access-copy-btn" data-copy-url="${safeUrl}" data-feedback-target="${target}">复制</button>
      </div>${row.ip ? `<p class="lan-access-ip-hint">IP：${row.ip}</p>` : ""}`;
    })
    .join("");
  container.querySelectorAll(".lan-access-copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const url = btn.getAttribute("data-copy-url") || "";
      const targetId = btn.getAttribute("data-feedback-target");
      const target = targetId ? document.getElementById(targetId) : feedbackEl;
      copyLanAccessUrl(url, target);
    });
  });
  container.querySelectorAll(".lan-access-url").forEach((input) => {
    input.addEventListener("click", () => {
      input.select();
      const row = input.closest(".lan-access-row");
      const btn = row?.querySelector(".lan-access-copy-btn");
      const url = btn?.getAttribute("data-copy-url") || input.value || "";
      const targetId = btn?.getAttribute("data-feedback-target");
      const target = targetId ? document.getElementById(targetId) : feedbackEl;
      copyLanAccessUrl(url, target);
    });
  });
}

async function copyLanAccessUrl(url, feedbackEl) {
  const text = (url || "").trim();
  if (!text) return false;
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
    } else {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    if (feedbackEl) {
      feedbackEl.textContent = `已复制：${text}`;
      feedbackEl.dataset.tone = "ok";
    }
    return true;
  } catch {
    if (feedbackEl) {
      feedbackEl.textContent = "复制失败，请手动长按选择地址复制";
      feedbackEl.dataset.tone = "error";
    }
    return false;
  }
}

async function refreshLanAccessBox() {
  const ping = await fetchLanPingInfo();
  serverReportsLocalClient = Boolean(ping?.isLocalClient);
  updateParentPinPanel();
  const urls = buildLanAccessUrls(ping);
  renderLanAccessUrlList(elements.lanAccessUrlList, urls, elements.lanAccessCopyFeedback);
  renderLanAccessUrlList(elements.lanAccessUrlListMobile, urls, elements.lanAccessCopyFeedbackMobile);
  if (elements.lanAccessAlt) {
    const onLocalhost = /^https?:\/\/(localhost|127\.0\.0\.1)/i.test(window.location.href);
    if (onLocalhost && urls.length) {
      elements.lanAccessAlt.textContent = "提示：手机请用上方局域网地址打开，不要用 localhost。";
      elements.lanAccessAlt.classList.remove("hidden");
    } else {
      elements.lanAccessAlt.classList.add("hidden");
      elements.lanAccessAlt.textContent = "";
    }
  }
  if (elements.lanAccessBox) elements.lanAccessBox.classList.toggle("lan-access-unavailable", !ping);
  if (elements.lanAccessBoxMobile) elements.lanAccessBoxMobile.classList.toggle("lan-access-unavailable", !ping);
}

async function fetchServerSyncLogs(syncId) {
  const res = await fetch(`/api/sync/logs?syncId=${encodeURIComponent(syncId)}`, { cache: "no-store" });
  if (!res.ok) return null;
  const data = await res.json();
  return Array.isArray(data.logs) ? data.logs : null;
}

function setSyncButtonBusy(busy) {
  if (!elements.syncDataBtn) return;
  elements.syncDataBtn.disabled = busy;
  elements.syncDataBtn.textContent = busy ? "同步中…" : "同步数据（多端刷新）";
}

async function syncDataNow(options = {}) {
  const silent = Boolean(options.silent);
  const syncId = resolveLanSyncId();
  if (!syncId) {
    if (!silent) setLanSyncFeedback("请先保存学生昵称，再点同步。", "warn");
    return false;
  }
  if (lanSyncInFlight) return false;
  lanSyncInFlight = true;
  if (!silent) setSyncButtonBusy(true);
  if (!silent) setLanSyncFeedback("正在与班级服务器比对数据…", "info");
  try {
    if (!(await pingLanServer())) {
      throw new Error("no_server");
    }
    const res = await fetch("/api/sync/merge", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        syncId,
        payload: collectSyncPayload(),
        device: getDeviceLabel(),
      }),
    });
    if (!res.ok) throw new Error("merge_failed");
    const result = await res.json();
    if (result.action === "same" && options.silent) {
      if (window.StudyHub && typeof window.StudyHub.applyLanSync === "function") {
        await window.StudyHub.applyLanSync();
      }
      return true;
    }
    applySyncPayload(result.payload);
    if (result.log) appendLocalSyncLog(result.log);
    if (Array.isArray(result.logs) && result.logs.length > 0) {
      saveLocalSyncLogs(result.logs);
      renderSyncLogs(result.logs);
    }
    if (!silent) {
      const label = SYNC_ACTION_LABELS[result.action] || "同步完成";
      const when = result.payload?.updatedAt ? formatSyncLogTime(result.payload.updatedAt) : "";
      setLanSyncFeedback(`${label}${when ? `（数据时间 ${when}）` : ""}`, "ok");
    } else if (elements.lanSyncFeedback && result.action === "merged") {
      setLanSyncFeedback("局域网数据已自动同步", "ok");
    }
    return true;
  } catch {
    if (!silent) {
      setLanSyncFeedback("同步失败：请用启动.bat 启动服务，手机与电脑须打开同一局域网地址。", "error");
    }
    return false;
  } finally {
    lanSyncInFlight = false;
    if (!silent) setSyncButtonBusy(false);
  }
}

async function loadSyncLogsFromServer() {
  const syncId = getLanSyncId();
  if (!syncId) {
    renderSyncLogs(loadLocalSyncLogs());
    return;
  }
  try {
    if (!(await pingLanServer())) {
      renderSyncLogs(loadLocalSyncLogs());
      return;
    }
    const serverLogs = await fetchServerSyncLogs(syncId);
    if (serverLogs && serverLogs.length > 0) {
      saveLocalSyncLogs(serverLogs);
      renderSyncLogs(serverLogs);
    } else {
      renderSyncLogs(loadLocalSyncLogs());
    }
  } catch {
    renderSyncLogs(loadLocalSyncLogs());
  }
}

function parseCsvLine(line) {
  const cells = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === "," && !inQuotes) {
      cells.push(current.trim());
      current = "";
    } else {
      current += ch;
    }
  }
  cells.push(current.trim());
  return cells;
}

function parseImportTable(text) {
  const lines = text
    .replace(/^\uFEFF/, "")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"));
  if (lines.length === 0) return [];

  const delimiter = lines[0].includes("\t") && !lines[0].includes(",") ? "\t" : ",";
  const splitLine = (line) => (delimiter === "\t" ? line.split("\t").map((c) => c.trim()) : parseCsvLine(line));

  let header = splitLine(lines[0]).map((h) => h.toLowerCase());
  let start = 1;
  if (!header.includes("type") && !header.includes("id")) {
    header = IMPORT_CSV_HEADER;
    start = 0;
  }

  const rows = [];
  for (let i = start; i < lines.length; i += 1) {
    const cells = splitLine(lines[i]);
    if (cells.every((c) => !c)) continue;
    const row = {};
    header.forEach((key, idx) => {
      row[key] = cells[idx] || "";
    });
    rows.push(row);
  }
  return rows;
}

function rowToQuiz(row) {
  const options = String(row.options || "")
    .split("|")
    .map((s) => s.trim())
    .filter(Boolean);
  if (options.length < 2) return null;
  const answer = String(row.answer || "").trim();
  const optionReasons = {};
  options.forEach((opt) => {
    optionReasons[opt] = opt === answer ? "正确选项。" : "请再想想。";
  });
  return {
    id: String(row.id).trim(),
    unit: Number(row.unit) || 1,
    part: String(row.part || "A").toUpperCase(),
    badge: row.badge || `Unit ${row.unit || 1} 导入题`,
    prompt: String(row.prompt || "").trim(),
    options,
    answer,
    explainCorrect: row.explain || "请参考正确答案。",
    optionReasons,
  };
}

function rowToFillblank(row) {
  return {
    id: String(row.id).trim(),
    unit: Number(row.unit) || 1,
    part: String(row.part || "A").toUpperCase(),
    type: row.itemtype || row.itemType || row.type2 || "verb",
    prompt: String(row.prompt || "").trim(),
    clue: String(row.clue || "").trim(),
    answer: String(row.answer || "").trim().toLowerCase(),
    analysis: row.explain || "",
  };
}

function rowToWriting(row) {
  return {
    id: String(row.id).trim(),
    unit: Number(row.unit) || 1,
    title: row.title || `Unit ${row.unit || 1} 导入范文`,
    en: String(row.en || "").trim(),
    zh: String(row.zh || "").trim(),
    fillPrompt: String(row.fillprompt || row.fillPrompt || "").trim(),
    fillAnswer: String(row.answer || row.fillanswer || row.fillAnswer || "").trim().toLowerCase(),
  };
}

function importRowsToBanks(rows) {
  const result = { quiz: [], fillblank: [], writing: [] };
  const errors = [];
  rows.forEach((row, idx) => {
    const type = String(row.type || "").trim().toLowerCase();
    const lineNo = idx + 1;
    if (!row.id) {
      errors.push(`第 ${lineNo} 行缺少 id`);
      return;
    }
    if (type === "quiz") {
      const item = rowToQuiz(row);
      if (!item || !item.prompt || !item.answer) errors.push(`第 ${lineNo} 行选择题字段不完整`);
      else result.quiz.push(item);
    } else if (type === "fillblank" || type === "fill") {
      const item = rowToFillblank(row);
      if (!item.prompt || !item.answer) errors.push(`第 ${lineNo} 行填空字段不完整`);
      else result.fillblank.push(item);
    } else if (type === "writing") {
      const item = rowToWriting(row);
      if (!item.en || !item.fillPrompt || !item.fillAnswer) errors.push(`第 ${lineNo} 行范文字段不完整`);
      else result.writing.push(item);
    } else {
      errors.push(`第 ${lineNo} 行 type 无效: ${type}`);
    }
  });
  return { result, errors };
}

function refreshBanksAfterChange() {
  applyMergedQuestionBanks(loadCustomBanks());
  applyQuizFilters();
  updateWritingFilter();
  buildFillBlankSet({ preserve: false });
  renderQuiz({ forceNew: true });
}

function handleImportBankFile(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const rows = parseImportTable(String(reader.result || ""));
      if (rows.length === 0) {
        elements.importBankFeedback.textContent = "文件为空或格式不正确。";
        elements.importBankFeedback.style.color = "#b00020";
        return;
      }
      const { result, errors } = importRowsToBanks(rows);
      const total = result.quiz.length + result.fillblank.length + result.writing.length;
      if (total === 0) {
        elements.importBankFeedback.textContent = `导入失败：${errors.join("；")}`;
        elements.importBankFeedback.style.color = "#b00020";
        return;
      }
      const custom = loadCustomBanks();
      custom.quiz = mergeBankById(custom.quiz, result.quiz);
      custom.fillblank = mergeBankById(custom.fillblank, result.fillblank);
      custom.writing = mergeBankById(custom.writing, result.writing);
      saveCustomBanks(custom);
      refreshBanksAfterChange();
      const msg = `导入成功：选择题 ${result.quiz.length}，填空 ${result.fillblank.length}，作文 ${result.writing.length}。`;
      elements.importBankFeedback.textContent = errors.length ? `${msg}（警告：${errors.join("；")}）` : msg;
      elements.importBankFeedback.style.color = "#0f9d58";
      addChallengeLog("题库导入", file.name, 0);
      renderChallengeLogs();
    } catch (err) {
      elements.importBankFeedback.textContent = `导入失败：${err.message}`;
      elements.importBankFeedback.style.color = "#b00020";
    }
  };
  reader.readAsText(file, "UTF-8");
}

function downloadImportTemplateFile() {
  fetch(IMPORT_TEMPLATE_PATH)
    .then((res) => (res.ok ? res.text() : Promise.reject(new Error("模板不存在"))))
    .then((text) => downloadTextFile("import-template.csv", text, "text/csv"))
    .catch(() => {
      const fallback = `${IMPORT_CSV_HEADER.join(",")}\nquiz,u3-demo-01,3,A,,What should he do?,He should see a doctor.,,"A|B|C|D",Unit3,解析,,,,\n`;
      downloadTextFile("import-template.csv", fallback, "text/csv");
    });
  elements.importBankFeedback.textContent = "模板已下载，用 Excel 填写后保存为 CSV 再导入。";
  elements.importBankFeedback.style.color = "#0f9d58";
}

function clearCustomImportedBanks() {
  requireParentAuth(() => {
    const ok = window.confirm("确定清除本机已导入的加题吗？默认题库不受影响。");
    if (!ok) return;
    saveCustomBanks({ quiz: [], fillblank: [], writing: [] });
    refreshBanksAfterChange();
    elements.importBankFeedback.textContent = "已清除导入加题，已恢复为默认题库。";
    elements.importBankFeedback.style.color = "#0f9d58";
  });
}

function mergeVocabByKey(baseList, extraList) {
  const map = new Map(baseList.map((item) => [`${item.unit}:${item.front}`, item]));
  extraList.forEach((item) => {
    const key = `${item.unit ?? 0}:${item.front}`;
    if (!map.has(key)) map.set(key, item);
  });
  return [...map.values()];
}

function mergePhrasesByKey(baseList, extraList) {
  const map = new Map(baseList.map((item) => [`${item.unit ?? 0}:${item.en}`, item]));
  extraList.forEach((item) => {
    const key = `${item.unit ?? 0}:${item.en}`;
    if (!map.has(key)) {
      map.set(key, {
        ...item,
        key: item.key || pickKeyFromText(item.en),
      });
    }
  });
  return [...map.values()];
}

function applyPracticeSupplement(supp) {
  if (!supp) return;
  vocabularyCards = mergeVocabByKey(vocabularyCards, supp.vocabularyCards || []);
  commonPhrases = mergePhrasesByKey(commonPhrases, supp.phrases || []);
  grammarPoints = mergeBankById(grammarPoints, (supp.grammarPoints || []).map((point) => ({
    ...point,
    unit: point.unit ?? inferGrammarUnit(point.title),
  })));
  defaultQuizzes = mergeBankById(defaultQuizzes, supp.quiz || []);
  defaultFillBlankBank = mergeBankById(defaultFillBlankBank, supp.fillblank || []);
}

async function loadPracticeSupplement() {
  try {
    const res = await fetch("data/practice/supplement.json", { cache: "no-store" });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.warn("练习补充包未加载（可运行 scripts/build_practice_supplement.py）", err);
    return null;
  }
}

async function loadQuestionBanks() {
  try {
    const [quizRes, fillRes, writingRes, supp] = await Promise.all([
      fetch(`${QUESTION_BANK_BASE}/quiz-bank.json`),
      fetch(`${QUESTION_BANK_BASE}/fillblank-bank.json`),
      fetch(`${QUESTION_BANK_BASE}/writing-bank.json`),
      loadPracticeSupplement(),
    ]);
    if (!quizRes.ok || !fillRes.ok || !writingRes.ok) throw new Error("题库加载失败");
    const quizData = await quizRes.json();
    const fillData = await fillRes.json();
    const writingData = await writingRes.json();
    defaultQuizzes = Array.isArray(quizData.questions) ? quizData.questions : [];
    defaultFillBlankBank = Array.isArray(fillData.questions) ? fillData.questions : [];
    defaultWritingSamples = Array.isArray(writingData.samples) ? writingData.samples : [];
    applyPracticeSupplement(supp);
  } catch (err) {
    console.error("题库加载失败", err);
    defaultQuizzes = [];
    defaultFillBlankBank = [];
    defaultWritingSamples = [];
  }
  applyMergedQuestionBanks(loadCustomBanks());
}

async function init() {
  await loadQuestionBanks();
  verbTriples = await loadIrregularVerbs();
  filteredVerbTriples = [...verbTriples];
  migrateStatsOnLoad();
  bindParentPinHiddenPath();
  applyCompoundInterestIfNeeded();
  populateBehaviorActions();
  updateDashboard();
  renderLeaderboard();
  renderWrongBookItems();
  renderWrongBookPanel();
  updateParentModeUI();
  renderBadgeList();
  renderCharts();
  renderChallengeLogs();
  renderRedeemLogs();
  updateUnitFilter();
  updateGrammarUnitFilter();
  updatePhraseUnitFilter();
  updateVerbUnitFilter();
  updateWritingFilter();
  buildFillBlankSet();
  applyQuizFilters();
  updateWrongBookStatus();
  renderGrammar();
  renderSvoExercise();
  renderPhrase();
  renderAppendixPanel();
  renderJournal();
  if (window.GratitudeHub && typeof window.GratitudeHub.onTabActivate === "function") {
    window.GratitudeHub.onTabActivate();
  }
  renderQuiz();
  renderVerb();
  bindEvents();
  updateParentPinPanel();
  window.pep6ForgotParentPin = forgotParentPinRecovery;
  window.tryParentModePassphrase = tryParentModePassphrase;
  window.isParentModeActive = isParentModeActive;
  window.requireParentAuth = requireParentAuth;
  window.updateTabCounts = updateTabCounts;
  window.touchDataUpdatedAt = touchDataUpdatedAt;
  if (window.GratitudeHub) window.GratitudeHub.init();
  syncNicknameInputs();
  if (isMobileDevice() && elements.studentSidebar && !getLanSyncId()) {
    elements.studentSidebar.classList.remove("collapsed-on-mobile");
    if (elements.toggleStudentSidebar) {
      elements.toggleStudentSidebar.setAttribute("aria-expanded", "true");
      elements.toggleStudentSidebar.textContent = "▲ 收起档案与设置";
    }
    setLanSyncFeedback("手机端：请先保存昵称，再点绿色「同步」按钮。", "warn");
  }
  if (!getDataUpdatedAt()) touchDataUpdatedAt();
  await loadSyncLogsFromServer();
  try {
    if (await pingLanServer()) {
      setLanSyncFeedback(
        isMobileDevice()
          ? "已连接局域网。保存昵称后点顶部绿色「同步」即可与电脑对齐。"
          : "已连接同步服务。练习与精讲会自动在局域网内同步。",
        "info",
      );
      startLanSyncPolling();
      initHostAdminPanel();
      await refreshLanAccessBox();
      window.setInterval(() => refreshLanAccessBox(), 60000);
      if (getLanSyncId()) {
        await syncDataNow({ silent: true, reason: "init" });
      }
    }
  } catch {
    // static hosting without sync API
  }
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden && getLanSyncId()) {
      syncDataNow({ silent: true, reason: "visible" });
    }
  });
  window.addEventListener("focus", () => {
    if (getLanSyncId()) scheduleLanSync(true);
  });
  const custom = loadCustomBanks();
  const importedCount = custom.quiz.length + custom.fillblank.length + custom.writing.length;
  if (importedCount > 0 && elements.importBankFeedback) {
    elements.importBankFeedback.textContent = `已加载默认题库，并合并本机导入加题 ${importedCount} 条。`;
    elements.importBankFeedback.style.color = "#0f9d58";
  }
}

window.scheduleLanSync = scheduleLanSync;
window.getAdminPin = getAdminPin;

init();
