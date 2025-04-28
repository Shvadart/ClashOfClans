import unittest
from unittest.mock import patch, MagicMock
from collect import collect_resources_if_visible

class TestCollectResources(unittest.TestCase):
    
    @patch('collect.find_and_click')
    @patch('collect.debug_screenshot')
    @patch('collect.log')
    def test_collect_resources_success(self, mock_log, mock_debug_screenshot, mock_find_and_click):
        # Мокируем поведение find_and_click, чтобы он возвращал True при нахождении ресурса
        mock_find_and_click.return_value = True
        
        # Запуск тестируемой функции
        result = collect_resources_if_visible()
        
        # Проверка, что функция вернула True (ресурсы были собраны)
        self.assertTrue(result)
        
        # Проверка, что log был вызван с правильным сообщением
        mock_log.assert_called_with('💰 Ресурсы собраны (confidence=0.7): collect_gold.png')

    @patch('collect.find_and_click')
    @patch('collect.debug_screenshot')
    @patch('collect.log')
    def test_collect_resources_not_found(self, mock_log, mock_debug_screenshot, mock_find_and_click):
        # Мокируем find_and_click, чтобы он всегда возвращал False
        mock_find_and_click.return_value = False
        
        # Мокируем debug_screenshot, чтобы вернуть фиктивный путь к скриншоту
        mock_debug_screenshot.return_value = '/fake/path/screenshot.png'
        
        # Запуск тестируемой функции
        result = collect_resources_if_visible()
        
        # Проверка, что функция вернула False (ресурсы не были собраны)
        self.assertFalse(result)
        
        # Проверка, что лог был вызван с правильным сообщением
        mock_log.assert_called_with('⚠️ Ресурсы не найдены. Скриншот сохранен: /fake/path/screenshot.png')
        
    @patch('collect.find_and_click')
    @patch('collect.debug_screenshot')
    @patch('collect.log')
    def test_collect_resources_partial_success(self, mock_log, mock_debug_screenshot, mock_find_and_click):
        # Мокируем find_and_click для имитации нахождения ресурса только с одним изображением
        mock_find_and_click.side_effect = [True, False, False]
        
        # Запуск тестируемой функции
        result = collect_resources_if_visible()
        
        # Проверка, что функция вернула True (ресурс был найден и собран)
        self.assertTrue(result)
        
        # Проверка, что log был вызван с правильным сообщением
        mock_log.assert_called_with('💰 Ресурсы собраны (confidence=0.7): collect_gold.png')
    
if __name__ == '__main__':
    unittest.main()
