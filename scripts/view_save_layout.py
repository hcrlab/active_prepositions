import ai2thor.controller
import cv2
import os
import sys
from generate_layout import objectId_dict, player_screen_height, player_screen_width

out_root = 'data'

layout_dict = {
    # 'layout name': [[['object name 1', x1, y1, z1], ['object name 2', x2, y2, z2], ...],
    # needs to settle (i.e. add delay for gravity to work before screen grab)]
    'tomato up': [[['tomato', -0.39, 1.74, -0.81]], False],
    'tomato in bowl': [[['tomato', 0.23, 1.3, -0.62]], True],
    'tomato on plate': [[['plate', -0.39, 1.14, -0.81], ['tomato', -0.39, 1.3, -0.81]], True],
    'bowl on plate': [[['bowl', 0.23, 1.4, -0.62], ['plate', 0.23, 1.2, -0.62]], True],
    'plate on bowl': [[['plate', 0.23, 1.4, -0.62]], True],
    'tomato next to plate': [[['plate', -0.39, 1.14, -0.81], ['tomato', -0.10, 1.3, -0.81]], True]
}


# y   z
# ^   ^
# |  /
# | /
# |/
# -------> x


def arrange(controller, layout):
    try:
        params = layout_dict[layout]
    except KeyError:
        print("Layout not found")
        sys.exit(1)
    for move in params[0]:
        event = controller.step(
            dict(action='TeleportObject', objectId=objectId_dict[move[0]], x=move[1], y=move[2], z=move[3]))
    if params[1]:
        controller.step(dict(action='LookUp'))
        event = controller.step(dict(action='LookDown'))

    return event


def save_img(event, name):
    cv2.imwrite(os.path.join(out_root, name + '.png'), event.cv2img)


def view_layout(layout, controller=None, wait=True):
    # layout: layout that you would like to view
    # controller: feed in a controller, or leave as None to have the function create one. Providing a controller is
    # useful if you are viewing multiple layouts consecutively and want only one unity window
    # wait: whether to wait for user input before closing unity window

    if controller is None:
        controller = ai2thor.controller.Controller(quality='High')
        controller.start(player_screen_height=player_screen_height, player_screen_width=player_screen_width)
        controller.reset('FloorPlan1')
        controller.step(dict(action='Initialize', gridsize=0.25))
    else:
        controller.reset('FloorPlan1')

    # how to create/teleport an object
    # controller.step(
    #     dict(action='CreateObject', objectType='Tomato', randomizeObjectAppearance=False, objectVariation=1))
    # controller.step(dict(action='DropHandObject'))
    # controller.step(dict(action='TeleportObject', objectId='Tomato|1', x=-0.39, y=1.74, z=-0.81))
    event = arrange(controller, layout)
    if wait:
        input("press enter to close...")

    return event


def save_layout(*layouts, wait=False, save_all=False):
    # layouts: list of layouts you want to save.
    # wait: whether to wait for user input before moving on to next layout
    # save_all: whether to save all layouts
    controller = ai2thor.controller.Controller(quality='High')
    controller.start(player_screen_height=800, player_screen_width=1200)
    controller.reset('FloorPlan1')
    controller.step(dict(action='Initialize', gridsize=0.25))
    if save_all:
        for layout in layout_dict.keys():
            if wait:
                event = view_layout(layout, controller)
            else:
                event = view_layout(layout, controller, False)
            save_img(event, layout)
    else:
        for layout in layouts:
            if wait:
                event = view_layout(layout, controller)
            else:
                event = view_layout(layout, controller, False)
            save_img(event, layout)


def main():
    view_layout('tomato up')
    # save_layout(save_all=True)


if __name__ == "__main__":
    main()
