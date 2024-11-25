import flet as ft
import math


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class ScientificButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.GREY
        self.color = ft.colors.WHITE


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=40)
        self.width = 500
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
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
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ],
                    expand=True,
                ),
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

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value += data

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

        elif data == "=":
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data == "%":
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data == "+/-":
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

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
                    self.result.value = self.format_number(math.pow(10, value))
            except:
                self.result.value = "Error"

        self.update()

    def format_number(self, num):
        return int(num) if num % 1 == 0 else num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            return "Error" if operand2 == 0 else self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calc App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    calc = CalculatorApp()
    page.add(calc)


ft.app(target=main)
