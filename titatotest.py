import unittest
import titato

class TestTTT(unittest.TestCase):
	'''Tests things'''
	def test_playfirst(self):
		obj = titato.Tic_tac_toe()
		assert obj
		assert obj.start(1)
		assert obj.turn(True)
		assert obj.turn(2)
		assert obj.turn(7)
		assert obj.turn(6)
		assert not obj.turn(9)
		assert not obj.turn(0)
		assert not obj.turn(-1)
		assert not obj.turn('11')
		assert not obj.turn('O')
		assert obj.turn(8)
		assert obj.is_tied()
		assert obj.turn_number() == 9
	def test_playsecond(self):
		obj = titato.Tic_tac_toe()
		assert obj
		assert obj.start(2)
		assert obj.turn(2)
		assert obj.turn(4)
		assert obj.is_won()
		assert obj.turn_number() == 5

if __name__ == '__main__':
	unittest.main()
