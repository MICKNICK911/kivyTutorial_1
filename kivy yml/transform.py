def transform(self, x, y):
    return self.perspective(x, y)
    pass

def transform_2D(self, x, y):
    return int(x), int(y)

def perspective(self, x, y):
    translin_y = y * self.perspective_y / self.height
    if translin_y > self.perspective_y:
        translin_y = self.perspective_y

    diff_x = x - self.perspective_x
    diff_y = self.perspective_y - translin_y

    proportionlin_y = diff_y / self.perspective_y
    proportionlin_y = pow(proportionlin_y, 2)

    trans_x = self.perspective_x + diff_x * proportionlin_y
    trans_y = self.perspective_y - proportionlin_y * self.perspective_y

    return int(trans_x), int(trans_y)