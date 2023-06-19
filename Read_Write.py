import os
from osgeo import ogr
import sys

'''Read in vector data (shp)'''


def Read_Shapfile(fn_ori):
    ds = ogr.Open(fn_ori, 0)
    if ds is None:
        sys.exit("Could not open {0}.".format(fn_ori))
    layer = ds.GetLayer(0)
    feature_num = layer.GetFeatureCount(0)
    X_Lst, Y_Lst = [], []
    for i in range(0, feature_num):
        feature = layer.GetFeature(i)
        geometry = feature.GetGeometryRef()
        if geometry.GetGeometryName() == 'POLYGON':
            geometry = geometry.GetGeometryRef(0)
        x, y = [0] * geometry.GetPointCount(), [0] * geometry.GetPointCount()
        for j in range(geometry.GetPointCount()):
            x[j] = geometry.GetX(j)
            y[j] = geometry.GetY(j)
        X_Lst.append(x), Y_Lst.append(y)
    ds.Destroy()
    return X_Lst, Y_Lst, feature_num


'''Write out vector data (shp)'''


def write_encrytpion_shp(ori_shp, outputfile, En_X, En_Y):
    ds = ogr.Open(ori_shp, 0)
    if ds is None:
        sys.exit('Could not open {0}.'.format(ori_shp))
    '''1. Create a data source'''
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.access(outputfile, os.F_OK):
        driver.DeleteDataSource(outputfile)
    '''2. Duplicate a new layer'''
    layer = ds.GetLayer(0)
    newds = driver.CreateDataSource(outputfile)
    pt_layer = newds.CopyLayer(layer, 'a')
    newds.Destroy()
    nds = ogr.Open(outputfile, 1)
    nlayer = nds.GetLayer(0)
    for i in range(nlayer.GetFeatureCount(0)):
        feature = nlayer.GetFeature(i)
        # geometry = feature.GetGeometryRef().GetGeometryRef(0)
        geometry = feature.GetGeometryRef()
        if geometry.GetGeometryName() == 'POLYGON':
            geometry = geometry.GetGeometryRef(0)
        for k in range(geometry.GetPointCount()):
            geometry.SetPoint_2D(k, En_X[i][k], En_Y[i][k])
        nlayer.SetFeature(feature)
    nds.Destroy()


"""Store all X, Y coordinates into two separate lists"""


def GetSum(XLst, YLst):
    X_sum, Y_sum = [], []
    for i in range(len(XLst)):
        for j in range(len(XLst[i])):
            X_sum.append(XLst[i][j])
    for m in range(len(YLst)):
        for n in range(len(YLst[m])):
            Y_sum.append(YLst[m][n])
    return X_sum, Y_sum


if __name__ == '__main__':
    fn = r'Absolute path to vector map data'
    XLst1, YLst1, feature_num1 = Read_Shapfile(fn)
    X_sum1, Y_sum1 = GetSum(XLst1, YLst1)
    print(len(X_sum1))
