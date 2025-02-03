对于获取对应话数的方法暂且有两种

一种是直接进行搜索 

e.g. `https://bbs.yamibo.com/search.php?mod=forum&searchid=21177&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw=CARNEADES`

一种是汉化组创建了tag进行搜索

e.g. `https://bbs.yamibo.com/misc.php?mod=tag&id=8812&type=thread&page=2`

对于这两种情况可以在第一次用户下载前先让用户填写相关信息，如列表情况为：
```text
[悠悠式] 完结杀猫
【汉化工房九九组】[三上小又]悠悠式 第18话
【汉化工房九九组】[三上小又]悠悠式 第17话
【汉化工房九九组】[三上小又]悠悠式 第16话
【汉化工房九九组】[三上小又]悠悠式 第15话
【汉化工房九九组】[三上小又]悠悠式 第14话及1卷尾页 
```
这种情况下，可以让用户手动填写正则表达式e.g. `{前置信息}{作品名}`

将所有不相关信息去除后提取第一个“第”或数字之后的所有字符串就为当前的话数名

并将相关信息存储到数据库中以供之后进行使用