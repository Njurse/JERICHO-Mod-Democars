DEMOCARS - one-car Driver 2 car-data bank
================================

Source: VEGAS model 1
Destination model slot: 1

This bank carries ONE car: clean, damaged and low. Every other model
slot is -1.

Files:
  bank.json          the declaration (slot order, cars)
  DEMOCARS.LEV / .LCF      installed copies of build/ (loadable pair)
  cars/              the car's editable OBJ/MTL, page PNGs and sounds
  build/             the bake output, never edited (safe to delete)

Install:
  Shipped as a mod (JERICHO/MODS/<id>/banks/<dir>/), carhacks 0.2.7+
  registers it on its own when the mod is enabled. By hand:
  1. Put this folder where cities.ini can reach it.
  2. Add the line from cities.ini under [cities] in
     JERICHO/CONFIG/cities.ini.
  3. Import it with import = <resident slot>:<city index>:<model>.
     city_N has city index 11 (11 + N).

Stage scripts (written beside this file):
  wizard.bat    hub for every stage below
  rebake.bat    bake + install + register, then preview / ride
  preview.bat   pick a slot, endless preview until you quit
  playtest.bat  Take a Ride with a car, no bake

Rebuild after editing the car's OBJ or bank.json:
  rebake.bat

Wheel art (cars/<car>/handling.json -> "wheels"):
  Each car may declare its own clean/damaged/fast sprites. They live on a page
  and a rect (set + island), and nothing may share a rect unless it is the same
  sprite: the bake refuses a wheel that overlaps another car's wheel or the
  body art on that page, naming both sides.

  Let the bake place them instead of guessing coordinates:

      "clean": {"png": "textures/wheelclean.png", "set": 20, "island": "auto"}

  "auto" puts the sprite in the first free rect on the page (after the body's
  art and the wheels already placed), moves it to another page the bank carries
  when that page is full, and stops with a per-page inventory when nothing has
  room. The placement is the same on every bake, and rebake.bat records it.
