from Encryption_all import *

'''Vector map decryption'''


def jiemi(XLst, YLst, Rclx, Rcly):
    x_count = y_count = len(X_sum)
    for i in reversed(range(len(XLst))):
        for j in reversed(range(len(XLst[i]))):
            xx = Rclx[x_count - (len(XLst[i]) - j)]  # corresponding to n in the index
            a, k = suoyin(xx, XLst)
            XLst[i][j], XLst[a][k] = XLst[a][k], XLst[i][j]
        x_count -= len(XLst[i])
    for m in reversed(range(len(YLst))):
        for n in reversed(range(len(YLst[m]))):
            yy = Rcly[y_count - (len(YLst[m]) - n)]  # corresponding to n in the index
            q, e = suoyin(yy, YLst)
            YLst[m][n], YLst[q][e]= YLst[q][e], YLst[m][n]
        y_count -= len(YLst[m])
    return XLst, YLst


if __name__ == '__main__':
    fn_r = r"D:\Code-of-CEW\test1.shp"  # The absolute path of the vector map to be decrypted
    fn_w = r"D:\Code-of-CEW\jiemi1.shp"
    XLst, YLst, PLst, feature_num, X_sum, Y_sum = Read_XYPo_fromshp(fn_r)
    N = len(X_sum)
    x0, B, = 0.45, 0.25
    Xor, Yor = 0.45, 0.55
    a,  t0 = 1.5, 1000
    RcLi=PWLCM(x0, B, t0, N)
    reXLst, reYLst=jiemi(XLst, YLst, RcLi, RcLi)
    RcLx = Tent(N, Xor, a,  t0)
    RcLy = Tent(N, Yor, a,  t0)
    reXLst1, reYLst1 = jiemi(reXLst, reYLst, RcLx, RcLy)
    Write_XYPo_toshp(fn_r, fn_w, reXLst1, reYLst1)
    print("finish")
