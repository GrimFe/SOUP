import SOUP.Serpent2InputWriter as siw


def simulation_gu3_cycle_16(exitfile=None):
    # --------------------------------- PARAMETERS ------------------------------------
    pin_radius = 0.4555
    cell_side_length = 0.715 * 2
    extra_water_thickness = 0.055
    n_side_pins = 15

    # --------------------------------- COMPOSITION ------------------------------------
    fuel_temperature = 1200
    environment_temperature = 600
    fuel = siw.Material(name='fuel_1',
                        dens=-10.4,
                        comment=siw.Comment("UO2 fuel with enrichment 4.1%"),
                        representation=siw.MaterialRepresentation.from_material_composition(
                            siw.MaterialComposition.from_za(
                                {92234: 9.90723e-6, 92235: 9.63007e-4, 92238: 2.22307e-2, 8016: 4.64201e-2,
                                 8017: 1.85755e-5}), tmp=fuel_temperature),
                        burn=True,
                        tmp=fuel_temperature
                        )
    fuel.divide(lvl=1, kind="radial", sub=(10, 0, pin_radius))
    fuel_sample = siw.Material(name='fuel_3',
                               dens=-10.4,
                               comment=siw.Comment("UO2 fuel with enrichment 4.1% - Fuel sample"),
                               representation=siw.MaterialRepresentation.from_material_composition(
                                   siw.MaterialComposition.from_zam(
                                       {922340: 9.90723e-6, 922350: 9.63007e-4, 922380: 2.22307e-2, 80160: 4.64201e-2,
                                        80170: 1.85755e-5}), tmp=fuel_temperature),
                               burn=True,
                               tmp=fuel_temperature
                               )
    fuel_sample.divide(lvl=1, kind="radial", sub=(10, 0, pin_radius))
    helium = siw.Material(name='He_2',
                          dens=1.23372e-4,
                          comment=siw.Comment("Helium gap material"),
                          representation=siw.MaterialRepresentation.from_material_composition(
                              siw.MaterialComposition.from_nuclides({"He-3": 2.46744e-10, "He-4": 1.23372e-4}),
                              tmp=environment_temperature),
                          tmp=environment_temperature
                          )
    zircaloy = siw.Material(name='clad_3',
                            dens=-6.55,
                            tmp=environment_temperature,
                            comment=siw.Comment("Zircaloy cladding"),
                            representation=siw.MaterialRepresentation.from_string(string="""    40090 2.18292E-02
    40091 4.76042E-03
    40092 7.27640E-03
    40094 7.37399E-03
    40096 1.18798E-03
    26054 9.09090E-06
    26056 1.42580E-04
    26057 3.29448E-06
    26058 4.35120E-07
    24050 3.62373E-06
    24052 6.98800E-05
    24053 7.92383E-06
    24054 1.97241E-06
    08016 2.71092E-04
    08017 1.08480E-07
    50112 4.64145E-06
    50114 3.15810E-06
    50115 1.62690E-06
    50116 6.95739E-05
    50117 3.67488E-05
    50118 1.15893E-04
    50119 4.11032E-05
    50120 1.55895E-04
    50122 2.21546E-05
    50124 2.77052E-05""",
                                                                                  tmp=environment_temperature)
                            )
    water_components = "H1, H2, O16, O17, B10, B11".split()
    water_densities = [4.70654e-2, 5.41314e-6, 2.35265e-2, 8.94345e-6, 5.37619e-6, 1.96183e-5]
    moderator_library = "lwe70"
    hydrogen_za = 1001
    water = siw.Material(name="water",
                         dens=-0.7042,
                         tmp=environment_temperature,
                         comment=siw.Comment("Borated water - 638 ppm B"),
                         moder=[(moderator_library, hydrogen_za)],
                         representation=siw.MaterialRepresentation.from_material_composition(
                             siw.MaterialComposition.from_nuclides(dict(zip(water_components, water_densities))),
                             tmp=environment_temperature
                         ))

    # --------------------------------- GEOMETRY ------------------------------------
    all_fuel = siw.NestedUniverse(name=10)
    all_guides = siw.NestedUniverse(name=20)
    sample_universe = siw.NestedUniverse(name=30)
    external_universe = siw.NestedUniverse(name=0)

    fuel_pin = siw.Pin(name=1, radi=[(fuel, pin_radius), (helium, 0.465), (zircaloy, 0.5375), (water, 0)])
    guide_tube = siw.Pin.from_dict(name=2, radi={water: 0.62, zircaloy: 0.69, water.copy(): 0})
    sample_pin = siw.Pin.from_dict(name=3, radi={fuel_sample: pin_radius, helium: 0.465, zircaloy: 0.5375, water: 0})

    pin_delimiter = siw.Surface(name=100, parameters=[0, 0, cell_side_length / 2])
    lattice_delimiter = siw.Surface(name=7, parameters=[0, 0, cell_side_length / 2 * n_side_pins])
    external_delimiter = siw.Surface(name=1, parameters=[0, 0, cell_side_length / 2 * n_side_pins +
                                                         extra_water_thickness])

    fuel_region = siw.Cell(name=1,
                           father=all_fuel,
                           delimiters=siw.surface_complement([pin_delimiter]),
                           kind='fill',
                           filler=fuel_pin)
    water_around_fuel = siw.Cell(name=2,
                                 father=all_fuel,
                                 delimiters=[pin_delimiter],
                                 kind="material",
                                 material=water)
    guide_tubes_region = siw.Cell(name=3,
                                  father=all_guides,
                                  kind='fill',
                                  delimiters=siw.surface_complement([pin_delimiter]),
                                  filler=guide_tube)
    water_around_guides = siw.Cell(name=4,
                                   father=all_guides,
                                   delimiters=[pin_delimiter],
                                   kind="material",
                                   material=water)
    sample_fuel_region = siw.Cell(name=5,
                                  father=sample_universe,
                                  kind='fill',
                                  delimiters=siw.surface_complement([pin_delimiter]),
                                  filler=sample_pin)
    water_around_sample = siw.Cell(name=6,
                                   father=sample_universe,
                                   delimiters=[pin_delimiter],
                                   kind="material",
                                   material=water)
    control_rod_coordinates = [("C", 3), ("F", 3), ("J", 3), ("M", 3),
                               ("E", 5), ("H", 5), ("K", 5),
                               ("C", 6), ("M", 6),
                               ("E", 8), ("K", 8),
                               ("C", 10), ("M", 10),
                               ("E", 11), ("H", 11), ("K", 11),
                               ("C", 13), ("F", 13), ("J", 13), ("M", 13)]
    sample_position = [("M", 7)]
    lattice_ = siw.Lattice(name=100,
                           parameters=[0, 0, n_side_pins, n_side_pins, 1.43],
                           representation=siw.LatticeRepresentation.from_cartesian(shape=(n_side_pins, n_side_pins),
                                                                                   filler=all_fuel,
                                                                                   other={
                                                                                       all_guides: control_rod_coordinates,
                                                                                       sample_universe: sample_position}))
    lattice = siw.Cell(name=11,
                       father=external_universe,
                       delimiters=siw.surface_complement([lattice_delimiter]),
                       filler=lattice_)
    out_of_lattice = siw.Cell(name=12,
                              father=external_universe,
                              kind="material",
                              delimiters=[lattice_delimiter] + siw.surface_complement([external_delimiter]),
                              material=water)
    external_boundary = siw.Cell(name=13,
                                 father=external_universe,
                                 delimiters=[external_delimiter],
                                 kind="outside")

    # --------------------------------- DEPLETION ------------------------------------
    power_densities = [0.067167, 0.067833, 0.067833, 0.067833, 0.067833, 0.067833, 0.067833, 0.062500,
                       0.062500, 0.062500, 0.062500, 0.062500, 0.062500, 0.058036, 0]
    n = [siw.Normalization(value=p, material=fuel_sample) for p in power_densities]

    time_steps = [6, 23.54, 29.48, 29.48, 29.48, 29.48, 2.52, 29.26, 32, 32, 32, 32, 12.74, 16.8, 34.2]
    t = [siw.Interval(span=t) for t in time_steps[:-1]] + [siw.Interval(span=time_steps[-1], span_type='dec')]

    # --------------------------------- WRAPPERS --------------------------------------
    material_composition = siw.Composition(
        materials=[fuel, fuel_sample, helium, water, zircaloy],
        libraries={
            "acelib": "/srv/sci/pack/nuclear-data/endfb_71/ace/xsdata.endfb71",
            "bralib": "/srv/sci/pack/nuclear-data/endfb_71/bralib.endfb71",
            "declib": "/srv/sci/pack/nuclear-data/endfb_71/decay/rdd.endfb71",
            "nfylib": "/srv/sci/pack/nuclear-data/endfb_71/nfy/nfy.endfb71",
            "sfylib": "/srv/sci/pack/nuclear-data/endfb_71/sfy/sfy.endfb71"},
        scattering={('', 'lwe70'): (-1, ['lwtr.16t'])})
    material_composition.to_restart = "/scratch/s1/fgrimald/GU3_cycle16/Serpent2/Concentrations_Cycle_16"

    geometry = siw.Geometry(pins=[fuel_pin, guide_tube, sample_pin],
                            surfaces=[pin_delimiter, lattice_delimiter, external_delimiter],
                            cells=[fuel_region, water_around_fuel, guide_tubes_region, water_around_guides,
                                   sample_fuel_region, water_around_sample, lattice, out_of_lattice, external_boundary],
                            lattices=[lattice_])

    depletion = siw.Depletion(list(zip(n, t)))

    # --------------------------------- SIMULATION ------------------------------------
    comments = {'Intro': siw.Comment('Gosgen 3 GU3_cycle16 assembly simulation according to the benchmark. Cycle 16.',
                                     standalone=True),
                'Geometry': siw.Comment('15x15 squared lattice where the rods changed during the cycle are not '
                                        'modeled.'),
                'Steps': siw.Comment('Depletion steps according to the benchmark'),
                'Materials': siw.Comment('Materials according to the benchmark or to the results of the previous '
                                         'simulation.\n'
                                         'Boron concentration in water is kept constant during the cycle'),
                'Others': siw.Comment('Entities needed but not implemented yet in the API'),
                'Concluding': siw.Comment('Concluding comments if needed')}
    cycles = (175, 25)
    simulation = siw.Simulation(geometry, depletion, material_composition, cycles, comments=comments)
    simulation.seed = 1423124306
    simulation.population = (100000, 238, 30)

    if exitfile is not None:
        simulation.write(exitfile)
