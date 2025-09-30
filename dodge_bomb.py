import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

"""
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_dict = {
        (0 , 0): rotozoom(kk_img, 0, 1.0),
        (+5, 0): rotozoom(kk_img, 180, 1.0),
        (+5, -5): rotozoom(kk_img,135, 1.0),
        (0, -5): rotozoom(kk_img,90, 1.0)

    }
"""


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数なし
    戻り値：拡大率と加速度のタプル
    10回分の加速度と拡大率の作成
    """
    bb_imgs = []
    for r in range(1, 11):  #10回ループ
        bb_img = pg.Surface((20*r, 20*r))  #Surfaceをr倍
        bb_img.set_colorkey((0, 0, 0))  #色をなくして枠を消す
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  #bombをr倍
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]  #加速度の設定
    return bb_imgs, bb_accs


def gameover(screen: pg.Surface) -> None:
    """
    引数はscreen
    5秒間ゲームオーバー画面を表示する
    """
    gobg_img = pg.Surface((WIDTH, HEIGHT))  #空のSurfaceの作成
    bk_img = gobg_img.get_rect()
    pg.draw.rect(gobg_img, (0, 0, 0), bk_img, 0)  #黒の矩形の作成
    gobg_img.set_alpha(200)  #透明度の設定
    go_fonto  = pg.font.Font(None, 80)
    txt = go_fonto.render("Game Over", True, (255, 255, 255))  #ゲームオーバーという文字を作成
    txt.set_alpha(255)  #ゲームオーバーの文字を不透明に
    gobg_img.blit(txt,(WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2)) #中央にゲームオーバーをblit
    go_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    go_kk_img.set_alpha(255) #こうかとんを不透明に
    gobg_img.blit(go_kk_img, (320, 325))
    gobg_img.blit(go_kk_img,(730, 325))
    screen.blit(gobg_img, [0, 0])
    pg.display.update()
    time.sleep(5)
    return
    

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数はこうかとんRect or 爆弾Rect
    戻り値:判定結果タプル（横方向, 縦方向）
    画面内ならTrue/画面がいならFalse
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:  #横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  #縦方向にはみ出していたら
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")   
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    vx, vy = 5, 5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  #こうかとんと爆弾の衝突判定
            gameover(screen)
            return #ゲームオーバー

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        #if key_lst[pg.K_DOWN]:
            #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
            #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
            #sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
