from flask import Flask, render_template, request, session

from DBConnection import Db

import numpy as np
from skimage import io, color, img_as_ubyte
import os
from skimage.feature import greycomatrix, greycoprops
import pandas as pd
from sklearn.metrics.cluster import entropy
app = Flask(__name__)

app.secret_key='hiii'

static_path="C:\\Users\\asus\\PycharmProjects\\Leaf_disease\\static\\"


@app.route('/')
def launch():
    return render_template('launch_index.html')

@app.route('/login')
def hello_world():
    return render_template('index.html')

@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form['textfield']
    passwd=request.form['textfield2']
    db=Db()
    qry="SELECT * FROM login WHERE username='"+username+"' AND PASSWORD='"+passwd+"'"
    res=db.selectOne(qry)
    if res!='':
        session['lid']=res['id']
        type=res['u_type']

        if type=='admin':
            return '''<script>alert('login successfully');window.location='/Admin_home'</script>'''
        elif type=='user':
            return '''<script>alert('login successfully');window.location='/User_home'</script>'''
        else:

            return '''<script>alert('Invalid');window.location='/'</script>'''
    else:
        return '''<script>alert('Invalid');window.location='/'</script>'''


###-------ADMIN------------

@app.route('/Admin_home')
def Admin_home():
    return render_template('Admin/admin_index.html')


@app.route('/View_user')
def View_user():
    db=Db()
    qry="SELECT * FROM USER "
    res=db.select(qry)
    return render_template('Admin/viewuser.html',data=res)
@app.route('/View_user_post',methods=['post'])
def View_user_post():
    name=request.form['textfield']
    db = Db()
    qry = "SELECT * FROM USER WHERE name LIKE '%"+name+"%'"
    res = db.select(qry)
    return render_template('Admin/viewuser.html', data=res)

@app.route('/Add_disease')
def Add_disease():
    return render_template('Admin/addDisease.html')


@app.route('/Add_disease_post',methods=['post'])
def Add_disease_post():
    dname=request.form['textfield2']
    discription=request.form['textarea']
    db=Db()
    qry="INSERT INTO disease(NAME, discription)VALUES('"+dname+"','"+discription+"')"
    res=db.insert(qry)
    return render_template('Admin/addDisease.html')

@app.route('/Disease_view_admin')
def Disease_view_admin():
    db = Db()
    qry = "SELECT user.name,`user`.`phone`,`user`.`place`,prediction.* from USER INNER JOIN prediction ON user.u_log_id=prediction.u_id"
    res = db.select(qry)
    return render_template('Admin/DiseaseView.html',data=res)


@app.route('/Update_passwordAdmin')
def Update_passwordAdmin():
    return render_template('Admin/Update_passwd.html')

@app.route('/Update_passwordAdmin_post',methods=['post'])
def Update_passwordAdmin_post():
    current_passwd=request.form['textfield']
    new_passwd = request.form['textfield2']
    Retype_passwd = request.form['textfield3']
    db=Db()
    qry="SELECT * FROM login where password='"+current_passwd+"'"
    res=db.selectOne(qry)
    if res!='':
        if new_passwd==Retype_passwd:
            qry1="update login set password='"+new_passwd+"' where id='"+str(session['lid'])+"'  "
            res1=db.update(qry1)
            return '''<script>alert('successfully updated');window.location='/'</script>'''
        else:
            return '''<script>alert('password not changed');window.location='/Update_passwordAdmin'</script>'''
    else:
         return '''<script>alert('password not changed');window.location='/Update_passwordAdmin'</script>'''


@app.route('/ViewDisease_Admin')
def ViewDisease_Admin():
    db = Db()
    qry = "SELECT * FROM disease "
    res = db.select(qry)
    return render_template('Admin/ViewDiseaseAdmin.html',data=res)

@app.route('/ViewDisease_Admin_post',methods=['post'])
def ViewDisease_Admin_post():
    name=request.form['textfield']
    db = Db()
    qry = "SELECT * FROM disease WHERE name LIKE '%"+name+"%'"
    res = db.select(qry)
    return render_template('Admin/ViewDiseaseAdmin.html', data=res)

@app.route('/delete_disease/<id>')
def delete_disease(id):
    db = Db()
    qry = "delete from disease where d_id='"+id+"' "
    res = db.delete(qry)
    return '''<script>alert('deleted');window.location='/ViewDisease_Admin'</script>'''

@app.route('/edit_disease/<id>')
def edit_disease(id):
    db=Db()
    qry="select * from disease where d_id='"+id+"'"
    res= db.selectOne(qry)
    return render_template('Admin/edit_disease.html',data=res)


@app.route('/edit_disease_post',methods=['post'])
def edit_disease_post():
    did=request.form['did']
    dname=request.form['textfield2']
    discription=request.form['textarea']
    db=Db()
    qry="UPDATE disease SET NAME='"+dname+"',discription='"+discription+"' WHERE d_id='"+str(did)+"'"
    res=db.update(qry)
    return '''<script>alert('sucessfully upadated');window.location='/ViewDisease_Admin'</script>'''


###-------USER------------



@app.route('/User_home')
def User_home():
    return render_template('user/user_index.html')


@app.route('/User_selection')
def User_selection():
    return render_template('user/d_user_selection.html')

@app.route('/User_selection_post',methods=['post'])
def User_selection_post():
    selectfile= request.files['fileField']
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    selectfile.save('C:\\Users\\asus\\PycharmProjects\\Leaf_disease\\static\\user_cheking\\'+timestr+".jpg")
    path="C:\\Users\\asus\\PycharmProjects\\Leaf_disease\\static\\user_cheking\\"+timestr+".jpg"
    url='/static/user_cheking/'+timestr+'.jpg'

    alllist = []

    features = []
    labels = []
    rgbImg = io.imread(str(path))
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

    aa=[k, l, m, n, o]

    df = pd.read_csv('C:\\Users\\asus\\PycharmProjects\\Leaf_disease\\static\\dataset\\d.csv')
    attributes = df.values[:, 1:6]
    print(len(attributes))
    label = df.values[:, 6]
    print(len(label))
    str(df)
    # for i in df:
    #     print(i)
    # b = str(df)
    print(attributes)
    print(label)
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        attributes, label, test_size=0.1, random_state=42)

    from sklearn.ensemble import RandomForestClassifier
    a = RandomForestClassifier(n_estimators=100)

    a.fit(X_train, y_train)

    predictedresult = a.predict([aa])
    print(predictedresult)
    print("ppp")
    # actualresult = y_test
    # testdata = X_test

    # l = len(testdata)

    # from sklearn.metrics import accuracy_score

    # sc = accuracy_score(actualresult, predictedresult)

    # print(sc)
    db = Db()
    qry="INSERT INTO `prediction`(`u_id`,`prediction`,`image`,`date`)VALUES('"+str(session['lid'])+"','"+predictedresult[0]+"','"+url+"',curdate())"
    res = db.insert(qry)

    return str(predictedresult[0])

    return render_template('user/d_user_selection.html')


@app.route('/Diseaseview_user')
def ViewDisease_user():
    db = Db()
    qry = "SELECT * FROM disease "
    res = db.select(qry)
    return render_template('user/DiseaseView.html',data=res)

@app.route('/Diseaseview_user_post',methods=['post'])
def ViewDisease_user_post():
    name=request.form['textfield']
    db = Db()
    qry = "SELECT * FROM disease WHERE name LIKE '%"+name+"%'"
    res = db.select(qry)
    return render_template('user/DiseaseView.html', data=res)


@app.route('/Update_password')
def Update_password():
    return render_template('user/Update_passwd.html')

@app.route('/Update_password_post',methods=['post'])
def Update_password_post():
    current_passwd=request.form['textfield']
    new_passwd = request.form['textfield2']
    Retype_passwd = request.form['textfield3']
    db=Db()
    qry="SELECT * FROM login where password='"+current_passwd+"'"
    res=db.selectOne(qry)
    if res!='':
        if new_passwd==Retype_passwd:
            qry1="update login set password='"+new_passwd+"' where id='"+str(session['lid'])+"'  "
            res1=db.update(qry1)
            return '''<script>alert('successfully updated');window.location='/'</script>'''
        else:
            return '''<script>alert('password not changed');window.location='/Update_password'</script>'''
    else:
         return '''<script>alert('password not changed');window.location='/Update_password'</script>'''


@app.route('/registration')
def registration():
    return render_template('user/reg_index.html')

@app.route('/registration_post',methods=['post'])
def registration_post():
    name= request.form['textfield2']
    gender=request.form['radio']
    e_mail = request.form['textfield3']
    phone = request.form['textfield4']
    place = request.form['textfield5']
    district = request.form['textfield6']
    image = request.files['fileField']
    password = request.form['textfield7']

    import datetime

    image.save(static_path+'image\\'+image.filename)
    path = '/static/image/'+image.filename

    db = Db()
    qry1="INSERT INTO `login`(`username`,`password`,`u_type`)VALUES('"+e_mail+"','"+password+"','user')"
    res1=db.insert(qry1)
    qry = "INSERT INTO USER (name,email,phone,place,district,image,u_log_id,gender)VALUES('" +name+ "','" +e_mail+ "','" +phone+ "','" +place+ "','" +district+ "','" +path+ "','"+str(res1)+"','"+gender+"')"
    res = db.insert(qry)
    return '''<script>alert('successfully registered');window.location='/'</script>'''

@app.route('/profile')
def profile():
    db = Db()
    qry ="SELECT * FROM USER WHERE u_log_id='"+str(session['lid'])+"'"
    res = db.selectOne(qry)
    return render_template('user/Userview.html',data=res)


@app.route('/edit_profile/<id>')
def edit_profile(id):
    db = Db()
    qry = "select * from user where u_log_id='" + id + "'"
    res = db.selectOne(qry)
    return render_template('user/edit_profile_user.html',data=res)

@app.route('/edit_profile_post',methods=['post'])
def edit_profile_post():
    u_id=request.form['u_id']
    name = request.form['textfield2']
    gender = request.form['radio']
    e_mail = request.form['textfield3']
    phone = request.form['textfield4']
    place = request.form['textfield5']
    district = request.form['textfield6']
    db = Db()
    if 'fileField' in request.files:
        image = request.files['fileField']
        if image.filename!="":
            image.save(static_path+'image\\'+image.filename)
            path = '/static/image/'+image.filename
            qry1 = "update login set username='"+e_mail+"' where id='"+str(u_id)+"'"
            res1 = db.update(qry1)
            qry =" UPDATE `user` SET `name`='"+name+"',`gender`='"+gender+"',`email`='"+e_mail+"', `image`='"+path+"',`phone`='"+phone+"',`place`='"+place+"',`district`='"+district+"' WHERE `u_log_id`='"+str(u_id)+"'"
            res = db.update(qry)
            return '''<script>alert('profile updated');window.location='/profile'</script>'''
        else:
            qry1 = "update login set username='" + e_mail + "' where id='" + str(u_id) + "'"
            res1 = db.update(qry1)
            qry = " UPDATE `user` SET `name`='"+name+"',`gender`='"+gender+"',`email`='"+e_mail+"',`phone`='"+phone+"',`place`='"+place+"',`district`='"+district+"' WHERE `u_log_id`='"+str(u_id)+"'"
            res = db.update(qry)
            return '''<script>alert('profile updated');window.location='/profile'</script>'''
    else:

        qry1 = "update login set username='" + e_mail + "' where id='" + str(u_id) + "'"
        res1 = db.update(qry1)
        qry = " UPDATE `user` SET `name`='"+name+"',`gender`='"+gender+"',`email`='"+e_mail+"',`phone`='"+phone+"',`place`='"+place+"',`district`='"+district+"' WHERE `u_log_id`='"+str(u_id)+"'"
        res = db.update(qry)
        return '''<script>alert('profile updated');window.location='/profile'</script>'''




@app.route('/reg')
def reg():
    return render_template('reg.html')



if __name__ == '__main__':
    app.run(debug=True)
