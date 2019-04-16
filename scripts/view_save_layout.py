import ai2thor.controller
import cv2  # save screengrabs
import os
import sys

out_root = 'data'
objectIds = {  # FloorPlan1 objectIds: (note: gravity doesn't work on apple for some reason...)
    'apple': 'Apple|-00.47|+01.15|+00.48',
    'bowl': 'Bowl|+00.23|+01.10|-00.62',
    'cup': 'Cup|+00.37|+01.65|-02.58',
    'kettle': 'Kettle|+01.04|+00.90|-02.60',
    'plate': 'Plate|+00.96|+01.65|-02.61',
    'potato': 'Potato|-01.66|+00.92|-02.15',
    'tomato': 'Tomato|-00.39|+01.14|-00.81'
}

layouts = {
    # 'layout name': [[['object name 1', x1, y1, z1], ['object name 2', x2, y2, z2], ...],
    #   needs to settle (i.e. add delay for gravity to work before screen grab)]
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
        params = layouts[layout]
    except KeyError:
        print("Layout not found")
        sys.exit(1)
    for move in params[0]:
        event = controller.step(
            dict(action='TeleportObject', objectId=objectIds[move[0]], x=move[1], y=move[2], z=move[3]))
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
        controller.start(player_screen_height=800, player_screen_width=1200)
        controller.reset('FloorPlan1')
        controller.step(dict(action='Initialize', gridsize=0.25))
    else:
        controller.reset('FloorPlan1')

    event = arrange(controller, layout)
    if wait:
        input("press enter to close...")

    return event


def save_layout(layout_list=None, wait=False, save_all=False):
    # layout_list: list of layouts you want to save. Must be a list, even for one layout TODO: better way not requiring list?
    # wait: whether to wait for user input before moving on to next layout
    # save_all: whether to save all layouts
    controller = ai2thor.controller.Controller(quality='High')
    controller.start(player_screen_height=800, player_screen_width=1200)
    controller.reset('FloorPlan1')
    controller.step(dict(action='Initialize', gridsize=0.25))
    if save_all:
        for layout in layouts.keys():
            if wait:
                event = view_layout(layout, controller)
            else:
                event = view_layout(layout, controller, False)
            save_img(event, layout)
    else:
        for layout in layout_list:
            if wait:
                event = view_layout(layout, controller)
            else:
                event = view_layout(layout, controller, False)
            save_img(event, layout)


def main(layout=None, save_all=False):  # save rgb image of layout
    # view_layout('tomato in bowl')
    # save_layout(['tomato next to plate'])
    # save_layout(['tomato up', 'tomato on plate'])
    save_layout(save_all=True)


if __name__ == "__main__":
    main()
