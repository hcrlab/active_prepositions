import ai2thor.controller

objectId_dict = {  # FloorPlan1 objectId_dict:
    'apple': 'Apple|-00.47|+01.15|+00.48',  # gravity doesn't work on apple for some reason...
    'bowl': 'Bowl|+00.23|+01.10|-00.62',
    'bread': 'Bread|-00.52|+01.18|-00.03',
    'butter_knife': 'ButterKnife|-00.41|+01.10|-00.46',
    'cup': 'Cup|+00.37|+01.65|-02.58',
    'kettle': 'Kettle|+01.04|+00.90|-02.60',
    'plate': 'Plate|+00.96|+01.65|-02.61',
    'potato': 'Potato|-01.66|+00.92|-02.15',
    'tomato': 'Tomato|-00.39|+01.14|-00.81'
}


def main():
    wait = True
    offscreen_z = -3  # set z to here to teleport object off-screen
    # should work for objects we're using... if object still visible, decrease number
    controller = ai2thor.controller.Controller(quality='High')
    controller.start(player_screen_height=800, player_screen_width=1200)
    controller.reset('FloorPlan1')
    controller.step(dict(action='Initialize', gridsize=0.25))
    # move unnecessary objects offscreen
    # controller.step(dict(action='TeleportObject', objectId=objectId_dict['apple'], z=offscreen_z))
    # controller.step(dict(action='TeleportObject', objectId=objectId_dict['bread'], z=offscreen_z))
    # controller.step(dict(action='TeleportObject', objectId=objectId_dict['butter_knife'], z=offscreen_z))
    # controller.step(dict(action='TeleportObject', objectId=objectId_dict['butter_knife'], z=offscreen_z))
    # controller.step(dict(action='TeleportFull', x=0, y=1, z=-1.75, rotation=180, horizon=0))
    if wait:
        input("press enter to close...")


if __name__ == "__main__":
    main()
