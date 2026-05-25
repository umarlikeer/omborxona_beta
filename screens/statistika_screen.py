from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.properties import ListProperty, NumericProperty
from kivy.metrics import dp
from kivy.app import App
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

# ── Rang palitasi ──────────────────────────────────────────────────────────────
CHART_COLORS = [
    (0.91, 0.12, 0.39, 1),
    (0.13, 0.59, 0.95, 1),
    (0.30, 0.69, 0.31, 1),
    (1.00, 0.60, 0.00, 1),
    (0.61, 0.15, 0.69, 1),
    (0.00, 0.74, 0.83, 1),
    (0.55, 0.76, 0.29, 1),
    (0.91, 0.46, 0.00, 1),
    (0.33, 0.83, 0.62, 1),
    (0.96, 0.26, 0.21, 1),
]


# ── Dumaloq grafik widget ──────────────────────────────────────────────────────

class PieChart(Widget):
    """
    data = [(product_name, qty_sold, revenue, color_tuple), ...]
    """
    data          = ListProperty([])
    total_revenue = NumericProperty(0)

    def on_data(self, *args):   self._draw()
    def on_size(self, *args):   self._draw()
    def on_pos(self, *args):    self._draw()

    def _draw(self):
        self.canvas.clear()
        if not self.data:
            self._draw_empty()
            return

        total_rev = sum(item[2] for item in self.data)
        if total_rev == 0:
            self._draw_empty()
            return

        cx = self.x + self.width  / 2
        cy = self.y + self.height / 2
        r  = min(self.width, self.height) / 2 * 0.84
        ri = r * 0.52          # Ichki bo'shliq (donut)

        angle = 90.0           # Tepadan boshlanadi

        with self.canvas:
            for name, qty, rev, color in self.data:
                sweep = (rev / total_rev) * 360.0
                Color(*color)
                Ellipse(
                    pos=(cx - r, cy - r),
                    size=(r * 2, r * 2),
                    angle_start=angle - sweep,
                    angle_end=angle,
                )
                angle -= sweep

            # Oq markaziy doira
            Color(0.97, 0.97, 0.97, 1)
            Ellipse(
                pos=(cx - ri, cy - ri),
                size=(ri * 2, ri * 2),
            )

            # Markazda umumiy summa matni
            text = f"{self.total_revenue:,.0f}\nso'm"
            cl = CoreLabel(text=text, font_size=dp(13), halign='center')
            cl.refresh()
            tex = cl.texture
            Color(0.18, 0.18, 0.18, 1)
            Rectangle(
                texture=tex,
                pos=(cx - tex.width / 2, cy - tex.height / 2),
                size=tex.size,
            )

    def _draw_empty(self):
        cx = self.x + self.width  / 2
        cy = self.y + self.height / 2
        r  = min(self.width, self.height) / 2 * 0.84
        with self.canvas:
            Color(0.88, 0.88, 0.88, 1)
            Ellipse(pos=(cx - r, cy - r), size=(r * 2, r * 2))
            Color(0.97, 0.97, 0.97, 1)
            ri = r * 0.52
            Ellipse(pos=(cx - ri, cy - ri), size=(ri * 2, ri * 2))
            cl = CoreLabel(text="Ma'lumot\nyo'q", font_size=dp(13), halign='center')
            cl.refresh()
            tex = cl.texture
            Color(0.5, 0.5, 0.5, 1)
            Rectangle(
                texture=tex,
                pos=(cx - tex.width / 2, cy - tex.height / 2),
                size=tex.size,
            )


# ── KV ────────────────────────────────────────────────────────────────────────

KV = """
#:import dp kivy.metrics.dp

<StatistikaScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.bg_normal
        padding: [dp(8), dp(8)]
        spacing: dp(6)

        # Sarlavha
        MDLabel:
            text: "Savdo statistikasi"
            font_style: 'H6'
            bold: True
            size_hint_y: None
            height: dp(36)
            halign: 'center'

        # Dumaloq grafik
        PieChart:
            id: pie
            size_hint_y: None
            height: dp(240)

        MDSeparator:

        # Izoh (legend) ro'yxati
        ScrollView:
            id: legend_scroll
            size_hint_y: 1
            MDBoxLayout:
                id: legend_container
                orientation: 'vertical'
                spacing: dp(4)
                size_hint_y: None
                height: self.minimum_height

        MDSeparator:

        # Statistikani tozalash
        MDRaisedButton:
            text: "🗑  Statistikani tozalash"
            size_hint_y: None
            height: dp(44)
            md_bg_color: 0.85, 0.2, 0.2, 1
            on_release: root.clear_stats()
"""

Builder.load_string(KV)


# ── Legend qatori ─────────────────────────────────────────────────────────────

class LegendRow(MDBoxLayout):
    def __init__(self, name, qty, revenue, color, **kwargs):
        super().__init__(**kwargs)
        self.orientation  = 'horizontal'
        self.size_hint_y  = None
        self.height       = dp(36)
        self.spacing      = dp(8)
        self.padding      = [dp(4), dp(4)]

        # Rang bloki
        color_box = Widget(size_hint=(None, None), size=(dp(18), dp(18)))
        with color_box.canvas:
            Color(*color)
            Rectangle(pos=color_box.pos, size=color_box.size)
        color_box.bind(
            pos=lambda w, p: self._update_box(w),
            size=lambda w, s: self._update_box(w),
        )
        color_box._color = color
        self._color_box  = color_box

        # Tovar nomi
        name_lbl = MDLabel(
            text=name,
            size_hint_x=1,
            font_size=dp(13),
            valign='middle',
        )

        # Sotilgan dona
        qty_lbl = MDLabel(
            text=f"{qty} ta",
            size_hint_x=None,
            width=dp(56),
            halign='right',
            font_size=dp(13),
            bold=True,
            valign='middle',
        )

        self.add_widget(color_box)
        self.add_widget(name_lbl)
        self.add_widget(qty_lbl)

    def _update_box(self, widget):
        widget.canvas.clear()
        with widget.canvas:
            Color(*widget._color)
            Rectangle(pos=widget.pos, size=widget.size)


# ── Statistika ekrani ─────────────────────────────────────────────────────────

class StatistikaScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        app   = App.get_running_app()
        stats = app.db.get_stats()          # [(name, qty, revenue), ...]
        total = app.db.get_total_revenue()

        pie  = self.ids.pie
        cont = self.ids.legend_container
        cont.clear_widgets()

        if not stats:
            pie.data          = []
            pie.total_revenue = 0
            cont.add_widget(MDLabel(
                text="Hali savdo amalga oshirilmagan",
                halign='center',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(40),
            ))
            return

        chart_data = []
        for i, (name, qty, revenue) in enumerate(stats):
            color = CHART_COLORS[i % len(CHART_COLORS)]
            chart_data.append((name, qty, revenue, color))
            cont.add_widget(LegendRow(name, qty, revenue, color))

        pie.total_revenue = total
        pie.data          = chart_data

    def clear_stats(self):
        dialog = [None]

        def do_clear(x):
            App.get_running_app().db.clear_stats()
            dialog[0].dismiss()
            self.refresh()

        dialog[0] = MDDialog(
            title="Statistikani tozalash",
            text="Barcha savdo ma'lumotlari o'chiriladi. Davom etasizmi?",
            buttons=[
                MDFlatButton(
                    text="Bekor",
                    on_release=lambda x: dialog[0].dismiss()
                ),
                MDRaisedButton(
                    text="Ha, tozalash",
                    md_bg_color=(0.85, 0.2, 0.2, 1),
                    on_release=do_clear,
                ),
            ],
        )
        dialog[0].open()
