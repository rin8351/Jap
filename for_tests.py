kanji_list1 = eval(''.join(open('кандзи.txt', encoding='utf-8').readlines()))

print(f"Количество уникальных кандзи: {len(kanji_list1)}")

# Second list from the text input
kanji_list2 = "虫 途 神 豆 登 富 士 畑 欠 探 深 林 森 古 井 知 泣 共 腺 衣 短 王 玉 囚 美 羊 暮 毛 陽 陰 牛 枯 枝 支 止 烏 歯 米 粍 辻 島 鳴 蛙 居 尾 尿 米 拍 泊 泉 線 幹 干 干 汗 刊 供 供 楊 柳 皮 達 達 撻 抜 齧 刀 刃 彼 被 波 很 戸 戻 石 破 笠 傘 疲 痴 痒 婆 姦 芸 術 云 雲 曇 発 跋 客 路 露 露 露 梅 雷 灯 竜 編 扁 老 磨 研 麻 摩 成 昔 付 寸 吋 村 野 里 里 予 幸 不 武 鳶 戈 式 或 年 歳 未 才 団 池 也 訓 言 舌 飛 込 肉 背 世 界 介 紹 召 芥 之 隠 心 示 甲 訳 訳 初 始 籠 竹 聾 耳 襲 瀧 朧 寵 馬 力 男 車 重 動 働 頭 貝 頁 尻 鳩 鹿 指 甘 旨 外 麗 綺 奇 椅 机 寄 軍 連 相 談 想 思 列 死 苦 万 桜 切 腹 運 運 箱 霜 穴 突 穽 舟 船 舶 航 港 巷 巻 画 落 降 機 織 幾 様 猿 巻 巻".split()

# Combine both lists and convert to set to remove duplicates
unique_kanji = sorted(list(set(kanji_list1 + kanji_list2)))

# Print the actual number of unique kanji
print(f"Количество уникальных кандзи: {len(unique_kanji)}")

# Create a properly formatted Python list string
result = "['" + "', '".join(unique_kanji) + "']"

print("\nСписок уникальных кандзи:")
print(result)

# Для проверки можно также напечатать количество символов в строке result
print(f"\nКоличество символов в строке result (включая форматирование): {len(result)}")