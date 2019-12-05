#!/usr/bin/env python
# coding: utf-8
'''
整體功能描述
Application 主架構
'''

# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入json處理套件
import json

# 載入基礎設定檔
secretFileContentJson=json.load(open("./line_secret_key",'r',encoding='utf8'))
server_url=secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/素材" , static_folder = "./素材/")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


'''

消息判斷器

讀取指定的json檔案後，把json解析成不同格式的SendMessage

讀取檔案，
把內容轉換成json
將json轉換成消息
放回array中，並把array傳出。

'''

# 引用會用到的套件
from linebot.models import (
    ImagemapSendMessage,TextSendMessage,ImageSendMessage,LocationSendMessage,FlexSendMessage,VideoSendMessage
)

from linebot.models.template import (
    ButtonsTemplate,CarouselTemplate,ConfirmTemplate,ImageCarouselTemplate
    
)

from linebot.models.template import *

def detect_json_array_to_new_message_array(fileName):
    
    #開啟檔案，轉成json
    with open(fileName) as f:
        jsonArray = json.load(f)
    
    # 解析json
    returnArray = []
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')
        
        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'video':
            returnArray.append(VideoSendMessage.new_from_json_dict(jsonObject))    


    # 回傳
    return returnArray


# In[42]:


'''

handler處理關注消息

用戶關注時，讀取 素材 -> 關注 -> reply.json

將其轉換成可寄發的消息，傳回給Line

'''

# 引用套件
from linebot.models import (
    FollowEvent
)

# 關注事件處理
@handler.add(FollowEvent)
def process_follow_event(event):
    
    # 讀取並轉換
    result_message_array =[]
    replyJsonPath = "素材/關注/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

    # 消息發送
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )


# In[43]:


'''

準備QuickReply的Button


'''

# 引入相關套件
from linebot.models import (
    MessageAction, PostbackAction,
    URIAction,
    QuickReply, QuickReplyButton
)

# 創建QuickReplyButton 

# QuickReplyButton(action)
# Action(label= , 依照不同Action會有不同參數。)

## 點擊後，以用戶身份發送文字消息
## MessageAction
#No
textQuickReplyButton_NO = QuickReplyButton(
    action=MessageAction(
        label="不要", 
        text="去別的地方看看吧"
    )
)
#上個廁所
textQuickReplyButton_toilet = QuickReplyButton(
    action=MessageAction(
        label="打開水箱", 
        text="打開水箱"
    )
)
#坐上椅子
textQuickReplyButton_chair = QuickReplyButton(
    action=MessageAction(
        label="撿起紙條", 
        text="撿起紙條"
    )
)
#打開洗衣機
textQuickReplyButton_wash_1 = QuickReplyButton(
    action=PostbackAction(
        label="要", 
        text="拿衣服，發現底部有五塊錢",
        data="menu=rich_menu_bal2"
    )
)
#打開洗衣機
textQuickReplyButton_wash_2 = QuickReplyButton(
    action=PostbackAction(
        label="要", 
        text="拿衣服，發現底部有五十塊錢",
        data="menu=rich_menu_bal2"
    )
)

#洗手台上有面鏡子
textQuickReplyButton_mirror = QuickReplyButton(
    action=MessageAction(
        label="打開它", 
        text="只有發現一面口罩"
    )
)
#發現一顆大冰塊
textQuickReplyButton_ice = QuickReplyButton(
    action=MessageAction(
        label="要", 
        text="融化了"
    )
)
#翻找衣服
textQuickReplyButton_key_1 = QuickReplyButton(
    action=PostbackAction(
        label="要", 
        text="前往書房",
        data="menu=rich_menu_book"
    )
)
textQuickReplyButton_key_2 = QuickReplyButton(
    action=PostbackAction(
        label="要", 
        text="前往書房，發現打不開！\n衣服裡好像還有別的鑰匙，再回去拿吧",
        data="menu=rich_menu_room"
    )
)
#民主 不能使用url
#textQuickReplyButton_dem = QuickReplyButton(
#    action=URIAction(
#        label="好，我要離開", 
#        uri="https://www.thenewslens.com/article/127718"
#    )
#)


# In[44]:


'''

以QuickReply封裝該些QuickReply Button

'''
## 設計QuickReplyButton的List
#上個廁所
quickReplyList_toilet = QuickReply(
    items = [textQuickReplyButton_toilet, textQuickReplyButton_NO]
)
#坐上椅子
quickReplyList_chair = QuickReply(
    items = [textQuickReplyButton_chair, textQuickReplyButton_NO]
)
#打開洗衣機
quickReplyList_wash_1 = QuickReply(
    items = [textQuickReplyButton_wash_1, textQuickReplyButton_NO]
)
quickReplyList_wash_2 = QuickReply(
    items = [textQuickReplyButton_wash_2, textQuickReplyButton_NO]
)

#洗手台上有面鏡子
quickReplyList_mirror = QuickReply(
    items = [textQuickReplyButton_mirror, textQuickReplyButton_NO]
)

#發現一顆大冰塊
quickReplyList_ice = QuickReply(
    items = [textQuickReplyButton_ice, textQuickReplyButton_NO]
)

#翻找衣服
quickReplyList_key_1 = QuickReply(
    items = [textQuickReplyButton_key_1, textQuickReplyButton_NO]
)
quickReplyList_key_2 = QuickReply(
    items = [textQuickReplyButton_key_2, textQuickReplyButton_NO]
)

#民主
#quickReplyList_dem = QuickReply(
#    items = [textQuickReplyButton_dem, textQuickReplyButton_NO]
#)


# In[45]:


'''

製作TextSendMessage，並將剛封裝的QuickReply放入

'''
## 將quickReplyList 塞入TextSendMessage 中 
from linebot.models import (
    TextSendMessage,
)

quickReplyTextSendMessage_toilet = TextSendMessage(text='沖水時，水箱的聲音有點特別，要打開看看嗎？',
                                                   quick_reply=quickReplyList_toilet)

quickReplyTextSendMessage_chair = TextSendMessage(text='坐上椅子，望著書櫃，突然發現角落好像有張紙',
                                                   quick_reply=quickReplyList_chair)

quickReplyTextSendMessage_wash_1 = TextSendMessage(text='有一堆衣服\n你要晾衣服嗎？',
                                                   quick_reply=quickReplyList_wash_1)
quickReplyTextSendMessage_wash_2 = TextSendMessage(text='有一堆衣服\n你要晾衣服嗎？',
                                                   quick_reply=quickReplyList_wash_2)

quickReplyTextSendMessage_mirror = TextSendMessage(text='鏡子映照出自己的臉，卻不是很清楚，鏡子後方有個小櫃子',
                                                   quick_reply=quickReplyList_mirror)

quickReplyTextSendMessage_ice = TextSendMessage(text='冰塊內好像有東西，要開火融化它嗎？',
                                                   quick_reply=quickReplyList_ice)

quickReplyTextSendMessage_key_1 = TextSendMessage(text='從一件褲子口袋中找到一把鑰匙，上面寫著S，好像是書房鑰匙？要試試看嗎？',
                                                   quick_reply=quickReplyList_key_1)
quickReplyTextSendMessage_key_2 = TextSendMessage(text='從一件褲子口袋中找到一把鑰匙，上面寫著B，難道是書房鑰匙？要試試看嗎？',
                                                   quick_reply=quickReplyList_key_2)

#quickReplyTextSendMessage_dem = TextSendMessage(text='終於解開門鎖，要離開房間嗎？',
#                                                   quick_reply=quickReplyList_dem)


# In[46]:


'''
設計一個字典

'''
template_message_dict = {
    "上個廁所":quickReplyTextSendMessage_toilet,
    "坐上椅子":quickReplyTextSendMessage_chair,
    #"打開洗衣機":quickReplyTextSendMessage_wash,
    "洗手台上有面鏡子":quickReplyTextSendMessage_mirror,
    "發現一顆大冰塊":quickReplyTextSendMessage_ice
    #"翻找衣服":quickReplyTextSendMessage_key
    #"民主":quickReplyTextSendMessage_dem
}


# In[47]:


'''

handler處理文字消息

收到用戶回應的文字消息，
按文字消息內容，往素材資料夾中，找尋以該內容命名的資料夾，讀取裡面的reply.json

轉譯json後，將消息回傳給用戶

'''

# 引用套件
from linebot.models import (
    MessageEvent, TextMessage
)

# 文字消息處理
@handler.add(MessageEvent,message=TextMessage)
def process_text_message(event):
    # 發送
    if event.message.text == "打開洗衣機":
        import random
        a = random.randint(1,2)
        if a == 1:
            line_bot_api.reply_message(
                event.reply_token,
                quickReplyTextSendMessage_wash_1
            )
        elif a == 2:
            line_bot_api.reply_message(
                event.reply_token,
                quickReplyTextSendMessage_wash_2
            )
    elif event.message.text == "翻找衣服":
        import random
        a = random.randint(1,2)
        if a == 1:
            line_bot_api.reply_message(
                event.reply_token,
                quickReplyTextSendMessage_key_1
            )
        elif a == 2:
            line_bot_api.reply_message(
                event.reply_token,
                quickReplyTextSendMessage_key_2
            )
    elif event.message.text in template_message_dict.keys():
        line_bot_api.reply_message(
            event.reply_token,
            template_message_dict.get(event.message.text)
        )
    elif event.message.text == "躺入浴缸，為什麼我會被困在這呢？":
        import random
        a = random.randint(1,2)
        if a == 1:
            pass
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="門外傳來聲音：\n若有來世\n你還願意嗎")
            )
    elif event.message.text == "望向梳妝台":
        import random
        a = random.randint(1,2)
        result_message_array =[]
        replyJsonPath = "素材/"+event.message.text+str(a)+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )
    else: 
        # 讀取本地檔案，並轉譯成消息
        result_message_array =[]
        replyJsonPath = "素材/"+event.message.text+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )


# In[48]:


'''

handler處理Postback Event

載入功能選單與啟動特殊功能

解析postback的data，並按照data欄位判斷處理

現有三個欄位
menu, folder, tag

若folder欄位有值，則
    讀取其reply.json，轉譯成消息，並發送

若menu欄位有值，則
    讀取其rich_menu_id，並取得用戶id，將用戶與選單綁定
    讀取其reply.json，轉譯成消息，並發送

'''
from linebot.models import (
    PostbackEvent
)

from urllib.parse import parse_qs 

@handler.add(PostbackEvent)
def process_postback_event(event):
    


    query_string_dict = parse_qs(event.postback.data)
    
    print(query_string_dict)
    if 'folder' in query_string_dict:
    
        result_message_array =[]

        replyJsonPath = '素材/'+query_string_dict.get('folder')[0]+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
  
        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )
    elif 'menu' in query_string_dict:
 
        linkRichMenuId = open("素材/"+query_string_dict.get('menu')[0]+'/rich_menu_id', 'r').read()
        line_bot_api.link_rich_menu_to_user(event.source.user_id,linkRichMenuId)
        
        replyJsonPath = '素材/'+query_string_dict.get('menu')[0]+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
  
        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )


# In[49]:


'''

Application 運行（開發版）


if __name__ == "__main__":
    app.run(host='0.0.0.0')


# In[50]:




Application 運行（heroku版）

'''

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])


# In[ ]:




