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
        sections = content.split('---')
        new_conversations = []

        # 提取第三行標題
        title_section = sections[0]
        title_lines = title_section.strip().split('\n')
        main_title = None
        for line in title_lines:
            if '(' in line and ')' in line and line.startswith('## '):
                main_title = line.split('(')[0].strip()  # 只保留括號前的部分
                break

        # 如果輸出檔案已存在，檢查標題
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                output_content = f.read()
                # 如果標題不存在，添加到開頭
                if main_title and main_title not in output_content:
                    output_content = f"{main_title}\n\n{output_content}"
        else:
            # 如果是新檔案，加入標題
            output_content = f"{main_title}\n\n" if main_title else ""

        # 處理每個區塊，提取新的對話
        for section in sections:
            if '_**User**_' in section:
                # 提取 User 內容
                user_content = section.split('_**User**_')[1].strip()
                # 尋找下一個區塊的 Assistant 內容
                next_section = sections[sections.index(section) + 1]
                if '_**Assistant**_' in next_section:
                    assistant_content = next_section.split('_**Assistant**_')[1].strip()
                    # 儲存對話
                    new_conversations.append({
                        'user': user_content,
                        'assistant': assistant_content
                    })

        # 檢查現有對話
        existing_conversations = []
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
                existing_sections = existing_content.split('---')
                for section in existing_sections:
                    if '_**User**_' in section:
                        user_content = section.split('_**User**_')[1].strip()
                        existing_conversations.append(user_content)

        # 只添加新的對話
        for conv in new_conversations:
            if conv['user'] not in existing_conversations:
                output_content += f"_**User**_\n\n{conv['user']}\n\n---\n\n"
                output_content += f"_**Assistant**_\n\n{conv['assistant']}\n\n---\n\n"
                output_content += f"_**Feedback**_\n\n---\n\n"

        # 寫入檔案
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        print(f"已處理檔案：{output_file}")

if __name__ == "__main__":
    input_dir = ".specstory/history"
    output_dir = ".specstory/feedback"
    
    # 處理所有檔案
    process_conversations_and_add_feedback(input_dir, output_dir)
    print(f"已完成所有檔案的處理")
