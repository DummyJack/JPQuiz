## 抓取 md 檔

_**User**_

@scratch.py 檔案寫一個讀取 md 檔( @app-開發需求.md )，功能為抓取裡面的的內容(User and Assistant)，再加一個 Feedback 進去，並儲存為一個新的 md 檔

---

_**Assistant**_

我會幫你寫一個程式來讀取和處理 md 檔案。以下是實現代碼：

```python:scratch.py
import re
from datetime import datetime

def read_and_process_md(input_file, output_file):
    try:
        # 讀取輸入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取標題和時間
        title_match = re.search(r'## (.*?)\((.*?)\)', content)
        if title_match:
            title = title_match.group(1).strip()
            timestamp = title_match.group(2).strip()
        else:
            title = "Unknown Title"
            timestamp = datetime.now().strftime("%Y/%m/%d %p%I:%M:%S")

        # 提取 User 和 Assistant 內容
        sections = content.split('

---

_**Feedback**_

---

_**User**_

沒有讀取到 @app-開發需求.md 裡面的內容

---

_**Assistant**_

看起來程式碼中的 `output_content` 變數沒有被初始化。讓我修正這個問題：

````python:scratch.py
# ... existing code ...

        # 生成新的 md 文件內容
        current_time = datetime.now().strftime("%Y/%m/%d %p%I:%M:%S")
        output_content = f"## SpecStory\n\n"  # 添加 SpecStory 標題
        output_content += f"## {title}({timestamp})\n\n"  # 添加原標題和時間戳
        
        for i, conv in enumerate(conversations, 1):
            output_content += f"### Conversation {i}\n\n"
            output_content += f"_**User**_\n\n{conv['user']}\n\n"
            output_content += f"

---

_**Feedback**_

---

_**User**_

抓取 @app-開發需求.md 中的 User 和 Assistant 的內容

---

_**Assistant**_

我注意到問題了。讓我修改程式碼來正確抓取內容：

````python:scratch.py
import re
from datetime import datetime

def read_and_process_md(input_file, output_file):
    try:
        # 讀取輸入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取標題和時間
        title_match = re.search(r'## (.*?)\((.*?)\)', content)
        if title_match:
            title = title_match.group(1).strip()
            timestamp = title_match.group(2).strip()
        else:
            title = "Unknown Title"
            timestamp = datetime.now().strftime("%Y/%m/%d %p%I:%M:%S")

        # 提取 User 和 Assistant 內容
        sections = content.split('

---

_**Feedback**_

---

_**User**_

使用 html_content 這個抓取 User 和 Assistent 裡面的內容

---

_**Assistant**_

我會修改程式碼來使用 `html_content` 來抓取內容：

````python:scratch.py
import markdown
from bs4 import BeautifulSoup
from datetime import datetime

def read_and_process_md(input_file, output_file):
    try:
        # 讀取輸入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 轉換為 HTML
        html_content = markdown.markdown(content)
        
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取標題和時間
        title_text = soup.find_all('h2')[1].text  # 第二個 h2 是標題
        title_parts = title_text.split('(')
        title = title_parts[0].strip()
        timestamp = title_parts[1].replace(')', '').strip()
        
        # 提取對話內容
        conversations = []
        paragraphs = soup.find_all('p')
        
        i = 0
        while i < len(paragraphs):
            if '_**User**_' in paragraphs[i].text:
                user_content = paragraphs[i+1].text if i+1 < len(paragraphs) else ""
                assistant_content = ""
                
                # 尋找對應的 Assistant 內容
                j = i + 2
                while j < len(paragraphs):
                    if '

---

_**Feedback**_

---

_**User**_

@1.py 先做到抓取 @app-開發需求.md  User 和 Asssistant 的內容

---

_**Assistant**_

好的，我來幫你修改程式碼來抓取 User 和 Assistant 的內容：

````python:1.py
import markdown
from bs4 import BeautifulSoup

# 讀取 md 文件
with open(".specstory/history/app-開發需求.md", 'r', encoding='utf-8') as f:
    content = f.read()

# 轉換為 HTML
html_content = markdown.markdown(content)

# 解析 HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 找出所有段落
paragraphs = soup.find_all('p')

# 儲存對話內容
conversations = []
current_conversation = {}

# 遍歷所有段落來提取對話
for p in paragraphs:
    text = p.text.strip()
    if '_**User**_' in text:
        if current_conversation:
            conversations.append(current_conversation)
        current_conversation = {'user': '', 'assistant': ''}
    elif '

---

_**Feedback**_

---

_**User**_

出現錯誤，請修正

---

_**Assistant**_

我看到問題了，讓我修正程式碼：

````python:1.py
import markdown
from bs4 import BeautifulSoup

# 讀取 md 文件
with open(".specstory/history/app-開發需求.md", 'r', encoding='utf-8') as f:
    content = f.read()

# 轉換為 HTML
html_content = markdown.markdown(content)

# 解析 HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 找出所有段落
paragraphs = soup.find_all('p')

# 儲存對話內容
conversations = []
current_conversation = None

# 遍歷所有段落來提取對話
for p in paragraphs:
    text = p.text.strip()
    
    # 當遇到 User 標記時，創建新的對話
    if '_**User**_' in text:
        if current_conversation:
            conversations.append(current_conversation)
        current_conversation = {'user': '', 'assistant': ''}
        continue
        
    # 當遇到 Assistant 標記時，跳過
    if '

---

_**Feedback**_

---

_**User**_

沒有抓到 user 的內容

---

_**Assistant**_

我看到問題了。讓我修改程式碼來正確抓取 user 的內容：

````python:1.py
import markdown
from bs4 import BeautifulSoup

# 讀取 md 文件
with open(".specstory/history/app-開發需求.md", 'r', encoding='utf-8') as f:
    content = f.read()

# 轉換為 HTML
html_content = markdown.markdown(content)

# 解析 HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 儲存對話內容
conversations = []
current_user = None
current_assistant = None

# 遍歷所有文本內容
for element in soup.stripped_strings:
    # 檢查是否為標記
    if '_**User**_' in element:
        # 如果有前一個對話，保存它
        if current_user is not None:
            conversations.append({
                'user': current_user,
                'assistant': current_assistant if current_assistant else ''
            })
        # 重置當前對話
        current_user = None
        current_assistant = None
    elif '

---

_**Feedback**_

---

_**User**_

' in section:
        # 提取 User 內容
        user_content = section.split('

---

_**Assistant**_

" 標記
3. 使用分割方法來提取內容
4. 配對 User 和 Assistant 的內容
5. 改進輸出格式，使其更易讀

中文說明：
修改了内容提取的方式，现在使用 "

---

_**Feedback**_

---

_**User**_

加入 Feedback 這一個進去

---

_**Assistant**_

好的，我來修改程式碼，加入 Feedback 部分：

````python:1.py
import markdown
from bs4 import BeautifulSoup

# 讀取 md 文件
with open(".specstory/history/app-開發需求.md", 'r', encoding='utf-8') as f:
    content = f.read()

# 分割對話區塊
sections = content.split('

---

_**Feedback**_

---

_**User**_

之後功能會手動填寫內容進去 md 檔，所以新增的內容不要直接覆蓋內容，而是用加進去的方式，注意只加入新內容

---

_**Assistant**_

好的，我修改程式碼，改用追加的方式來處理內容：

````python:1.py
import markdown
from bs4 import BeautifulSoup

# 讀取 md 文件
with open(".specstory/history/app-開發需求.md", 'r', encoding='utf-8') as f:
    content = f.read()

# 分割對話區塊
sections = content.split('

---

_**Feedback**_

---

_**User**_

要創立一個新檔案

---

_**Assistant**_

好的，我修改程式碼，將結果寫入新檔案：

````python:1.py
import markdown
from bs4 import BeautifulSoup
from datetime import datetime

# 讀取 md 文件
with open(".specstory/history/app-開發需求.md", 'r', encoding='utf-8') as f:
    content = f.read()

# 分割對話區塊
sections = content.split('

---

_**Feedback**_

---

_**User**_

首先內容要寫進一個新檔案裡面，接下來再用新增的方式加入內容

---

_**Assistant**_

好的，我將程式碼拆分成兩個步驟：

````python:1.py
import markdown
from bs4 import BeautifulSoup
from datetime import datetime
import os

def create_new_file(input_file, output_file):
    # 讀取原始 md 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割對話區塊
    sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
            # 提取 User 內容
            user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n

---

_**Feedback**_

---

_**User**_

Feedback 的位置在 Assistant 下面

---

_**Assistant**_

好的，我修改程式碼，將 Feedback 放在 Assistant 的下面：

````python:1.py
import markdown
from bs4 import BeautifulSoup
from datetime import datetime

def create_new_file(input_file, output_file):
    # 讀取原始 md 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割對話區塊
    sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
            # 提取 User 內容
            user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
        output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

再新增檔案中加入 feedback

---

_**Assistant**_

我來修改程式碼，讓它可以在已有的檔案中加入 feedback：

````python:1.py
def create_new_file(input_file, output_file):
    # 讀取原始 md 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割對話區塊
    sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
            # 提取 User 內容
            user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
        output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

假如已有 output_file，新增的內容則用加入方式寫進檔案中，不要覆蓋裡面的內容

---

_**Assistant**_

好的，我修改程式碼來處理已存在的檔案：

````python:1.py
import os

def create_new_file(input_file, output_file):
    # 如果輸出檔案已存在，則讀取其內容
    existing_content = ""
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        print(f"檔案 {output_file} 已存在，將在檔案末尾添加新內容")
    
    # 讀取原始 md 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割對話區塊
    sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
            # 提取 User 內容
            user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
        output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

新增的內容要判斷是沒有寫進去過的內容，舊內容不需要重複寫進去

---

_**Assistant**_

好的，我修改程式碼來檢查並只添加新內容：

````python:1.py
import os

def create_new_file(input_file, output_file):
    # 讀取原始 md 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割對話區塊
    sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
                    user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
            output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

input_file 為 .specstory/history 中的所有 md 檔案，output_file 改為在 .specstory/feedback/ 中

---

_**Assistant**_

好的，我修改程式碼來處理所有 md 檔案：

````python:1.py
import os

def create_new_file(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
                        user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
                output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

只抓標題

---

_**Assistant**_

好的，我修改程式碼，在新檔案時只抓取標題部分：

````python:1.py
import os

def create_new_file(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
                        user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
                output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

函式重新命名合適這個功能的

---

_**Assistant**_

好的，我將函式名稱修改得更符合功能：

````python:1.py
import os

def process_conversations_and_add_feedback(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
                        user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
                output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

@app-開發需求.md 中的第三行標題(只要這個)判斷是否有寫進新檔案(feedback中的檔案)中，如果沒有，就加進去

---

_**Assistant**_

好的，我修改程式碼來檢查並添加標題：

````python:1.py
import os

def process_conversations_and_add_feedback(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
                        user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
                output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

去掉時間

---

_**Assistant**_

好的，我修改程式碼來去掉標題中的時間：

````python:1.py
import os

def process_conversations_and_add_feedback(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
                        user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
                output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

標題不需要後面括號鐘的時間

---

_**Assistant**_

好的，我修改程式碼來處理標題，去掉括號中的時間：

`````python:1.py
import os

def process_conversations_and_add_feedback(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
                        user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
                output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

剛剛抓取的 title 把時間去掉

---

_**Assistant**_

好的，我修改程式碼來去掉標題中的時間：

````python:1.py
import os

def process_conversations_and_add_feedback(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

' in section:
                        user_content = section.split('

---

_**Assistant**_

\n\n{conv['assistant']}\n\n"
                output_content += f"_**Feedback**_\n\n請在此處填寫反饋...\n\n

---

_**Feedback**_

---

_**User**_

接下來做程式碼處理，md 檔案中會寫進程式碼，但程式碼只是修改一小部分，那需要把那一小段提取出來替代現有

---

_**Assistant**_

好的，我來修改程式碼來處理 md 檔案中的程式碼片段：

````python:1.py
import os
import re

def process_conversations_and_add_feedback(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

先把 input_file 中的 md 檔案中的程式碼區塊抓出來

---

_**Assistant**_

好的，我修改程式碼來提取 md 檔案中的程式碼區塊：

````python:1.py
import os
import re

def process_conversations_and_add_feedback(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

測試這個 extract_code_blocks 函式

---

_**Assistant**_

好的，我來新增測試程式碼：

````python:1.py
import os
import re

def process_conversations_and_add_feedback(input_dir, output_dir):
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入和輸出檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        output_file = input_file.replace('.md', '-with-feedback.md')
        output_path = os.path.join(output_dir, output_file)
        
        # 讀取原始 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

把 md 檔案中的程式碼區塊都 print 出來

---

_**Assistant**_

好的，我修改程式碼來印出 md 檔案中的所有程式碼區塊：

````python:1.py
import os
import re

def extract_code_blocks(input_dir):
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        
        # 讀取 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

_**User**_

程式碼提取只要程式碼就好，不用檔案和語言

---

_**Assistant**_

好的，我修改程式碼只提取程式碼內容：

````python:1.py
import os
import re

def extract_code_blocks(input_dir):
    # 取得所有 md 檔案
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    for input_file in md_files:
        # 設定輸入檔案的完整路徑
        input_path = os.path.join(input_dir, input_file)
        
        # 讀取 md 文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割對話區塊
        sections = content.split('

---

_**Feedback**_

---

