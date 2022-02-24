#######################################################################
# Govinda KC                                                          #
# Last modified: 02/15/2022                                           #
#######################################################################

import flask, sys, os, joblib
from flask import request
from rdkit import Chem
from run_biasnet import preprocess_smi
from rdkit.Chem import rdDepictor
from features import FeaturesGeneration
import requests

app = flask.Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def predict():

    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html'))

    if flask.request.method == 'POST':
        SMILES = request.form['SMILES']      
        print("PREDICTING FOR {}".format(SMILES), file=sys.stderr)
        Dictn = dict()
        # Preprocessing of the SMILES
        processed_smiles = preprocess_smi(SMILES)
    
        try:
            def get_features(processed_smiles):

                fg = FeaturesGeneration()
                features = fg.get_fingerprints(processed_smiles)

                return features

            def get_results(smiles):
                # Load models
                model = joblib.load('model/model_lecfp4.mlp')
                
                features = get_features(smiles)


                model_result = {}

                label_zero = model.predict_proba(features)[0][0].round(3)
                label_one = model.predict_proba(features)[0][1].round(3)

                if label_one >= 0.5:
                    model_result['Prediction'] = 'B-Arrestin'
                    model_result['Confidence'] = label_one

                else:
                    model_result['Prediction'] = 'G-Protein'
                    model_result['Confidence'] = label_zero
                return model_result

            model_result = get_results(processed_smiles)

            Dictn[SMILES] = model_result
            result = Dictn[SMILES]['Prediction']

            return flask.render_template('index.html',
                                     original_input={'SMILES':SMILES
                                         },  
                                     result=result,
                                     )   
        except Exception as e:
            print('Error encountered: ', e)
            return flask.render_template('index.html',
                                         original_input={'SMILES':SMILES
                                             },
                                         result='Unknown',
                                         )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
   # app.run(debug=False)
