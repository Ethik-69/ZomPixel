#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time


def test(main):
    """Affiche des valeur de test"""
    text0 = main.test_font0.render('ClickPosX : %s ClickPosY : %s' % (main.click_pos_x, main.click_pos_y), True, (0, 0, 0))
    text1 = main.test_font0.render('Zombie X : %s Y : %s moveX : %s moveY : %s - %s' % (main.player.rect.x, main.player.rect.y, main.player.moveX, main.player.moveY, main.player.action), True, (0, 0, 0))
    text2 = main.test_font0.render('Score : %s' % main.player.score, True, (0, 0, 0))
    text3 = main.test_font0.render('Is Feeding : %s' % main.player.is_feeding, True, (0, 0, 0))
    text4 = main.test_font0.render('Lvl Number : %s' % main.levels.current_level.number, True, (0, 0, 0))
    text5 = main.test_font0.render('Time - %s : %s : %s ' % (main.time.chronos['current_level'].Time[0],
                                                             main.time.chronos['current_level'].Time[1],
                                                             main.time.chronos['current_level'].Time[2]), True, (0, 0, 0))
    main.window.blit(text0, (680, 5))
    main.window.blit(text1, (600, 20))
    main.window.blit(text2, (600, 40))
    main.window.blit(text3, (600, 60))
    main.window.blit(text4, (10, 25))
    main.window.blit(text5, (10, 45))
    fps(main)


def fps(main):
    """Affiche les frames par seconde"""
    main.frameCount += 1
    if main.frameCount % 500 == 0:
        t1 = time.clock()
        main.frameRate = 500 / (t1 - main.t0Fps)
        main.t0Fps = t1
    the_text = main.test_font0.render("Frame = {0},  rate = {1:.2f} fps".format(main.frameCount, main.frameRate), True, (0, 0, 0))
    main.window.blit(the_text, (10, 5))
