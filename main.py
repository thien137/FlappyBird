#!/usr/bin/env python
#
# Flappy Bird
#
#

import pygame
import time
import random

# Initialize
pygame.init()
pygame.mixer.init()
# Window

window = pygame.display.set_mode((288, 512))

# Title and Icon
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('yellowbird-midflap.png')
pygame.display.set_icon(icon)

# Background
if list(time.localtime())[3] > 4 and list(time.localtime())[3] < 19:
	background_img = pygame.image.load('background-day.png')
else:
	background_img = pygame.image.load('background-night.png')

# Numbers
IMAGES = []
for i in range(10):
	eval(f'IMAGES.append(pygame.image.load("{i}.png"))')
# Music
score_sound = pygame.mixer.Sound('sfx_point.wav')
hit_sound = pygame.mixer.Sound('sfx_hit.wav')
die_sound = pygame.mixer.Sound('sfx_die.wav')
jump_sound = pygame.mixer.Sound('sfx_wing.wav')
score_sound.set_volume(0.05)
hit_sound.set_volume(0.05)
die_sound.set_volume(0.05)
jump_sound.set_volume(0.05)

# GAME OVER
gameover = pygame.image.load('gameover.png')
#score_noise = mixer.music.load('point.mp3')
# Character
class YellowBird:
	def __init__(self):
		self.x = 90
		self.y = 175
		self.upflap = pygame.image.load('yellowbird-upflap.png')
		self.midflap = pygame.image.load('yellowbird-midflap.png')
		self.downflap = pygame.image.load('yellowbird-downflap.png')
		self.counter = 0
		
	def draw(self, x, y, counter):
		img = self.midflap
		if self.counter <= 100:
			img = self.midflap
		elif self.counter <= 200:
			img = self.upflap
		elif self.counter <= 300:
			img = self.midflap
		elif self.counter <= 400:
			img = self.downflap

		if self.counter == 400:
			self.counter = 0
		else:
			self.counter += 5

		img = pygame.transform.rotate(img, counter)
		window.blit(img, (x, y))

# Pipe
class Pipes:
	def __init__(self):
		self.P1 = pygame.image.load('pipe-green.png')
		self.P2 = pygame.transform.flip(pygame.image.load('pipe-green.png'), False, True)
		self.P_X = 288
		self.P1_Y = random.randint(200 , 350)
		self.P2_Y = self.P1_Y - 500
		self.velocity = 1
		self.moving = False
		self.past = False

	def draw(self, x1, y1, x2, y2):
		window.blit(self.P1, (x1, y1))
		window.blit(self.P2, (x2, y2))

	def isCollision(self, birdx, birdy):
		if abs(self.P_X - birdx) <= 32 or ((birdx > self.P_X) and abs(self.P_X - birdx) <= 52):
			if self.P1_Y-birdy - 32 <= 0 or (self.P2_Y + 320) - birdy >= 0: 
				return True
		if birdy >= 365:
			return True

# Ground
class Grounds():
	def __init__(self):
		self.img = pygame.image.load('base.png')
		self.x = 288
		self.y = 400
		self.moving = False
		self.velocity = 1

	def draw(self, x, y):
		window.blit(self.img, (x, y))

# Show Score
def show_score(score):
	scoreDigits = [int(x) for x in list(str(score))]
	totalWidth = sum([IMAGES[x].get_width() for x in scoreDigits])

	Xoffset = (window.get_width() - totalWidth) / 2

	for digit in scoreDigits:
		window.blit(IMAGES[digit], (Xoffset, 60))
		Xoffset += IMAGES[digit].get_width()

# Variables

#CHARACTER
yellowbird = YellowBird()

#PIPES
pipes = []
for i in range(4):
	pipe = Pipes()
	pipes.append(pipe)

# Ground
grounds = []
ground_zero = Grounds()
ground_zero.x = 0
grounds.append(ground_zero)
for i in range(3):
	ground = Grounds()
	grounds.append(ground)

# BIRD STATES	
isJump = False
isFall = False

# ANGLE DEVELOPMENT
FallCounter = 0

# MOVEMENT MATH 
jumpCount = 500
fallCount = 100

# Score

score = 0

# GAME OVER
Alive = True

# Main Loop

running = True
while running:
	pygame.time.delay(5)

	window.fill((0, 0, 0))

	for event in pygame.event.get():
		
		# Quit Game
		if event.type == pygame.QUIT:
			running = False

		# Get Jump Press
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and Alive == True:
				isJump = True
				jump_sound.play()
				jumpCount = 500
				fallCount = 0
			#RESTART
			if event.key == pygame.K_r and Alive == False:
				Alive = True
				yellowbird.x = 90
				yellowbird.y = 175
				pipes = []
				for i in range(4):
					pipe = Pipes()
					pipes.append(pipe)
				isJump = False
				score = 0
				isFall = False
				FallCounter = 0

	# Falling
	if yellowbird.y <= 365:
		if not Alive:
			if fallCount % 10 == 0:
				yellowbird.y += fallCount ** 2 * 0.00002
			isFall = True
			fallCount += 10
			die_sound.play()
	
	# Jumping
	if Alive:
		if isJump:
			neg = 1
			if jumpCount < 0:
				neg = -1
				isFall = True
			else:
				isFall = False
			if yellowbird.y <= 0:
				jumpCount = -100
			if abs(jumpCount) % 10 == 0:
				yellowbird.y -= jumpCount ** 2 * 0.00002 * neg
				jumpCount
			if jumpCount > -500:
				jumpCount -= 10

	# Calibration
	if isFall:
		if FallCounter >= -25:
			FallCounter -= 25
	elif not isFall:
		if FallCounter <= 25:
			FallCounter += 25


	# Pipe Movement
	if Alive and isJump:
		for i in range(len(pipes)):
			# Generating and Moving Pipes
			if i == 0:
				pipes[i].moving = True
			elif pipes[i-1].P_X <= 130:
				pipes[i].moving = True
			if pipes[i].P_X <= -52:
				new_pipe = Pipes()
				pipes.pop(0)
				pipes.append(new_pipe)
			if pipes[i].moving == True:
				pipes[i].P_X -= pipes[i].velocity

			# Scoring Passing Pipes
			if pipes[i].past == False:
				if pipes[i].P_X <= 50:
					score += 1
					score_sound.play()
					pipes[i].past = True

	# Ground Movement
	if Alive and isJump:
		for i in range(len(grounds)):
			# Generating and Moving Pipes
			if i == 0:
				grounds[i].moving = True
			elif grounds[i-1].x <= 0:
				grounds[i].moving = True
			if grounds[i].x <= -336:
				new_ground = Grounds()
				grounds.pop(0)
				grounds.append(new_ground)
			if grounds[i].moving == True:
				grounds[i].x -= grounds[i].velocity

	# BLITTING

	# Backgroung Image
	window.blit(background_img, (0, 0))

	#Pipes
	for pipe in pipes:
		pipe.draw(pipe.P_X, pipe.P1_Y, pipe.P_X, pipe.P2_Y)
		# PIPE COLLISION
		if pipe.isCollision(yellowbird.x, yellowbird.y):
			if Alive == True:
				hit_sound.play()
			Alive = False

	# Bird
	yellowbird.draw(yellowbird.x, yellowbird.y, FallCounter)

	# Ground Image
	for ground in grounds:
		ground.draw(ground.x, ground.y)

	# Show Score
	if Alive:
		show_score(score)

	# Game Over
	if not Alive:
		window.blit(gameover, ((window.get_width()-gameover.get_width())/2, 50))
	
	pygame.display.update()

