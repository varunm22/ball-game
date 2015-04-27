from tkinter import *
import time

class pGame:

	def __init__(self):
		self.root = Tk()
		self.root.bind('<Left>', self.leftKey)
		self.root.bind('<Right>', self.rightKey)
		self.root.bind('<space>', self.play)
		self.played = False
		self.root.bind('r', self.rules)
		self.rule = 1
		self.root.bind('a', self.switch)
		self.c = Canvas(self.root, width = 400, height = 400)
		self.c.pack()
		
		self.char = character(50, 250)
		self.levels = []
		self.levels.append(level(list([platform(0, 350, 400, 50), platform(100, 290, 100, 30), platform(200, 230, 100, 30), platform(300, 170, 100, 30), platform(200, 110, 100, 30), platform(100, 50, 100, 30)])))
		self.levels.append(level(list([platform(0, 350, 400, 50), platform(130, 200, 200, 30), platform(50, 130, 100, 30)])))
		self.levels.append(level(list([platform(0, 350, 400, 50), platform(80, 150, 250, 30), platform(360, 290, 40, 30), platform(80, 100, 50, 50)]), list([platform(150, 350, 150, 20)])))
		self.levels.append(level(list([platform(0, 350, 400, 50), platform(350, 125, 50, 225), platform(125, 25, 275, 50), platform(150, 125, 250, 50), platform(0, 200, 80, 20)])))
		
		self.menu()
		self.root.mainloop()

	def leftKey(self, event):
		self.char.sidemove(-3)

	def rightKey(self, event):
		self.char.sidemove(3)

	def menu(self):
		self.c.create_rectangle(0, 350, 400, 400, fill='#32CD32')
		self.c.create_text(200, 100, text='Bouncing Ball Game')
		self.c.create_text(200, 150, text='Press SPACE to play')
		self.c.create_text(200, 200, text='Press the "r" key to see controls and rules')

	def play(self, event):
		if not self.played:
			self.c.delete('all')
			self.levels[0].draw(self.c)
			self.c.create_rectangle(25, 25, 75, 75, fill='#7B68EE')
			self.lvcount = 0
			self.played = True
		
		self.root.after(20, self.animate)

	def rules(self, event):
		if self.rule == 1:
			self.c.delete('all')
			self.c.create_rectangle(0, 350, 400, 400, fill='#32CD32')
			self.c.create_text(200, 100, text='Rules')
			self.c.create_text(200, 150, text='Use the left and right arrow keys to control the ball')
			self.c.create_text(200, 175, text='Bounce on green, avoid red, get to the purple square')
			self.c.create_text(200, 200, text='You can bounce off the walls (This will come in handy later)')
			self.c.create_text(200, 225, text='Press "r" again to return to the main menu')
			self.rule = 2
		elif self.rule == 2:
			self.c.delete('all')
			self.menu()
			self.rule = 1
		
	def switch(self, event):
		if self.lvcount < len(self.levels):
			self.lvcount += 1
			self.c.delete('all')
			self.levels[self.lvcount].draw(self.c)
			self.c.create_rectangle(25, 25, 75, 75, fill='#7B68EE')
		else:
			self.c.delete('all')
			self.c.create_rectangle(0, 350, 400, 400, fill='#32CD32')
			self.c.create_text(200, 100, text='Congrats, you\'ve won!')
			self.c.create_text(200, 150, text='Press SPACE to play again')
		
	def animate(self):
		if self.char.atGoal():
			self.char.goTo(50, 250)
			if self.lvcount < len(self.levels)-1:
				self.lvcount += 1
				self.c.delete('all')
				self.levels[self.lvcount].draw(self.c)
				self.c.create_rectangle(25, 25, 75, 75, fill='#7B68EE')
				self.char.draw(self.c, self.levels[self.lvcount])
				self.root.after(20, self.animate)
			else:
				self.c.delete('all')
				self.c.create_rectangle(0, 350, 400, 400, fill='#32CD32')
				self.c.create_text(200, 100, text='Congrats, you\'ve won!')
		else:
			self.char.draw(self.c, self.levels[self.lvcount])
			self.root.after(20, self.animate)

class character:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.xvel = 0
		self.yvel = 0
		self.count=0

	def draw(self, canv, level):
		self.x += self.xvel
		self.y += self.yvel
		if self.x > 370 and self.xvel > 0:
			self.xvel = -17
			self.yvel -= 8
		elif self.x < 0 and self.xvel < 0:
			self.xvel = 17
			self.yvel -= 8

		if self.xvel > 0:
			self.xvel -= 1
		elif self.xvel < 0:
			self.xvel += 1
		
		if level.onRed(self.x + 15, self.y + 30):
			self.goTo(50, 250)
		if level.touching(self.x + 15, self.y + 30):
			self.yvel = -10
		elif level.touching(self.x + 15, self.y):
			self.yvel = abs(self.yvel) + 3
		else:
			self.yvel += 1

		if self.count == 1:
			canv.delete(self.i)
		self.i = canv.create_oval(self.x, self.y, self.x + 30, self.y + 30, fill='blue')
		
		if self.count == 0:
			self.count = 1

	def sidemove(self, x):
		if (self.xvel < 10 and self.xvel > -10) or (self.xvel > 10 and x < 0) or (self.xvel < -10 and x > 0):
			self.xvel += x

	def goTo(self, x, y):
		self.x = x
		self.y = y

	def atGoal(self):
		return (self.x < 75 and self.y < 75)

class level:

	def __init__(self, platlist, lavalist = []):
		self.platforms = platlist
		self.lavalist = lavalist

	def touching(self, x, y):
		t = False
		for i in self.platforms:
			if i.touch(x, y):
				t = True
		return t	

	def onRed(self, x, y):
		if len(self.lavalist) > 0:
			t = False
			for i in self.lavalist:
				if i.touch(x, y):
					t = True
			return t
		else:
			return False

	def draw(self, canv):
		for i in self.platforms:
			i.draw(canv, '#32CD32')
		for i in self.lavalist:
			i.draw(canv, '#CD3232')

class platform:

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.w = width
		self.h = height

	def touch(self, x, y):
		if y > self.y and y < self.y + self.h and x > self.x and x < self.x + self.w:
			return True
		else:
			return False

	def draw(self, canv, col):
		self.i = canv.create_rectangle(self.x, self.y, self.x + self.w, self.y + self.h, fill=col)

a = pGame()	
