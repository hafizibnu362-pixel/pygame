#Create your own shooter

import pygame as gm

class GameSprite(gm.sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        gm.sprite.Sprite.__init__(self)
        self.img = gm.transform.scale(gm.image.load(img), (width, height))
        self.image = gm.transform.scale(gm.image.load(img), (width, height))
        self.speed = speed 
        self.rect = self.img.get_rect()
        self.rect.x = x 
        self.rect.y = y 
    def reset(self):
        mw.blit(self.img, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = gm.key.get_pressed()
        if keys[gm.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[gm.K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        #varibale untuk memunculkan bullet
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed #buat biar musuhnya bisa turun (jatuh)
        global lost #agar variable lost bisa dipakai dimana aja bukan cuma di kelas enemy
        if self.rect.y > 500:
            self.rect.x = randint(80, 620) #buat muncul posisi x monsternya random dimana aja
            self.rect.y = 0
            lost += 1

#untuk membuat sprite (Bullet => salah satu dari sprite)
class Bullet(GameSprite):
    #behaviour dari peluru
    def update(self):
        self.rect.y += self.speed #biar si bulletnya bergerak ke atas
        if self.rect.y < 0: #untuk mendeteksi posisi peluru atas
            self.kill() #menghapus diri sendiri


from random import randint

rocket = Player("rocket.png", 5, 400, 80, 100, 10) #cuma bikin variable player
#sprite group => tempat penampungan sprite
monsters = gm.sprite.Group() #mirip list <= bisa menambahkan item, memanipulasi item dll 
for i in range(1, 6): #for i in range(6) => 0 1 2 3 4 5. range(1, 6) => 1, 2, 3, 4, 5
    #img, x, y, lebar, tinggi, kecepatan
    #saran dean (kalo ada waktu) => enemynya ditambahi dengan asteroid
    monster = Enemy("ufo.png", randint(80, 620), 0, 80, 50, randint(1, 5)) #memunculkan emey
    monsters.add(monster) #menambahkan monster ke dalam monsters (menambahkan item kedalam lisy)
lost = 0

gm.init() #persiapan sebelum bikin game
mw = gm.display.set_mode((700, 500)) #membuat tampilan dengan ukuran 700px 500px
gm.display.set_caption("Shooter game") #membuat judul game
bg = gm.transform.scale(gm.image.load("galaxy.jpg"), (700, 500)) #mengybah ukuran dari ganbar tersebut
fps = gm.time.Clock() #configurasi untuk men setting fps

gm.mixer.init() #persiapan sebelum membuat music
gm.mixer.music.load("space.ogg")
gm.mixer.music.set_volume(0.1)
gm.mixer.music.play(loops=True) #memainkan music
finish = False #check apakah permaianan selesai atau belum
score = 0

#define pergerakan bullet dan membuat win lost screen
bullets = gm.sprite.Group()
gm.font.init() #buat persiapan penggunaan fontnya
font1 = gm.font.Font(None, 80) #variable agar font bisa dipakai
win = font1.render("YOU WIN!", True, (255, 255, 255)) #mengeluarkan tulisan you win dengan warna putih
lose = font1.render("YOU LOSE!", True, (180, 0, 0)) #mengeluarkan tulisan you lose dengan warna merah tua


while True: #yang mengindikasikan gamenya keluar atau tidak ini si while
    for e in gm.event.get():
        if e.type == gm.QUIT: #gm.QUIT = tanda x di layar
            break

        elif e.type == gm.KEYDOWN: #ketika tombol ditekan
            if e.key == gm.K_SPACE: #ini seumpama space atau spasi ditekan
                sound = gm.mixer.Sound("fire.ogg") #untuk melancarkan suara piupiu
                sound.play() #memainkan suara tembakan
                rocket.fire() #untuk menembakkan

    if not finish: #kalo game belom finish maka game berjalan
        mw.blit(bg, (0,0))
        rocket.update() #pergerakan rocket kekanan ke kiri
        monsters.update() #pergerakan mosnternya yang jatuh
        rocket.reset() #agar gambarnya muncul di layar
        monsters.draw(mw) #agar gambarnya muncul di layar
        bullets.update()
        bullets.draw(mw)
        font2 = gm.font.Font(None, 36) #agar font bisa dipakai
        missed = font2.render(f"Missed: {lost}", 1, gm.Color("white")) #buat ngasik tulisan berapa yang sudah miised
        mw.blit(missed, (10, 50)) #menambahkan tulisan kedalam layar
        scored = font2.render(f"Score: {score}", 1, gm.Color("white")) #buat ngasik tulisan berapa yang sudah miised
        mw.blit(scored, (10, 20)) #menambahkan tulisan kedalam layar
        
        #Mendeteksi tabrakan antar bullets dan monster
        collides = gm.sprite.groupcollide(monsters, bullets, True, True) #Kedua true disini dia itu kalo tabrakan spritenya dihilangan gak?
        for c in collides: #mengambil data apakah ada sprite yang bersentuhan, code yang berlaku dijalanka
            score += 1
            monster = Enemy("ufo.png", randint(80, 620), 0, 80, 50, randint(1, 5)) #memunculkan emey
            monsters.add(monster) #menambahkan monster ke dalam monsters (menambahkan item kedalam lisy)
        
        #kalo misal roket dan monsternya tabrakan dan lost sudah lebih dari 5 kali
        if gm.sprite.spritecollide(rocket, monsters, False) or lost >= 5:
            finish = True #game nya selesai
            game = "lose" #gamenya kalah
        
        #ksalo skor melebihi 10
        if score >= 10:
            finish = True #gamenya selesai
            game = "win" #gamenya menang
    
    else:
        #pas game variable ity win
        if game == "win":
            mw.blit(win, (200, 200)) #text winnya di munculkan di koordinat 200, 200
        else: #kalo gamenya adalah lose
            mw.blit(lose, (200, 200)) #tex lose tnya di munculkan di koordinat 200, 200

    gm.display.update() #perintah agar displaynya selalu di update
    fps.tick(60) #tick(detikan) dalam 1 detik layar mau di update berapa kali sih