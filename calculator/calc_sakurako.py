import flet as ft
import math

# # クラス: CalcButton
# 数字や演算子ボタンの基本クラス。ボタンの基本的なプロパティを設定。
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text

# # クラス: DigitButton
# 数字ボタン専用クラス。スタイルを設定。
class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE

# # クラス: ActionButton
# 演算ボタン専用クラス (+, -, *, /, =) のスタイルを設定。
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE

# # クラス: ExtraActionButton
# 追加アクションボタン用クラス (AC, +/-, %) のスタイルを設定。
class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK

# # クラス: ScientificButton
# 科学計算用ボタン専用クラス (sin, cos, tan, ln, etc.) のスタイルを設定。
class ScientificButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.GREY
        self.color = ft.colors.WHITE

# # クラス: CalculatorApp
# 電卓のメインロジックとUIを管理。
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()  # 初期化メソッドを呼び出し、状態をリセット。

        # # 表示画面の設定
        # 計算結果を表示する画面を設定。
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=40)
        self.width = 500
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20

        # # UIのレイアウト設定
        # 各種ボタンと行・列のレイアウトを設定。
        self.content = ft.Column(
            controls=[
                # 計算結果表示エリア
                ft.Row(controls=[self.result], alignment="end"),
                
                # アクションボタンの行 (AC, +/-, %, /)
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),
                
                # 科学計算ボタンの行 (sin, cos, tan, ln, e^x)
                ft.Row(
                    controls=[
                        ScientificButton(text="sin", button_clicked=self.button_clicked),
                        ScientificButton(text="cos", button_clicked=self.button_clicked),
                        ScientificButton(text="tan", button_clicked=self.button_clicked),
                        ScientificButton(text="ln", button_clicked=self.button_clicked),
                        ScientificButton(text="e^x", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),

                # 科学計算ボタンの行 (π, x^2, x^3, 1/x, 10^x)
                ft.Row(
                    controls=[
                        ScientificButton(text="π", button_clicked=self.button_clicked),
                        ScientificButton(text="x^2", button_clicked=self.button_clicked),
                        ScientificButton(text="x^3", button_clicked=self.button_clicked),
                        ScientificButton(text="1/x", button_clicked=self.button_clicked),
                        ScientificButton(text="10^x", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),

                # 数字ボタンの行 (7, 8, 9, *)
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),
                
                # 数字ボタンの行 (4, 5, 6, -)
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),

                # 数字ボタンの行 (1, 2, 3, +)
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),

                # 数字ボタンの行 (0, ., =)
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),
            ]
        )

    # # ボタンが押された時の動作を定義
    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        
        # エラー状態やリセット時の処理
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        # 数字入力の処理
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value += data

        # 基本演算の処理 (+, -, *, /)
        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        # 等号 (=) を押した際の処理
        elif data == "=":
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        # パーセント (%) 計算
        elif data == "%":
            self.result.value = float(self.result.value) / 100
            self.reset()

        # +/- ボタン (符号の切り替え)
        elif data == "+/-":
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        # 科学計算の処理
        elif data in ("sin", "cos", "tan", "ln", "e^x", "π", "x^2", "x^3", "1/x", "10^x"):
            try:
                value = float(self.result.value)
                if data == "sin":
                    self.result.value = self.format_number(math.sin(math.radians(value)))
                elif data == "cos":
                    self.result.value = self.format_number(math.cos(math.radians(value)))
                elif data == "tan":
                    self.result.value = self.format_number(math.tan(math.radians(value)))
                elif data == "ln":
                    self.result.value = (
                        "Error" if value <= 0 else self.format_number(math.log(value))
                    )
                elif data == "e^x":
                    self.result.value = self.format_number(math.exp(value))
                elif data == "π":
                    self.result.value = math.pi
                elif data == "x^2":
                    self.result.value = self.format_number(math.pow(value, 2))
                elif data == "x^3":
                    self.result.value = self.format_number(math.pow(value, 3))
                elif data == "1/x":
                    self.result.value = (
                        "Error" if value == 0 else self.format_number(1 / value)
                    )
                elif data == "10^x":
                    self.result.value = self.format_number(math.pow(10
        # # 画面の更新
        # 計算結果が変更された場合にUIを更新
        self.update()

    # # メソッド: format_number
    # 浮動小数点数をフォーマットし、小数部が0の場合は整数として表示
    def format_number(self, num):
        return int(num) if num % 1 == 0 else num

    # # メソッド: calculate
    # 基本的な四則演算 (+, -, *, /) を実行
    # 割り算の際にゼロ除算エラーを防ぐ処理を追加
    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            return "Error" if operand2 == 0 else self.format_number(operand1 / operand2)

    # # メソッド: reset
    # 計算状態を初期化
    def reset(self):
        self.operator = "+"  # 初期演算子を "+" に設定
        self.operand1 = 0    # 最初のオペランドを 0 に設定。
        self.new_operand = True  # 新しいオペランドを受け付ける状態に設定


# # 関数: main
# アプリのメインエントリーポイント
# ページのレイアウトを設定し、CalculatorAppを追加
def main(page: ft.Page):
    # アプリケーションのタイトルを設定
    page.title = "Calc App"

    # ページの中央にコンテンツを配置
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 電卓アプリをインスタンス化し、ページに追加
    calc = CalculatorApp()
    page.add(calc)


# # アプリケーションの開始
# Fletアプリケーションを起動し、main関数をターゲットとして指定
ft.app(target=main)
