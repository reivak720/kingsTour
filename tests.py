import kingsTour
import roomba
import unittest

class TestPositions(unittest.TestCase):

    def testGetX(self):
        p = roomba.Position(1,2)
        x = p.getX()
        self.assertEqual(x, 1)

    def testGetY(self):
        p = roomba.Position(1, 2)
        y = p.getY()
        self.assertEqual(y, 2)

    def testGetTimeToPos(self):
        p = roomba.Position(1, 1)
        posible_positions = roomba.product(range(3), repeat=2)
        func_soultions = []
        for element in posible_positions:
            solution = p.getTimeToPos(roomba.Position(element[0], element[1]),1)
            func_soultions.append(solution)
        repetition = [2**.5, 1.0]
        solutions = repetition*2 + [0] + list(reversed(repetition)) * 2
        self.assertListEqual(func_soultions, solutions)

    def testGetBearing(self):
        p = roomba.Position(1, 1)
        posible_positions =[element for element in roomba.product(range(3), repeat=2) if element != (1,1)]
        func_soultions = []
        for element in posible_positions:
            solution = p.getBearing(roomba.Position(element[0], element[1]))
            func_soultions.append(solution)
        solutions = [225.0, 180.0, 135.0, 270.0, 90.0, 315.0, 0.0, 45.0]
        self.assertListEqual(func_soultions, solutions)

    def testGetNewPosition(self):
        pass

class TestRooom(unittest.TestCase):

    def testGetDimensions(self):
        r = roomba.RectangularRoom(50, 6)
        self.assertEqual(r.get_dimensions(), (6, 50))


    def testIsTileClean(self):
        r = roomba.RectangularRoom(6, 10)
        self.assertFalse(r.isTileCleaned(1, 1))


    def testCleanTileAtPosition(self):
        r = roomba.RectangularRoom(10, 10)
        r.cleanTileAtPosition(roomba.Position(1, 1))
        self.assertTrue(r.isTileCleaned(1,1))


    def testGetNumberOfTiles(self):
        r = roomba.RectangularRoom(3, 4)
        self.assertEqual(r.getNumTiles(), 12)


    def testGetNumCleanedTiles(self):
        r = roomba.RectangularRoom(3, 4)
        self.assertEqual(r.getNumCleanedTiles(), 0)    


    def testGetNumClenedTiles1(self):
        r = roomba.RectangularRoom(3, 4)
        r.cleanTileAtPosition(roomba.Position(2, 2))
        self.assertEqual(r.getNumCleanedTiles(), 1)


    def testGetNumCleanedTilesAll(self):
        r = roomba.RectangularRoom(3, 4)
        for tile in roomba.product(range(4), range(3)):
            x, y = tile
            r.cleanTileAtPosition(roomba.Position(x, y))
        self.assertEqual(r.getNumCleanedTiles(), 12)


    def testIsPositionInRoom(self):
        r = roomba.RectangularRoom(4, 3)
        self.assertTrue(r.isPositionInRoom(roomba.Position(2, 3)))


    def testIsPositionInRoomNot(self):
        r = roomba.RectangularRoom(4, 3)
        self.assertFalse(r.isPositionInRoom(roomba.Position(3, 2)))


    def testGetRandomPosition(self):
        r = roomba.RectangularRoom(4, 3)
        position = r.getRandomPosition()
        self.assertTrue(r.isPositionInRoom(position))


class TestRobot(unittest.TestCase):
    r = roomba.RectangularRoom(5, 5)
    robot = roomba.Robot(r, 1)
    
    def testCleanedInitTile(self):
        position = self.robot.getRobotPosition()
        x, y = position.getX(), position.getY()
        self.assertTrue(self.r.isTileCleaned(int(x), int(y)))

    def testSetPosition(self):
        self.robot.setRobotPosition(roomba.Position(3, 3))
        position = self.robot.getRobotPosition()
        self.assertEqual((position.getX(), position.getY()), (3, 3))


    def testSetDirection(self):
        r = roomba.RectangularRoom(5, 5)
        self.robot = roomba.Robot(r, 1)
        self.robot.setRobotDirection(227)
        self.assertEqual(self.robot.getRobotDirection(), 227)

class TestStandardRobot(unittest.TestCase):

    r = roomba.RectangularRoom(5, 5)

    
    def testMovement(self):
        robot = roomba.StandardRobot(self.r, 1)
        position = robot.getRobotPosition()
        robot.updatePositionAndClean()
        bearing = robot.getRobotDirection()
        rob_pos = robot.getRobotPosition()
        calc_pos = position.getNewPosition(bearing, 1)
        self.assertEqual((rob_pos.getX(), rob_pos.getY()), (calc_pos.getX(), calc_pos.getY()))

    def testChangeHeading(self):
        robot = roomba.StandardRobot(self.r, 1)
        robot.setRobotPosition(roomba.Position(0,0))
        robot.setRobotDirection(180)
        robot.updatePositionAndClean()
        self.assertNotEqual(robot.getRobotDirection(), 180) and self.assertTrue(self.r.isPositionInRoom(robot.getRobotPosition()))

    def testPositionIsClean(self):
        robot = roomba.StandardRobot(self.r, 1)
        robot.updatePositionAndClean()
        position = robot.getRobotPosition()
        self.assertTrue(self.r.isTileCleaned(int(position.getX()), int(position.getY())))


class TestRandomRobot(unittest.TestCase):
    r = roomba.RectangularRoom(10, 10)

    def testHeadingChange(self):
        robot = roomba.RandomWalkRobot(self.r, 1)
        direction = robot.getRobotDirection()
        robot.updatePositionAndClean()
        self.assertNotEqual(direction, robot.getRobotDirection())

    def testMovement(self):
        robot = roomba.RandomWalkRobot(self.r, 1)
        position = robot.getRobotPosition()
        robot.updatePositionAndClean()
        direction = robot.getRobotDirection()
        rob_p = robot.getRobotPosition()
        calc_p = position.getNewPosition(direction, 1)
        self.assertEqual((rob_p.getX(), rob_p.getY()), (calc_p.getX(), calc_p.getY()))

    
    def testPositionIsClean(self):
        robot = roomba.RandomWalkRobot(self.r, 1)
        robot.updatePositionAndClean()
        position = robot.getRobotPosition()
        self.assertTrue(self.r.isTileCleaned(int(position.getX()), int(position.getY())))


class TestGraphDrivenRobot(unittest.TestCase):
    r = roomba.RectangularRoom(10, 8)

    def testPositions(self):
        robot = roomba.GraphDrivenRobot(self.r, 1)
        position = robot.getRobotPosition()
        positions = [(int(pos.getX()), int(pos.getY())) for pos in robot.get_positions()]
        king = kingsTour.PathFinder(8, 10, (int(position.getX()), int(position.getY())))
        kings_positons = king.get_path()
        self.assertListEqual(positions, kings_positons)

    def testBearings(self):
        robot = roomba.GraphDrivenRobot(self.r, 1)
        headings = robot.get_headings()
        position = robot.getRobotPosition()
        king = kingsTour.PathFinder(8, 10, (int(position.getX()), int(position.getY())))
        kings_positions = [roomba.Position(x, y) for x, y in king.get_path()]
        kings_bearings = [pos.getBearing(kings_positions[i+1]) for i, pos in enumerate(kings_positions[:-1])]
        self.assertListEqual(headings, kings_bearings)

    def testNavigate(self):
        robot = roomba.GraphDrivenRobot(self.r, 1)
        position = robot.getRobotPosition()
        positions = robot.get_positions()
        time_to_way = position.getTimeToPos(positions[0], 1)
        time = robot.Navigate(time_to_way)
        r_pos = robot.getRobotPosition()
        self.assertEqual((positions[0].getX(), positions[0].getY()), (r_pos.getX(), r_pos.getY())) and self.assertEqual(time, 1-time_to_way)

    
    def testNavigateRaise(self):
        robot = roomba.GraphDrivenRobot(self.r, 1)
        robot.setRobotDirection(0)
        robot.Navigate(100)
        self.assertRaises(ValueError)

        
if __name__=="__main__":
    unittest.main()


