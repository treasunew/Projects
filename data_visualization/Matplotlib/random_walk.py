from random import choice


class RandWalk:
    """ 一个生成随机游走数据的类 """
    def __init__(self, num_points=5000):
        """ 初始化随机游走的属性 """
        self.num_points = num_points
        
        # 所有随机游走的都始于(0,0)
        self.x_values = [0]
        self.y_values = [0]
    
    def fill_walk(self):
        """ 计算随机游走包含的所有点 """
        # 不断游走直到达到列表的长度
        while len(self.x_values) < self.num_points:
            # 决定前进的方向以及沿着个方向前进的距离
            x_step = self.get_step()
            y_step = self.get_step()
            
            # 拒绝原地踏步
            if x_step == 0 and y_step == 0:
                continue
            
            # 计算下一个点的x坐标值和y坐标值
            x = self.x_values[-1] + x_step
            y = self.y_values[-1] + y_step  
            
            self.x_values.append(x)
            self.y_values.append(y)
            
    def get_step(self):
        r_direction = choice([-1,1])
        r_distance = choice([0,1,2,3,4])
        return r_direction * r_distance