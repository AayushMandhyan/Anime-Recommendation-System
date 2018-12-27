from core.implement import RecommendationEngine
from flask import Flask, render_template, request, jsonify
import os
import sys

app = Flask(__name__)
re = RecommendationEngine()


@app.route('/')
def home():
    return render_template('index.html')

#top movies
@app.route('/top_movies', methods=['GET', 'POST'])
def top_movies():
    width = '150'
    height = '200'
    anime_list = "<table bgcolor='#D3D3D3' align='center'><tr>"
    top_anime_list = ['Boruto', 'Hy5', 'Rwby', 'Tokyo Ghoul', 'Beautiful Bones', 'Something']
    name_list = ""

    #creating image tags to display top anime
    for anime in top_anime_list:
        anime_img = 'static/posters/'+anime.replace(' ', '')+'.jpg' if os.path.isfile('static/posters/'+anime.replace(' ', '').lower()+'.jpg') else 'static/posters/poster_not_found.jpg'
        image_div = "<td><img src='"+anime_img+"' alt='" +anime+"' width='" +width+ "' height='" +height+ "'></td> \n"
        anime_list += image_div
        name_list += '<td><p>' + anime + '</p></td>'
    anime_list = anime_list + '</tr><br><tr>' + name_list + '</tr></table>'
    print('return top movies')
    #print(anime_list)
    return anime_list


#movies watched
@app.route('/movies_watched', methods=['POST'])
def movies_watched():
    if request.method == 'POST':
        data = request.get_json()
    user_id = data['user_id']
    print(user_id)
    #check user id, if not present return "user not found"
    width = '150'
    height = '200'
    anime_list = "<br><h5 style='color:gray;'>Anime Watched</h5><table bgcolor='#D3D3D3' align='center'><tr>"
    #watched_list = ['boruto', 'hy5', 'rwby', 'tokyo ghoul', 'beautiful bones']
    watched_list = re.user_watched(user_id)
    print("watched list  "+ str(watched_list))
    try:
        if watched_list[0] != 'UserNotFound':
            name_list = ""
            #creating image tags to display top anime
            for anime in watched_list:
                anime_img = 'static/posters/' + anime.replace(' ', '') + '.jpg' if os.path.isfile('static/posters/' + anime.replace(' ', '').lower() + '.jpg') else 'static/posters/poster_not_found.jpg'
                image_div = "<td><img src='"+anime_img+"' alt='" +anime+"' width='" +width+ "' height='" +height+ "'></td> \n"
                anime_list += image_div
                name_list += '<td><p>' + anime + '</p></td>'
            anime_list = anime_list + '</tr><br><tr>' + name_list + '</tr></table>'
            data = {"user" : user_id, "value": anime_list}
            print('return movies watched')
            print(jsonify(data))
            return jsonify(data)
        else:
            return jsonify(" ")
    except:
        return jsonify(" ")


#recommended movies
@app.route('/recommended_movies', methods=['POST'])
def recommended_movies():
    if request.method == 'POST':
        data = request.get_json()
    user_id = data['user_id']
    #check user id, if not found send blank
    print(user_id)
    #fetching the similarity list
    recommended_list = re.similar_user_recs(user_id)
    if recommended_list[0] != 'UserNotFound':
        recommended_list = [recommendation[0] for recommendation in recommended_list]
        print(recommended_list)
        width = '150'
        height = '200'
        anime_list = "<br><h5 style='color:gray;'>Recommended Anime</h5><table bgcolor='#D3D3D3' align='center'><tr>"
        #recommended_list = ['boruto', 'hy5', 'rwby', 'tokyo ghoul', 'beautiful bones']
        name_list = ""

        #creating image tags to display top anime
        for anime in recommended_list:
            anime_img = 'static/posters/' + anime.replace(' ', '') + '.jpg' if os.path.isfile('static/posters/' + anime.replace(' ', '').lower() + '.jpg') else 'static/posters/poster_not_found.jpg'
            image_div = "<td><img src='"+anime_img+"' alt='" +anime+"' width='" +width+ "' height='" +height+ "'></td> \n"
            anime_list += image_div
            name_list += '<td><p>' + anime + '</p></td>'
        anime_list = anime_list + '</tr><br><tr>' + name_list + '</tr></table>'
        print('return recommended movies')
        print(jsonify(anime_list))
        return jsonify(anime_list)
    else:
        return jsonify("<p style='color:gray;'>No Recommendations!</p>")


if __name__ == '__main__':
    app.run(port=sys.argv[1], debug=True)
