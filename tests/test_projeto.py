import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import utils  # noqa: E402


class TestArquivosJson(unittest.TestCase):
    def test_todos_os_json_de_dados_sao_validos(self):
        arquivos = list((ROOT / "data").glob("*.json"))
        self.assertTrue(arquivos, "Nenhum arquivo JSON foi encontrado em data/.")

        for caminho in arquivos:
            with self.subTest(arquivo=caminho.name):
                with caminho.open("r", encoding="utf-8") as arquivo:
                    json.load(arquivo)


class TestUtils(unittest.TestCase):
    def test_salvar_e_carregar_json_preserva_acentos(self):
        with tempfile.TemporaryDirectory() as pasta:
            data_dir_original = utils.DATA_DIR
            utils.DATA_DIR = Path(pasta)
            try:
                esperado = [{"competência": "Comunicação"}]
                utils.salvar_json("teste.json", esperado)
                self.assertEqual(utils.carregar_json("teste.json"), esperado)
            finally:
                utils.DATA_DIR = data_dir_original

    def test_carregar_json_inexistente_retorna_padrao(self):
        with tempfile.TemporaryDirectory() as pasta:
            data_dir_original = utils.DATA_DIR
            utils.DATA_DIR = Path(pasta)
            try:
                self.assertEqual(utils.carregar_json("ausente.json", {}), {})
            finally:
                utils.DATA_DIR = data_dir_original


if __name__ == "__main__":
    unittest.main()
