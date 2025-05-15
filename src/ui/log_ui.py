from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
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
        
        # 創建浮動佈局作為根佈局
        root_layout = FloatLayout()
        
        # 關閉按鈕
        close_button = Button(
            text="X",
            size_hint=(0.08, 0.06),
            pos_hint={'right': 0.98, 'top': 0.98},
            background_color=(0.7, 0.7, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        root_layout.add_widget(close_button)
        
        # 創建垂直佈局包含標題和表格
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(0.95, 0.9),
            pos_hint={'center_x': 0.5, 'top': 0.97}
        )
        
        # 標題標籤
        title_label = Label(
            text="歷史記錄",
            font_name="NotoSansTC",
            font_size=dp(24),
            bold=True,
            size_hint=(1, None),
            height=dp(40),
            halign='center'
        )
        
        # 添加標題到主佈局
        main_layout.add_widget(title_label)
        
        # 表格佈局
        table_layout = BoxLayout(
            orientation='vertical',
            spacing=0,
            size_hint=(1, 1)
        )
        
        # 表格標題行（帶背景顏色）
        header = GridLayout(cols=4, size_hint_y=None, height=dp(50))
        with header.canvas.before:
            Color(0.25, 0.25, 0.35, 1)  # 設置標題背景顏色
            self.header_bg = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self._update_header_rect, size=self._update_header_rect)
        
        titles = ["難度", "分數", "日期", "詳情紀錄"]
        widths = [0.15, 0.15, 0.35, 0.35]  # 定義各列寬度比例
        
        for i, title in enumerate(titles):
            header_container = GridLayout(cols=1, size_hint_x=widths[i])
            lbl = Label(
                text=title, 
                font_name="NotoSansTC", 
                bold=True, 
                halign='center',
                valign='middle',
                size_hint=(1, 1)
            )
            lbl.bind(size=lbl.setter('text_size'))
            header_container.add_widget(lbl)
            header.add_widget(header_container)
        
        # 添加表格標題到表格佈局
        table_layout.add_widget(header)
        
        # 創建容器佈局用於滾動內容
        scroll_content = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=[0, dp(10), 0, dp(10)])
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        
        if not logs:
            label = Label(
                text="暫無遊戲記錄",
                font_name="NotoSansTC",
                size_hint_y=None,
                height=dp(40),
                halign='center'
            )
            label.bind(size=label.setter('text_size'))
            scroll_content.add_widget(label)
        else:
            # 添加每條日誌記錄
            for log in logs:
                row = GridLayout(cols=4, size_hint_y=None, height=dp(60))
                
                # 難度
                level = f"N{log.get('level', 5)}"
                level_container = GridLayout(cols=1, size_hint_x=widths[0])
                level_lbl = Label(
                    text=level, 
                    font_name="NotoSansTC",
                    font_size=dp(20),
                    halign='center',
                    valign='middle',
                    size_hint=(1, 1)
                )
                level_lbl.bind(size=level_lbl.setter('text_size'))
                level_container.add_widget(level_lbl)
                row.add_widget(level_container)
                
                # 分數
                score = f"{log.get('correct_answers', 0)}/{log.get('total_questions', 0)}"
                score_container = GridLayout(cols=1, size_hint_x=widths[1])
                score_lbl = Label(
                    text=score, 
                    font_name="NotoSansTC",
                    font_size=dp(20),
                    halign='center',
                    valign='middle',
                    size_hint=(1, 1)
                )
                score_lbl.bind(size=score_lbl.setter('text_size'))
                score_container.add_widget(score_lbl)
                row.add_widget(score_container)
                
                # 時間（只顯示日期）
                timestamp = self.log_function.format_timestamp(log.get("timestamp", ""), date_only=True)
                date_container = GridLayout(cols=1, size_hint_x=widths[2])
                date_lbl = Label(
                    text=timestamp, 
                    font_name="NotoSansTC",
                    font_size=dp(20),
                    halign='center',
                    valign='middle',
                    size_hint=(1, 1)
                )
                date_lbl.bind(size=date_lbl.setter('text_size'))
                date_container.add_widget(date_lbl)
                row.add_widget(date_container)
                
                # 詳情按鈕
                details_btn_container = GridLayout(cols=1, size_hint_x=widths[3])
                details_btn = Button(
                    text="查看",
                    font_name="NotoSansTC",
                    font_size=dp(18),  # 縮小字體
                    size_hint=(0.35, 0.5),  # 縮小按鈕
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    background_color=(0.4, 0.5, 0.9, 1)
                )
                details_btn.log_id = log.get("_id")  # 保存日誌ID
                details_btn.bind(on_press=self.show_log_details)
                details_btn_container.add_widget(details_btn)
                row.add_widget(details_btn_container)
                
                scroll_content.add_widget(row)
        
        # 創建滾動視圖
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False, 
            do_scroll_y=True,
            scroll_y=1  # 1 表示初始滾動位置在頂部
        )
        scroll_view.add_widget(scroll_content)
        
        # 添加滾動視圖到表格佈局
        table_layout.add_widget(scroll_view)
        
        # 添加表格佈局到主佈局
        main_layout.add_widget(table_layout)
        
        # 添加主佈局到根佈局
        root_layout.add_widget(main_layout)
        
        # 創建無邊框的彈出窗口
        popup = Popup(
            content=root_layout,
            size_hint=(0.9, 0.8),
            title="",
            separator_height=0,  # 移除分隔線
            background_color=(0.18, 0.18, 0.25, 1)  # 設置較亮的深藍灰色背景
        )
        
        # 綁定關閉按鈕事件
        close_button.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def _update_header_rect(self, instance, value):
        """更新表格標題背景矩形的大小和位置"""
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size
    
    def show_log_details(self, instance):
        """顯示特定日誌的詳細信息"""
        log_id = instance.log_id
        log = self.log_function.get_log_by_id(log_id)
        
        if not log:
            return
        
        # 創建浮動佈局作為根佈局
        root_layout = FloatLayout()
        
        # 關閉按鈕
        close_button = Button(
            text="X",
            size_hint=(0.08, 0.06),
            pos_hint={'right': 0.98, 'top': 0.98},
            background_color=(0.7, 0.7, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        root_layout.add_widget(close_button)
        
        # 創建垂直佈局包含標題和表格
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(0.95, 0.9),
            pos_hint={'center_x': 0.5, 'top': 0.97}
        )
        
        # 標題標籤
        title_label = Label(
            text="詳細記錄",
            font_name="NotoSansTC",
            font_size=dp(22),
            bold=True,
            size_hint=(1, None),
            height=dp(40),
            halign='center'
        )
        
        # 添加標題到主佈局
        main_layout.add_widget(title_label)
        
        # 表格佈局
        table_layout = BoxLayout(
            orientation='vertical',
            spacing=0,
            size_hint=(1, 1)
        )
        
        # 表格標題行（帶背景顏色）
        questions_header = GridLayout(cols=3, size_hint_y=None, height=dp(50))
        with questions_header.canvas.before:
            Color(0.25, 0.25, 0.35, 1)  # 設置標題背景顏色
            self.questions_header_bg = Rectangle(pos=questions_header.pos, size=questions_header.size)
        questions_header.bind(pos=self._update_questions_header_rect, size=self._update_questions_header_rect)
        
        widths = [0.35, 0.35, 0.3]  # 定義各列寬度比例
        
        for i, title in enumerate(["日文", "中文", "結果"]):
            header_container = GridLayout(cols=1, size_hint_x=widths[i])
            lbl = Label(
                text=title, 
                font_name="NotoSansTC", 
                bold=True, 
                halign='center',
                valign='middle',
                size_hint=(1, 1)
            )
            lbl.bind(size=lbl.setter('text_size'))
            header_container.add_widget(lbl)
            questions_header.add_widget(header_container)
        
        # 添加表格標題到表格佈局
        table_layout.add_widget(questions_header)
        
        # 創建容器佈局用於滾動內容
        scroll_content = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=[0, dp(10), 0, dp(10)])
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        
        # 添加每個問題的詳細信息
        for question in log.get("questions", []):
            question_row = GridLayout(cols=3, size_hint_y=None, height=dp(50))
            
            # 日文單詞
            jp_container = GridLayout(cols=1, size_hint_x=widths[0])
            jp_lbl = Label(
                text=question.get("japanese", ""),
                font_name="NotoSansTC",
                font_size=dp(20),
                halign='center',
                valign='middle',
                size_hint=(1, 1)
            )
            jp_lbl.bind(size=jp_lbl.setter('text_size'))
            jp_container.add_widget(jp_lbl)
            question_row.add_widget(jp_container)
            
            # 中文意思
            cn_container = GridLayout(cols=1, size_hint_x=widths[1])
            cn_lbl = Label(
                text=question.get("meaning", ""),
                font_name="NotoSansTC",
                font_size=dp(20),
                halign='center',
                valign='middle',
                size_hint=(1, 1)
            )
            cn_lbl.bind(size=cn_lbl.setter('text_size'))
            cn_container.add_widget(cn_lbl)
            question_row.add_widget(cn_container)
            
            # 答題結果
            result_container = GridLayout(cols=1, size_hint_x=widths[2])
            result_text = "✓" if question.get("is_correct", False) else "X"
            result_color = (0.2, 0.8, 0.2, 1) if question.get("is_correct", False) else (0.8, 0.2, 0.2, 1)
            result_label = Label(
                text=result_text,
                font_name="NotoSansTC",
                font_size=dp(22),
                color=result_color,
                bold=True,
                halign='center',
                valign='middle',
                size_hint=(1, 1)
            )
            result_label.bind(size=result_label.setter('text_size'))
            result_container.add_widget(result_label)
            question_row.add_widget(result_container)
            
            scroll_content.add_widget(question_row)
        
        # 創建滾動視圖
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False, 
            do_scroll_y=True,
            scroll_y=1  # 1 表示初始滾動位置在頂部
        )
        scroll_view.add_widget(scroll_content)
        
        # 添加滾動視圖到表格佈局
        table_layout.add_widget(scroll_view)
        
        # 添加表格佈局到主佈局
        main_layout.add_widget(table_layout)
        
        # 添加主佈局到根佈局
        root_layout.add_widget(main_layout)
        
        # 創建無邊框的彈出窗口
        popup = Popup(
            content=root_layout,
            size_hint=(0.9, 0.8),
            title="",
            separator_height=0,  # 移除分隔線
            background_color=(0.18, 0.18, 0.25, 1)  # 設置較亮的深藍灰色背景
        )
        
        # 綁定關閉按鈕事件
        close_button.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def _update_questions_header_rect(self, instance, value):
        """更新問題表格標題背景矩形的大小和位置"""
        self.questions_header_bg.pos = instance.pos
        self.questions_header_bg.size = instance.size