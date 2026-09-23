#!/usr/bin/env python3
import sys, zipfile, struct, binascii, zlib

ALIGN = 4
DEFAULT_DATE = (2009, 1, 1, 0, 0, 0)

def dos_date_time(dt):
    d, t = dt
    return (d[2] + (d[1] << 5) + (d[0] - 1980) << 9) | t[1] << 11 | t[0] >> 1, (t[2] // 2) | (t[1] << 5) | (t[0] << 11)

def dos_time(info):
    dt = info.date_time
    msdos_time = (dt[3] << 11) | (dt[4] << 5) | (dt[5] // 2)
    msdos_date = ((dt[0] - 1980) << 9) | (dt[1] << 5) | dt[2]
    return msdos_date, msdos_time

def align_apk(src, dst):
    zin = zipfile.ZipFile(src, 'r')
    out = open(dst, 'wb')
    central = []
    out.seek(0)
    for info in zin.infolist():
        raw = zin.read(info)
        crc = binascii.crc32(raw) & 0xffffffff
        usize = len(raw)
        name = info.filename.encode('utf-8')
        header_offset = out.tell()
        method = info.compress_type
        extra = b''
        if method == zipfile.ZIP_STORED:
            local_head_size = 30 + len(name)
            pad = (ALIGN - ((header_offset + local_head_size) % ALIGN)) % ALIGN
            extra = b'\x00' * pad
            data = raw
        else:
            comp = zlib.compressobj(level=9, wbits=-15)
            data = comp.compress(raw) + comp.flush()
        extra_len = len(extra)
        date, dtime = dos_time(info)
        flag = 0
        csize = len(data)
        # local header
        out.write(struct.pack('<IHHHHHIIIHH', 0x04034b50, 20, flag, method, dtime, date, crc, csize, usize, len(name), extra_len))
        out.write(name)
        out.write(extra)
        out.write(data)
        # external attrs
        ext_attr = info.external_attr if info.external_attr else (0o100644 << 16)
        central.append((name, extra, method, dtime, date, crc, csize, usize, ext_attr, header_offset, info.comment.encode() if isinstance(info.comment, str) else info.comment))
    cd_offset = out.tell()
    for (name, extra, method, dtime, date, crc, csize, usize, ext_attr, offset, comment) in central:
        out.write(struct.pack('<IHHHHHHIIIHHHHHII', 0x02014b50, 20, 20, flag, method, dtime, date, crc, csize, usize, len(name), len(extra), len(comment), 0, 0, ext_attr, offset))
        out.write(name)
        out.write(extra)
        out.write(comment)
    cd_size = out.tell() - cd_offset
    entry_count = len(central)
    out.write(struct.pack('<IHHHHIIH', 0x06054b50, 0, 0, entry_count, entry_count, cd_size, cd_offset, 0))
    out.close()
    zin.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('usage: zipalign.py <input.apk> <output.apk>')
    align_apk(sys.argv[1], sys.argv[2])
    print('aligned:', sys.argv[1], '->', sys.argv[2])
