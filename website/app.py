from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import  TINYINT,MEDIUMINT
from sqlalchemy import text
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/imginsights'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def dl_img(img_url):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ur;q=0.8',
    }

    downloaded_file_name = None
    downloaded_file_name = img_url.split('/')[-1]

    try:
            print('Downloading the file...' + img_url)
            response = requests.get(img_url, headers=headers, timeout=30)

            if response.status_code == 200:
                file_name = downloaded_file_name.replace(' ','-').lower()

                path = 'static/uploaded_images/'+file_name
                with open(path, 'wb') as fi:
                    fi.write(response.content)
    except Exception as ex:
        print('Exception in downloading image')
        print(str(ex))
    finally:
        return file_name

@app.route('/')
def index():
    sql = text("select count(images.id),images.name,images.id as img_id from images inner join image_colors on images.id = image_colors.image_id group by images.name,img_id")
    results = db.engine.execute(sql)
    return render_template('index.html',results=results)

@app.route('/search',methods=['POST'])
def search():
    if request.method == 'POST':
        form_data = request.form
        sql = text("select count(images.id),images.name,images.id as img_id from images  inner join image_colors on images.id = image_colors.image_id and image_colors.color_code LIKE '%{}%' group by images.name,img_id".format(form_data['query']))
        results = db.engine.execute(sql)
    return render_template('index.html',results=results)

@app.route('/view/<int:id>')
def get_single(id):
    query = "SELECT DISTINCT(color_code),name,code_frequency, code_frequency * 100 / (select sum(code_frequency) FROM image_colors where image_id = {}) AS 'percentage' FROM image_colors INNER JOIN images ON images.id = image_colors.image_id AND image_id = {} AND images.status = 3 order by code_frequency DESC LIMIT 5 ".format(id,id)
    print(query)
    sql = text(query)
    results = db.engine.execute(sql)
    color = []
    color_gradient = None
    file_name = None
    for result in results:
        percent = result.percentage
        if percent < 1:
            percent = percent * 100
        color.append({result.color_code:str(round(percent,2))+'%'})
        file_name = result.name
    
    return render_template('single.html',file_name=file_name,colors=color)

@app.route('/upload')
def upload():
    message = ''
    args = request.args
    if 'message' in args:
        message = args.get('message')
    
    return render_template('upload.html',message=message)

@app.route('/uploaded',methods=['POST'])
def uploaded():
    msg = ''
    if request.method == 'POST':
        form_data = request.form
        upload_type = form_data['upload_type']

        if upload_type.strip() == '2':
            download_image_url = form_data['url'] 
            print('THE DOWNLOAD IMAGE = {}'.format(download_image_url))
            img_file_name = dl_img(download_image_url.strip())        
            if img_file_name is not None and img_file_name != '':
                sql = text("INSERT INTO images(name) VALUES('{}')".format(img_file_name))
                results = db.engine.execute(sql)                                
                msg = 'Image Saved Successfully'
        else:
            msg = 'File Browsing was not implemented'
        return redirect(url_for('upload', message=msg))
    return render_template('upload.html')
    
if __name__ == "__main__":
    app.debug = True
    app.run()