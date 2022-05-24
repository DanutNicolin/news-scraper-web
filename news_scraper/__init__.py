from flask import Flask, jsonify, redirect, render_template, request, url_for, session

from news_scraper.src import commands
from news_scraper.src import presentation



app = Flask(__name__)

from news_scraper import views