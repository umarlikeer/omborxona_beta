import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.app import App
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog

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
#:import md_icons kivymd.icon_definitions.md_icons

<BoshqaruvCard>:
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

    # Miqdor tahrirlash
    MDBoxLayout:
        size_hint_x: None
        width: dp(88)
        spacing: dp(2)

        MDRaisedButton:
            text: '-'
            size_hint: (None, None)
            size: (dp(30), dp(34))
            md_bg_color: 0.85, 0.2, 0.2, 1
            on_release: root.decrement()

        MDTextField:
            id: qty_field
            text: root.qty_str
            size_hint: (1, None)
            height: dp(40)
            input_filter: 'int'
            halign: 'center'
            mode: "rectangle"
            on_focus: if not self.focus: root.save_qty(self.text)

        MDRaisedButton:
            text: '+'
            size_hint: (None, None)
            size: (dp(30), dp(34))
            md_bg_color: 0.13, 0.69, 0.31, 1
            on_release: root.increment()

<BoshqaruvScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.bg_normal

        # "Tovar yaratish" paneli (savat kabi, tepada)
        MDBoxLayout:
            size_hint_y: None
            height: dp(52)
            md_bg_color: app.theme_cls.primary_color
            padding: [dp(14), dp(6)]
            spacing: dp(8)

            MDLabel:
                text: md_icons.get('plus-circle-outline', '') + "  Tovar yaratish"
                font_size: dp(14)
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                valign: 'middle'
                size_hint_x: 1

            MDRaisedButton:
                text: "Ochish"
                size_hint: (None, None)
                size: (dp(84), dp(36))
                md_bg_color: 1, 1, 1, 0.22
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                on_release: root.show_add_form()

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


# ── Tovar kartasi ──────────────────────────────────────────────────────────────

class BoshqaruvCard(MDCard):
    color     = ListProperty([0.5, 0.5, 0.5, 1])
    letter    = StringProperty('?')
    pname     = StringProperty('')
    price_str = StringProperty('')
    qty_str   = StringProperty('0')

    def __init__(self, product, **kwargs):
        super().__init__(**kwargs)
        pid, name, price, qty, img = product
        self.pid       = pid
        self._qty      = int(qty)
        self.pname     = name
        self.price_str = f"{price:,.0f} so'm"
        self.letter    = name[0].upper() if name else '?'
        self.color     = COLORS[sum(ord(c) for c in name) % len(COLORS)]
        self.qty_str   = str(qty)

    def increment(self):
        self._qty += 1
        self.qty_str = str(self._qty)
        self.ids.qty_field.text = self.qty_str
        App.get_running_app().db.set_quantity(self.pid, self._qty)

    def decrement(self):
        self._qty = max(0, self._qty - 1)
        self.qty_str = str(self._qty)
        self.ids.qty_field.text = self.qty_str
        App.get_running_app().db.set_quantity(self.pid, self._qty)

    def save_qty(self, text):
        try:
            val = int(text) if text else 0
        except ValueError:
            val = 0
        val = max(0, val)
        self._qty    = val
        self.qty_str = str(val)
        self.ids.qty_field.text = self.qty_str
        App.get_running_app().db.set_quantity(self.pid, val)


# ── Tovar yaratish formasi (MDDialog ichida) ───────────────────────────────────

class AddProductContent(MDBoxLayout):
    """MDDialog uchun maxsus kontent."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing     = dp(8)
        self.padding     = [dp(4), dp(4)]
        self.size_hint_y = None
        self.height      = dp(220)

        self.name_field = MDTextField(
            hint_text="Tovar nomi *",
            mode="rectangle",
            size_hint_y=None,
            height=dp(56),
        )
        self.price_field = MDTextField(
            hint_text="Narxi (so'm) *",
            mode="rectangle",
            input_filter='float',
            size_hint_y=None,
            height=dp(56),
        )
        self.image_field = MDTextField(
            hint_text="Rasm yo'li (ixtiyoriy)",
            mode="rectangle",
            size_hint_y=None,
            height=dp(56),
        )

        browse_btn = MDRaisedButton(
            text="📁 Rasm tanlash",
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self._browse()
        )

        self.add_widget(self.name_field)
        self.add_widget(self.price_field)
        self.add_widget(self.image_field)
        self.add_widget(browse_btn)

    def _browse(self):
        try:
            from plyer import filechooser
            filechooser.open_file(
                on_selection=self._on_selected,
                filters=[["Rasmlar", "*.jpg", "*.jpeg", "*.png", "*.webp"]]
            )
        except Exception:
            pass  # plyer yo'q bo'lsa, qo'lda yoziladi

    def _on_selected(self, selection):
        if selection:
            self.image_field.text = selection[0]

    def get_values(self):
        return (
            self.name_field.text.strip(),
            self.price_field.text.strip(),
            self.image_field.text.strip(),
        )


# ── Asosiy ekran ───────────────────────────────────────────────────────────────

class BoshqaruvScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        container = self.ids.container
        container.clear_widgets()
        app = App.get_running_app()
        products = app.db.get_products()
        if not products:
            container.add_widget(MDLabel(
                text="Hali tovar yo'q.\n\"Tovar yaratish\" tugmasini bosing.",
                halign='center',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(80),
            ))
            return
        for product in products:
            container.add_widget(BoshqaruvCard(product))

    def show_add_form(self):
        """Tovar yaratish dialogini ochadi."""
        self._form_content = AddProductContent()
        self._add_dialog = MDDialog(
            title="Yangi tovar qo'shish",
            type="custom",
            content_cls=self._form_content,
            buttons=[
                MDFlatButton(
                    text="◀ Orqaga",
                    on_release=lambda x: self._add_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Saqlash",
                    on_release=lambda x: self._save_product()
                ),
            ],
        )
        self._add_dialog.open()

    def _save_product(self):
        name, price_str, image = self._form_content.get_values()

        # Validatsiya
        if not name:
            self._form_content.name_field.error = True
            self._form_content.name_field.helper_text = "Iltimos nomni kiriting!"
            return
        if not price_str:
            self._form_content.price_field.error = True
            self._form_content.price_field.helper_text = "Iltimos narxni kiriting!"
            return

        try:
            price = float(price_str)
        except ValueError:
            self._form_content.price_field.error = True
            return

        app = App.get_running_app()
        product_id = app.db.add_product(name, price, image)
        self._add_dialog.dismiss()

        # Miqdor qo'shish dialogi
        self._ask_initial_qty(product_id, name)

    def _ask_initial_qty(self, product_id, name):
        """Yangi tovar uchun boshlang'ich miqdorni so'raydi."""
        qty_field = MDTextField(
            hint_text="Nechta dona?",
            input_filter='int',
            mode="rectangle",
            size_hint_y=None,
            height=dp(56),
        )
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(80),
            padding=[dp(4), dp(4)],
        )
        content.add_widget(MDLabel(
            text=f"'{name}' omborga nechta qo'shilsin?",
            size_hint_y=None,
            height=dp(24),
        ))
        content.add_widget(qty_field)

        qty_dialog = [None]

        def confirm(x):
            try:
                qty = int(qty_field.text) if qty_field.text else 0
            except ValueError:
                qty = 0
            if qty > 0:
                app = App.get_running_app()
                app.db.add_quantity(product_id, qty)
            if qty_dialog[0]:
                qty_dialog[0].dismiss()
            Clock.schedule_once(lambda dt: self.refresh(), 0.1)

        qty_dialog[0] = MDDialog(
            title="Omborga qo'shish",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="O'tkazib yuborish",
                    on_release=lambda x: (qty_dialog[0].dismiss(),
                                         Clock.schedule_once(lambda dt: self.refresh(), 0.1))
                ),
                MDRaisedButton(
                    text="Qo'shish",
                    on_release=confirm,
                ),
            ],
        )
        qty_dialog[0].open()
