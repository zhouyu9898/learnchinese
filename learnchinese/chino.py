import random

vocabulary = {
  "搬": "ban",
  "简单": "jiandan",
  "渴": "ke",
  "空调": "kongtiao",
  "衬衫": "chenshan",
  "复习": "fuxi",
  "超市": "chaoshi",
  "护照": "huzhao",
  "哭": "ku",
  "难": "nan",
  "节目": "jiemu",
  "结婚": "jiehun",
  "差": "cha",
  "附近": "fujin",
  "刻": "ke",
  "必须": "bixu",
  "历史": "lishi",
  "南": "nan",
  "秋": "qiu",
  "坏": "huai",
  "画": "hua",
  "举行": "juxing",
  "蓝": "lan",
  "菜单": "caidan",
  "河": "he",
  "礼物": "liwu",
  "爬山": "pashan",
  "裙子": "qunzi",
  "裤子": "kuzi",
  "参加": "canjia",
  "低": "di",
  "干净": "ganjing",
  "环境": "huanjing",
  "客人": "keren",
  "筷子": "kuaizi",
  "满意": "manyi",
  "阿姨": "ayi",
  "矮": "ai",
  "安静": "anjing",
  "把": "ba",
  "打扫": "dasao",
  "短": "duan",
  "根据": "genju",
  "借": "jie",
  "努力": "nuli",
  "健康": "jiankang",
  "办法": "banfa",
  "关系": "guanxi",
  "而且": "erqie",
  "角": "jiao",
  "脸": "lian",
  "胖": "pang",
  "其实": "qishi",
  "年级": "nianji",
  "年轻": "nianqing",
  "啤酒": "pijiu",
}

numbers = []
while(len(numbers) < len(vocabulary)):
  print(str(len(numbers))+"/"+str(len(vocabulary)))
  i = random.randint(0,len(vocabulary)-1)
  if i in numbers:
    while i in numbers:
      i += 1
      if i > len(vocabulary)-1:
        i=0

  keys = list(vocabulary.keys())
  print(keys[i])
  answer = input()
  if answer == vocabulary.get(keys[i]):
    numbers.append(i)
  else:
    print("wrong")

print("Test completed")