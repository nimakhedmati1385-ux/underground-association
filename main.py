from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform


class UndergroundApp(App):

    def build(self):
        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        self.title = Label(
            text="UNDERGROUND ASSOCIATION",
            font_size=24,
            size_hint_y=None,
            height=60
        )

        self.status = Label(
            text="Ready",
            size_hint_y=None,
            height=40
        )

        self.wifi_button = Button(
            text="📶  WI-FI SCANNER",
            size_hint_y=None,
            height=60
        )
        self.wifi_button.bind(on_press=self.scan_wifi)

        self.bluetooth_button = Button(
            text="🟦  BLUETOOTH SCANNER",
            size_hint_y=None,
            height=60
        )

        self.location_button = Button(
            text="📍  LOCATION SCANNER",
            size_hint_y=None,
            height=60
        )

        self.results = Label(
            text="Wi-Fi results will appear here.",
            size_hint_y=None,
            halign="left",
            valign="top"
        )
        self.results.bind(
            texture_size=lambda instance, value:
            setattr(instance, "height", value[1])
        )

        scroll = ScrollView()
        scroll.add_widget(self.results)

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.status)
        self.layout.add_widget(self.wifi_button)
        self.layout.add_widget(self.bluetooth_button)
        self.layout.add_widget(self.location_button)
        self.layout.add_widget(scroll)

        return self.layout

    def scan_wifi(self, instance):

        self.status.text = "Scanning Wi-Fi..."

        if platform != "android":
            self.results.text = (
                "Wi-Fi scanning requires Android."
            )
            self.status.text = "Android required"
            return

        try:
            from jnius import autoclass

            Context = autoclass(
                "android.content.Context"
            )

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            wifi_manager = activity.getSystemService(
                Context.WIFI_SERVICE
            )

            wifi_manager.startScan()

            networks = wifi_manager.getScanResults()

            output = []

            for network in networks:
                ssid = network.SSID
                bssid = network.BSSID
                level = network.level
                frequency = network.frequency

                output.append(
                    f"SSID: {ssid}\n"
                    f"BSSID: {bssid}\n"
                    f"Signal: {level} dBm\n"
                    f"Frequency: {frequency} MHz\n"
                    f"----------------------"
                )

            if output:
                self.results.text = "\n".join(output)
                self.status.text = (
                    f"Found {len(output)} networks"
                )
            else:
                self.results.text = (
                    "No Wi-Fi networks found."
                )
                self.status.text = "Scan finished"

        except Exception as e:

            self.status.text = "Scan error"

            self.results.text = (
                "Wi-Fi scan could not start.\n\n"
                + str(e)
            )


if __name__ == "__main__":
    UndergroundApp().run()