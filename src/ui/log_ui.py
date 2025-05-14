from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

from functions.log_function import LogFunctions

class LogUI:
    def __init__(self):
        """初始化日誌界面"""
        self.log_function = LogFunctions()
    
    def show_logs(self, instance):
        """顯示歷史記錄"""
        logs = self.log_function.get_all_logs()
        
        # 創建容器佈局
        content_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=[0, dp(20), 0, 0])
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        if not logs:
            label = Label(
                text="暫無遊戲記錄",
                font_name="NotoSansTC",
                size_hint_y=None,
                height=dp(40),
                halign='center'
            )
            label.bind(size=label.setter('text_size'))
            content_layout.add_widget(label)
        else:
            # 添加標題行
            header = GridLayout(cols=4, size_hint_y=None, height=dp(50))
            
            for title in ["難度", "分數", "日期", "詳情紀錄"]:
                lbl = Label(
                    text=title, 
                    font_name="NotoSansTC", 
                    bold=True, 
                    halign='center',
                    valign='middle'
                )
                lbl.bind(size=lbl.setter('text_size'))
                header.add_widget(lbl)
                
            content_layout.add_widget(header)
            
            # 添加每條日誌記錄
            for log in logs:
                row = GridLayout(cols=4, size_hint_y=None, height=dp(60))
                
                # 難度
                level = f"N{log.get('level', 5)}"
                level_lbl = Label(
                    text=level, 
                    font_name="NotoSansTC",
                    size_hint_x=0.15,
                    halign='center',
                    valign='middle'
                )
                level_lbl.bind(size=level_lbl.setter('text_size'))
                row.add_widget(level_lbl)
                
                # 分數
                score = f"{log.get('correct_answers', 0)}/{log.get('total_questions', 0)}"
                score_lbl = Label(
                    text=score, 
                    font_name="NotoSansTC",
                    size_hint_x=0.15,
                    halign='center',
                    valign='middle'
                )
                score_lbl.bind(size=score_lbl.setter('text_size'))
                row.add_widget(score_lbl)
                
                # 時間（只顯示日期）
                timestamp = self.log_function.format_timestamp(log.get("timestamp", ""), date_only=True)
                date_lbl = Label(
                    text=timestamp, 
                    font_name="NotoSansTC",
                    size_hint_x=0.35,
                    halign='center',
                    valign='middle'
                )
                date_lbl.bind(size=date_lbl.setter('text_size'))
                row.add_widget(date_lbl)
                
                # 詳情按鈕
                details_btn_container = GridLayout(cols=1, size_hint_x=0.35)
                details_btn = Button(
                    text="查看",
                    font_name="NotoSansTC",
                    size_hint=(0.5, 0.7),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    background_color=(0.4, 0.5, 0.9, 1)
                )
                details_btn.log_id = log.get("_id")  # 保存日誌ID
                details_btn.bind(on_press=self.show_log_details)
                details_btn_container.add_widget(details_btn)
                row.add_widget(details_btn_container)
                
                content_layout.add_widget(row)
        
        # 創建滾動視圖
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(content_layout)
        
        # 創建無邊框的彈出窗口
        popup = Popup(
            content=scroll_view,
            size_hint=(0.9, 0.8),
            title="",
            separator_height=0,  # 移除分隔線
            background_color=(0.15, 0.15, 0.2, 1)  # 設置與應用相同的背景色
        )
        popup.open()
    
    def show_log_details(self, instance):
        """顯示特定日誌的詳細信息"""
        log_id = instance.log_id
        log = self.log_function.get_log_by_id(log_id)
        
        if not log:
            return
        
        # 創建容器佈局
        content_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=[0, dp(20), 0, 0])
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # 創建問題標題行
        questions_header = GridLayout(cols=3, size_hint_y=None, height=dp(40))
        
        for title in ["日文", "中文", "結果"]:
            lbl = Label(
                text=title, 
                font_name="NotoSansTC", 
                bold=True, 
                halign='center',
                valign='middle'
            )
            lbl.bind(size=lbl.setter('text_size'))
            questions_header.add_widget(lbl)
            
        content_layout.add_widget(questions_header)
        
        # 添加每個問題的詳細信息
        for question in log.get("questions", []):
            question_row = GridLayout(cols=3, size_hint_y=None, height=dp(50))
            
            # 日文單詞
            jp_lbl = Label(
                text=question.get("japanese", ""),
                font_name="NotoSansTC",
                halign='center',
                valign='middle'
            )
            jp_lbl.bind(size=jp_lbl.setter('text_size'))
            question_row.add_widget(jp_lbl)
            
            # 中文意思
            cn_lbl = Label(
                text=question.get("meaning", ""),
                font_name="NotoSansTC",
                halign='center',
                valign='middle'
            )
            cn_lbl.bind(size=cn_lbl.setter('text_size'))
            question_row.add_widget(cn_lbl)
            
            # 答題結果
            result_text = "✓" if question.get("is_correct", False) else "X"
            result_color = (0.2, 0.8, 0.2, 1) if question.get("is_correct", False) else (0.8, 0.2, 0.2, 1)
            result_label = Label(
                text=result_text,
                font_name="NotoSansTC",
                color=result_color,
                bold=True,
                halign='center',
                valign='middle'
            )
            result_label.bind(size=result_label.setter('text_size'))
            question_row.add_widget(result_label)
            
            content_layout.add_widget(question_row)
        
        # 創建滾動視圖
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(content_layout)
        
        # 創建無邊框的彈出窗口
        popup = Popup(
            content=scroll_view,
            size_hint=(0.9, 0.8),
            title="",
            separator_height=0,  # 移除分隔線
            background_color=(0.15, 0.15, 0.2, 1)  # 設置與應用相同的背景色
        )
        popup.open()