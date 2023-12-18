import tools.regex_bsc_parser as regex_bsc_parser
import sys
import csv
import tools.info as info
import pathlib

known_consts = info.get_available_consts()

def display_stars(stars):
    datalist = []
    for star in stars:
        if True:    # star.star_num.startswith('77')
            data = {}

            # data['source'] = star.source
            data['constellation'] = star.const
            data['star_num'] = star.star_num
            data['bd_name'] = star.bd_name
            data['magnitude'] = star.mag
            data['right ascendance'] = star.ra
            data['declination'] = star.dec
            data['spectral type'] = star.spectral_type
            data['rotation'] = star.rotation
            data['temperature'] = star.temperature
            data['luminosity'] = star.lum

            # data = star.name, star.mag, star.ra, star.dec, star.spectral_type, star.rotation, star.temperature, star.lum
            print(f'{data}\n')
        # else:
        #     print(star.name, star.mag, star.ra, star.dec, star.spectral_type, star.temperature)
            datalist.append(data)
    # DEBUG print(len(datalist))

    return datalist

def generate_csv(const, datalist):
    keys = datalist[0].keys()
    pathlib.Path('data/csv').mkdir(parents=True, exist_ok=True)
    
    with open(f'data/csv/{const}_consts_catalog.csv', 'w', encoding='ascii', newline='') as f:
        dict_writer = csv.DictWriter(f, keys, dialect='excel', delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(datalist)

if sys.argv:
    if sys.argv[1:]:
        if sys.argv[1] == '--help':
            info.help_module()

        elif sys.argv[1] in known_consts:
            const = sys.argv[1]
            stars, n = regex_bsc_parser.get_stars_in_constellation(const)
            regex_bsc_parser.generate_stars_map(stars, n, const)

            if n==0:
                print('Constellation {:s} not found.'.format(const))
                sys.exit(1)

            else:
                print('Found {:d} stars in the constellation {:s}'.format(n, const))
                print('equinox J2000, epoch 2000.0')
                datalist = display_stars(stars)

                generate_csv(const, datalist)

    elif not sys.argv[1:]:
        consts = info.get_available_consts()
        print(consts)

        for const in consts:
            stars, _ = regex_bsc_parser.get_stars_in_constellation(const)
            datalist = display_stars(stars)

            generate_csv(const, datalist)

else:
    print('''usage:
        python {:s} <constellation>
        where <constellation> is the three-letter abbreviation for a
        constellation name (e.g. Ori, Lyr, UMa, ...)'''.format(sys.argv[0]))
    print('Type --help for more information')
    sys.exit(1)




