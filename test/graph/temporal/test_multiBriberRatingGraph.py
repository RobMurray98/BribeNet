from copy import deepcopy
from unittest import TestCase

from bribery.temporal.nonBriber import NonBriber
from bribery.temporal.randomBriber import RandomBriber
from graph.temporal.noCustomerActionGraph import NoCustomerActionGraph


class TestMultiBriberRatingGraph(TestCase):

    def setUp(self) -> None:
        self.rg = NoCustomerActionGraph((RandomBriber(10), NonBriber(10)))

    def tearDown(self) -> None:
        del self.rg

    def test_neighbours(self):
        for i in range(len(self.rg.get_bribers())):
            for node in self.rg.get_customers():
                self.assertIsInstance(self.rg._neighbours(node, i), list)

    def test_p_rating(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertTrue(self.rg._p_rating(i, b) >= 0)

    def test_median_p_rating(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertTrue(self.rg._median_p_rating(i, b) >= 0)

    def test_sample_p_rating(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertTrue(self.rg._sample_p_rating(i, b) >= 0)

    def test_o_rating(self):
        for b in range(len(self.rg.get_bribers())):
            self.assertTrue(self.rg._o_rating(b) >= 0)

    def test_p_gamma_rating(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertTrue(self.rg._p_gamma_rating(i) >= 0)
                self.assertAlmostEqual(self.rg._p_gamma_rating(i, gamma=0), self.rg._p_rating(i))
                # NOTE: the below test doesn't actually work!
                # P-rating doesn't use the node itself, while O-rating does.
                # So these values will actually differ.
                # self.assertAlmostEqual(self.rg._p_gamma_rating(i, gamma=1), self.rg._o_rating())

    def test_is_influential(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertGreaterEqual(self.rg.is_influential(i, 0.2, b, charge_briber=False), 0)

    def test_bribe(self):
        for i in range(len(self.rg.get_bribers())):
            initial_value = self.rg.eval_graph(i)
            for j in self.rg.get_customers():
                g_copy = deepcopy(self.rg)
                g_copy.bribe(j, 0.1, i)
                bribed_value = g_copy.eval_graph(i)
                self.assertTrue(initial_value != bribed_value)

    def test_eval_graph(self):
        for b in range(len(self.rg.get_bribers())):
            self.assertGreaterEqual(self.rg.eval_graph(b), 0)

    def test_trust_update(self):
        # Set all votes to 0.
        g_copy = deepcopy(self.rg)
        for u in g_copy.get_customers():
            g_copy._votes[u][0] = 0
        for c in g_copy.get_customers():
            g_copy_2 = deepcopy(g_copy)
            # Then bribe one individual.
            g_copy_2.bribe(0, 1, 0)
            # Update the trust.
            g_copy_2._update_trust()
            # Make sure that the trust goes down for each connected node.
            for n in g_copy.get_customers():
                if self.rg._g.hasEdge(c, n):
                    initial_trust = g_copy.get_weight(c, n)
                    updated_trust = g_copy_2.get_weight(c, n)
                    self.assertGreater(initial_trust, updated_trust)
