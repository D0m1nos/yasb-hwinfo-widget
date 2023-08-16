import winreg
from PyQt6.QtWidgets import QLabel
from core.widgets.base import BaseWidget
from core.validation.widgets.hwinfo.monitor import VALIDATION_SCHEMA


class Monitor(BaseWidget):
    validation_schema = VALIDATION_SCHEMA

    def __init__(
            self,
            label: str,
            label_alt: str,
            update_interval: int,
            index: int,
            class_name: str,
            callbacks: dict[str, str],
    ):
        super().__init__(update_interval, class_name=f"hwinfo {class_name}")
        self._show_alt_label = False
        self._label_content = label
        self._label_alt_content = label_alt

        self._label = QLabel()
        self._label_alt = QLabel()
        self._label.setProperty("class", "label")
        self._label_alt.setProperty("class", "label alt")
        self.widget_layout.addWidget(self._label)
        self.widget_layout.addWidget(self._label_alt)

        self.register_callback("toggle_label", self._toggle_label)
        self.register_callback("update_label", self._update_label)

        self.callback_left = callbacks['on_left']
        self.callback_right = callbacks['on_right']
        self.callback_middle = callbacks['on_middle']
        self.callback_timer = "update_label"

        self._label.show()
        self._label_alt.hide()

        self.index = index

        self.start_timer()

    def _toggle_label(self):
        self._show_alt_label = not self._show_alt_label

        if self._show_alt_label:
            self._label.hide()
            self._label_alt.show()
        else:
            self._label.show()
            self._label_alt.hide()

        self._update_label()

    def _update_label(self):
        active_label = self._label_alt if self._show_alt_label else self._label
        active_label_content = self._label_alt_content if self._show_alt_label else self._label_content
        active_label.setText(active_label_content)

        try:
            info = self._get_values()
            active_label.setText(active_label_content.format(info=info))
        except Exception:
            active_label.setText(active_label_content)

    def _get_values(self) -> dict:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

        vsbKey = winreg.OpenKey(registry, r'Software\HWiNFO64\VSB')

        sensorTuple = winreg.QueryValueEx(vsbKey, 'Sensor' + str(self.index))
        labelTuple = winreg.QueryValueEx(vsbKey, 'Label' + str(self.index))
        valueTuple = winreg.QueryValueEx(vsbKey, 'Value' + str(self.index))
        valueRawTuple = winreg.QueryValueEx(vsbKey, 'ValueRaw' + str(self.index))
        colorTuple = winreg.QueryValueEx(vsbKey, 'Color' + str(self.index))

        return {
            'sensor': sensorTuple[0],
            'label': labelTuple[0],
            'value': valueTuple[0],
            'valueRaw': valueRawTuple[0],
            'color': colorTuple[0]
        }
