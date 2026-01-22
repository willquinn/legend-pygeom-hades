from __future__ import annotations

SOURCE_HOLDER = {
    "lat": {"height": 0.0, "cavity_height": 0.0, "cavity_width": 0.0},
    "am": {
        "top_height": 0.0,
        "top_inner_width": 0.0,
        "top_inner_depth": 0.0,
        "bottom_inner_width": 0.0,
        "top_bottom_height": 0.0,
        "top_plate_width": 0.0,
        "top_plate_depth": 0.0,
        "top_plate_height": 0.0,
    },
    "copper": {"height": 0.0, "width": 0.0, "cavity_width": 0.0, "bottom_height": 0.0, "bottom_width": 0.0},
    "top": {
        "top_plate_height": 0.0,
        "top_plate_width": 0.0,
        "top_height": 0.0,
        "top_inner_width": 0.0,
        "bottom_inner_width": 0.0,
        "top_bottom_height": 0.0,
    },
    "inner_width": 0.0,
    "holder_width": 0.0,
    "outer_width": 0.0,
}

SOURCE = {
    "height": 0.0,
    "width": 0.0,
    "foil": {"height": 0.0, "width": 0.0},
    "al_ring": {"height": 0.0, "width_max": 0.0, "width_min": 0.0},
    "capsule": {"width": 0.0, "depth": 0.0, "height": 0.0},
    "collimator": {
        "width": 0.0,
        "depth": 0.0,
        "height": 0.0,
        "beam_width": 0.0,
        "beam_height": 0.0,
        "window": 0.0,
    },
    "epoxy": {"height": 0.0, "width": 0.0},
    "plates": {"height": 0.0, "width": 0.0, "cavity_width": 0.0},
    "offset_height": 0.0,  # only used in the th
    "gdml_dummy": "",
}

LEAD_CASTLE_1 = {
    "base_width": 480,
    "base_depth": 450,
    "base_height": 500,
    "inner_cavity_width": 300,
    "inner_cavity_depth": 250,
    "inner_cavity_height": 500,
    "cavity_width": 120,
    "cavity_depth": 100,
    "cavity_height": 400,
    "top_width": 300,
    "top_depth": 300,
    "top_height": 90,
    "front_width": 160,
    "front_depth": 100,
    "front_height": 400,
}

LEAD_CASTLE_2 = {
    "base_width": 350,
    "base_depth": 350,
    "base_height": 400,
    "inner_cavity_width": 250,
    "inner_cavity_depth": 250,
    "inner_cavity_height": 400,
    "top_width": 200,
    "top_depth": 200,
    "top_height": 50,
    "copper_plate_width": 350,
    "copper_plate_depth": 350,
    "copper_plate_height": 10,
}

LEAD_CASTLE = {}

BOTTOM_PLATE = {
    "width": 750,
    "depth": 750,
    "height": 15,
    "cavity_width": 120,
    "cavity_depth": 940,  # <!--475*2-->
    "cavity_height": 20,
}

CRYOSTAT = {
    "height": 0,
    "width": 0,
    "thickness": 0,
    "position_cavity_from_top": 0,
    "position_cavity_from_bottom": 0,
    "position_from_bottom": 0,
}

POSITIONS_FROM_CRYOSTAT = {
    "detector": 0.0,
    "holder": 0.0,
    "wrap": 0.0,
    "source": {"phi": 0.0, "r": 0.0, "x": 0.0, "y": 0.0, "z": 0.0},
}


def update_dims(hpge_meta: dict, config: dict) -> None:
    POSITIONS_FROM_CRYOSTAT["detector"] = hpge_meta["hades"]["dimensions"]["detector"]["position"]
    POSITIONS_FROM_CRYOSTAT["holder"] = hpge_meta["hades"]["dimensions"]["holder"]["position"]
    POSITIONS_FROM_CRYOSTAT["wrap"] = hpge_meta["hades"]["dimensions"]["wrap"]["position"]

    CRYOSTAT["position_cavity_from_top"] = 1.5
    CRYOSTAT["position_cavity_from_bottom"] = 0.8
    CRYOSTAT["position_from_bottom"] = 250.0
    CRYOSTAT["thickness"] = 1.5

    if hpge_meta["type"] == "bege":
        CRYOSTAT["height"] = 122.2
        CRYOSTAT["width"] = 101.6

    elif hpge_meta["type"] == "icpc":
        xl_orders = [3, 8, 9, 10]
        CRYOSTAT["height"] = 171.0
        if hpge_meta["production"]["order"] in xl_orders:
            CRYOSTAT["width"] = 114.3
        else:
            CRYOSTAT["width"] = 101.6

        if hpge_meta["production"]["order"] == 9 and hpge_meta["production"]["slice"] == "B":
            CRYOSTAT["width"] = 107.95

    LEAD_CASTLE.clear()
    if config["lead_castle"] == 1:
        LEAD_CASTLE.update(LEAD_CASTLE_1)
    elif config["lead_castle"] == 2:
        LEAD_CASTLE.update(LEAD_CASTLE_2)
    else:
        msg = "only 2 lead castle options"
        raise RuntimeError(msg)

    POSITIONS_FROM_CRYOSTAT["source"]["phi"] = 0
    POSITIONS_FROM_CRYOSTAT["source"]["x"] = 0.0
    POSITIONS_FROM_CRYOSTAT["source"]["y"] = 0.0
    POSITIONS_FROM_CRYOSTAT["source"]["z"] = 0.0
    if config["source"] == "am_collimated":
        SOURCE["height"] = 2.0
        SOURCE["width"] = 1.0
        SOURCE["capsule"]["width"] = 20
        SOURCE["capsule"]["depth"] = None
        SOURCE["capsule"]["height"] = 10.0
        SOURCE["collimator"]["width"] = 30.0
        SOURCE["collimator"]["depth"] = 30.0
        SOURCE["collimator"]["height"] = 65.0
        SOURCE["collimator"]["beam_width"] = 1.0
        SOURCE["collimator"]["beam_height"] = 25.6
        SOURCE["collimator"]["window"] = 0.2
    elif config["source"] == "am":
        SOURCE["height"] = 0.1
        SOURCE["width"] = 1.0
        SOURCE["capsule"]["width"] = 11.08
        SOURCE["capsule"]["depth"] = 23.08
        SOURCE["capsule"]["height"] = 2.02
    elif config["source"] == "co":
        SOURCE["height"] = 0.1
        SOURCE["width"] = 5.0
        SOURCE["foil"]["width"] = 20.0
        SOURCE["foil"]["height"] = 0.5
        SOURCE["al_ring"]["height"] = 3.0
        SOURCE["al_ring"]["width_max"] = 30.0
        SOURCE["al_ring"]["width_min"] = 20.0
    elif config["source"] == "ba":
        SOURCE["height"] = 0.1
        SOURCE["width"] = 5.0
        SOURCE["foil"]["width"] = 26.0
        SOURCE["foil"]["height"] = 0.5
        SOURCE["al_ring"]["height"] = 3.0
        SOURCE["al_ring"]["width_max"] = 30.0
        SOURCE["al_ring"]["width_min"] = 26.0
    elif config["source"] == "th":
        SOURCE["height"] = 1.0
        SOURCE["width"] = 1.0
        SOURCE["capsule"]["height"] = 7.0
        SOURCE["capsule"]["width"] = 2.0
        SOURCE["epoxy"]["height"] = 2.2
        SOURCE["epoxy"]["width"] = 1.6
        SOURCE["plates"]["height"] = 2.0
        SOURCE["plates"]["width"] = 8.0
        SOURCE["plates"]["cavity_width"] = 2.0
        SOURCE["collimator"]["height"] = 30.0
        SOURCE["collimator"]["depth"] = 30.0
        SOURCE["collimator"]["width"] = 30.0
        SOURCE["collimator"]["beam_height"] = 15.0
        SOURCE["collimator"]["beam_width"] = 1.0

        if config["measurement_type"] == "top":
            SOURCE["offset_height"] = 0.0
        elif config["measurement_type"] == "lat":
            SOURCE["offset_height"] = 18.0
        else:
            msg = "can only have top or lat measurements"
            raise RuntimeError(msg)
    else:
        msg = "only configured 5 source types"
        raise RuntimeError(msg)

    if config["source"] in ["co", "ba", "am_collimated"]:
        SOURCE_HOLDER["top"]["top_plate_height"] = 3.0
        SOURCE_HOLDER["top"]["top_plate_width"] = 30.0
        SOURCE_HOLDER["top"]["top_height"] = 10.0
        SOURCE_HOLDER["top"]["top_inner_width"] = 20.0
        SOURCE_HOLDER["top"]["top_bottom_height"] = 6.1
        SOURCE_HOLDER["top"]["bottom_inner_width"] = 102.0
        SOURCE_HOLDER["outer_width"] = 108.0
        SOURCE_HOLDER["inner_width"] = 87.0
    elif config["source"] == "am":
        SOURCE_HOLDER["outer_width"] = 108.0
        SOURCE_HOLDER["inner_width"] = 87.0
        SOURCE_HOLDER["am"]["top_height"] = 10.0
        SOURCE_HOLDER["am"]["top_inner_width"] = 7.39
        SOURCE_HOLDER["am"]["top_inner_depth"] = 15.39
        SOURCE_HOLDER["am"]["bottom_inner_width"] = 102.0
        SOURCE_HOLDER["am"]["top_bottom_height"] = 5.6
        SOURCE_HOLDER["am"]["top_plate_width"] = 11.08
        SOURCE_HOLDER["am"]["top_plate_depth"] = 23.08
        SOURCE_HOLDER["am"]["top_plate_height"] = 2.0
    elif config["source"] == "th":
        SOURCE_HOLDER["copper"]["height"] = 30.0
        SOURCE_HOLDER["copper"]["height"] = 32.0
        SOURCE_HOLDER["copper"]["cavity_width"] = 3.0
        SOURCE_HOLDER["copper"]["bottom_height"] = 3.0
        SOURCE_HOLDER["copper"]["bottom_width"] = 50.0
        if config["measurement_type"] == "lat":
            SOURCE_HOLDER["outer_width"] = 181.6
            SOURCE_HOLDER["inner_width"] = 101.6
            SOURCE_HOLDER["lat"]["height"] = 65.0
            SOURCE_HOLDER["lat"]["cavity_height"] = 60.0
            SOURCE_HOLDER["lat"]["cavity_width"] = 50.0
    else:
        msg = ""
        raise RuntimeError(msg)
