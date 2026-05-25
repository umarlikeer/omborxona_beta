import os
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.properties import StringProperty, BooleanProperty
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from database import Database

# Register all screens before Builder.load_string uses them
from screens.sotish_screen import SotishScreen          # noqa: F401
from screens.ombor_screen import OmborScreen            # noqa: F401
from screens.boshqaruv_screen import BoshqaruvScreen    # noqa: F401
from screens.statistika_screen import StatistikaScreen  # noqa: F401

KV = """
#:import dp kivy.metrics.dp
#:import md_icons kivymd.icon_definitions.md_icons
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<NavItem>:
    orientation: 'vertical'
    size_hint_x: 1
    padding: [dp(2), dp(6), dp(2), dp(4)]

    MDLabel:
        text: md_icons.get(root.icon, '')
        font_name: 'Icons'
        font_size: dp(22)
        halign: 'center'
        valign: 'middle'
        size_hint_y: 1
        theme_text_color: 'Custom'
        text_color: (1,1,1,1) if root.is_active else (1,1,1,0.48)

    MDLabel:
        text: root.nav_label
        font_size: dp(9)
        halign: 'center'
        size_hint_y: None
        height: dp(14)
        theme_text_color: 'Custom'
        text_color: (1,1,1,1) if root.is_active else (1,1,1,0.48)

<RootLayout>:
    orientation: 'vertical'
    md_bg_color: app.theme_cls.bg_normal

    ScreenManager:
        id: sm
        transition: FadeTransition(duration=0.12)
        size_hint_y: 1

        SotishScreen:
            name: 'sotish'
        OmborScreen:
            name: 'ombor'
        BoshqaruvScreen:
            name: 'boshqaruv'
        StatistikaScreen:
            name: 'statistika'

    # --- Savat paneli (faqat Sotish tabida ko'rinadi) ---
    MDBoxLayout:
        id: cart_bar
        size_hint_y: None
        height: 0
        opacity: 0
        md_bg_color: 0.11, 0.68, 0.31, 1
        padding: [dp(14), dp(6)]
        spacing: dp(8)
        elevation: 6

        MDLabel:
            id: cart_label
            text: ''
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1
            font_style: 'Subtitle2'
            valign: 'middle'
            size_hint_x: 1

        MDRaisedButton:
            text: "Ko'rish >"
            size_hint: (None, None)
            size: (dp(96), dp(36))
            md_bg_color: 1, 1, 1, 0.22
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1
            on_release: app.show_cart()

    # --- Pastki navigatsiya ---
    MDBoxLayout:
        size_hint_y: None
        height: dp(58)
        md_bg_color: app.theme_cls.primary_color
        elevation: 10

        NavItem:
            icon: 'cart-outline'
            nav_label: 'Sotish'
            is_active: app.tab == 'sotish'
            on_release: app.go('sotish')

        NavItem:
            icon: 'eye-outline'
            nav_label: 'Ombor'
            is_active: app.tab == 'ombor'
            on_release: app.go('ombor')

        NavItem:
            icon: 'package-variant'
            nav_label: 'Boshqaruv'
            is_active: app.tab == 'boshqaruv'
            on_release: app.go('boshqaruv')

        NavItem:
            icon: 'chart-pie'
            nav_label: 'Statistika'
            is_active: app.tab == 'statistika'
            on_release: app.go('statistika')
"""

Builder.load_string(KV)


class NavItem(ButtonBehavior, MDBoxLayout):
    icon      = StringProperty('home')
    nav_label = StringProperty('')
    is_active = BooleanProperty(False)


class RootLayout(MDBoxLayout):
    pass


class OmborxonaApp(MDApp):
    tab = StringProperty('sotish')

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette  = 'Orange'
        self.theme_cls.theme_style     = 'Light'
        self.db      = Database()
        self.cart    = {}       # {pid: {'name':str, 'price':float, 'qty':int}}
        self._dialog = None
        return RootLayout()

    # ── Navigatsiya ────────────────────────────────────────────────────────────

    def go(self, name):
        self.tab = name
        self.root.ids.sm.current = name
        self._refresh_bar()

    # ── Savat ─────────────────────────────────────────────────────────────────

    @property
    def cart_count(self):
        return sum(v['qty'] for v in self.cart.values())

    @property
    def cart_total(self):
        return sum(v['qty'] * v['price'] for v in self.cart.values())

    def add_to_cart(self, pid, name, price, max_qty):
        cur = self.cart.get(pid, {}).get('qty', 0)
        if cur >= max_qty:
            return
        if pid in self.cart:
            self.cart[pid]['qty'] += 1
        else:
            self.cart[pid] = {'name': name, 'price': float(price), 'qty': 1}
        self._refresh_bar()

    def remove_from_cart(self, pid):
        if pid not in self.cart:
            return
        self.cart[pid]['qty'] -= 1
        if self.cart[pid]['qty'] <= 0:
            del self.cart[pid]
        self._refresh_bar()

    def clear_cart(self):
        self.cart = {}
        self._refresh_bar()

    def _refresh_bar(self):
        bar = self.root.ids.cart_bar
        lbl = self.root.ids.cart_label
        show = (self.tab == 'sotish') and self.cart_count > 0
        if show:
            lbl.text    = f"🛒  {self.cart_count} ta  |  {self.cart_total:,.0f} so'm"
            bar.height  = dp(50)
            bar.opacity = 1
        else:
            bar.height  = 0
            bar.opacity = 0

    # ── Savat dialogi ─────────────────────────────────────────────────────────

    def show_cart(self):
        if not self.cart:
            return
        lines = [
            f"• {v['name']}  ×{v['qty']}  =  {v['qty']*v['price']:,.0f} so'm"
            for v in self.cart.values()
        ]
        lines.append(f"\n[b]Jami:[/b]  {self.cart_total:,.0f} so'm")

        self._dialog = MDDialog(
            title="Savat",
            text="\n".join(lines),
            buttons=[
                MDFlatButton(
                    text="Yopish",
                    on_release=lambda x: self._dialog.dismiss()
                ),
                MDRaisedButton(
                    text="✔  Sotish",
                    md_bg_color=self.theme_cls.primary_color,
                    on_release=lambda x: self._do_sale()
                ),
            ],
        )
        self._dialog.open()

    def _do_sale(self):
        if self._dialog:
            self._dialog.dismiss()
        self.db.process_sale(dict(self.cart))
        self.clear_cart()
        Clock.schedule_once(
            lambda dt: self.root.ids.sm.get_screen('sotish').refresh(), 0.15
        )


if __name__ == '__main__':
    OmborxonaApp().run()
