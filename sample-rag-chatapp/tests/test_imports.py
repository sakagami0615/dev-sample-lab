import importlib
import os
import sys
import unittest
from unittest.mock import patch


ENVIRONMENT = {
    "OPENAI_API_KEY": "test-key",
    "OPENAI_API_MODEL": "gpt-4.1-mini",
    "OPENAI_API_TEMPERATURE": "0",
    "USER_AGENT": "dev-sample-lab-test",
}


class ImportTests(unittest.TestCase):
    def setUp(self) -> None:
        for module_name in ("app.main", "app.setting", "sample.sample_rag"):
            sys.modules.pop(module_name, None)

    def test_streamlit_app_imports_as_project_module(self) -> None:
        with patch.dict(os.environ, ENVIRONMENT, clear=False):
            module = importlib.import_module("app.main")

        self.assertTrue(callable(module.main))

    def test_standalone_rag_sample_imports_from_project_root(self) -> None:
        with patch.dict(os.environ, ENVIRONMENT, clear=False):
            module = importlib.import_module("sample.sample_rag")

        self.assertTrue(callable(module.main))


if __name__ == "__main__":
    unittest.main()
