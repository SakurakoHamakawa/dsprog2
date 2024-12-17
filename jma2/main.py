import sqlite3
import requests
import flet as ft

# SQLiteデータベースの初期化
DB_NAME = "weather_forecast.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # 地域情報テーブル
    cur.execute('''
    CREATE TABLE IF NOT EXISTS areas (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )''')

    # 天気予報テーブル
    cur.execute('''
    CREATE TABLE IF NOT EXISTS forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area_id INTEGER,
        report_datetime TEXT,
        forecast_time TEXT,
        weather TEXT,
        wind TEXT,
        FOREIGN KEY (area_id) REFERENCES areas (id)
    )''')
    conn.commit()
    conn.close()

# 天気予報データをDBに保存
def insert_forecast_data(area_id, forecast_data):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    report_datetime = forecast_data[0]["reportDatetime"]
    time_series = forecast_data[0]["timeSeries"][0]
    time_defines = time_series["timeDefines"]
    areas = time_series["areas"]

    for area in areas:
        for i, time_define in enumerate(time_defines):
            weather = area["weathers"][i]
            wind = area["winds"][i] if i < len(area["winds"]) else "情報なし"
            cur.execute('''
            INSERT INTO forecasts (area_id, report_datetime, forecast_time, weather, wind)
            VALUES (?, ?, ?, ?, ?)''', (area_id, report_datetime, time_define, weather, wind))
    conn.commit()
    conn.close()

# 地域リストの取得エンドポイント
AREA_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

# 地域リストを取得する関数
def fetch_area_list():
    try:
        response = requests.get(AREA_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"地域リストの取得中にエラーが発生しました: {e}")
        return None

# 天気予報を取得する関数
def fetch_forecast(area_code):
    try:
        url = FORECAST_URL_TEMPLATE.format(area_code=area_code)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"天気予報の取得中にエラーが発生しました: {e}")
        return None

# Flet アプリのメイン関数
def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    # DB初期化
    init_db()

    # ヘッダー
    app_bar = ft.AppBar(
        title=ft.Text("天気予報", style=ft.TextThemeStyle.HEADLINE_MEDIUM, color=ft.colors.WHITE),
        bgcolor=ft.colors.PURPLE,
    )

    # サイドバー
    sidebar = ft.Column(
        controls=[
            ft.Text("地域を選択", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ],
        scroll=ft.ScrollMode.AUTO,
        width=250,
    )

    # 地域リストを取得してサイドバーに追加
    area_data = fetch_area_list()
    if area_data:
        centers = area_data.get("centers", {})
        offices = area_data.get("offices", {})

        for key, value in centers.items():
            dropdown = ft.Dropdown(
                label=value["name"],
                label_style=ft.TextStyle(color=ft.colors.WHITE),  # ドロップダウンラベルを白に設定
                border_color=ft.colors.WHITE,  # ドロップダウンの枠を白に設定
            )
            
            # 子地域を取得
            for child_code in value.get("children", []):
                child_region = offices.get(child_code)
                if child_region:
                    dropdown.options.append(
                        ft.dropdown.Option(text=child_region["name"], key=child_code)
                    )
            
            dropdown.on_change = lambda e: on_select(e)
            sidebar.controls.append(dropdown)
    else:
        sidebar.controls.append(ft.Text("地域リストの取得に失敗しました", color=ft.colors.WHITE))

    # メインビュー
    main_view = ft.Container(
        content=ft.Text("Active View", style=ft.TextThemeStyle.HEADLINE_SMALL),
        alignment=ft.alignment.center,
        expand=True,
    )

    # 地域選択時のイベント処理
    def on_select(e):
        area_code = e.control.value  # 選択された地域コード
        forecast_data = fetch_forecast(area_code)
        if forecast_data:
            insert_forecast_data(area_code, forecast_data)  # DBに格納
            display_weather(forecast_data)
        else:
            main_view.content = ft.Text(
                "天気予報の取得に失敗しました", style=ft.TextThemeStyle.BODY_LARGE, color=ft.colors.RED
            )
        page.update()

    # 天気予報データを表示
    def display_weather(data):
        if data:
            main_view.content = None  # メインビューの内容をクリア
            report_datetime = data[0]["reportDatetime"]
            time_series = data[0]["timeSeries"][0]

            content = ft.Column(controls=[], scroll=ft.ScrollMode.AUTO)
            content.controls.append(ft.Text(f"発表日時: {report_datetime}"))

            time_defines = time_series["timeDefines"]
            areas = time_series["areas"]
            for area in areas:
                content.controls.append(
                    ft.Text(f"地域: {area['area']['name']}", size=20, weight="bold")
                )
                for i, time_define in enumerate(time_defines):
                    weather = area["weathers"][i]
                    wind = area["winds"][i] if i < len(area["winds"]) else "情報なし"
                    content.controls.append(ft.Text(f"{time_define}: {weather} / {wind}"))
            main_view.content = content
        else:
            main_view.content = ft.Text("データなし", color="red")

    # ページのレイアウトを作成
    page.add(
        ft.Row(
            controls=[
                ft.Container(sidebar, bgcolor=ft.colors.LIGHT_BLUE, padding=10),
                main_view,
            ],
            expand=True,
        )
    )

    # ヘッダーを設定
    page.appbar = app_bar

ft.app(target=main)
