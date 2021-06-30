import datetime
import unittest

from phyton.core.simulation import Simulation, date_index, timedelta_step

one_day = datetime.timedelta(days=1)


class CoreTestCase(unittest.TestCase):
    def test_simulation(self):
        today = datetime.date.today()
        tomorrow = today + one_day
        sim = Simulation(today, tomorrow)
        self.assertEqual(sim.start_date, today)
        self.assertEqual(sim.stop_date, tomorrow)
        self.assertIsNotNone(sim[today])
        for state in sim:
            self.assertFalse(state.evaluated)
        self.assertIsNone(sim[tomorrow])
        sim.run()
        self.assertIsNotNone(sim[tomorrow])
        self.assertEqual(len(sim.states), 2)
        for state in sim:
            self.assertTrue(state.evaluated)
        self.assertEqual(len(sim[today : tomorrow + datetime.timedelta(days=1) : 2]), 1)
        self.assertEqual(len(sim[tomorrow:]), 1)
        self.assertEqual(len(sim[today.isoformat() : tomorrow.isoformat()]), 1)
        with self.assertRaises(IndexError):
            _state = sim[today - one_day]
        with self.assertRaises(ValueError):
            _sim = Simulation(tomorrow, today)

    def test_date_index(self):
        with self.assertRaises(TypeError):
            date_index(())

    def test_timedelta_step(self):
        self.assertEqual(timedelta_step(one_day), one_day)
        with self.assertRaises(TypeError):
            timedelta_step(())
