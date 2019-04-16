# Python Line Bot

## 使用前須知

- `confidential.txt`格式為  
[username]  
[password]
- `line_bot_confidential.txt`格式為  
[CHANNEL_ACCESS_TOKEN]  
[CHANNEL_SECRET]  
[USER_ID]

## 查詢即時股價
  
輸入台灣股票代碼，即可查詢目前該檔股票價格
  
![](https://i.imgur.com/fhc9rO3.png)

## 即時推播目前艙位

當偵測到目標帳戶(預設為期貨帳戶)中的艙位有變動時，立即自動推播  
(使用群益 python API，利用模擬帳戶進行實作)

![](https://i.imgur.com/jge3FHS.png)
