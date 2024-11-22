import os
import csv
import re

def map_fonts(fonts_path, fs_path, csv_path):
    font_map_fs = 'export const fontMap is map = {\n'
    font_index = 0
    jhf_files = sorted([f for f in os.listdir(fonts_path) if f.endswith('.jhf')])
    font_data = []
    for filename in jhf_files:
        height, offset, font_lines = parse_jhf(os.path.join(fonts_path, filename))
        font_map_fs += f"'{filename}' : [{height}, {offset}, {font_index}],\n"
        font_data.extend(font_lines)
        num_lines = len(font_lines)
        print(f'found {num_lines} glyphs from {filename}')
        font_index += num_lines
    font_map_fs = font_map_fs[:-1] + '\n};'
    with open(fs_path, 'w') as file:
        file.write(font_map_fs)
    with open(csv_path, 'w', newline='\n') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in font_data:
            csvwriter.writerow(row)

def parse_jhf(path):
    with open(path, 'r') as file:
        content = file.read()
    h_height = 0
    h_offset = 0
    glyph_lines = []
    glyphs = re.split(r'[0-9 ]{5}', content)[1:] 
    for i, glyph in enumerate(glyphs):
        char = chr(i + 32)
        if i + 32 > 126:
            print(f'ignored character in {path}')
            continue
        height, y_offset, glyph_line = parse_glyph(glyph.replace('\n', ''))
        if height is None:
            print(f'failed to parse {path} glyph {glyph_line}')
            exit()
        if char == 'H':
            h_height = height
            h_offset = y_offset
        glyph_lines.append(glyph_line)
    return h_height, -h_offset, glyph_lines

def parse_glyph(glyph):
    try:
        num_pairs = int(glyph[:3]) - 1
        left = ord(glyph[3]) - ord('R')
        right = ord(glyph[4]) - ord('R')
        index = 5
        csv_row = [left, right, num_pairs]
        max_y = -100
        min_y = 100
        while index < len(glyph) - 1:
            char1 = glyph[index]
            char2 = glyph[index+1]
            if char1 == ' ' and char2 == 'R':
                csv_row.append('S')
                csv_row.append('S')
                index += 2
                continue
            x = ord(char1) - ord('R')
            y = -(ord(char2) - ord('R'))
            if y > max_y: 
                max_y = y
            if y < min_y:
                min_y = y
            csv_row.append(x)
            csv_row.append(y)
            index += 2
        height = max_y - min_y
        return height, min_y, csv_row
    except:
        return None, None, glyph

if __name__ == '__main__':
    map_fonts('fonts/', 'font_map.txt', 'font_data.csv')
