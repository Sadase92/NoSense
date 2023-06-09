from ursina import *
import random

app = Ursina()
camera.orthographic = True
camera.fov = 10

# Inisialisasi suara
move_sound = Audio('assets/sound/soundmv.mp3', autoplay=False, loop=True)
crash_sound = Audio('assets/sound/crash_sound.wav', autoplay=False)

car = Entity(model='quad', texture='assets/mycar', collider='box', scale=(2, 1), rotation_z=-90, y=-3)

road1 = Entity(model='quad', texture='assets/road', scale=15, z=1)
road2 = duplicate(road1, y=15)
pair = [road1, road2]

enemies = []

score = 0
score_text = Text(text=f"Score: {score}", origin=(-window.aspect_ratio + 5.3, -8.8), scale=2)

def newEnemy():
    if run:
        val = random.uniform(-3.5, 3.5)
        enemy_texture = random.choice(['assets/enemy/enemy1', 'assets/enemy/enemy2', 'assets/enemy/enemy3'])
        new = duplicate(car, texture=enemy_texture, x=2 * val, y=20, color=color.random_color(),
                        rotation_z=90 if val < 0 else -90)
        enemies.append(new)
        invoke(newEnemy, delay=0.6)

newEnemy()

run = True
crash_text = None

def update():
    global score, run, crash_text

    if not run:
        if held_keys['space']:
            restart_game()
        return

    car.x -= held_keys['a'] * 5 * time.dt
    car.x += held_keys['d'] * 5 * time.dt

    car.x = clamp(car.x, -road1.scale_x / 2 + car.scale_x / 2, road1.scale_x / 2 - car.scale_x / 2)

    for road in pair:
        road.y -= 6 * time.dt
        if road.y < -15:
            road.y += 30

    for enemy in enemies:
        if enemy.x < 0:
            enemy.y -= 10 * time.dt
        else:
            enemy.y -= 5 * time.dt
        if enemy.y < -10:
            enemies.remove(enemy)
            destroy(enemy)

    score += time.dt
    score_text.text = f"Score: {int(score):02d}"

    if car.intersects().hit:
        crash()

    play_move_sound()

def crash():
    global run, crash_text
    run = False
    crash_sound.play()
    crash_text = Text(text='Mobil anda kecelakaan!!! Tekan "Space" untuk memulai ulang', origin=(0, 0), scale=2, color=color.red, background=True)

def play_move_sound():
    if run:
        if not move_sound.playing or move_sound.time >= move_sound.length:
            move_sound.play()
        if move_sound.time >= move_sound.length:
            move_sound.time = 0
    else:
        move_sound.stop()

def restart_game():
    global run, score, crash_text, enemies
    run = True
    score = 0
    score_text.text = f"Score: {score:02d}"
    car.x = 0

    if crash_text:
        destroy(crash_text)
        crash_text = None

    for enemy in enemies:
        destroy(enemy)
    enemies = []

    invoke(newEnemy, delay=0.6)

app.run()
