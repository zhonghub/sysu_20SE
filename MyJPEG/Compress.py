import numpy as np
import cv2
import os
from PIL import Image
from pathlib import Path


class MyJPEG:
    # 标准亮度量化表
    lq_Table = np.array([16, 11, 10, 16, 24, 40, 51, 61,
                         12, 12, 14, 19, 26, 58, 60, 55,
                         14, 13, 16, 24, 40, 57, 69, 56,
                         14, 17, 22, 29, 51, 87, 80, 62,
                         18, 22, 37, 56, 68, 109, 103, 77,
                         24, 35, 55, 64, 81, 104, 113, 92,
                         49, 64, 78, 87, 103, 121, 120, 101,
                         72, 92, 95, 98, 112, 100, 103, 99], dtype=np.uint8)
    # 标准色度量化表
    cq_Table = np.array([17, 18, 24, 47, 99, 99, 99, 99,
                         18, 21, 26, 66, 99, 99, 99, 99,
                         24, 26, 56, 99, 99, 99, 99, 99,
                         47, 66, 99, 99, 99, 99, 99, 99,
                         99, 99, 99, 99, 99, 99, 99, 99,
                         99, 99, 99, 99, 99, 99, 99, 99,
                         99, 99, 99, 99, 99, 99, 99, 99,
                         99, 99, 99, 99, 99, 99, 99, 99], dtype=np.uint8)
    # Zig编码表
    __zig = np.array([
        0, 1, 8, 16, 9, 2, 3, 10,
        17, 24, 32, 25, 18, 11, 4, 5,
        12, 19, 26, 33, 40, 48, 41, 34,
        27, 20, 13, 6, 7, 14, 21, 28,
        35, 42, 49, 56, 57, 50, 43, 36,
        29, 22, 15, 23, 30, 37, 44, 51,
        58, 59, 52, 45, 38, 31, 39, 46,
        53, 60, 61, 54, 47, 55, 62, 63
    ])
    # Zag编码表
    __zag = np.array([
        0, 1, 5, 6, 14, 15, 27, 28,
        2, 4, 7, 13, 16, 26, 29, 42,
        3, 8, 12, 17, 25, 30, 41, 43,
        9, 11, 18, 24, 31, 40, 44, 53,
        10, 19, 23, 32, 39, 45, 52, 54,
        20, 22, 33, 38, 46, 41, 55, 60,
        21, 34, 37, 47, 50, 56, 59, 61,
        35, 36, 48, 49, 57, 58, 62, 63
    ])

    def __init__(self):
        # 初始化
        self.width = None
        self.height = None
        # 亮度量化矩阵
        self.__lq = np.zeros(64, dtype=np.uint8)
        # 色度量化矩阵
        self.__cq = np.zeros(64, dtype=np.uint8)
        # 压缩程度
        self.quality_scale = 100
        # 初始化量化表，改变压缩质量，参数1~999，数字越大压缩程度越高
        self.init_Quantization_Table(100)
        # 标记矩阵类型，lt是亮度矩阵，ct是色度矩阵
        self.__lt = 0
        self.__ct = 1

    # 初始化量化表，改变压缩质量，参数1~999，数字越大压缩程度越高
    def init_Quantization_Table(self, quality_scale):
        self.quality_scale = quality_scale
        if quality_scale <= 0:
            quality_scale = 1
        elif quality_scale >= 1000:
            quality_scale = 999
        for i in range(64):
            tmp = int((self.lq_Table[i] * quality_scale + 100) / 100)
            if tmp > 255:
                tmp = 255
            self.__lq[i] = tmp 
            tmp = int((self.cq_Table[i] * quality_scale + 100) / 100)
            if tmp > 255:
                tmp = 255
            self.__cq[i] = tmp

    def __Rgb2Yuv(self, r, g, b):
        # 从图像获取YUV矩阵
        y = 0.299 * r + 0.587 * g + 0.114 * b
        u = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
        v = 0.5 * r - 0.419 * g - 0.081 * b + 128
        return y, u, v

    def __Yuv2Rgb(self, y, u, v):
        r = (y + 1.402 * (v - 128))
        g = (y - 0.34414 * (u - 128) - 0.71414 * (v - 128))
        b = (y + 1.772 * (u - 128))
        return r, g, b

    ##############################################################################################
    # 以下为编码部分
    ##############################################################################################
    # 图片填充
    def __Fill(self, matrix):
        # 图片的长宽都需要满足是16的倍数（采样长宽会缩小1/2和取块长宽会缩小1/8）
        # 图像压缩三种取样方式4:4:4、4:2:2、4:2:0
        fh, fw = 0, 0
        if self.height % 16 != 0:
            fh = 16 - self.height % 16
        if self.width % 16 != 0:
            fw = 16 - self.width % 16
        res = np.pad(matrix, ((0, fh), (0, fw)), 'constant', constant_values=(0, 0))
        return res
    
    # DPCM编码
    def __DPCM(self, blocks):
        preDc = 0
        for i in range(len(blocks)):
            nowDc = blocks[i][0]
            blocks[i][0] = nowDc - preDc
            preDc = nowDc

    # DCT变换+数据量化+DPCM差分编码
    def __Encode(self, matrix, tag):
        # 先对矩阵进行填充
        matrix = self.__Fill(matrix)
        # 4:2:0降采样，亮度Y不变，色度UV下采样
        if tag == self.__ct:
            matrix = cv2.resize(matrix, (matrix.shape[1]//2, matrix.shape[0]//2), interpolation=cv2.INTER_NEAREST)
        # 将图像矩阵切割成8*8小块
        height, width = matrix.shape
        # 减少for循环语句, 利用numpy的自带函数来提升算法效率, numpy的函数自带并行处理, 不用像for循环一样串行处理
        shape = (height // 8, width // 8, 8, 8)
        strides = matrix.itemsize * np.array([width * 8, 8, width, 1])
        blocks = np.lib.stride_tricks.as_strided(matrix, shape=shape, strides=strides)
        res = []
        q_table = None
        # 选择对应的量化表：亮度/色度
        if tag == self.__lt:
            q_table = self.__lq
        elif tag == self.__ct:
            q_table = self.__cq
        # DCT变换+数据量化
        for i in range(height // 8):
            for j in range(width // 8):
                # DCT变换
                block = cv2.dct(blocks[i, j])
                block = block.flatten(order='C')
                # 数据量化
                block[:] = np.round(np.divide(block, q_table))
                res.append(block)
        # DPCM差分编码
        self.__DPCM(res)
        return res

    def __Zig(self, blocks):
        ty = np.array(blocks)
        tz = np.zeros(ty.shape)
        for i in range(len(self.__zig)):
            tz[:, i] = ty[:, self.__zig[i]]
        tz = tz.reshape(tz.shape[0] * tz.shape[1])
        return tz.tolist()

    # RLC编码，行程编码
    def __Rlc(self, blist):
        res = []
        cnt = 0
        for i in range(len(blist)):
            if blist[i] != 0:
                res.append(cnt)
                res.append(int(blist[i]))
                cnt = 0
            elif cnt == 15:
                res.append(cnt)
                res.append(int(blist[i]))
                cnt = 0
            else:
                cnt += 1
        # 末尾全是0的情况
        if cnt != 0:
            res.append(cnt - 1)
            res.append(0)
        return res

    # 压缩
    def Compress(self, filename):
        # 根据路径image_path读取图片，并存储为RGB矩阵
        image = Image.open(filename)
        # 获取图片宽度width和高度height
        self.width, self.height = image.size
        image = image.convert('RGB')
        image = np.asarray(image)
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        # 将图像RGB转YUV
        y, u, v = self.__Rgb2Yuv(r, g, b)
        # 对图像矩阵进行DCT变换+量化+DPCM差分编码
        y_blocks = self.__Encode(y, self.__lt)
        u_blocks = self.__Encode(u, self.__ct)
        v_blocks = self.__Encode(v, self.__ct)
        # 对图像小块进行Zig编码和RLc编码
        y_code = self.__Rlc(self.__Zig(y_blocks))
        u_code = self.__Rlc(self.__Zig(u_blocks))
        v_code = self.__Rlc(self.__Zig(v_blocks))
        # 计算VLI可变字长整数编码并写入文件，未实现Huffman编码
        # 写入文件
        tfile = os.path.splitext(filename)[0] + "_result_" + str(self.quality_scale) + ".txt"
        if os.path.exists(tfile):
            os.remove(tfile)
        # 写入图片的大小
        with open(tfile, 'wb') as o:
            o.write(self.height.to_bytes(2, byteorder='big'))
            o.flush()
            o.write(self.width.to_bytes(2, byteorder='big'))
            o.flush()
            o.write((len(y_code)).to_bytes(4, byteorder='big'))
            o.flush()
            o.write((len(u_code)).to_bytes(4, byteorder='big'))
            o.flush()
            o.write((len(v_code)).to_bytes(4, byteorder='big'))
            o.flush()
            o.write(self.quality_scale.to_bytes(4, byteorder='big'))
            o.flush()
        # 写入图片的YUV 3个通道
        self.__Write2File(tfile, y_code, u_code, v_code)

    # 写入文件
    def __Write2File(self, filename, y_code, u_code, v_code):
        with open(filename, "ab+") as o:
            buff = 0
            bcnt = 0
            data = y_code + u_code + v_code
            for i in range(len(data)):
                if i % 2 == 0:
                    td = data[i]
                    for ti in range(4):
                        buff = (buff << 1) | ((td & 0x08) >> 3)
                        td <<= 1
                        bcnt += 1
                        if bcnt == 8:
                            o.write(buff.to_bytes(1, byteorder='big'))
                            o.flush()
                            buff = 0
                            bcnt = 0
                else:
                    td = data[i]
                    vtl, vts = self.__VLI(td)
                    for ti in range(4):
                        buff = (buff << 1) | ((vtl & 0x08) >> 3)
                        vtl <<= 1
                        bcnt += 1
                        if bcnt == 8:
                            o.write(buff.to_bytes(1, byteorder='big'))
                            o.flush()
                            buff = 0
                            bcnt = 0
                    for ts in vts:
                        buff <<= 1
                        if ts == '1':
                            buff |= 1
                        bcnt += 1
                        if bcnt == 8:
                            o.write(buff.to_bytes(1, byteorder='big'))
                            o.flush()
                            buff = 0
                            bcnt = 0
            if bcnt != 0:
                buff <<= (8 - bcnt)
                o.write(buff.to_bytes(1, byteorder='big'))
                o.flush()

    ##############################################################################################
    # 以下为解码部分
    ##############################################################################################
    # 逆量化
    def __IQuantize(self, block, tag):
        res = block
        if tag == self.__lt:
            res *= self.__lq
        elif tag == self.__ct:
            res *= self.__cq
        return res

    # DPCM解码
    def __IDPCM(self, blocks):
        preDc = 0
        for i in range(len(blocks)):
            nowDc = blocks[i][0]
            preDc = nowDc + preDc
            blocks[i][0] = preDc

    # 逆填充，保证图片size不变
    def __IFill(self, matrix, h, w):
        matrix = matrix[:h, :w]
        return matrix

    # 解码：DPCM解码，逆量化，逆DCT变换
    def __Decode(self, blocks, tag):
        # DPCM解码
        self.__IDPCM(blocks)
        tlist = []
        # 逆量化，逆DCT变换
        for b in blocks:
            b = np.array(b)
            tlist.append(cv2.idct(self.__IQuantize(b, tag).reshape(8, 8)))
        height_fill, width_fill = self.height, self.width
        if height_fill % 16 != 0:
            height_fill += 16 - height_fill % 16
        if width_fill % 16 != 0:
            width_fill += 16 - width_fill % 16
        # 色度UV进行了下采样，width和height变为原来的1/2
        if tag == self.__ct:
            height_fill = height_fill // 2
            width_fill = width_fill // 2
        rlist = []
        for hi in range(height_fill // 8):
            start = hi * width_fill // 8
            rlist.append(np.hstack(tuple(tlist[start: start + (width_fill // 8)])))
        matrix = np.vstack(tuple(rlist))
        # 上采样：将下采样的色度UV通道还原为原图像大小
        if tag == self.__ct:
            # 插值方式：双线性插值、最近邻插值——cv2.INTER_LINEAR_EXACT cv2.INTER_NEAREST
            matrix = cv2.resize(matrix, (matrix.shape[1] * 2, matrix.shape[0]*2), interpolation=cv2.INTER_NEAREST)
        # 逆填充，分割出原图像大小
        res = self.__IFill(matrix, self.height, self.width)
        return res
    
    # 读取图像压缩文件
    def __ReadFile(self, filename):
        with open(filename, "rb") as o:
            tb = o.read(2)
            self.height = int.from_bytes(tb, byteorder='big')
            tb = o.read(2)
            self.width = int.from_bytes(tb, byteorder='big')
            tb = o.read(4)
            ylen = int.from_bytes(tb, byteorder='big')
            tb = o.read(4)
            ulen = int.from_bytes(tb, byteorder='big')
            tb = o.read(4)
            vlen = int.from_bytes(tb, byteorder='big')
            tb = o.read(4)
            self.quality_scale = int.from_bytes(tb, byteorder='big')
            self.init_Quantization_Table(self.quality_scale)
            buff = 0
            bcnt = 0
            rlist = []
            itag = 0
            icnt = 0
            vtl, tb, tvtl = None, None, None
            while len(rlist) < ylen + ulen + vlen:
                if bcnt == 0:
                    tb = o.read(1)
                    if not tb:
                        break
                    tb = int.from_bytes(tb, byteorder='big')
                    bcnt = 8
                if itag == 0:
                    buff = (buff << 1) | ((tb & 0x80) >> 7)
                    tb <<= 1
                    bcnt -= 1
                    icnt += 1
                    if icnt == 4:
                        rlist.append(buff & 0x0F)
                    elif icnt == 8:
                        vtl = buff & 0x0F
                        tvtl = vtl
                        itag = 1
                        buff = 0
                else:
                    buff = (buff << 1) | ((tb & 0x80) >> 7)
                    tb <<= 1
                    bcnt -= 1
                    tvtl -= 1
                    if tvtl == 0 or tvtl == -1:
                        rlist.append(self.__IVLI(vtl, bin(buff)[2:].rjust(vtl, '0')))
                        itag = 0
                        icnt = 0
        y_dcode = rlist[:ylen]
        u_dcode = rlist[ylen:ylen + ulen]
        v_dcode = rlist[ylen + ulen:ylen + ulen + vlen]
        return y_dcode, u_dcode, v_dcode

    # 逆Z字形
    def __Zag(self, dcode):
        dcode = np.array(dcode).reshape((len(dcode) // 64, 64))
        tz = np.zeros(dcode.shape)
        for i in range(len(self.__zag)):
            tz[:, i] = dcode[:, self.__zag[i]]
        rlist = tz.tolist()
        return rlist

    # RLC解码
    def __IRlc(self, dcode):
        rlist = []
        for i in range(len(dcode)):
            if i % 2 == 0:
                rlist += [0] * dcode[i]
            else:
                rlist.append(dcode[i])
        return rlist

    def Decompress(self, filename):
        y_dcode, u_dcode, v_dcode = self.__ReadFile(filename)
        # RLC解码，逆Z字形
        y_blocks = self.__Zag(self.__IRlc(y_dcode))
        u_blocks = self.__Zag(self.__IRlc(u_dcode))
        v_blocks = self.__Zag(self.__IRlc(v_dcode))
        # DPCM解码，逆量化，逆DCT变换
        y = self.__Decode(y_blocks, self.__lt)
        u = self.__Decode(u_blocks, self.__ct)
        v = self.__Decode(v_blocks, self.__ct)
        # 颜色空间从YUV转换回RGB
        r, g, b = self.__Yuv2Rgb(y, u, v)
        r = Image.fromarray(r).convert('L')
        g = Image.fromarray(g).convert('L')
        b = Image.fromarray(b).convert('L')
        image = Image.merge("RGB", (r, g, b))
        new_name = os.path.splitext(filename)[0] + ".png"
        path1 = Path(__file__).parent / new_name
        image.save(path1, "png")
        # image.show()

    # 获取整数n的可变字长整数编码
    def __VLI(self, n):
        if n > 0:
            ts = bin(n)[2:]
            tl = len(ts)
        elif n < 0:
            tn = (-n) ^ 0xFFFF
            tl = len(bin(-n)[2:])
            ts = bin(tn)[-tl:]
        else:
            tl = 0
            ts = '0'
        return tl, ts

    # 获取可变字长整数编码对应的整数n
    def __IVLI(self, tl, ts):
        if tl != 0:
            n = int(ts, 2)
            if ts[0] == '0':
                n = n ^ 0xFFFF
                n = int(bin(n)[-tl:], 2)
                n = -n
        else:
            n = 0
        return n


# 计算PSNR, 衡量解压图像质量
def compute_psnr(img_path1, img_path2):
    img1 = np.array(Image.open(img_path1))
    img2 = np.array(Image.open(img_path2))
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        psnr = 100
    else:
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    print("PSNR value is {}".format(psnr))
    return psnr


if __name__ == '__main__':
    # 选择压缩质量，参数1~999，数字越大压缩程度越高
    quality_scale = 100
    # 原始图片路径
    img_path1 = Path(__file__).parent / "./图片/test.png"
    
    myJpeg = MyJPEG()
    print("start\n压缩信息:\n\n压缩程度(quality_scale): " , quality_scale ,"\n")
    # 压缩文件路径
    img_path2 = os.path.splitext(img_path1)[0] + "_result_" + str(quality_scale) + ".txt"
    # 解压图片路径
    img_path3 = os.path.splitext(img_path2)[0] + ".png"
    file_size1 = os.path.getsize(img_path1)
    print("原始图片大小(Byte): —— " ,str(img_path1) ,"\n" , file_size1,"\n开始压缩\n")
    # 压缩
    myJpeg.init_Quantization_Table(quality_scale)
    myJpeg.Compress(img_path1)
    file_size2 = os.path.getsize(img_path2)
    msg = "压缩完成\n压缩文件大小(Byte): —— " + img_path2 + "\n"
    msg += "" + str(file_size2) + "\n" + "压缩比=" + str(file_size1 / file_size2) + "\n\n开始解压"
    print(msg)
    # 解压
    myJpeg.Decompress(img_path2)
    print("解压完成: —— ",img_path3)
    print("end")
    # 计算PSNR
    compute_psnr(img_path1, img_path3)

