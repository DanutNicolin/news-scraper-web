
from news_scraper import(app, jsonify, redirect, render_template, request, url_for, session, presentation, commands)



app.config['SECRET_KEY'] = '9ba52c24bff7b5daa7b81c71dd10850b13f692077a445d03'





@app.route('/')
def home():
    title = 'Welcome to News Scraper'
    subtitle = 'Choose the website you want to scrape'
    options = presentation.get_menu(presentation.scrapers)
    return render_template('home.html', title=title, subtitle=subtitle, options=options)


@app.route('/actions/', methods=['POST'])
def action():
    req = request.form
    news_outlet = req['option']
    session['scraper'] = news_outlet
    subtitle = 'Choose a action'
    options = presentation.get_menu(presentation.options)
    return render_template('actions.html',title=news_outlet, subtitle=subtitle, options=options)


@app.route('/redirect/', methods=['POST'])
def go_to():
    req = request.form
    chosen_action = req['option']
    if chosen_action == 'Print todays news':
        return redirect(url_for('print_news'))
    if chosen_action == 'Search by key word':
        return redirect(url_for('keyword'))
    if chosen_action == 'Add all titles to database':
        return redirect(url_for('add_to_db'))
    if chosen_action == 'Plot words count':
        return redirect(url_for('plot'))





@app.route('/actions/print-news/')
def print_news():
    news_outlet = session['scraper']
    scraper = presentation.make_scraper(news_outlet)
    news_list = commands.GetAllTitles().execute(scraper)
    title = f'{str(scraper)} News'
    return render_template('print_news.html', title=title, news=news_list)


@app.route('/actions/add-to-db')
def add_to_db():
    scraper = session['scraper']
    response = commands.WriteToDataBase().execute(presentation.make_scraper(scraper))
    return render_template('succes_page.html', news_outlet=scraper, added=response['titles not in db'], existing=response['titles in db'])


@app.route('/actions/keyword')
def keyword():
    subtitle = 'Enter keyword you want to search'
    return render_template('search.html', subtitle=subtitle)


@app.route('/actions/keyword/search-by-keyword/', methods=['POST'])
def search_by_keyword():
    req = request.form
    keyword = req['keyword']
    scraper = presentation.make_scraper(session['scraper'])
    news_list = commands.SearchKeyword().execute(scraper, keyword)
    return render_template('print_news.html', news=news_list)


@app.route('/actions/plot')
def plot():
    response = commands.PlotData().execute(presentation.get_scraper())
    return jsonify({'message': response})

