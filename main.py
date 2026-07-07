from overlay_lib import Overlay
from classes_directory.minesweeper import *
from classes_directory.vpnmanager import *

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
size = [1920, 1080]
screen = pygame.display.set_mode(size)
overlay = Overlay()
pygame.display.set_caption("igraOverlay")
clock = pygame.time.Clock()
check_box_minesweeper = CheckBox((10, 10, 100, 32), "MINESWEEPER")
check_box_VPN = CheckBox((10, 42, 100, 32), "VPN")

running = True
while running:
    mouse_pos = pyautogui.position()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    overlay.draw_begin()

    overlay.screen.fill([0, 255, 0])
    pygame.draw.rect(overlay.screen, [24, 24, 24], (0, 0, 400, 1080))
    check_box_minesweeper.draw(overlay.screen)
    check_box_VPN.draw(overlay.screen)

    # minesweeper
    if check_box_minesweeper.enabled:
        try:
            worldOfMineSweeper.draw(screen, check_box_minesweeper)
        except Exception as e:
            worldOfMineSweeper = WorldOfMineSweeper([400, 0, 10, 10])
    else:
        try:
            del worldOfMineSweeper
        except Exception as e:
            pass

    # VPN
    if check_box_VPN.enabled:
        try:
            vpn_manager.wait()
        except Exception as e:
            vpn_manager = VPNManager()
    else:
        try:
            del vpn_manager
        except Exception as e:
            pass

    pygame.display.flip()

    overlay.draw_end()
    clock.tick(60)
pygame.quit()
