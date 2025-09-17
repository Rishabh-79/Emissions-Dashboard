from flask import Flask, render_template,request,redirect
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app=Flask(__name__)
d={'CHN':0,'IND':0,'AUS':0}
CT_API='https://api.climatetrace.org/v7/sources/'

@app.route('/update', methods=["GET","POST"])
def updatingplots():
    if request.method=="POST":
        val=requests.get(CT_API, params={
        "year": "2023",
        "gas": "co2",
        "sectors": "",
        "subsectors": "",
        "gadmId": "",
        "cityId": "",
        "countryGroup": "",
        "continent": "",
        "ownerIds": "",
        "limit": "50000",
        "offset": "0"
        })
        final_val=val.json()
        for i in final_val:
            cntry=i['country']
            d[cntry]=d.get(cntry,0)+i['emissionsQuantity']
            if len(d)>14:
                break
    
        keys=list(d.keys())
        vals=list(d.values())

        plt.bar(keys,vals)
        plt.title("Carbon emissions")
        plt.savefig("static/plot.png")
        plt.close()

        plt.pie(vals, labels=keys)
        plt.legend(keys,loc='best')
        plt.savefig("static/pieplot.png")
        plt.close()
        return redirect('/')

@app.route('/', methods=["GET","POST"])
def mainpage():
    return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True)