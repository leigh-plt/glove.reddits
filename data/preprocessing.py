try:
    import ujson as json
except:
    import json
import os, gzip, lzma, time, pathlib, argparse
from smart_open import open, register_compressor
from utils import RegExCleaner
import multiprocessing as mp
import zstandard as zstd


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, default='./', help="path to data")
ap.add_argument("-t", "--tmp", required=False, default='tmp', help="path to tmp folder")
ap.add_argument("-s", "--suffix", required=False, default='.txt', help="type saving files")
ap.add_argument("-n", "--process", required=False, default=24, help="number of processes")

args = vars(ap.parse_args())

def _handle_xz(file_obj, mode):
    return lzma.LZMAFile(filename=file_obj, mode=mode, format=lzma.FORMAT_XZ)

register_compressor('.xz', _handle_xz)

tknz = RegExCleaner.reddits()

def prestage(src, dst_folder=args['tmp'], suf=args['suffix']):

    dst = pathlib.Path(dst_folder) / src.with_suffix(suf).name

    start_time = time.time()
    file2file(src, dst)
    end_time = time.time() - start_time

    print(f"Preprocessing {src.name} took {end_time:.3f} seconds") 

def file2file(src, dst, cleaner=tknz):
    if dst.suffix == '.txt':
        mode = 'w'
        encod = False
    else:
        mode = 'wb'
        encod = True
    with open(dst, mode) as dstf:
        with open(src, 'rb') as srcf:
            if src.suffix == '.zst':
                dctx = zstd.ZstdDecompressor()
                reader = dctx.stream_reader(srcf)
                buffer = ''
                while True:
                    chunk = reader.read(16384)
                    if not chunk:
                        break
                    string = chunk
                    buffer += string.decode()
                    lines = buffer.split('\n')
                    if len(lines) > 0:
                        buffer = lines[-1]
                        writer(lines[:-1], dstf, cleaner, encod)
            else:
                writer(srcf, dstf, cleaner, encod)

def writer(lines, dstf, cleaner, encod=False):
    for line in lines:
        comment = json.loads(line)["body"]
        if comment == '[removed]' or comment == '[deleted]':
            continue
        s = cleaner(comment)
        s += "\n"
        if encod: s = s.encode('utf-8')
        dstf.write(s)

def get_files(p, suffixes = ['.bz2', '.xz', '.zst']):
    files = []
    for x in p.iterdir():
        if x.is_dir():
            [files.append(f) for f in get_files(x)]
        else:
            if x.suffix in suffixes and x.name[:5] == 'RC_20':
                files.append(x)
    return files

files = get_files(pathlib.Path(args['path']))

files = [pathlib.Path('./')/ f for f in files]

if __name__ == '__main__':

    start_time = time.time()

    with mp.Pool(int(args['process'])) as p:
        p.map(prestage, files)

    end_time = time.time() - start_time
    print(f"Total time {end_time:.3f} seconds") 
