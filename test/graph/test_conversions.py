from unittest import TestCase
from networkit.generators import WattsStrogatzGenerator

from graph import conversions

class TestConversions(TestCase):
    def setUp(self) -> None:
        self.gen = WattsStrogatzGenerator(30, 2, 0.3)
        self.graph = self.gen.generate()
    
    def test_add_weights(self):
        g_weighted = conversions.to_weighted(self.graph)
        self.assertEqual(self.graph.nodes(), g_weighted.nodes())
        self.assertEqual(self.graph.edges(), g_weighted.edges())
        self.assertEqual(True, g_weighted.isWeighted())