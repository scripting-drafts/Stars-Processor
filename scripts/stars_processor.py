import re
from math import floor, modf
import numpy as np
import info

class stars_processor():
    def __init__(self):
        '''
        TODO:
         - No rotation desginated for M and K class Spectral Types
         -  Clear up 'if num is not None'
        
        Additional Information:
        Class L dwarfs get their designation because they are cooler than M stars and L is the remaining letter alphabetically closest to M. 
        Class T dwarfs are cool brown dwarfs with surface temperatures between approximately 550 and 1,300 K (277 and 1,027 °C; 530 and 1,880 °F).
        Class Y brown dwarfs are cooler than those of spectral class T and have qualitatively different spectra from them.
        Class C were originally classified as R and N stars, these are also known as carbon stars.
        Class S stars have excess amounts of zirconium and other elements produced by the s-process (slow neutron capture process), and have more similar carbon and oxygen abundances than class M or carbon stars'''
        
    def parse_spectral_type(self, spectral_type):
        spectral_type = spectral_type.strip()
        letter = ''.join(re.findall(r'^(O|B|A|F|G|K|M|R|N|L|T|Y|C|S)', spectral_type[:1]))
        nums = ''.join(re.findall(r'(\d.\d|\d?)', spectral_type[1:])[0])
        # print(spectral_type)

        if nums != '':
            if nums.isdigit():
                num = int(nums)
            elif not nums.isdigit():
                if '/' in nums or '-' in nums or ',' in nums:
                    nums_l = [each for each in nums]
                    any(each in nums_l for each in ['/', '-', ','])
                    nums = re.sub(r'/\d?|\-\d?|,\d?', '', nums)
                num = float(nums)
        else:
            num = None
        
        try:
            if num is not None:
                props = spectral_type.lstrip(f'{letter}{num}')
            else:
                props = spectral_type.lstrip(f'{letter}')
        except Exception as e:
            props = ''
            print(e)
        
        return letter, num, props
    
    def parse_name(self, const, name):
        name = name.strip()
        name = re.search(r'(\b\d+)?(\s+)?(\w+[\.*]?[\w+]*)(\s+)?(\w+)', name)
        # print(name.groups())
        star_num = name.group(1)
        Durchmusterung_name = f'{name.group(3)}'
        print(name.groups())
        Durchmusterung_name = Durchmusterung_name.lstrip(const)
        
        return star_num, Durchmusterung_name

    def get_temperature(self, spectral_type):
        letter, num, _ = self.parse_spectral_type(spectral_type)

        if num is not None:
            t_scale = {
                'O': [30000, 70000],
                'B': [10000, 30000],
                'A': [7500, 10000],
                'F': [6000, 7500],
                'G': [5200, 6000],
                'K': [3700, 5200],
                'M': [2400, 3700],
                'R': [2400, 3700],  # TODO: To Review
                'N': [2400, 3700],  # TODO: To Review
                'S': [1800, 4000],
                'C': [700, 3500],   # Specular temperature
                'Y': [300, 700]
            }

            selected_temp_range = t_scale[f'{letter}']
            logarythmic_temp_range_for_int = np.linspace(selected_temp_range[1], selected_temp_range[0], 10)
            
            if type(num) is int:
                temperature = logarythmic_temp_range_for_int[num]            
            else:
                floor_value = int(floor(num))
                frac, _ = modf(num)
                abs_frac = frac * 10

                logarythmic_temp_for_int = logarythmic_temp_range_for_int[floor_value]
                logarythmic_temp_for_float = np.linspace(selected_temp_range[1], selected_temp_range[0], 100)
                diff = (logarythmic_temp_for_float[1] - logarythmic_temp_for_float[0]) * abs_frac
                temperature = logarythmic_temp_for_int + diff
            
            return temperature
        else:
            return None
        
    def get_rotation_velocity(self, spectral_type):
        '''TODO:
        K, M Spectral
        Assumes same Spectral Type limits (F0 == A9)  and min rotation at G9'''
        letter, num, _ = self.parse_spectral_type(spectral_type)

        if letter not in ['M', 'K', 'S', 'C'] and num is not None:
            r_scale = {
                'O0': 190,
                'B0': 200,
                'B5': 210,
                'A0': 190,
                'A5': 160,
                'F0': 95,
                'F5': 25,
                'G0': 12,
                'G9': 1
            }
            
            if type(num) is int:
                logarythmic_rotations_for_int = {
                    f'O{num}': np.linspace(r_scale['O0'], r_scale['B0'], 10)[num],
                    f'B{num}': np.linspace(r_scale['B0'], r_scale['A0'], 10)[num],
                    f'A{num}': np.linspace(r_scale['A0'], r_scale['F0'], 10)[num],
                    f'F{num}': np.linspace(r_scale['F0'], r_scale['G0'], 10)[num],
                    f'G{num}': np.linspace(r_scale['G0'], r_scale['G9'], 10)[num]
                }
                
                rotation = float(logarythmic_rotations_for_int[f'{letter}{num}'])

            else:
                floor_value = int(floor(num))
                frac, _ = modf(num)
                abs_frac = frac * 10

                logarythmic_rotations_for_float = {
                    f'O{floor_value}': np.linspace(r_scale['O0'], r_scale['B0'], 10)[floor_value],
                    f'B{floor_value}': np.linspace(r_scale['B0'], r_scale['A0'], 10)[floor_value],
                    f'A{floor_value}': np.linspace(r_scale['A0'], r_scale['F0'], 10)[floor_value],
                    f'F{floor_value}': np.linspace(r_scale['F0'], r_scale['G0'], 10)[floor_value],
                    f'G{floor_value}': np.linspace(r_scale['G0'], r_scale['G9'], 10)[floor_value]
                }

                # TODO: REVIEW
                logarythmic_rotations_float = {
                    f'O{floor_value}': np.linspace(r_scale['O0'], r_scale['B0'], 100),
                    f'B{floor_value}': np.linspace(r_scale['B0'], r_scale['A0'], 100),
                    f'A{floor_value}': np.linspace(r_scale['A0'], r_scale['F0'], 100),
                    f'F{floor_value}': np.linspace(r_scale['F0'], r_scale['G0'], 100),
                    f'G{floor_value}': np.linspace(r_scale['G0'], r_scale['G9'], 100)
                }

                diff = (logarythmic_rotations_float[f'{letter}{floor_value}'][0] - logarythmic_rotations_float[f'{letter}{floor_value}'][1]) * abs_frac
                rotation = float(logarythmic_rotations_for_float[f'{letter}{floor_value}'] + diff)
        
        elif letter in ['M', 'K', 'S', 'C'] or num is None:
            rotation = np.nan
        
        return rotation
        
    def get_luminosity(self, spectral_type):
        '''Yerkes luminosity classes
        Randomest example K0II-IIIFe-0.5 (Tau Puppies)'''
        _, _, props = self.parse_spectral_type(spectral_type)

        return props
    
    def get_const_complete_name(self, const):

        '''
        TODO:
            MAKES IT SOOOOOOOOO SLOW
            Get only new constellation name every time it changes
        
        '''
        consts = info.get_available_consts()

        # def check_const_name_arch(const):
        #     is_compound_noun = const[1].isupper()
            
        #     return is_compound_noun
        
        # is_compound_noun = check_const_name_arch(const)
        # if is_compound_noun:

        
        # const_name = ''.join([each for each in info.constellations if each.startswith(const)])
        const_name = info.constellations[consts.index(const)]

        return const_name

