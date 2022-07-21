

print("Data-----------")
import numpy as np
from skimage import io, color, img_as_ubyte
import os
from skimage.feature import greycomatrix, greycoprops
import pandas as pd
from sklearn.metrics.cluster import entropy

# img = cv2.imread(path)
# aa = ['Acne and Rosacea Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions',
#       'Atopic Dermatitis Photos', 'Bullous Disease Photos', 'Cellulitis Impetigo and other Bacterial Infections', 'Eczema Photos', 'Exanthems and Drug Eruptions', 'Herpes HPV and other STDs Photos', 'Light Diseases and Disorders of Pigmentation', 'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles', 'Poison Ivy Photos and other Contact Dermatitis', 'Psoriasis pictures Lichen Planus and related diseases', 'Scabies Lyme Disease and other Infestations and Bites', 'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease', 'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 'Vascular Tumors', 'Vasculitis Photos', 'Warts Molluscum and other Viral Infections']
aa = ['Apple Scab Leaf','Blight','Brown spot','Gray_leaf_Spot','Leaf smut','septoria','Tomato___Early_blight','Tomato___Late_blight','Tomato___Septoria_leaf_spot']
for i in aa:
    print(i)
# search = str(input('Enter the folder name'))
# path = 'C:\\Users\\rsmp\\Desktop\\dataset\\train\\' + search
# a = os.listdir(path)
# b = str(a)
# print(b)
alllist = []

features = []
labels = []

# ===========================================================

for myfolders in aa:
    path = 'C:\\Users\\asus\\PycharmProjects\\Leaf_disease\\static\\dataset\\' +str(myfolders)
    print(path)

    # path = 'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\dataset_train_backup\\datasetBackup-17-01-22\\train\\' + \
    #     str(myfolders)
    a = os.listdir(path)
    for ii in a:
        rgbImg = io.imread(str(path + "\\" + str(ii)))
        grayImg = img_as_ubyte(color.rgb2gray(rgbImg))

        distances = [1, 2, 3]
        angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
        properties = ['energy', 'homogeneity',
                      'dissimilarity', 'correlation', 'contrast']

        glcm = greycomatrix(grayImg,
                            distances=distances,
                            angles=angles,
                            symmetric=True,
                            normed=True)

        feats = np.hstack([greycoprops(glcm, 'homogeneity').ravel()
                           for prop in properties])
        feats1 = np.hstack([greycoprops(glcm, 'energy').ravel()
                            for prop in properties])
        feats2 = np.hstack(
            [greycoprops(glcm, 'dissimilarity').ravel() for prop in properties])
        feats3 = np.hstack(
            [greycoprops(glcm, 'correlation').ravel() for prop in properties])
        feats4 = np.hstack([greycoprops(glcm, 'contrast').ravel()
                            for prop in properties])

        k = np.mean(feats)
        l = np.mean(feats1)
        m = np.mean(feats2)
        n = np.mean(feats3)
        o = np.mean(feats4)
        # print(k)
        # print(l)
        # print(m)
        # print(n)
        # print(o)

        features.append([k, l, m, n, o])
        labels.append(myfolders)
        disease = myfolders
        # print(disease)
        aa = [k, l, m, n, o, disease]
        alllist.append(aa)
        data = pd.DataFrame(
            alllist, columns=['f1', 'f2', 'f3', 'f4', 'f5', 'Disease'])

        data.to_csv(
            'C:\\Users\\asus\\PycharmProjects\\Leaf_disease\\static\\dataset\\d.csv')

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.1, random_state=0)

from sklearn.ensemble import RandomForestClassifier

a = RandomForestClassifier(n_estimators=100)

a.fit(features, labels)

m = a.predict(X_test)

from sklearn.metrics import accuracy_score

s = accuracy_score(y_test, m)

print(s, "acccuracy")