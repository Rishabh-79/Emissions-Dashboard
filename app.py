from flask import Flask, render_template,request,redirect
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app=Flask(__name__)

CT_API='https://api.climatetrace.org/v7/sources/'

@app.route('/NotFound', methods=["GET","POST"])
def unavailable():
    if request.method=="POST":
        return redirect('/')
    else:
        return render_template('Notfound.html')
 
@app.route('/update', methods=["GET","POST"])
def updatingplots():
    if request.method=="POST":
        d={}
        cont=request.form['Cont']
        gaaas=request.form['Gases']
        years=int(request.form['Year'])
        val=requests.get(CT_API, params={
        f"year": {years},
        "gas": {gaaas},
        "sectors": "",
        "subsectors": "",
        "gadmId": "",
        "cityId": "",
        "countryGroup": "",
        "continent": {cont},
        "ownerIds": "",
        "limit": "50000",
        "offset": "0"
        })
        final_val=val.json()
        if final_val==None:
            return redirect("/NotFound")
        for i in final_val:
            cntry=i['country']
            d[cntry]=d.get(cntry,0)+i['emissionsQuantity']
        finald = dict(sorted(d.items(), key=lambda item: item[1]))
        finald = dict(reversed(finald.items()))

        actually_the_final_dict={}
        for i in finald:
            actually_the_final_dict[i]=finald[i]
            if len(actually_the_final_dict)>9:
                break
        
        keys=list(actually_the_final_dict.keys())
        vals=list(actually_the_final_dict.values())

        plt.bar(keys,vals)
        plt.title(f" Emissions ({gaaas})")
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