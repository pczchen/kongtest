from flask import Flask,url_for,request,render_template

app = Flask(__name__)

import tools as base

conn = base.get_connection(["localhost"])
sess = base.get_session(conn, "kong")
keyspaces = base.get_keyspaces(sess)
tables = base.get_tables(sess)

@app.route("/cassandra")
def show_cassandra():
    return render_template("show_cassandra.html",tables=tables)


@app.route("/cassandra/<table>")
def show_data(table):
    rows = sess.execute("select * from "+table)
    
    return render_template("show_table.html", table=table, rows=rows)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
    
