"""
Internationalization (i18n) module for 2048-CLI.
Provides translation functionality with support for multiple languages.
"""

import json
from pathlib import Path
from typing import Any

# Default language
DEFAULT_LANGUAGE = "en"


class I18nManager:
    """Manages internationalization and localization for the application."""

    def __init__(self):
        self._current_language = DEFAULT_LANGUAGE
        self._translations: dict[str, dict[str, Any]] = {}
        self._emoji_enabled = True
        self._locales_dir = Path(__file__).parent.parent / "locales"
        self._load_all_translations()

    def _load_all_translations(self) -> None:
        """Load all available translation files."""
        if not self._locales_dir.exists():
            return

        for locale_file in self._locales_dir.glob("*.json"):
            language_code = locale_file.stem
            try:
                with open(locale_file, encoding="utf-8") as f:
                    self._translations[language_code] = json.load(f)
            except (OSError, json.JSONDecodeError) as e:
                print(f"Warning: Failed to load locale file {locale_file}: {e}")

    def set_language(self, language_code: str) -> bool:
        """
        Set the current language.

        Args:
            language_code: Language code (e.g., 'en', 'ja')

        Returns:
            True if language was successfully set, False otherwise
        """
        if language_code in self._translations:
            self._current_language = language_code
            return True
        return False

    def get_language(self) -> str:
        """Get the current language code."""
        return self._current_language

    def get_available_languages(self) -> list[str]:
        """Get list of available language codes."""
        return list(self._translations.keys())

    def set_emoji_enabled(self, enabled: bool) -> None:
        """Enable or disable emoji display."""
        self._emoji_enabled = enabled

    def is_emoji_enabled(self) -> bool:
        """Check if emoji display is enabled."""
        return self._emoji_enabled

    def _get_nested_value(self, data: dict[str, Any], key_path: str) -> Any | None:
        """
        Get a nested value from dictionary using dot notation.

        Args:
            data: Dictionary to search in
            key_path: Dot-separated key path (e.g., 'menu.new_game')

        Returns:
            The value if found, None otherwise
        """
        keys = key_path.split(".")
        current = data

        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]

        return current

    def t(self, key: str, use_emoji: bool | None = None, **kwargs) -> str:
        """
        Translate a key to the current language.

        Args:
            key: Translation key (supports dot notation, e.g., 'menu.new_game')
            use_emoji: Override emoji setting for this translation
            **kwargs: Format arguments for string formatting

        Returns:
            Translated string, or the key itself if translation not found
        """
        # Determine if emoji should be used
        should_use_emoji = use_emoji if use_emoji is not None else self._emoji_enabled

        # Try to get emoji version first if enabled
        if should_use_emoji:
            emoji_key = key + "_emoji"
            emoji_translation = self._get_translation(emoji_key)
            if emoji_translation:
                try:
                    return emoji_translation.format(**kwargs)
                except (KeyError, ValueError):
                    pass

        # Get regular translation
        translation = self._get_translation(key)
        if translation:
            try:
                return translation.format(**kwargs)
            except (KeyError, ValueError):
                return translation

        # Fallback to key if no translation found
        return key

    def _get_translation(self, key: str) -> str | None:
        """
        Get translation for a key from current or fallback language.

        Args:
            key: Translation key

        Returns:
            Translation string or None if not found
        """
        # First try current language
        if self._current_language in self._translations:
            # Check for emoji variant
            if key.endswith("_emoji"):
                base_key = key[:-6]  # Remove '_emoji' suffix
                # Build correct emoji path: section.emoji.key_name
                parts = base_key.split(".")
                if len(parts) >= 2:
                    section = parts[0]
                    key_name = parts[-1]
                    emoji_path = f"{section}.emoji.{key_name}"
                    result = self._get_nested_value(
                        self._translations[self._current_language], emoji_path
                    )
                    if result:
                        return result

            # Check regular key
            result = self._get_nested_value(
                self._translations[self._current_language], key
            )
            if result:
                return result

        # Fallback to default language (English)
        if (
            self._current_language != DEFAULT_LANGUAGE
            and DEFAULT_LANGUAGE in self._translations
        ):
            # Check for emoji variant in fallback
            if key.endswith("_emoji"):
                base_key = key[:-6]
                parts = base_key.split(".")
                if len(parts) >= 2:
                    section = parts[0]
                    key_name = parts[-1]
                    emoji_path = f"{section}.emoji.{key_name}"
                    result = self._get_nested_value(
                        self._translations[DEFAULT_LANGUAGE], emoji_path
                    )
                    if result:
                        return result

            # Check regular key in fallback
            result = self._get_nested_value(self._translations[DEFAULT_LANGUAGE], key)
            if result:
                return result

        return None

    def get_language_display_name(self, language_code: str) -> str:
        """
        Get the display name for a language code.

        Args:
            language_code: Language code

        Returns:
            Display name for the language
        """
        if language_code in self._translations:
            display_name = self._get_nested_value(
                self._translations[language_code], f"language.{language_code}"
            )
            if display_name:
                return display_name

        # Fallback display names
        fallback_names = {
            "en": "English",
            "ja": "日本語",
        }
        return fallback_names.get(language_code, language_code)


# Global instance
_i18n_manager = I18nManager()


def get_i18n_manager() -> I18nManager:
    """Get the global i18n manager instance."""
    return _i18n_manager


def t(key: str, use_emoji: bool | None = None, **kwargs) -> str:
    """
    Convenience function for translation.

    Args:
        key: Translation key
        use_emoji: Override emoji setting for this translation
        **kwargs: Format arguments for string formatting

    Returns:
        Translated string
    """
    return _i18n_manager.t(key, use_emoji=use_emoji, **kwargs)


def set_language(language_code: str) -> bool:
    """
    Set the current language.

    Args:
        language_code: Language code

    Returns:
        True if successful, False otherwise
    """
    return _i18n_manager.set_language(language_code)


def get_language() -> str:
    """Get the current language code."""
    return _i18n_manager.get_language()


def get_available_languages() -> list[str]:
    """Get list of available language codes."""
    return _i18n_manager.get_available_languages()


def set_emoji_enabled(enabled: bool) -> None:
    """Enable or disable emoji display."""
    _i18n_manager.set_emoji_enabled(enabled)


def is_emoji_enabled() -> bool:
    """Check if emoji display is enabled."""
    return _i18n_manager.is_emoji_enabled()
