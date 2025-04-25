from collections import namedtuple
from unittest import TestCase

from api_pgd_client.namedtuples import HeaderItem
from api_pgd_client.utils.headers import create_headers_with


class CreateHeadersWithTestCase(TestCase):
    def setUp(self):
        self.header_items = [
            HeaderItem("key1", "value1"),
            HeaderItem("key2", "value2"),
        ]

    def test_deveria_retornar_dicionario_de_itens(self):
        expected_result = {
            "key1": "value1",
            "key2": "value2",
        }
        result = create_headers_with(self.header_items)
        self.assertEqual(expected_result, result)

    def test_deveria_levantar_exception_quando_tupla_nao_tem_name(self):
        WithoutName = namedtuple("WithoutName", ("name_", "value"))
        header_items = [
            self.header_items[0],
            WithoutName("key2", "value2"),
        ]
        with self.assertRaises(Exception) as context:
            create_headers_with(header_items)
        self.assertEqual(
            "All header items should be a api_pgd_client.namedtuples.HeaderItem object",
            str(context.exception),
        )

    def test_deveria_levantar_exception_quando_tupla_nao_tem_value(self):
        WithoutValue = namedtuple("WithoutValue", ("name", "value_"))
        header_items = [
            self.header_items[0],
            WithoutValue("key2", "value2"),
        ]
        with self.assertRaises(Exception) as context:
            create_headers_with(header_items)
        self.assertEqual(
            "All header items should be a api_pgd_client.namedtuples.HeaderItem object",
            str(context.exception),
        )
