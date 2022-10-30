from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            naukri_url = "https://www.naukri.com/data-analyst-jobs?k=" + searchString
            uClient = uReq(naukri_url)
            naukriPage = uClient.read()
            uClient.close()
            naukri_html = bs(naukriPage, "html.parser")
            box = naukri_html.findAll("article", {"class": "jobTuple bgWhite br4 mb-8"})
            # del bigboxes[0:1]
            # box = bigboxes[0]
            jobLink = "https://www.naukri.com" + box.div.div.a['href']
            prodRes = requests.get(jobLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "top"})

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('a', {'class': 'pad-rt-8',}).text

                except:
                    name = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    # rating = commentbox.div.div.div.div.text
                    rating = commentbox.div.find_all('div', {'class': 'exp'}).text


                except:
                    rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    # commentHead = commentbox.div.div.div.p.text
                    commentHead = commentbox.div.find_all('div', {'class': 'salary'}).text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    # comtag = commentbox.div.div.find_all('div', {'class': ''})
                    comtag = commentbox.div.find_all('div', {'class': 'loc'}).text
                    #custComment.encode(encoding='utf-8')
                    # custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": comtag}
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
	# app.run(debug=True)



