from flask import Flask
from flask import request

from flask_restplus import Resource, Api
from flask_restplus import fields

import pandas as pd

books_df = pd.read_csv('Books.csv')

app = Flask(__name__)
api = Api(app)

book_model = api.model('Book', {
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})

def print_dataframe(dataframe, print_column=True, print_rows=True):
    # print column names
    if print_column:
        print(",".join([column for column in dataframe]))

    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))

def clean(dataframe):
    columns_to_drop = ['Edition Statement',
                       'Corporate Author',
                       'Corporate Contributors',
                       'Former owner',
                       'Engraver',
                       'Contributors',
                       'Issuance type',
                       'Shelfmarks'
                       ]
    dataframe.drop(columns_to_drop, inplace=True, axis=1)

    dataframe['Place of Publication'] = dataframe['Place of Publication'].apply(
        lambda x: 'London' if 'London' in x else x.replace('-', ' '))
    dataframe.columns = [c.replace(' ', '_') for c in books_df.columns]
    dataframe = dataframe.set_index('Identifier')

    new_date = dataframe['Date_of_Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    dataframe['Date_of_Publication'] = new_date
    

    return dataframe


@api.route('/books/<int:id>')
class Books(Resource):
    def get(self, id):
        if id not in books_df.index:
            api.abort(404, "Book {} doesn't exist".format(id))

        book = dict(books_df.loc[id])
        return book

    def delete(self, id):
        if id not in books_df.index:
            api.abort(404, "Book {} doesn't exist".format(id))

        books_df.drop(id, inplace=True)
        return {"message": "Book {} is removed.".format(id)}, 200

    @api.expect(book_model)
    def put(self, id):
        if id not in books_df.index:
            api.abort(404, "Book {} doesn't exist.".format(id))
        
        book = request.get_json()

        if 'Identifier' in book and id != book['Identifier']:
            return {"message": "Identifier cannot be changed".format(id)}, 400

        for k in book:
            if k not in book_model.keys():
                return{"message" : "Property {} is invalid".format(k)}, 400
            books_df.loc[id, k] = book[k]

        return {"message": "Book {} has been successfully updated".format(id)}, 200

if __name__ == '__main__':
    books_df = clean(books_df)
    #a = books_df.query('206')
    #print(a)
    #print_dataframe(books_df)
    #df.to_csv('t4.csv')
    app.run(debug=True)