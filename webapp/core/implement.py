# Import relevant libraries 

import pandas as pd
import numpy as np
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
import operator
import pickle 

class RecommendationEngine():

    user_sim_df = None
    item_sim_df = None
    piv_norm = None
    merged_sub = None

    def __init__(self):
        file_1 = open('core/user_sim_df.obj', 'rb')
        self.user_sim_df = pickle.load(file_1)

        file_2 = open('core/item_sim_df.obj', 'rb')
        self.item_sim_df = pickle.load(file_2)

        file_3 = open('core/piv_norm.obj', 'rb')
        self.piv_norm = pickle.load(file_3)

        file_4 = open('core/merged_sub.obj', 'rb')
        self.merged_sub = pickle.load(file_4)

    # This function will return the top 10 shows with the highest cosine similarity value

    def top_animes(self, anime_name):
        count = 1
        print('Similar shows to {} include:\n'.format(anime_name))
        for item in self.item_sim_df.sort_values(by = anime_name, ascending = False).index[1:11]:
            print('No. {}: {}'.format(count, item))
            count +=1

    # This function will return the top 5 users with the highest similarity value

    def top_users(self, user):
        user = int(user)
        if user not in self.piv_norm.columns:
            return('No data available on user {}'.format(user))

        print('Most Similar Users:\n')
        sim_values = self.user_sim_df.sort_values(by=user, ascending=False).loc[:,user].tolist()[1:11]
        sim_users = self.user_sim_df.sort_values(by=user, ascending=False).index[1:11]
        zipped = zip(sim_users, sim_values,)
        for user, sim in zipped:
            print('User #{0}, Similarity value: {1:.2f}'.format(user, sim))

    def user_watched(self, user):
        user = int(user)
        try:
            watched_list = list(self.merged_sub['name'][self.merged_sub['user_id'] == user])
        except:
            watched_list = ['UserNotFound']
        return watched_list

    # This function constructs a list of lists containing the highest rated shows per similar user
    # and returns the name of the show along with the frequency it appears in the list

    def similar_user_recs(self, user):

        user = int(user)
        if user not in self.piv_norm.columns:
            return(['UserNotFound'])

        sim_users = self.user_sim_df.sort_values(by=user, ascending=False).index[1:11]
        best = []
        most_common = {}

        for i in sim_users:
            max_score = self.piv_norm.loc[:, i].max()
            best.append(self.piv_norm[self.piv_norm.loc[:, i]==max_score].index.tolist())
        for i in range(len(best)):
            for j in best[i]:
                if j in most_common:
                    most_common[j] += 1
                else:
                    most_common[j] = 1
        sorted_list = sorted(most_common.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_list[:5]


if __name__ == '__main__':
    object = RecommendationEngine()
    object.top_animes('Cowboy Bebop')

#top_animes('Cowboy Bebop')
#print(top_users(3))
#similar_user_recs(10)