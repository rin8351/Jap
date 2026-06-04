import importlib
import os

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

import styles

SECRETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_secrets.py')


def load_ai_secrets():
    empty = {"AI_API_KEY": "", "AI_MODEL": "", "AI_API_URL": ""}
    if not os.path.exists(SECRETS_PATH):
        return empty.copy()
    try:
        import ai_secrets
        importlib.reload(ai_secrets)
        return {
            "AI_API_KEY": (getattr(ai_secrets, "AI_API_KEY", "") or "").strip(),
            "AI_MODEL": (getattr(ai_secrets, "AI_MODEL", "") or "").strip(),
            "AI_API_URL": (getattr(ai_secrets, "AI_API_URL", "") or "").strip(),
        }
    except Exception:
        return empty.copy()


def save_ai_secrets(api_key, model, api_url):
    content = (
        f'AI_API_KEY = {repr(api_key.strip())}\n'
        f'AI_MODEL = {repr(model.strip())}\n'
        f'AI_API_URL = {repr(api_url.strip())}\n'
    )
    with open(SECRETS_PATH, 'w', encoding='utf-8') as f:
        f.write(content)


def ai_secrets_complete():
    secrets = load_ai_secrets()
    return all(secrets[key] for key in ("AI_API_KEY", "AI_MODEL", "AI_API_URL"))


class AISettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("АИ настройки")
        self.setStyleSheet(styles.button_style)
        self.resize(520, 240)

        layout = QVBoxLayout(self)
        secrets = load_ai_secrets()

        layout.addWidget(QLabel("API ключ (AI_API_KEY)"))
        self.api_key_input = QLineEdit(secrets["AI_API_KEY"])
        layout.addWidget(self.api_key_input)

        layout.addWidget(QLabel("Модель (AI_MODEL)"))
        self.model_input = QLineEdit(secrets["AI_MODEL"])
        layout.addWidget(self.model_input)

        layout.addWidget(QLabel("URL API (AI_API_URL)"))
        self.url_input = QLineEdit(secrets["AI_API_URL"])
        layout.addWidget(self.url_input)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить", clicked=self.save)
        cancel_btn = QPushButton("Отмена", clicked=self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def save(self):
        save_ai_secrets(
            self.api_key_input.text(),
            self.model_input.text(),
            self.url_input.text(),
        )
        self.accept()
