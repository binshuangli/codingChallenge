import unittest
import maze

class MazeTest(unittest.TestCase):

	def setUp(self):
		self.test_maze = maze.Maze()

	def test_setDimension(self):
		self.test_maze.setDimension([4,5])
		self.assertEqual(self.test_maze.height, 5)
		self.assertEqual(self.test_maze.width, 4)

	def test_addMirror(self):
		self.assertEqual(self.test_maze.mirrors, [])

		self.test_maze.addMirror([3, 4, '/'])
		self.assertEqual(self.test_maze.mirrors, [[3, 4, '/']])

		self.test_maze.addMirror([3, 0, '/']) 
		self.test_maze.addMirror([1, 2, '\\'])
		self.assertEqual(self.test_maze.mirrors, [[3, 4, '/'],[3, 0, '/'],[1, 2, '\\']])

class LaserTest(unittest.TestCase):
	input_file = "test_input.txt"	#original test maze

	def test_findNextMirror(self):
		test_maze, laser = maze.parseInput(self.__class__.input_file)

		laser.curr_dirc = 'W'
		laser.curr_loc = [4,4]
		self.assertEqual(laser.findClosestMirror(), [3, 4, '/'])

		laser.curr_dirc = 'E'
		laser.curr_loc = [0,2]
		self.assertEqual(laser.findClosestMirror(), [1, 2, '\\'])

		laser.curr_dirc = 'S'
		laser.curr_loc = [3,5]
		self.assertEqual(laser.findClosestMirror(), [3, 4, '/'])

		laser.curr_dirc = 'N'
		laser.curr_loc = [2,2]
		self.assertEqual(laser.findClosestMirror(), [])

	def test_newLaserDirection(self):
		test_maze, laser = maze.parseInput(self.__class__.input_file)

		laser.curr_dirc = 'W'
		laser.newLaserDirection("/")
		self.assertEqual(laser.curr_dirc, 'S')

		laser.curr_dirc = 'E'
		laser.newLaserDirection("/")
		self.assertEqual(laser.curr_dirc, 'N')

		laser.curr_dirc = 'S'
		laser.newLaserDirection("\\")
		self.assertEqual(laser.curr_dirc, 'E')

		laser.curr_dirc = 'N'
		laser.newLaserDirection("\\")
		self.assertEqual(laser.curr_dirc, 'W')

	def test_findFinalLocation(self):
		test_maze, laser = maze.parseInput(self.__class__.input_file)

		laser.curr_dirc = "N"
		laser.curr_loc = [1,4]
		self.assertEqual(laser.findFinalLocation(), [1,5])

		laser.curr_dirc = "W"
		laser.curr_loc = [1,4]
		self.assertEqual(laser.findFinalLocation(), [0,4])

		laser.curr_dirc = "S"
		laser.curr_loc = [2,2]
		self.assertEqual(laser.findFinalLocation(), [2,0])

		laser.curr_dirc = "E"
		laser.curr_loc = [2,3]
		self.assertEqual(laser.findFinalLocation(), [4,3])

class OtherFunctionsTest(unittest.TestCase):

	input_file = "test_input.txt"	#original test maze
	test_input2 = "laserMaze2.txt"	#opposite direciton of the original test maze
	test_input3 = "laserMaze3.txt"	#maze without mirrors
	test_input4 = "laserMaze4.txt"	#maze where laser is trapped in a loop
	
	def test_parseInput(self):
		test_maze, laser = maze.parseInput(self.__class__.input_file)
 		self.assertEqual(test_maze.height, 6)
 		self.assertEqual(test_maze.width, 5)
		self.assertEqual(test_maze.mirrors, [[3, 4, '/'], [3, 0, '/'], [1, 2, '\\'], [3, 2, '\\'], [4, 3, '\\']])
		self.assertEqual(laser.curr_loc, [1,4])
		self.assertEqual(laser.curr_dirc, 'S')

	def test_traverseMaze(self):
		test_maze, laser = maze.parseInput(self.__class__.input_file)
		self.assertEqual(maze.traverseMaze(test_maze, laser), (9, [0,0]))

		test_maze, laser = maze.parseInput(self.__class__.test_input2)
		self.assertEqual(maze.traverseMaze(test_maze, laser), (10, [1,5]))

		test_maze, laser = maze.parseInput(self.__class__.test_input3)
		self.assertEqual(maze.traverseMaze(test_maze, laser), (5, [0,5]))

		test_maze, laser = maze.parseInput(self.__class__.test_input4)
		self.assertEqual(maze.traverseMaze(test_maze, laser), (-1,"NA"))

if __name__ == '__main__':
	unittest.main()