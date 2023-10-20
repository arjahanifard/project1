from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty,NumericProperty,ReferenceListProperty
from kivy.vector import Vector
from random import randint
class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velicity = Vector(4,0).rotate(randint(0,360))
    def update(self,dt):
        self.ball.move()
        if self.ball.y<0 or self.ball.top > self.height:
            self.ball.velicity_y *=-1
        # if self.ball.x<0 or self.ball.right > self.width:
        #     self.ball.velocity_x *=-1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        if self.ball.x < 0:
            self.player2.score+=1
            self.serve_ball()
        if self.ball.right > self.width:
            self.player1.score+=1
            self.serve_ball()

    def on_touch_move(self,touch):
        if touch.x < self.width/3:
            self.player1.center_y=touch.y
        if touch.x > 2 * self.width/3:
            self.player2.center_y=touch.y

class PongBall(Widget):
    velocity_x=NumericProperty(0)
    velicity_y=NumericProperty(0)
    velicity = ReferenceListProperty(velocity_x,velicity_y)
    def move(self):
        self.pos = Vector(self.pos)+Vector(self.velicity)
        #self.velicity = Vector(self.velicity)
class PongPaddle(Widget):
    score = NumericProperty()
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            vx,vy = ball.velicity
            bounced = Vector(-1*vx,vy)
            vel = 1.1 * bounced
            ball.velicity = vel.x,vel.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update,1.0/60.0)
        return game
PongApp().run()