from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp
from kivy.app import App
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

COLORS = [
    [0.91, 0.12, 0.39, 1],
    [0.13, 0.59, 0.95, 1],
    [0.30, 0.69, 0.31, 1],
    [1.00, 0.60, 0.00, 1],
    [0.61, 0.15, 0.69, 1],
    [0.00, 0.74, 0.83, 1],
    [0.55, 0.76, 0.29, 1],
    [0.91, 0.46, 0.00, 1],
]

KV = """
#:import dp kivy.metrics.dp

<OmborCard>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(82)
    padding: dp(8)
    spacing: dp(10)
    radius: [dp(10)]
    elevation: 1
    md_bg_color: app.theme_cls.bg_light

    # Avatar
    MDBoxLayout:
        size_hint_x: None
        width: dp(58)
        canvas.before:
            Color:
                rgba: root.color
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(8)]
        MDLabel:
            text: root.letter
            font_size: dp(26)
            bold: True
            halign: 'center'
            valign: 'middle'
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1

    # Nom va narx
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(2)
        MDLabel:
            text: root.pname
            bold: True
            size_hint_y: None
            height: dp(26)
            font_size: dp(14)
        MDLabel:
            text: root.price_str
            theme_text_color: 'Secondary'
            font_size: dp(13)

    # Qoldiq miqdori
    MDBoxLayout:
        size_hint_x: None
        width: dp(80)
        orientation: 'vertical'
        padding: [0, dp(4)]

        MDLabel:
            text: root.qty_str
            halign: 'right'
            bold: True
            font_size: dp(22)
            theme_text_color: 'Custom'
            text_color: (0.13,0.69,0.31,1) if root.qty_val > 0 else (0.8,0.2,0.2,1)

        MDLabel:
            text: 'dona'
            halign: 'right'
            font_size: dp(11)
            theme_text_color: 'Secondary'

<OmborScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.bg_normal

        MDTextField:
            id: search_field
            hint_text: "🔍  Tovar qidirish..."
            size_hint_y: None
            height: dp(56)
            on_text: root.search(self.text)
            mode: "rectangle"
            padding: [dp(12), 0]

        MDSeparator:

        ScrollView:
            MDBoxLayout:
                id: container
                orientation: 'vertical'
                spacing: dp(6)
                padding: [dp(8), dp(8)]
                size_hint_y: None
                height: self.minimum_height
"""

Builder.load_string(KV)


class OmborCard(MDCard):
    color     = ListProperty([0.5, 0.5, 0.5, 1])
    letter    = StringProperty('?')
    pname     = StringProperty('')
    price_str = StringProperty('')
    qty_str   = StringProperty('0')
    qty_val   = 0

    def __init__(self, product, **kwargs):
        super().__init__(**kwargs)
        pid, name, price, qty, img = product
        self.pname     = name
        self.price_str = f"{price:,.0f} so'm"
        self.letter    = name[0].upper() if name else '?'
        self.color     = COLORS[sum(ord(c) for c in name) % len(COLORS)]
        self.qty_val   = int(qty)
        self.qty_str   = str(qty)


class OmborScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self, search=''):
        container = self.ids.container
        container.clear_widgets()
        app = App.get_running_app()
        products = app.db.get_products(search)
        if not products:
            container.add_widget(MDLabel(
                text="Hali tovar qo'shilmagan",
                halign='center',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(60),
            ))
            return
        for product in products:
            container.add_widget(OmborCard(product))

    def search(self, text):
        self.refresh(text)
