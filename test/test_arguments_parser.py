from unittest import TestCase

from arguments import ArgumentsParser


class TestArgumentsParser(TestCase):
    def test_binning(self):
        arguments_as_string = "n_bins=[3, 2, 2], encode=ordinal, strategy=quantile"
        arguments = ArgumentsParser.parse(arguments_as_string)
        self.assertIsNotNone(arguments, "Argument list cannot be None")
