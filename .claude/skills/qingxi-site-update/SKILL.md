---
name: qingxi-site-update
description: 更新青溪里里長辦公室網站（GitHub Pages）的內容：從里長臉書補齊活動紀錄／公告／里務進度與照片、更新垃圾車時刻、檢查常用連結，然後重建頁面並推上線。使用者說「臉書有新貼文要補」「更新網站內容」「垃圾車時間變了」「連結打不開」時使用。
---

# 青溪里網站內容更新

網站：https://a8594755-maker.github.io/qingxi-service/（repo `a8594755-maker/qingxi-service`，main 分支根目錄即網站，推上去約 1 分鐘自動上線）。
里長：李詠芳（桃園市中壢區青溪里，無黨籍）。使用者是里長的家人，已授權：網站更新可直接 commit 並 push 到 main；臉書上的照片可下載使用。

## 檔案地圖

| 檔案 | 用途 |
|---|---|
| `tools/content.py` | **所有內容資料**：ACTS 活動、NEWS 公告、PROG 里務進度、HOME_CARDS、FACTS、PLACES、LINKS 常用連結、TRASH_POINTS 垃圾車點 |
| `tools/build.py` | 版型產生器，產生 6 個 HTML。一般更新不用改 |
| `tools/fetch_garbage.py` | 從市府垃圾清運系統重新查青溪里清運點 |
| `tools/check_links.py` | 檢查所有對外連結 |
| `*.html` | 產生出來的，**不要手改**，改 content.py 後重建 |
| `assets/css/site.css`、`assets/js/site.js` | 樣式與互動（紙與墨配色，不用紅綠藍政黨色） |
| `images/` | 網站用照片，命名 `主題-年份.jpg`。純數字檔名（如 `28897216496559900.jpg`）是臉書匯出原檔，不要 commit |
| `fb_data/`、`facebook-cocolee58-*.zip` | 臉書資料匯出（gitignore，不上傳） |

重建（專案根目錄，Windows 一定要設編碼）：
```bash
PYTHONIOENCODING=utf-8 python tools/build.py
```

## 流程

### 0. 先同步
`git pull`。看 `tools/content.py` 裡 ACTS 與 NEWS 最新一筆的日期——那就是「補到哪裡」的起點。

### 1. 找臉書上缺的內容（依序）
1. **臉書資料匯出**（`fb_data/your_facebook_activity/posts/your_posts__check_ins__photos_and_videos_1.json`）：只涵蓋到匯出日（檔名日期），比那更新的一定要看線上。文字是亂碼，要 `text.encode('latin1').decode('utf8')` 還原；`timestamp` 是 Unix 秒。
2. **線上臉書**（用 Claude in Chrome，使用者的 Chrome 已登入）：
   - 里長個人頁（主要來源，里務貼文幾乎都在這）：https://www.facebook.com/coco.lee.58
   - 里辦粉絲專頁：https://www.facebook.com/profile.php?id=100083187639806
   - 相簿（找清楚的照片、大頭貼）：https://www.facebook.com/coco.lee.58/photos_albums
   - 從最新往回捲到 content.py 最新日期為止，把每則貼文列成清單：日期、標題、類別、是否可用、要不要照片。
3. 先把「建議新增清單」給使用者看數量與標題，再動手（使用者想全部補就全部補）。

### 2. 篩選規則（哪些能放）
- **放**：里務（道路、路燈、排水、交通、治安、會勘、爭取建設）、防災與消毒公告、節慶活動、長者與弱勢關懷、環保志工、公益講座、社區發展協會、運動社團、市府／區公所政策宣導。
- **不放**：里長私人生活與家庭、商業店家推薦或業配、以未成年人為主角的內容、其他政治人物的名字、任何與選舉有關的內容（里長已登記 2026 參選，網站頁尾註明「非選舉宣傳用途」，不能有拉票味道）。
- 拿不準就先不放，列出來問使用者。

### 3. 寫進 content.py
- 用「里長」第三人稱，平實溫暖；改寫摘要，不整段照抄；不放 emoji、hashtag。
- `ACTS`：`(id, 'images/x.jpg' 或 None, 分類, 標籤, 'YYYY/MM/DD', 標題, 替代文字, 圖片位置 'center 40%', 內文)`，新的放最前面。分類：festival／care／eco／sport／learn／meeting。
- `NEWS`：`(狀態, 分類, 標籤樣式, 標籤, 日期, 標題, 內文)`，狀態 `up`（即將舉辦）／`notice`／`past`。**活動日過了要把 `up` 改成 `past`**，不然網站會顯示過期的「即將舉辦」。
- `PROG`：里務進度有新進展就更新狀態（going／done／urgent）。
- `HOME_CARDS`：首頁顯示的活動 id，換成最新的七則。

### 4. 照片
- 在臉書貼文裡點開照片取大圖。臉書圖片網址帶 query string 會被工具擋，改在頁面裡 `fetch(img.src)` 取 blob，全部打包成**一個** JSON（base64）用 `<a download>` 下載到「下載」資料夾，再用 Python 解出來。一次下載一個檔，Chrome 才不會擋多重下載（若被擋，請使用者允許）。
- 貼文用 `document.querySelectorAll('[aria-posinset]')` 找，用貼文內文關鍵字定位。臉書的日期在 DOM 裡是亂碼，要用截圖放大看。
- 選大合照或活動現場，不選食物、飲料等細節照。**里長本人照片一定要對過**：`images/chief-portrait.jpg` 是正式照；不要憑臉猜，找賀卡上印「青溪里里長 李詠芳」的圖或大頭貼相簿確認。
- 用 PIL 處理：寬最多 1200（直式最多高 960）、JPEG quality 82，檔名 `主題-年份.jpg`。
- 下載資料夾裡用完的 `qingxi-*` 檔案提醒使用者自行刪除。

### 5. 重建、檢查
1. `PYTHONIOENCODING=utf-8 python tools/build.py`
2. 預覽：暫時建立 `.claude/launch.json`（`python -m http.server 8765`），用內建瀏覽器看桌面版與手機版（375 寬）；**commit 前刪掉 launch.json**。內建瀏覽器截圖若是空白（視窗在後面），改用 JS 檢查元素。
3. `PYTHONIOENCODING=utf-8 python tools/check_links.py`；失敗的網址用瀏覽器實際開一次再判斷（政府網站常很慢）。

### 6. 上線
`git add` 相關檔案（不要加數字檔名的照片、fb_data、zip）→ commit（中文訊息）→ `git push origin main` → 約 1 分鐘後用 curl 或瀏覽器確認線上版已更新。

## 垃圾車時刻（生活資訊頁）
- `PYTHONIOENCODING=utf-8 python tools/fetch_garbage.py` → 把結果更新到 `content.py` 的 `TRASH_POINTS`，並改註解裡的查詢日期與 build.py 內 TRASH_HTML 的「資料來源（日期）」。
- `run_type` 七碼，第 i 碼 = 星期（0 = 週日）：`0` 停收、`1` 只收垃圾、`2` 垃圾＋資源回收。目前青溪里 `0221222` ＝ 一般垃圾週一至週六、資源回收週一二四五六、週日停收。
- 清運點是否屬青溪里看班表 API（`lagifQueryTimeTableDetailByRoute`）的 `memo`；即時 API 收運結束後不帶 memo，不要用它判斷。
- 大樓「社區專車」點沒有里別標示，不列入；網站文字請住戶洽管委會。
- 官方網站禁止 iframe、沒開 CORS，所以網頁不能直接即時讀官方資料；即時位置只能連到 https://route.tyoem.gov.tw/ 或「桃園垃圾車」App。
- 其他：錯過垃圾車 → 中壢區中隊 華美一路 90 號，週一至週六 07:00–22:00；環保局 24h 0800-090-922。

## 常用連結
- 在 `content.py` 的 `LINKS`，維持**偶數**個（版面兩欄）。每個新網址都要實際打開確認。
- 已知失效、不要再用：cscp.tycg.gov.tw、eservices.tycg.gov.tw、law-free.tycg.gov.tw、socab.tycg.gov.tw、citybus.tycg.gov.tw、service.taipower.com.tw/nds、taotalk.tycg.gov.tw（2026/09 無法連線）。
- 找替代網址：先搜尋引擎，再用瀏覽器實際開；區公所網站（zhongli.tycg.gov.tw）的「生活資訊」頁通常最穩定。

## 常見坑
- Windows 印中文會 cp1252 錯誤 → 一律 `PYTHONIOENCODING=utf-8`。
- bash heredoc 放長內容容易壞 → 大檔案用 Write 工具。
- 公告頁「即將舉辦」會過期 → 每次更新都掃一遍 NEWS 的 `up`。
