from flask import render_template, request
from . import googoodan_bp

@googoodan_bp.route('/googoodan', methods=['GET', 'POST'])
def googoodan():
    number = request.form.get('number')
    if number is not None and number.isdigit():
        number = int(number)
    return render_template('googoodan/googoodan.html', number=number)
