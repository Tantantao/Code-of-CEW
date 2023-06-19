from osgeo import ogr
import os


'''Read in vector data (shp)'''


def Read_XYPo_fromshp(ori_shp):
    ds = ogr.Open(ori_shp, 0)
    layer = ds.GetLayer(0)
    feature_num = layer.GetFeatureCount()
    XLst, YLst, PoLst, X_sum, Y_sum = [], [], [], [], []
    for in_feature in layer:
        geom = in_feature.geometry()
        wkt = geom.ExportToWkt()
        pointstring = wkt[wkt.find('(') + 1:wkt.rfind(')')].split(',')
        x, y, po = [], [], []
        for point_value in pointstring:
            xy = point_value.split(' ')
            x += [float(xy[0])]
            y += [float(xy[1])]
            po += [(float(xy[0]), float(xy[1]))]
        X_sum += x
        Y_sum += y
        XLst.append(x), YLst.append(y), PoLst.append(po)
    ds.Destroy()
    return XLst, YLst, PoLst, feature_num, X_sum, Y_sum


'''write out vector data'''


def Write_XYPo_toshp(ori_shp, en_shp, XLst_emb, YLst_emb):
    ds = ogr.Open(ori_shp, 0)
    in_layer = ds.GetLayer(0)
    feature_num = in_layer.GetFeatureCount()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.CreateDataSource(en_shp)
    get_srs = in_layer.GetSpatialRef()
    out_layer = data_source.CreateLayer(en_shp, get_srs, ogr.wkbLineString)
    out_layer.CreateFields(in_layer.schema)
    out_defn = out_layer.GetLayerDefn()
    if os.access(en_shp, os.F_OK):
        driver.DeleteDataSource(en_shp)
    feat_count = 0
    for in_feature in in_layer:
        geom = in_feature.geometry()
        wkt = geom.ExportToWkt()
        pointstring = wkt[wkt.find('(') + 1:wkt.rfind(')')].split(',')
        pts_new = ''
        point_num = 0
        for point_value in pointstring:
            xy = point_value.split(' ')
            x = float(xy[0])
            y = float(xy[1])
            en_x = XLst_emb[feat_count][point_num]
            en_y = YLst_emb[feat_count][point_num]
            pts_new += str(en_x) + ' ' + str(en_y) + ','
            point_num += 1
        en_wkt = wkt[0:wkt.find('(') + 1] + pts_new[:-1] + ')'
        out_feature = ogr.Feature(out_defn)
        en_Geometry = ogr.CreateGeometryFromWkt(en_wkt)
        out_feature.SetGeometry(en_Geometry)
        for i in range(1, in_feature.GetFieldCount()):
            value = in_feature.GetField(i)
            out_feature.SetField(i, value)
        out_layer.CreateFeature(out_feature)
        feat_count += 1
    ds.Destroy()


"""indexing mechanism"""


def suoyin(n, XLst):
    a = -1
    for i in range(len(XLst)):
        for j in range(len(XLst[i])):
            a += 1
            if a == n:
                return i, j


'''Tent map'''


def Tent(N, Xor, a, t0):
    X0 = Xor
    Lx, RcLx = [], []
    for s in range(0, t0 + N):
        if X0 < 0.5:
            X0 = a * X0
        else:
            X0 = a * (1 - X0)
        Lx.append(X0)
    cLx = Lx[t0:]
    # round down
    for j in cLx:
        xi = int(N * j) % N
        RcLx.append(xi)
    return RcLx


'''PWLCM map'''


def PWLCM(x0, B, t0, N):
    xi = x0
    Li, RcLi = [], []
    for s in range(0, t0 + N):
        if 0 <= xi < B:
            xi = xi / B
        elif B <= xi < 0.5:
            xi = (xi - B) / (0.5 - B)
        elif 0.5 <= xi < 1 - B:
            xi = (1 - B - xi) / (0.5 - B)
        else:
            xi = (1 - xi) / B
        Li.append(xi)
    cLi = Li[t0:]
    # round down
    for j in cLi:
        x = int(N * j) % N
        RcLi.append(x)
    return RcLi


'''coordinate scrambling'''


def zhiluan(XLst, YLst, Rclx, Rcly):
    x_count = y_count = 0
    for i in range(len(XLst)):
        for j in range(len(XLst[i])):
            xx = Rclx[x_count + j]
            a, k = suoyin(xx, XLst)
            XLst[i][j], XLst[a][k] = XLst[a][k], XLst[i][j]
        x_count += len(XLst[i])
    for m in range(len(YLst)):
        for n in range(len(YLst[m])):
            yy = Rcly[y_count + n]
            q, e = suoyin(yy, YLst)
            YLst[m][n], YLst[q][e] = YLst[q][e], YLst[m][n]
        y_count += len(YLst[m])
    return XLst, YLst


if __name__ == '__main__':
    fn_r = r"The absolute path of the data to be encrypted"
    Xor, Yor = 0.45, 0.55
    a,  t0 = 1.5, 1000
    XLst, YLst, PLst, feature_num, X_sum, Y_sum = Read_XYPo_fromshp(fn_r)
    N = len(X_sum)
    RcLx = Tent(N, Xor, a,  t0)
    RcLy = Tent(N, Yor, a,  t0)
    RXLst, RYLst = zhiluan(XLst, YLst, RcLx, RcLy)
    x0, B, = 0.45, 0.25
    RcLi = PWLCM(x0, B, t0, N)
    RXLst1, RYLst1 = zhiluan(RXLst, RYLst, RcLi, RcLi)
    fn_w = r"D:\Code-of-CEW\test1.shp"
    Write_XYPo_toshp(fn_r, fn_w, RXLst1, RYLst1)  # Write out the encrypted vector data
    print("finish")
